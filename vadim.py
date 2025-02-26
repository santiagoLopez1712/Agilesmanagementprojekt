import pandas as pd
import matplotlib.pyplot as plt
import sys

def calculate_sales_stat(df, beginn_zeiraums, ende_zeitraums, stat_type):
    """
    Die Funktion berechnet die Verkaufsstatistiken für einen bestimmten Datumsbereich.

    :param df: DataFrame mit Verkaufsdaten
    :param start_date: Beginn des Zeitraum (Zeichenfolge im Format 'tt/mm/jjjj')
    :param end_date: Ende des Zeitraum (Zeichenfolge im Format 'tt/mm/jjjj')
    :param stat_type: Statistiktyp ('sum', 'mean', 'median', 'std')
    :return: Berechneter Statistikwert
    """
    # Konvertieren von Daten in das Format datetime
    df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d/%m/%Y")

    # Konvertieren die vom Benutzer eingegebenen Daten
    beginn_zeiraums = pd.to_datetime(beginn_zeiraums, format="%d/%m/%Y")
    ende_zeitraums = pd.to_datetime(ende_zeitraums, format="%d/%m/%Y")

    # Daten nach Datumsbereich filtern
    filtered_df = df[df["Order Date"].between(beginn_zeiraums, ende_zeitraums)]

    # Prüfen, ob es Daten für diesen Zeitraum gibt
    if filtered_df.empty:
        print("Keine Daten für den angegebenen Zeitraum.")
        return None

    # Wählen eine statistische Operation
    # Add test string
    if stat_type == "sum":
        result = filtered_df["Sales"].sum()
        operation_name = "Summe"
    elif stat_type == "mean":
        result = filtered_df["Sales"].mean()
        operation_name = "Durchschnittlicher Umsatz"
    elif stat_type == "median":
        result = filtered_df["Sales"].median()
        operation_name = "Median des Umsatzes"
    elif stat_type == "std":
        result = filtered_df["Sales"].std()
        operation_name = "Standardabweichung"
    else:
        print("Fehler: Ungultige statistische Operation angegeben")
        return None

    return operation_name, result

def trends_monthly_quarterly_sales(df, beginn_zr, ende_zr, stat_type):
    """
    die Funktion erstellt Diagramme des Umsatzvolumens nach Monat und Quartal
    innerhalb eines bestimmten Zeitraums, um den Umsatztrend zu messen
    """
    
    # Daten in das richtige Format bringen
    df["Sales"] = df["Sales"].astype(float)  # Sicherstellen, dass "Sales" ein numerisches Format ist

    # Umwandlung in das Datetime-Format
    beginn_zr = pd.to_datetime(beginn_zr, format="%d/%m/%Y")
    ende_zr = pd.to_datetime(ende_zr, format="%d/%m/%Y")

    df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d/%m/%Y", errors="coerce") # wenn falsche Daten vorkommen, ersetzen Pandas sie durch NaT (Not a Time), um Fehler zu vermeiden.

    # Datenfilterung nach Datumsbereich
    filtered_df = df[(df["Order Date"] >= beginn_zr) & (df["Order Date"] <= ende_zr)]

    # Gruppierung nach Monaten
    monthly_sales = filtered_df.resample("ME", on="Order Date")["Sales"].sum()

    # Gruppierung nach Quartalen
    quarterly_sales = filtered_df.resample("QE", on="Order Date")["Sales"].sum()

    # Datenvisualisierung
    plt.figure(figsize=(12, 5))

    # 1. Diagramm der monatlichen Verkäufe
    plt.subplot(1, 2, 1)  # 1 ряд, 2 столбца, 1-й график
    plt.plot(monthly_sales.index, monthly_sales.values, marker="o", linestyle="-", color="b")
    plt.xlabel("Datum")
    plt.ylabel("Verkaufsvolumen")
    plt.title("Monatliche Verkäufe")
    plt.xticks(rotation=45)

    # 2. Diagramm der quartalsweisen Verkäufe
    plt.subplot(1, 2, 2)  #  1 Zeile, 2 Spalten, 2. Diagramm
    plt.bar(quarterly_sales.index.strftime("%Y-Q%q"), quarterly_sales.values, color="g")
    plt.xlabel("Quartal")
    plt.ylabel("Verkaufsvolumen")
    plt.title("Quartalsweise Verkäufe")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()
    sys.exit()


# Haupteinheit des Programms
if __name__ == "__main__":

    # Laden der Daten aus der CSV-Datei
    df = pd.read_csv("train.csv", delimiter=",")

    # Konvertierung (Umwandeln) der Spalte „Sales“ in Float, falls sie kein numerisches Format hat
    df["Sales"] = df["Sales"].astype(float)

    # Eingabe des Datumsbereichs durch den Benutzer
    beginn_zr = input("Geben Sie das Startdatum ein (TT/MM/JJJJ): ")
    ende_zr = input("Geben Sie das Enddatum ein (TT/MM/JJJJ): ")

    # Auswählen einer statistischen Funktion
    print("\n Geben Sie die Nummer der Operation ein:")
    print("  1 - Summe")
    print("  2 - Durchschnittlicher Umsatz")
    print("  3 - Median des Umsatzes")
    print("  4 - Standardabweichung")
    print("  5 - Diagramme des Umsatzvolumens nach Monat und Quartal")

    stat_choice = input("Geben Sie die Nummer der Operation ein: ")

    # Zuordnung der Benutzereingabe zur Funktion
    stat_types = {
    "1": "sum",
    "2": "mean",
    "3": "median",
    "4": "std",
    "5": "trends_Monat-Quartal_Verkaufszahlen"
}

stat_type = stat_types.get(stat_choice)

if stat_type == "trends_Monat-Quartal_Verkaufszahlen":
    trends_monthly_quarterly_sales(df, beginn_zr, ende_zr, stat_type)
else:
    operation_name, result = calculate_sales_stat(df, beginn_zr, ende_zr, stat_type)
    if result is not None:
        print(f"\n {operation_name} zwischen {beginn_zr} und {ende_zr}: {result:.2f}")
    else:
        print("Fehler: Ungültige Eingabe. Bitte versuchen Sie es erneut.")