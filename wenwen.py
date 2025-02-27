import pandas as pd
import os
import re
import chardet

# Funktion zum Laden der Datei mit korrekter Kodierung
def lade_csv():
    file_path = "Agilesmanagementprojekt/train_cleaned.csv"

    # Kodierung erkennen
    with open(file_path, "rb") as f:
        result = chardet.detect(f.read(100000))  

    # CSV mit der erkannten Kodierung laden
    df = pd.read_csv(file_path, encoding=result["encoding"])
    print("CSV-Datei erfolgreich geladen mit Kodierung:", result["encoding"])
    return df

# Funktion zum Entfernen von Sonderzeichen
def entferne_sonderzeichen(df):
    def bereinige_text(text):
        if isinstance(text, str):
            text = text.encode("latin1", "ignore").decode("utf-8", "ignore")
            text = re.sub(r'[^\x00-\x7F]+', '', text)  
        return text

    spalten_zum_bereinigen = ["Customer Name", "Product Name"]
    for spalte in spalten_zum_bereinigen:
        df[spalte] = df[spalte].astype(str).apply(bereinige_text)

    print("Sonderzeichen entfernt.")
    return df

# Funktion zum Korrigieren von langen Produktnamen
def korrigiere_lange_texte(df):
    ersetzungen = {
        "I Need's 3d Hello Kitty Hybrid Silicone Case Cover for HTC One X 4g with 3d Hello Kitty Stylus Pen Green/pink":
        "3D Hello Kitty Silicone Case Cover, Green/Pink",
        "Ativa D5772 2-Line 5.8GHz Digital Expandable Corded/Cordless Phone System with Answering & Caller ID/Call Waiting, Black/Silver":
        "Ativa D5772 Digital Expandable Phone System, Black/Silver"
    }
    df["Product Name"] = df["Product Name"].replace(ersetzungen)
    print("Lange Texte korrigiert.")
    return df

# Hauptfunktion
if __name__ == "__main__":
    df = lade_csv()
    df = entferne_sonderzeichen(df)
    df = korrigiere_lange_texte(df)
    df.to_csv("Agilesmanagementprojekt/train_cleaned.csv", index=False, encoding="utf-8")
    print("Bereinigte Datei gespeichert.")
