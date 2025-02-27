import pandas as pd
import matplotlib.pyplot as plt


def daten_laden(dateiname):
    """Lädt die CSV-Datei in ein DataFrame."""
    return pd.read_csv(dateiname)


def daten_vorbereiten(df):
    """Bereitet die Daten für die Visualisierung vor."""
    df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d/%m/%Y")
    df["Jahr"] = df["Order Date"].dt.year
    df["Jahr-Monat"] = df["Order Date"].dt.to_period("M").astype(str)
    return df


def balkendiagramm_erstellen(df):
    """Erstellt ein Balkendiagramm der monatlichen Umsätze pro Jahr."""
    umsatz_pro_monat = df.groupby(["Jahr", "Jahr-Monat"])["Sales"].sum().reset_index()
    jahr_farben = {2015: "#FFA500", 2016: "#00008B", 2017: "#90EE90", 2018: "#006400"}

    plt.figure(figsize=(12, 6))
    for jahr in umsatz_pro_monat["Jahr"].unique():
        teilmenge = umsatz_pro_monat[umsatz_pro_monat["Jahr"] == jahr]
        plt.bar(teilmenge["Jahr-Monat"], teilmenge["Sales"], color=jahr_farben[jahr], label=str(jahr))

    plt.xticks(rotation=90)
    plt.xlabel("Monat-Jahr")
    plt.ylabel("Gesamtumsatz")
    plt.title("Gesamtumsatz pro Monat-Jahr")
    plt.legend(title="Jahr")
    plt.show()


def liniengrafik_erstellen(df):
    """Erstellt eine Liniendiagramm für den Umsatztrend pro Jahr."""
    umsatz_pro_monat = df.groupby(["Jahr", "Jahr-Monat"])["Sales"].sum().reset_index()
    jahr_farben = {2015: "orange", 2016: "darkblue", 2017: "lightgreen", 2018: "darkgreen"}

    plt.figure(figsize=(12, 6))
    for jahr, farbe in jahr_farben.items():
        jahr_daten = umsatz_pro_monat[umsatz_pro_monat["Jahr"] == jahr]
        plt.plot(jahr_daten["Jahr-Monat"], jahr_daten["Sales"], marker="o", linestyle="-", color=farbe, label=str(jahr))

    plt.xlabel("Monat-Jahr")
    plt.ylabel("Gesamtumsatz")
    plt.title("Monatlicher Umsatztrend")
    plt.xticks(rotation=90)
    plt.legend(title="Jahr")
    plt.grid(True)
    plt.show()


def main():
    dateiname = "train_cleaned.csv"
    df = daten_laden(dateiname)
    df = daten_vorbereiten(df)

    balkendiagramm_erstellen(df)
    liniengrafik_erstellen(df)


if __name__ == "__main__":
    main()
