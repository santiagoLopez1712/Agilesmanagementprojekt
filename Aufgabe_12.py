from flask import Flask, render_template, request, send_file
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import os

app = Flask(__name__)

# Cargar los datos
CSV_URL = "https://raw.githubusercontent.com/santiagoLopez1712/Agilesmanagementprojekt/refs/heads/main/train_cleaned.csv"
df = pd.read_csv(CSV_URL, parse_dates=["Order Date"])
df.dropna(subset=["Order Date"], inplace=True)

# Crear columnas adicionales
df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.month
df["Week"] = df["Order Date"].dt.isocalendar().week
df["Day"] = df["Order Date"].dt.day
df["Year-Month"] = df["Order Date"].dt.to_period("M").astype(str)

@app.route("/", methods=["GET", "POST"])
def index():
    filtered_df = df.copy()
    
    # Filtrado por fecha
    if request.method == "POST":
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")

        if start_date and end_date:
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)
            filtered_df = df[(df["Order Date"] >= start_date) & (df["Order Date"] <= end_date)]

    # KPI
    total_sales = filtered_df["Sales"].sum()
    average_sales = filtered_df["Sales"].mean()
    top_product = filtered_df.groupby("Product Name")["Sales"].sum().idxmax() if not filtered_df.empty else "N/A"

    # Gráfico de ventas por mes
    sales_trend = filtered_df.groupby("Year-Month")["Sales"].sum().reset_index()
    fig = px.line(sales_trend, x="Year-Month", y="Sales", title="Tendencia de Ventas")

    # Guardar gráfico temporalmente
    graph_path = "static/sales_graph.html"
    fig.write_html(graph_path)

    return render_template("index.html", total_sales=total_sales, average_sales=average_sales, 
                           top_product=top_product, graph_path=graph_path, df=filtered_df)

@app.route("/export/csv")
def export_csv():
    filename = "filtered_data.csv"
    df.to_csv(filename, index=False)
    return send_file(filename, as_attachment=True)

@app.route("/export/pdf")
def export_pdf():
    filename = "filtered_data.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Reporte de Ventas", ln=True, align="C")

    # Agregar datos (máx. 20 filas)
    for i in range(min(20, len(df))):
        row = df.iloc[i].astype(str).tolist()
        pdf.cell(200, 10, " | ".join(row), ln=True, align="L")

    pdf.output(filename)
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
