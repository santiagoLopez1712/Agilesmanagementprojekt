import streamlit as st
import pandas as pd
from wenwen import cargar_datos  # Importar funciones de los archivos correspondientes
from wenwen_2 import limpiar_datos
from wenwen_3 import calcular_estadisticas
from main_proekt_3_fragen import plot_ventas
from main_proekt_4_5_fragen import tabla_dinamica
from vadim import exportar_csv, exportar_pdf
from Aufgabe_10 import visualizacion_ventas
from Aufgabe_11 import crear_kpis
from Aufgabe_12 import generar_reportes

# Configuración de la página
st.set_page_config(page_title="Dashboard de Análisis de Ventas", layout="wide")

# Título de la aplicación
st.title("Dashboard de Análisis de Ventas")

# Cargar datos
@st.cache_data
def cargar_y_limpiar_datos():
    df = cargar_datos("train.csv")  # Cargar el dataset
    df = limpiar_datos(df)  # Limpiar los datos
    return df

# Llamar a la función de carga y limpieza de datos
df = cargar_y_limpiar_datos()

# Sidebar: Filtros
st.sidebar.header("Filtros")
selected_region = st.sidebar.selectbox("Seleccionar Región", ["Todas"] + list(df["Region"].unique()))
selected_categoria = st.sidebar.selectbox("Seleccionar Categoría de Producto", ["Todas"] + list(df["Categoria"].unique()))
start_date = st.sidebar.date_input("Fecha Inicio", pd.to_datetime("2015-01-01"))
end_date = st.sidebar.date_input("Fecha Fin", pd.to_datetime("2018-12-31"))

# Filtrar datos según las selecciones
df_filtrado = df[(df['Fecha'] >= pd.to_datetime(start_date)) & (df['Fecha'] <= pd.to_datetime(end_date))]
if selected_region != "Todas":
    df_filtrado = df_filtrado[df_filtrado['Region'] == selected_region]
if selected_categoria != "Todas":
    df_filtrado = df_filtrado[df_filtrado['Categoria'] == selected_categoria]

# 1. KPIs Principales
st.header("KPIs Principales")
kpis = calcular_estadisticas(df_filtrado)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Ventas", f"${kpis['total']}")
col2.metric("Media de Ventas", f"${kpis['media']}")
col3.metric("Mediana de Ventas", f"${kpis['mediana']}")
col4.metric("Desviación Estándar", f"${kpis['std']}")

# 2. Gráficos de Ventas
st.header("Visualización de Ventas")
grafico = plot_ventas(df_filtrado)  # Asume que esta función genera un gráfico interactivo
st.plotly_chart(grafico)

# 3. Tabla Dinámica
st.header("Crear Tabla Dinámica")
tabla_dinamica(df_filtrado)  # Función para crear tablas dinámicas
st.write("Tabla dinámica generada.")

# 4. Visualización de Ventas (por categorías, mensual, etc.)
st.header("Evolución de Ventas")
visualizacion_ventas(df_filtrado)

# 5. Exportar Datos
st.header("Exportar Resultados")
exportar_opcion = st.selectbox("Seleccionar Formato de Exportación", ["PDF", "CSV"])
if exportar_opcion == "CSV":
    exportar_csv(df_filtrado)
elif exportar_opcion == "PDF":
    exportar_pdf(df_filtrado)

# 6. Generación de Reportes
st.header("Generación de Reportes")
if st.button("Generar Reporte Completo"):
    generar_reportes(df_filtrado)
    st.write("Reporte generado.")

