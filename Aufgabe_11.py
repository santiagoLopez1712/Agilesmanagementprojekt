# 11. Benutzer sollen Zeiträume (Tag, Woche, Monat, Jahr) als Filter auswählen können.
# 12. Möglichkeit, Analyseergebnisse als PDF- oder CSV-Bericht zu exportieren.

# 11. los usuarios deben poder seleccionar periodos de tiempo (día, semana, mes, año) como filtros.
# 12. posibilidad de exportar los resultados de los análisis en formato PDF o CSV.

import pandas as pd


#CSV
csv_url = "https://raw.githubusercontent.com/santiagoLopez1712/Agilesmanagementprojekt/refs/heads/main/train_cleaned.csv"
df = pd.read_csv(csv_url)

df["Order Date"] = pd.to_datetime(df["Order Date"])
print(df.head())

df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.month 
df["Week"] = df["Order Date"].dt.isocalendar().week 
df["Day"] = df["Order Date"].dt.date  

print("\n🔹 Wählen Sie den Zeitraum zum Filtern aus:")
print(" - Jahr")
print(" - Monat")
print(" - Woche")
print(" - Tag")

option = input("Eingeben Sie die gewünschte Option: ").strip().lower()

df_filtrado = None

if option == "jahr":
    jahr = int(input("Geben Sie das Jahr ein (z.B. 2023): "))
    df_filtrado = df[df["Year"] == jahr]

elif option == "monat":
    jahr = int(input("Geben Sie das Jahr ein (z.B. 2023): "))
    monat = int(input("Geben Sie die Nummer des Monats ein (1-12): "))
    df_filtrado = df[(df["Year"] == jahr) & (df["Month"] == monat)]

elif option == "woche":
    jahr = int(input("Geben Sie das Jahr ein (z.B. 2023): "))
    woche = int(input("Geben Sie die Nummer der Woche (1-52) ein: "))
    df_filtrado = df[(df["Year"] == jahr) & (df["Week"] == woche)]

elif option == "tag":
    datum = input("Geben Sie das Datum im Format JJJJ-MM-TT ein: ")
    try:
        datum = pd.to_datetime(datum).date()
        df_filtrado = df[df["Day"] == datum]
    except ValueError:
        print("\n Fehler: Ungültiges Datum eingegeben.")

else:
    print("\n Fehler: Ungültige Option gewählt.")


if df_filtrado is not None and not df_filtrado.empty:
    print("\n Gefilterte Daten:")
    print(df_filtrado.head())
else:
    print("\n Keine Daten für den ausgewählten Zeitraum gefunden.")