import streamlit as st
import pandas as pd
import wenwen
import wenwen_2
import wenwen_3
import vadim
import main_proekt_3_fragen
import main_proekt_4_5_fragen
import Aufgabe_10

# Configuración
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# Cargar y limpiar datos
@st.cache_data
def load_and_clean_data():
    url = "https://raw.githubusercontent.com/santiagoLopez1712/Agilesmanagementprojekt/main/train_cleaned.csv"
    df = load_data(url)
    df = clean_data(df)
    return df

df = load_and_clean_data()

# Sidebar: Filtros
st.sidebar.header("Filtros")
selected_region = st.sidebar.selectbox("Seleccionar Región", ["Todas"] + list(df["Region"].unique()))
start_date = st.sidebar.date_input("Fecha Inicio", pd.to_datetime("2015-01-01"))
end_date = st.sidebar.date_input("Fecha Fin", pd.to_datetime("2018-12-31"))

# Filtrar datos
filtered_df = filter_by_region(df, selected_region)

# KPIs
st.header("KPIs Principales")
kpis = plot_kpis(filtered_df)
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${kpis['Total Sales']:,.2f}")
col2.metric("Average Sales", f"${kpis['Average Sales']:,.2f}")
col3.metric("Top Product", kpis["Top Product"])

# Gráficos
st.header("Evolución de Ventas")
fig = plot_sales_trend(filtered_df)
st.plotly_chart(fig)

# Estadísticas
st.header("Estadísticas Personalizadas")
stats = calculate_statistics(filtered_df, start_date, end_date)
st.write(f"**Total:** ${stats['Total']:,.2f}")
st.write(f"**Media:** ${stats['Mean']:,.2f}")
st.write(f"**Mediana:** ${stats['Median']:,.2f}")
st.write(f"**Desviación Estándar:** ${stats['Std']:,.2f}")