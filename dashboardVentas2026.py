import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Assuming df is already loaded in the Colab environment.
# For a standalone Streamlit app, you would load the data directly here.
# Since we are in Colab, we'll try to use the global df if available,
# otherwise, load it from the original path.

# It's better to load the data directly within the Streamlit script for portability
try:
    df = pd.read_excel('datos/SalidaVentas.xlsx')
except FileNotFoundError:
    st.error("Error: 'SalidaVentas.xlsx' not found. Please ensure the file is in the specified path.")
    st.stop()

st.set_page_config(layout='wide')

st.title('Sales Dashboard for USA Branches')

st.markdown("--- ")

# Display Key Metrics
st.header('Overall Sales Performance')

if not df.empty:
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    total_quantity = df['Quantity'].sum()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Sales", value=f"${total_sales:,.2f}")
    with col2:
        st.metric(label="Total Profit", value=f"${total_profit:,.2f}")
    with col3:
        st.metric(label="Total Quantity Sold", value=f"{total_quantity:,}")

    st.markdown("--- ")

    # Sales by Region
    st.header('Sales Analysis by Region')
    sales_by_region = df.groupby('Region')['Sales'].sum().sort_values(ascending=False).reset_index()

    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Region', y='Sales', data=sales_by_region, palette='viridis', ax=ax1)
    ax1.set_title('Total Sales by Region')
    ax1.set_xlabel('Region')
    ax1.set_ylabel('Total Sales')
    ax1.ticklabel_format(style='plain', axis='y') # Prevent scientific notation
    st.pyplot(fig1)

    st.markdown("--- ")

    # Profit by Region
    st.header('Profit Analysis by Region')
    profit_by_region = df.groupby('Region')['Profit'].sum().sort_values(ascending=False).reset_index()

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Region', y='Profit', data=profit_by_region, palette='magma', ax=ax2)
    ax2.set_title('Total Profit by Region')
    ax2.set_xlabel('Region')
    ax2.set_ylabel('Total Profit')
    ax2.ticklabel_format(style='plain', axis='y') # Prevent scientific notation
    st.pyplot(fig2)

else:
    st.warning("The DataFrame is empty. Please check the data loading step.")
