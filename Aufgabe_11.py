# 11. Benutzer sollen Zeiträume (Tag, Woche, Monat, Jahr) als Filter auswählen können.
# 12. Möglichkeit, Analyseergebnisse als PDF- oder CSV-Bericht zu exportieren.

# 11. los usuarios deben poder seleccionar periodos de tiempo (día, semana, mes, año) como filtros.
# 12. posibilidad de exportar los resultados de los análisis en formato PDF o CSV.

import pandas as pd


#CSV
csv_url = "https://raw.githubusercontent.com/santiagoLopez1712/Agilesmanagementprojekt/refs/heads/main/train_cleaned.csv"
df = pd.read_csv(csv_url)
print(df.head())

df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df.dropna(subset=["Order Date"], inplace=True)
# print(df.dtypes) 


df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.month 
df["Week"] = df["Order Date"].dt.isocalendar().week 
df["Day"] = df["Order Date"].dt.day 
df["Datum"] = df["Order Date"].dt.date  

df_filtrado = df.copy()


while True:
    print("\n Wählen Sie den Zeitraum zum Filtern aus:")
    print(" - Jahr  (Geben Sie: jahr)")
    print(" - Monat (Geben Sie: monat)")
    print(" - Woche (Geben Sie: woche)")
    print(" - Tag   (Geben Sie: tag)")
    print(" - Datumsbereich filtern (Geben Sie: datum)")
    print()
    print(" - Zurücksetzen (Geben Sie: reset)")
    print(" - Beenden      (Geben Sie: exit)")

    option = input("\n Eingeben Sie die gewünschte Option: ").strip().lower()

    if option == "exit":
        print("\nProgramm beendet.")
        break  # Schleife beendet

    if option == "reset":
        df_filtrado = df.copy()
        print("\n Filter zurückgesetzt!")
        continue  # Vuelve a mostrar las opciones

    if option == "jahr":
        jahr = int(input("Geben Sie das Jahr ein (z.B. 2023): "))
        df_filtrado = df_filtrado[df_filtrado["Year"] == jahr]

    elif option == "monat":
        monat = int(input("Geben Sie die Nummer des Monats ein (1-12): "))
        df_filtrado = df_filtrado[df_filtrado["Month"] == monat]

    elif option == "woche":
        woche = int(input("Geben Sie die Nummer der Woche (1-52) ein: "))
        df_filtrado = df_filtrado[df_filtrado["Week"] == woche]

    elif option == "tag":
        tag = int(input("Geben Sie die Nummer des Tages im Monat ein (1-31): "))
        df_filtrado = df_filtrado[df_filtrado["Order Date"].dt.day == tag]

    # elif option == "datum":
    #     datum = input("Geben Sie das Datum im Format JJJJ-MM-TT (z.B. 2017-12-06) ein: ")
    #     try:
    #         datum = pd.to_datetime(datum).date()
    #         df_filtrado = df_filtrado[df_filtrado["Datum"] == datum]
    #     except ValueError:
    #         print("\n Fehler: Ungültiges Datum eingegeben.")
    #         continue  # Vuelve al menú

    elif option == "datum":
        start_date = input("Geben Sie das Startdatum im Format JJJJ-MM-TT ein (z.B. 2017-01-01): ")
        end_date = input("Geben Sie das Enddatum im Format JJJJ-MM-TT ein (z.B. 2017-12-31): ")
        
        try:
            start_date = pd.to_datetime(start_date).date()
            end_date = pd.to_datetime(end_date).date()

            df_filtrado = df_filtrado[(df_filtrado["Datum"] >= start_date) & (df_filtrado["Datum"] <= end_date)]
        except ValueError:
            print("\n Fehler: Ungültiges Datum eingegeben.")
            continue 

    else:
        print("\n Fehler: Ungültige Option gewählt.")
        continue  # Vuelve al menú

    # Mostrar resultado filtrado
    if not df_filtrado.empty:
        print("\n Gefilterte Daten:")
        print(df_filtrado.head())
    else:
        print("\n Keine Daten für den ausgewählten Zeitraum gefunden.")



# option = input("Eingeben Sie die gewünschte Option: ").strip().lower()

# df_filtrado = None

# if option == "jahr":
#     jahr = int(input("Geben Sie das Jahr ein (z.B. 2023): "))
#     df_filtrado = df[df["Year"] == jahr]

# elif option == "monat":
#     jahr = int(input("Geben Sie das Jahr ein (z.B. 2023): "))
#     monat = int(input("Geben Sie die Nummer des Monats ein (1-12): "))
#     df_filtrado = df[(df["Year"] == jahr) & (df["Month"] == monat)]

# elif option == "woche":
#     jahr = int(input("Geben Sie das Jahr ein (z.B. 2023): "))
#     woche = int(input("Geben Sie die Nummer der Woche (1-52) ein: "))
#     df_filtrado = df[(df["Year"] == jahr) & (df["Week"] == woche)]

# elif option == "tag":
#     datum = input("Geben Sie das Datum im Format JJJJ-MM-TT (z.B ) ein: ")
#     try:
#         datum = pd.to_datetime(datum).date()
#         df_filtrado = df[df["Day"] == datum]
#     except ValueError:
#         print("\n Fehler: Ungültiges Datum eingegeben.")

# else:
#     print("\n Fehler: Ungültige Option gewählt.")


# if df_filtrado is not None and not df_filtrado.empty:
#     print("\n Gefilterte Daten:")
#     print(df_filtrado.head())
# else:
#     print("\n Keine Daten für den ausgewählten Zeitraum gefunden.")