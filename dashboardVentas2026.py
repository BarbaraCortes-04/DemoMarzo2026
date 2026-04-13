import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import plotly.express as px

# Cargar datos
try:
    df = pd.read_excel('datos/SalidaVentas.xlsx')
except FileNotFoundError:
    st.error("Error: 'SalidaVentas.xlsx' not found. Please ensure the file is in the specified path.")
    st.stop()

# Convertir fecha
df['Order Date'] = pd.to_datetime(df['Order Date'])

st.set_page_config(layout='wide')

st.title('Sales Dashboard for USA Branches')
st.markdown("--- ")

# --- FILTROS ---
st.sidebar.header('Filter Options')

min_date = df['Order Date'].min().date()
max_date = df['Order Date'].max().date()

start_date = st.sidebar.date_input('Start Date', min_value=min_date, max_value=max_date, value=min_date)
end_date = st.sidebar.date_input('End Date', min_value=min_date, max_value=max_date, value=max_date)

start_datetime = datetime.combine(start_date, datetime.min.time())
end_datetime = datetime.combine(end_date, datetime.max.time())

filtered_df = df[(df['Order Date'] >= start_datetime) & (df['Order Date'] <= end_datetime)]

if filtered_df.empty:
    st.warning("No data available for the selected date range.")
    st.stop()

# --- MÉTRICAS ---
st.header('Overall Sales Performance')

total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
total_quantity = filtered_df['Quantity'].sum()

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Total Quantity Sold", f"{total_quantity:,}")

st.markdown("--- ")

# --- TENDENCIA MENSUAL ---
st.header('Monthly Sales Trend')

monthly_df = filtered_df.copy()
monthly_df['YearMonth'] = monthly_df['Order Date'].dt.to_period('M').astype(str)

monthly_sales = monthly_df.groupby('YearMonth')['Sales'].sum().reset_index()
monthly_sales['YearMonth'] = pd.to_datetime(monthly_sales['YearMonth'])

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='YearMonth', y='Sales', data=monthly_sales, marker='o', ax=ax)

ax.set_title('Monthly Total Sales')
ax.tick_params(axis='x', rotation=45)
ax.grid(True)

st.pyplot(fig)

st.markdown("--- ")

# --- VENTAS POR REGIÓN ---
st.header('Sales by Region')

sales_region = filtered_df.groupby('Region')['Sales'].sum().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='Region', y='Sales', data=sales_region, palette='viridis', ax=ax)

st.pyplot(fig)

st.markdown("--- ")

# --- UTILIDAD POR REGIÓN ---
st.header('Profit by Region')

profit_region = filtered_df.groupby('Region')['Profit'].sum().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='Region', y='Profit', data=profit_region, palette='magma', ax=ax)

st.pyplot(fig)

st.markdown("--- ")

# --- TOP PRODUCTOS ---
st.header('Top Products')

n = st.sidebar.slider('Top Products', 5, 20, 10)

top_products = filtered_df.groupby('Product Name')['Sales'].sum().nlargest(n).reset_index()

fig, ax = plt.subplots(figsize=(12, 8))
sns.barplot(x='Sales', y='Product Name', data=top_products, palette='rocket', ax=ax)

st.pyplot(fig)

st.markdown("--- ")

# --- MAPA POR ESTADO (CORREGIDO) ---
st.header('Sales by State (USA Map)')

sales_by_state = filtered_df.groupby('State')['Sales'].sum().reset_index()

# Diccionario estados
state_abbrev = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT',
    'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL',
    'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
    'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME',
    'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI',
    'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
    'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
    'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM',
    'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND',
    'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR',
    'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX',
    'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA',
    'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

sales_by_state['State'] = sales_by_state['State'].map(state_abbrev)
sales_by_state = sales_by_state.dropna()

fig_map = px.choropleth(
    sales_by_state,
    locations='State',
    locationmode='USA-states',
    color='Sales',
    color_continuous_scale='Viridis',
    scope='usa',
    title='Total Sales by State',
    range_color=(sales_by_state['Sales'].min(), sales_by_state['Sales'].max())
)

fig_map.update_traces(marker_line_width=0.5, marker_line_color='white')
fig_map.update_layout(margin={"r":0,"t":50,"l":0,"b":0})

st.plotly_chart(fig_map)
