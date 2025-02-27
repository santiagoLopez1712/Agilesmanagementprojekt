import pandas as pd

# URL des heruntergeladenen Files
url = "https://raw.githubusercontent.com/santiagoLopez1712/Agilesmanagementprojekt/main/train_cleaned.csv"

# Daten werden von der URL geladen
df = pd.read_csv(url)

# Region als Eingabe des Benutzers
region_filter = input("Geben Sie die zu filternde Region ein (z. B. West): ")

# Dateninformationen anzeigen
#print("info")
#df.info()

# Filtern nach Region "..."
df_filtered = df[df["Region"] == region_filter]
print("Region gefiltert")

# Berechnung des Gesamtverkaufsbetrags
total_sales = df_filtered["Sales"].sum()

# Ausgabe der gefilterten Daten und des Verkaufsbetrags
print(df_filtered)
print(f"\nGesamtumsatz in der Region '{region_filter}': {total_sales}")

print("Kategoriefilter")
# Gruppieren von Daten nach Produktkategorien und Summieren von Verkäufen
sales_by_category = df_filtered.groupby("Category")["Sales"].sum().reset_index()

# Ausgabe der Nachberechnungsergebnisse
print(sales_by_category)

# Test bei Git
