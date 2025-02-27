import os
import pandas as pd
import subprocess

# URL der Datei auf GitHub
url = "https://raw.githubusercontent.com/santiagoLopez1712/Agilesmanagementprojekt/main/train_cleaned.csv"

# Lokaler Pfad des Repositorys auf Ihrem PC (anpassen, falls erforderlich)
repo_path = r"C:\Users\nutzer\Desktop\Agiles und Git\Agilesmanagementprojekt"
file_path = os.path.join(repo_path, "train_cleaned.csv")

try:
    # Datei von GitHub herunterladen
    df = pd.read_csv(url, encoding="utf-8")
    print("✅ Datei erfolgreich von GitHub heruntergeladen.")

    # Datumskonvertierung
    print("⚠️  Konvertiere Datumsangaben in das Format TT.MM.JJJJ...")
    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True, errors='coerce').dt.strftime("%d.%m.%Y")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True, errors='coerce').dt.strftime("%d.%m.%Y")

    # Datei lokal überschreiben
    df.to_csv(file_path, index=False, encoding="utf-8")
    print(f"✅ Datei überschrieben: {file_path}")


except Exception as e:
    print(f"❌ Fehler: {e}")
