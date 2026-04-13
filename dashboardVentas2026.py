import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data from the saved Excel file path
file_path = 'datos/SalidaVentas.xlsx'
df = pd.read_excel(file_path)

st.set_page_config(layout='wide')

st.title('Sales Dashboard for USA Regions')

st.markdown('### Overview of Sales Data')
st.write(df.head())

# Aggregate sales by Region
sales_by_region = df.groupby('Region')['Sales'].sum().reset_index()

st.markdown('### Total Sales by Region')
fig = px.bar(sales_by_region, x='Region', y='Sales', title='Total Sales by Region')
st.plotly_chart(fig, use_container_width=True)

# Aggregate sales by Category
category_sales = df.groupby('Category')[['Sales', 'Quantity']].sum().reset_index()
st.markdown('### Sales and Quantity by Category')
st.dataframe(category_sales)

# Aggregate sales by Sub-Category
subcategory_sales = df.groupby('Sub-Category')[['Sales', 'Quantity']].sum().reset_index().sort_values(by='Sales', ascending=False)
st.markdown('### Top 10 Sales by Sub-Category')
fig_sub = px.bar(subcategory_sales.head(10), x='Sub-Category', y='Sales', title='Top 10 Sales by Sub-Category')
st.plotly_chart(fig_sub, use_container_width=True)

# Sales over time (if 'Order Date' is a datetime column)
df['Order Date'] = pd.to_datetime(df['Order Date'])
sales_over_time = df.groupby(df['Order Date'].dt.to_period('M'))['Sales'].sum().reset_index()
sales_over_time['Order Date'] = sales_over_time['Order Date'].astype(str)
st.markdown('### Monthly Sales Trend')
fig_time = px.line(sales_over_time, x='Order Date', y='Sales', title='Monthly Sales Trend')
st.plotly_chart(fig_time, use_container_width=True)
