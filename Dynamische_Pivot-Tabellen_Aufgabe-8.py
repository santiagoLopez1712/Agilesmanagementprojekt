import pandas as pd
import openpyxl

# Laden der Daten
df = pd.read_csv("train.csv", delimiter=",")
df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d/%m/%Y")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%d/%m/%Y")

# Benutzerdefinierte Auswahl der Spalten
print("Verfügbare Spalten:")
print(df.columns.tolist())
selected_columns = input("Geben Sie die gewünschten Spalten durch Komma getrennt ein: ").split(",")
selected_columns = [col.strip() for col in selected_columns]

# Sicherstellen, dass "Order Date" enthalten ist
if "Order Date" not in selected_columns:
    selected_columns.insert(0, "Order Date")

# Gruppierungsoptionen anzeigen
print("Mögliche Gruppierung:")
grouping_options = ["Region", "City", "Country", "Customer Name", "Category", "Product Name"]
print(grouping_options)
grouping_column = input("Wählen Sie eine Gruppierungsspalte aus: ").strip()

if grouping_column not in grouping_options:
    print("Ungültige Gruppierungsspalte. Standardmäßig wird 'Region' verwendet.")
    grouping_column = "Region"

# Zeitliche Gruppierung auswählen
zeit_gruppe = input("Geben Sie das gewünschte Zeitintervall ein (ME für Monate, QE für Quartale, Y für Jahre): ").strip().upper()
if zeit_gruppe not in ["ME", "QE", "Y"]:
    print("Ungültige Eingabe. Standardmäßig wird 'ME' verwendet.")
    zeit_gruppe = "ME"

# Daten filtern
df_filtered = df[selected_columns].copy()  # Erstellen Sie eine Kopie, um SettingWithCopyWarning zu vermeiden
df_filtered["Order Date"] = pd.to_datetime(df_filtered["Order Date"])  
df_filtered.set_index("Order Date", inplace=True)

# Daten gruppieren: Erst nach der Gruppierung numerische Werte aggregieren
df_grouped = df_filtered.groupby([pd.Grouper(freq=zeit_gruppe), grouping_column]).sum(numeric_only=True)

# Ergebnisse in eine Excel-Datei speichern
df_grouped.to_excel("dynamische_tabelle.xlsx")
print("Die Daten wurden erfolgreich in 'dynamische_tabelle.xlsx' gespeichert.")
