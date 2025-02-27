import pandas as pd
import urllib.request


def csv_herunterladen(url, dateiname):
    """Lädt eine CSV-Datei von einer URL herunter."""
    urllib.request.urlretrieve(url, dateiname)
    print(f"CSV heruntergeladen als '{dateiname}'.")


def daten_laden(dateiname):
    """Lädt die CSV-Datei in ein DataFrame."""
    return pd.read_csv(dateiname)


def fehlende_werte_bereinigen(df):
    """Behandelt fehlende Werte in den Daten."""
    print("Fehlende Werte pro Spalte:\n", df.isnull().sum())
    df["Postal Code"] = pd.to_numeric(df["Postal Code"], errors="coerce").fillna(0).astype(int)
    df["Postal Code"] = df["Postal Code"].astype(str)
    df.loc[
        (df["City"] == "Burlington") & (df["State"] == "Vermont") & (df["Region"] == "East"),
        "Postal Code",
    ] = "05401"
    return df


def doppelte_werte_erkennen(df):
    """Erkennt doppelte Zeilen."""
    duplikate = df[df.duplicated()]
    print("Doppelte Zeilen:\n", duplikate)
    return duplikate


def ungültige_umsätze_prüfen(df):
    """Überprüft negative Werte in der Spalte 'Sales'."""
    ausreißer = df[df["Sales"] < 0]
    print("Negative Werte in 'Sales':\n", ausreißer)
    return ausreißer


def ungültige_daten_prüfen(df):
    """Konvertiert Datumswerte und prüft ungültige Werte."""
    df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d/%m/%Y", errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%d/%m/%Y", errors="coerce")
    ungültige_daten = df[df["Order Date"].isna() | df["Ship Date"].isna()]
    print("Ungültige Datumswerte:\n", ungültige_daten[["Order ID", "Order Date", "Ship Date"]])
    return df


def versandart_bereinigen(df):
    """Korrigiert fehlerhafte Werte in der Spalte 'Ship Mode'."""
    df["Ship Mode"] = df["Ship Mode"].replace("Same Day", "Standard Class")
    return df


def main():
    url = "https://raw.githubusercontent.com/santiagoLopez1712/Agilesmanagementprojekt/main/train_cleaned.csv"
    dateiname = "train.csv"

    csv_herunterladen(url, dateiname)
    df = daten_laden(dateiname)

    df = fehlende_werte_bereinigen(df)
    doppelte_werte_erkennen(df)
    ungültige_umsätze_prüfen(df)
    df = ungültige_daten_prüfen(df)
    df = versandart_bereinigen(df)

    print("Bereinigte Daten bereit zur Nutzung.")


if __name__ == "__main__":
    main()
