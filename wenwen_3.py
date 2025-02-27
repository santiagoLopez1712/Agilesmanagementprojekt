import pandas as pd
import matplotlib.pyplot as plt
import os

# Funktion zum Laden der bereinigten Daten
def lade_csv():
    file_path = "Agilesmanagementprojekt/train_cleaned.csv"
    df = pd.read_csv(file_path)
    df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d/%m/%Y")
    return df

# Funktion zur Erstellung eines Balkendiagramms
def erstelle_balkendiagramm(df):
    df["Year"] = df["Order Date"].dt.year
    sales_by_month = df.groupby(['Year', df["Order Date"].dt.strftime('%m/%Y')])["Sales"].sum().reset_index()
    
    farben = {2015: "#FFA500", 2016: "#00008B", 2017: "#90EE90", 2018: "#006400"}

    plt.figure(figsize=(12, 6))
    for year in sales_by_month["Year"].unique():
        plt.bar(sales_by_month[sales_by_month["Year"] == year]["Order Date"], 
                sales_by_month[sales_by_month["Year"] == year]["Sales"], 
                color=farben[year], label=str(year))

    plt.xticks(rotation=90)
    plt.xlabel("Monat-Jahr")
    plt.ylabel("Gesamtumsatz")
    plt.title("Umsatz pro Monat (nach Jahr gefärbt)")
    plt.legend(title="Jahr")
    plt.show()

# Funktion zur Erstellung eines Liniendiagramms
def erstelle_liniendiagramm(df):
    df["Year"] = df["Order Date"].dt.year
    sales_by_month = df.groupby(['Year', df["Order Date"].dt.to_period("M")])["Sales"].sum().reset_index()
    
    farben = {2015: 'orange', 2016: 'darkblue', 2017: 'lightgreen', 2018: 'darkgreen'}

    plt.figure(figsize=(12, 6))
    for year, farbe in farben.items():
        plt.plot(sales_by_month[sales_by_month["Year"] == year]["Order Date"].astype(str), 
                 sales_by_month[sales_by_month["Year"] == year]["Sales"], 
                 marker='o', linestyle='-', color=farbe, label=str(year))

    plt.xticks(rotation=90)
    plt.xlabel("Monat-Jahr")
    plt.ylabel("Gesamtumsatz")
    plt.title("Monatliche Umsatztrends nach Jahr")
    plt.legend(title="Jahr")
    plt.grid(True)
    plt.show()

# Hauptfunktion
if __name__ == "__main__":
    df = lade_csv()
    erstelle_balkendiagramm(df)
    erstelle_liniendiagramm(df)
