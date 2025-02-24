import pandas as pd
import urllib.request

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