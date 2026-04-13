import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title('Mi Aplicación Streamlit con DataFrame y Gráfica de Línea')

# 1. Crear un DataFrame de ejemplo
st.header('DataFrame de Ejemplo')

# Generar datos de ejemplo
data = {
    'Fecha': pd.to_datetime(pd.date_range(start='2023-01-01', periods=100, freq='D')),
    'Valor_A': np.random.rand(100).cumsum() * 100,
    'Valor_B': np.random.rand(100).cumsum() * 50 + 20
}
df = pd.DataFrame(data)

# Mostrar el DataFrame
st.dataframe(df)

# 2. Crear una gráfica de línea
st.header('Gráfica de Línea de Valores a lo Largo del Tiempo')

# Selector para elegir qué columna graficar
selected_column = st.selectbox(
    'Selecciona una columna para graficar:',
    ('Valor_A', 'Valor_B')
)

# Crear la gráfica interactiva con Plotly Express
fig = px.line(df, x='Fecha', y=selected_column,
              title=f'Tendencia de {selected_column}',
              labels={'Fecha': 'Fecha', selected_column: 'Valor'})

# Mostrar la gráfica en Streamlit
st.plotly_chart(fig)
