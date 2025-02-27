import pandas as pd
import urllib.request
import chardet
import re


def kodierung_erkennen(dateiname):
    """Erkennt die Kodierung der Datei."""
    with open(dateiname, "rb") as f:
        ergebnis = chardet.detect(f.read(100000))
        print("Erkannte Kodierung:", ergebnis["encoding"])
    return ergebnis["encoding"]


def daten_laden(dateiname, kodierung="ISO-8859-1"):
    """Lädt die CSV-Datei mit der richtigen Kodierung."""
    return pd.read_csv(dateiname, encoding=kodierung)


def fehlerhafte_zeichen_finden(text):
    """Findet fehlerhafte Zeichen in einem Text."""
    return bool(re.search(r"[^\x00-\x7F]", str(text)))


def text_bereinigen(text):
    """Bereinigt nicht-ASCII-Zeichen aus einem Text."""
    if isinstance(text, str):
        text = text.encode("latin1", "ignore").decode("utf-8", "ignore")
        text = re.sub(r"[^\x00-\x7F]+", "", text)
    return text


def fehlerhafte_zeichen_bereinigen(df, spalten):
    """Bereinigt fehlerhafte Zeichen in den angegebenen Spalten."""
    for spalte in spalten:
        df[spalte] = df[spalte].astype(str).apply(text_bereinigen)
    return df


def lange_texte_erkennen(df):
    """Erkennt Texte mit mehr als 100 Zeichen in jeder Spalte."""
    for spalte in df.columns:
        lange_texte = df[df[spalte].astype(str).str.len() > 100]
        if not lange_texte.empty:
            print(f"Lange Texte in '{spalte}':\n", lange_texte[spalte])


def main():
    dateiname = "train.csv"
    kodierung = kodierung_erkennen(dateiname)

    df = daten_laden(dateiname, kodierung)

    spalten_zur_bereinigung = ["Customer Name", "Product Name"]
    df = fehlerhafte_zeichen_bereinigen(df, spalten_zur_bereinigung)
    lange_texte_erkennen(df)

    df.to_csv("train_cleaned.csv", index=False, encoding="utf-8")
    print("Bereinigte Datei gespeichert als 'train_cleaned.csv'.")


if __name__ == "__main__":
    main()
