import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime # Import datetime for date operations
import plotly.express as px # Import plotly express for maps

# It's better to load the data directly within the Streamlit script for portability
try:
    df = pd.read_excel('/content/drive/MyDrive/Documentos/SalidaVentas.xlsx')
except FileNotFoundError:
    st.error("Error: 'SalidaVentas.xlsx' not found. Please ensure the file is in the specified path.")
    st.stop()

# Ensure 'Order Date' is in datetime format
df['Order Date'] = pd.to_datetime(df['Order Date'])

st.set_page_config(layout='wide')

st.title('Sales Dashboard for USA Branches')

st.markdown("--- ")

# --- Date Filtering ---
st.sidebar.header('Filter Options')
min_date = df['Order Date'].min().date()
max_date = df['Order Date'].max().date()

start_date = st.sidebar.date_input('Start Date', min_value=min_date, max_value=max_date, value=min_date)
end_date = st.sidebar.date_input('End Date', min_value=min_date, max_value=max_date, value=max_date)

# Convert selected dates to datetime objects for filtering
start_datetime = datetime.combine(start_date, datetime.min.time())
end_datetime = datetime.combine(end_date, datetime.max.time())

# Filter DataFrame based on selected dates
filtered_df = df[(df['Order Date'] >= start_datetime) & (df['Order Date'] <= end_datetime)]

if filtered_df.empty:
    st.warning("No data available for the selected date range. Please adjust your date filters.")
    st.stop()

# --- Display Key Metrics (using filtered_df) ---
st.header('Overall Sales Performance')

total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
total_quantity = filtered_df['Quantity'].sum()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Sales", value=f"${total_sales:,.2f}")
with col2:
    st.metric(label="Total Profit", value=f"${total_profit:,.2f}")
with col3:
    st.metric(label="Total Quantity Sold", value=f"{total_quantity:,}")

st.markdown("--- ")

# --- Monthly Sales Trend ---
st.header('Monthly Sales Trend')

# Extract Year and Month for monthly analysis
monthly_sales_df = filtered_df.copy()
monthly_sales_df['YearMonth'] = monthly_sales_df['Order Date'].dt.to_period('M').astype(str)
monthly_sales = monthly_sales_df.groupby('YearMonth')['Sales'].sum().reset_index()
monthly_sales['YearMonth'] = pd.to_datetime(monthly_sales['YearMonth']) # Convert back to datetime for proper sorting/plotting

fig_monthly, ax_monthly = plt.subplots(figsize=(12, 6))
sns.lineplot(x='YearMonth', y='Sales', data=monthly_sales, marker='o', ax=ax_monthly)
ax_monthly.set_title('Monthly Total Sales')
ax_monthly.set_xlabel('Month')
ax_monthly.set_ylabel('Total Sales')
ax_monthly.ticklabel_format(style='plain', axis='y') # Prevent scientific notation
ax_monthly.tick_params(axis='x', rotation=45)
ax_monthly.grid(True, linestyle='--', alpha=0.6)
st.pyplot(fig_monthly)

st.markdown("--- ")

# --- Sales by Region (using filtered_df) ---
st.header('Sales Analysis by Region')
sales_by_region = filtered_df.groupby('Region')['Sales'].sum().sort_values(ascending=False).reset_index()

fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(x='Region', y='Sales', data=sales_by_region, palette='viridis', ax=ax1)
ax1.set_title('Total Sales by Region')
ax1.set_xlabel('Region')
ax1.set_ylabel('Total Sales')
ax1.ticklabel_format(style='plain', axis='y') # Prevent scientific notation
st.pyplot(fig1)

st.markdown("--- ")

# --- Profit by Region (using filtered_df) ---
st.header('Profit Analysis by Region')
profit_by_region = filtered_df.groupby('Region')['Profit'].sum().sort_values(ascending=False).reset_index()

fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(x='Region', y='Profit', data=profit_by_region, palette='magma', ax=ax2)
ax2.set_title('Total Profit by Region')
ax2.set_xlabel('Region')
ax2.set_ylabel('Total Profit')
ax2.ticklabel_format(style='plain', axis='y') # Prevent scientific notation
st.pyplot(fig2)

st.markdown("--- ")

# --- Top Products by Sales ---
st.header('Top Products by Sales')

num_top_products = st.sidebar.slider('Number of Top Products', min_value=5, max_value=20, value=10)

top_products = filtered_df.groupby('Product Name')['Sales'].sum().nlargest(num_top_products).reset_index()

fig_products, ax_products = plt.subplots(figsize=(12, 8))
sns.barplot(x='Sales', y='Product Name', data=top_products, palette='rocket', ax=ax_products)
ax_products.set_title(f'Top {num_top_products} Products by Sales')
ax_products.set_xlabel('Total Sales')
ax_products.set_ylabel('Product Name')
ax_products.ticklabel_format(style='plain', axis='x') # Prevent scientific notation
st.pyplot(fig_products)

st.markdown("--- ")

# --- Sales by State Map (Added) ---
st.header('Sales by State (USA Map)')

sales_by_state = filtered_df.groupby('State')['Sales'].sum().reset_index()

fig_map = px.choropleth(
    sales_by_state,
    locations='State',
    locationmode='USA-states',
    color='Sales',
    color_continuous_scale='Viridis',
    scope='usa',
    title='Total Sales by State'
)
fig_map.update_layout(margin={"r":0,"t":50,"l":0,"b":0})
st.plotly_chart(fig_map)
