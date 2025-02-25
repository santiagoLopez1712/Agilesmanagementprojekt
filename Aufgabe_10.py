import streamlit as st
import pandas as pd
import plotly.express as px


#CSV
csv_url = "https://raw.githubusercontent.com/santiagoLopez1712/Agilesmanagementprojekt/refs/heads/main/train.csv"

# Cargar datos
@st.cache_data
def cargar_datos():
    df = pd.read_csv(csv_url, parse_dates=["Order Date"])
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors='coerce')
    df.dropna(subset=["Order Date"], inplace=True)
    df["Year-Month"] = df["Order Date"].dt.to_period("M").astype(str)
    return df

df = cargar_datos()

# KPIs
total_sales = df["Sales"].sum()
average_sales = df["Sales"].mean()
median_sales = df["Sales"].median()
top_product = df.groupby("Product Name")["Sales"].sum().idxmax()

# Dashboard
st.title("Dashboard Sales Data")
st.write("Diese Dashboard zeigt die wichtigsten KPIs")
st.metric("Gesamtumsatz", f"${total_sales:,.2f}")
st.metric("Durchschnittlicher Umsatz", f"${average_sales:,.2f}")
st.metric("Median des Umsatzes", f"${median_sales:,.2f}")
st.metric("Meistverkauftes Produkt", top_product)

fig_trends = px.line(df.groupby("Year-Month")["Sales"].sum().reset_index(), x="Year-Month", y="Sales", title="Meistverkauftes Produkt")
st.plotly_chart(fig_trends)

# RUN: streamlit run Aufgabe_10.py
# URL: http://localhost:8501