import pandas as pd

# Pfad zur heruntergeladenen Datei
file_path = "d:/Gut_proekt/train.csv"
# Daten werden geladen
df = pd.read_csv(file_path)

# Eingeben einer Region für Benutzer
region_filter = input("Geben Sie die zu filternde Region ein (z. B.West): ")
# Dateninformationen anzeigen
#print("info")
#df.info()

# Filtern nach Region "..."

df_filtered = df[df["Region"] == region_filter]
print("filtr region")

# Berechnung des Gesamtverkaufsbetrags
total_sales = df_filtered["Sales"].sum()

# Ausgabe der gefilterten Daten und des Verkaufsbetrags
print(df_filtered)
print(f"\nGesamtumsatz in der Region '{region_filter}': {total_sales}")

print("filtr Category")
df_filtered
# Gruppieren von Daten nach Produktkategorien und Summieren von Verkäufen
sales_by_category = df_filtered.groupby("Category")["Sales"].sum().reset_index()
# Ausgabe der Nachberechnungsergebnisse
print(sales_by_category)





