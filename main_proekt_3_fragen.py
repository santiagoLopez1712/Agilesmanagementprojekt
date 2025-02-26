import pandas as pd

# Wir arbeiten mit einer pandas.DataFrame-Tabelle, nicht mit Klassen und Objekten.
# Datei mit Kodierungsverarbeitung laden

file_path = r"d:\Gut_proekt\train.csv"
df = pd.read_csv(file_path, encoding="utf-8")

# Datenüberprüfung
#print("Erste Zeilen der Datei:")
#print(df.head())

# Warnung
print("Warnung: Alle Daten werden in das Format TT.MM.JJJJ konvertiert.")

# Datumskonvertierung mit Fehlerbehandlung
df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True, errors='coerce').dt.strftime("%d.%m.%Y")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True, errors='coerce').dt.strftime("%d.%m.%Y")

# Nach der Konvertierung prüfen
#print("Nach Datumsumrechnung:")
#print(df[["Bestelldatum", "Versanddatum"]].head())

# Datei speichern
output_path = r"d:\Gut_proekt\train_ddmmyyyy.csv"
df.to_csv(Ausgabepfad, Index=Falsch, Kodierung=„utf-8“)

print(f"Datei gespeichert: {output_path}")