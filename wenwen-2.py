# 2. Fehlende oder fehlerhafte Daten müssen erkannt und behandelt werden.
# 6) kommisches Zeichen
# 7) super lange Texte 

import pandas as pd
import urllib.request
url_csv = "https://raw.githubusercontent.com/santiagoLopez1712/Agilesmanagementprojekt/main/train.csv"
filename_csv = "train.csv"
urllib.request.urlretrieve(url_csv, filename_csv)
df_train = pd.read_csv(filename_csv)

# Für 6) kommisches Zeichen
import chardet  # Detect Encoding Issues
import re

# 1️. Detect Encoding First (to avoid misreading file)
with open("train.csv", "rb") as f:
    result = chardet.detect(f.read(100000))  # Read a part of the file
    print("Detected Encoding:", result)  # utf-8

# 2️. Load CSV with correct Encoding
df_train = pd.read_csv("train.csv", encoding="ISO-8859-1")

# 3️. Define Function to Find Garbled Text (Non-ASCII)
def find_garbled_text(text):
    return bool(re.search(r'[^\x00-\x7F]', str(text)))  # Detect non-ASCII characters

# 4️. Detect and Display Garbled Text Before Cleaning
print("Checking for Garbled Text BEFORE Cleaning: \n")
for column in df_train.columns:
    mask = df_train[column].astype(str).apply(find_garbled_text)
    df_garbled = df_train[mask]
    
    if not df_garbled.empty:
        print(f"Garbled text found in column: {column}")
        print(df_garbled[[column]].head(7).to_string(index=False))
## Result: only find the strange letters in the column "Customer Name" and column "Product Name"


# 5. Apply multiple cleaning techniques to Remove Unreadable Characters from all columns
def clean_text(text):
    if isinstance(text, str):
        text = text.encode("latin1", "ignore").decode("utf-8", "ignore")  # Convert correctly
        text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII characters
    return text
# Apply to specific columns
columns_to_clean = ["Customer Name", "Product Name"]
for column in columns_to_clean:
    df_train[column] = df_train[column].astype(str).apply(clean_text)


# 6️. Detect Garbled Text in column "Customer Name" and column "Product Name" After Cleaning
print("Checking for Garbled Text AFTER Cleaning: \n")
for column in ["Customer Name", "Product Name"]:
    mask2 = df_train[column].astype(str).apply(find_garbled_text)
    df_garbled2 = df_train[mask2]
    
    if not df_garbled.empty:
        print(f"Garbled text still found in column: {column}")
        print(df_garbled2[[column]].head(7).to_string(index=False))  
    else:
        print(f"Column '{column}' is now clean.")


# Für 7): Super lange Texte (>100 Zeichen) finden:
for column in df_train.columns:  
    df_long_text = df_train[df_train[column].astype(str).str.len() > 100]
    
    if not df_long_text.empty:  
        print(f"Lang Text in Colum: {column} \n")
        print(df_long_text[[column]].to_string(index=False))  # only show the problem column
## Result: the column "Product Name" has mistakes.
## 10 Products are "I Need's 3d Hello Kitty Hybrid Silicone Case Cover for HTC One X 4g with 3d Hello Kitty Stylus Pen Green/pink"
## 4 Products are "Ativa D5772 2-Line 5.8GHz Digital Expandable Corded/Cordless Phone System with Answering & Caller ID/Call Waiting, Black/Silver"

# change the 1st mistake into "3D Hello Kitty Silicone Case Cover, Green/Pink"
df_train["Product Name"] = df_train["Product Name"].replace("I Need's 3d Hello Kitty Hybrid Silicone Case Cover for HTC One X 4g with 3d Hello Kitty Stylus Pen Green/pink", 
                                                            "3D Hello Kitty Silicone Case Cover, Green/Pink")
# change the 2nd mistake into "Ativa D5772 Digital Expandable Phone System, Black/Silver"
df_train["Product Name"] = df_train["Product Name"].replace("Ativa D5772 2-Line 5.8GHz Digital Expandable Corded/Cordless Phone System with Answering & Caller ID/Call Waiting, Black/Silver",
                                                             "Ativa D5772 Digital Expandable Phone System, Black/Silver")

# search Super lang Text (>100 Zeichen) again:
for column in df_train.columns:  
    df_long_text = df_train[df_train[column].astype(str).str.len() > 100]
    
    if not df_long_text.empty:  
        print(f"Lang Text in Colum: {column} \n")
        print(df_long_text[[column]].to_string(index=False)) 
    else: 
        print(f"No Lang Text")
## Result: All 18 Columns' text length are less than 100.



# Am Ende: Save the cleaned dataset
# Define the save path
save_path = r"D:\4-IntoCode\12_PM\Git_test\Agilesmanagementprojekt\train_cleaned.csv"
# Save the cleaned dataset
df_train.to_csv(save_path, index=False, encoding="utf-8")
print(f"Cleaned file saved at: {save_path}")