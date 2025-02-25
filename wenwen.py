import pandas as pd
import urllib.request

# 1. Die Anwendung muss Verkaufsdaten aus einer CSV-Datei importieren.
# Use the correct raw GitHub URL for the CSV file
url_csv = "https://raw.githubusercontent.com/santiagoLopez1712/Agilesmanagementprojekt/main/train.csv"
filename_csv = "train.csv"

# Download the CSV file
urllib.request.urlretrieve(url_csv, filename_csv)
print(f"CSV-Datei wurde als '{filename_csv}' heruntergeladen.")

# Read the downloaded CSV file into a pandas DataFrame
df_train = pd.read_csv(filename_csv)

# Print the first 7 rows of the DataFrame
print("Erste 7 Zeilen des 'train'-Datensatzes:")
print(df_train.head(7))



# 2. Fehlende oder fehlerhafte Daten müssen erkannt und behandelt werden.
# 1) fehlende Werte (NaN)
# 2) doppelte Einträge
# 3) falsche Datentypen
# 4) negative Preise oder falsche Datumswerte
# 5) falsche Schreibweisen

print(df_train.info())  # Gibt einen Überblick über Sales Datei

# Für 1) fehlende Werte (NaN): 
print(df_train.isnull().sum())  # Zeigt die Anzahl fehlender Werte pro Spalte
## Result: "Postal Code      11"


# Filtern der Zeilen, in denen "Postal Code" fehlt
city_ohne_PLZ = df_train[df_train["Postal Code"].isnull()]["City"]

# Ausgabe der betroffenen Städte
print("Städte mit fehlender PLZ:")
print(city_ohne_PLZ) 
## Result: 11 PLZ der "Burlington" fehlen


# ob alle "Burlington" haben keine PLZ? Dann zeig alle Zeilen mit der Stadt "Burlington" an
burlington_rows = df_train[df_train["City"] == "Burlington"]
print(burlington_rows[["City", "State", "Region", "Postal Code"]])
## Result: Nur "City: Burlington, State: Vermont, Region: East" hat keine PLZ. 
## Andere "Burlington" haben entsprechende PLZ. Aber Dtype(float64)/Kommazahl ist falsch, es soll Dtype(int) sein.

# Für 3) falsche Datentypen:
# von float zu int umwandeln
df_train["Postal Code"] = pd.to_numeric(df_train["Postal Code"], errors='coerce').fillna(0).astype(int)

# nochmal alle Zeilen mit der Stadt "Burlington" anzeigen, keine Kommazahl
burlington_rows = df_train[df_train["City"] == "Burlington"]
print(burlington_rows[["City", "State", "Region", "Postal Code"]])

# nach Google: "City: Burlington, State: Vermont, Region: East" hat PLZ: 05401

# Alle "Postal Code" sollen als String umwandeln, weil Dtype(int) keine "0" am Start darf. 
df_train["Postal Code"] = df_train["Postal Code"].astype(str)

# PLZ für Burlington(Vermont, East) setzen
df_train.loc[
    (df_train["City"] == "Burlington") & 
    (df_train["State"] == "Vermont") & 
    (df_train["Region"] == "East"), 
    "Postal Code"] = "05401"  # "0" am Start

# nochmal alle Zeilen mit der Stadt "Burlington" anzeigen
burlington_rows = df_train[df_train["City"] == "Burlington"]
print(burlington_rows[["City", "State", "Region", "Postal Code"]])
## Result: jetzt keine fehlende PLZ, und alle PLZ haben richtige Datentype.

# Für 2): doppelte Zeilen zu finden
duplicates = df_train[df_train.duplicated()]
print("Duplicate rows:\n", duplicates)
## Result: keine Duppelte

# Für 4): negative Preise zu finden
outliers = df_train[df_train["Sales"] < 0]
print("Negative sales values:\n", outliers)
## Result: keine negative Sales Werte

# Für 4): falsche Datumswerte zu finden
# Convert "Order Date" and "Ship Date" to datetime with correct format, setting errors='coerce' to handle invalid dates
df_train["Order Date"] = pd.to_datetime(df_train["Order Date"], format="%d/%m/%Y", errors="coerce")
df_train["Ship Date"] = pd.to_datetime(df_train["Ship Date"], format="%d/%m/%Y", errors="coerce")

# Find rows where either "Order Date" or "Ship Date" is "NaT" (missing or incorrect)
problem_rows = df_train[df_train["Order Date"].isna() | df_train["Ship Date"].isna()]
# Show only relevant columns
print("invalid Dates are:\n", problem_rows[["Order ID", "Order Date", "Ship Date"]])

# Find rows where "Ship Date" is earlier than "Order Date"
invalid_ship_dates = df_train[df_train["Ship Date"] < df_train["Order Date"]]
# Show only relevant columns
print("invalid Ship Dates are:\n", invalid_ship_dates[["Order ID", "Order Date", "Ship Date"]])
## Result: keine falsche Datum


# Für 5): falsche Einträge zu finden
print("Unique Ship Modes:", df_train["Ship Mode"].unique())
## Result: ['Second Class' 'Standard Class' 'First Class' 'Same Day']. 'Same Day' ist falsch Input.

# Alle Zeilen mit "Same Day" anzeigen
SameDay_rows = df_train[df_train["Ship Mode"] == "Same Day"]
print("wrong Ship Mode:\n", SameDay_rows[["Row ID", "Order ID", "Order Date", "Ship Date", "Ship Mode", "Region", "Postal Code"]])
## Result: Es gibt 538 falsche Zeile mit "Same Day". 

## Wir können nicht wissen, was die richtige "Ship Mode" waren. 
## Aber es ist auch nicht so wichtig. Deshalb setze ich hier "Standard Class" statt "Same Day" um.
df_train["Ship Mode"] = df_train["Ship Mode"].replace("Same Day", "Standard Class")
# Verify the fix
print("Fixed Ship Modes:", df_train["Ship Mode"].unique())