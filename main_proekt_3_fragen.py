import os
import pandas as pd

# Definir la ruta de entrada del archivo CSV
file_path = r"C:\Users\nutzer\Desktop\Agiles und Git\Agilesmanagementprojekt\train_cleaned.csv"

# Überprüfen, ob die Datei existiert
if not os.path.exists(file_path):
    print(f"Fehler: Die Datei '{file_path}' wurde nicht gefunden.")
    exit()

# Datei mit UTF-8-Kodierung laden
df = pd.read_csv(file_path, encoding="utf-8")

# Warnung
print("Warnung: Alle Daten werden in das Format TT.MM.JJJJ konvertiert.")

# Sicherstellen, dass die benötigten Spalten existieren
if "Order Date" in df.columns and "Ship Date" in df.columns:
    # Datumskonvertierung mit Fehlerbehandlung
    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True, errors='coerce').dt.strftime("%d.%m.%Y")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True, errors='coerce').dt.strftime("%d.%m.%Y")
else:
    print("Fehler: Die Spalten 'Order Date' oder 'Ship Date' fehlen in der Datei.")
    exit()

# **SOBRESCRIBIR el archivo existente**
df.to_csv(file_path, index=False, encoding="utf-8")

print(f"✅ Datei erfolgreich überschrieben: {file_path}")
