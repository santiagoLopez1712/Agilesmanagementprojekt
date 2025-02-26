import pandas as pd

# Загрузка файла с обработкой кодировки
file_path = r"d:\Gut_proekt\train.csv"
df = pd.read_csv(file_path, encoding="utf-8")

# Проверка данных
#print("Первые строки файла:")
#print(df.head())

# Предупреждение
print("Внимание: Все даты будут преобразованы в формат DD.MM.YYYY.")

# Преобразование дат с обработкой ошибок
df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True, errors='coerce').dt.strftime("%d.%m.%Y")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True, errors='coerce').dt.strftime("%d.%m.%Y")

# Проверка после преобразования
#print("После преобразования дат:")
#print(df[["Order Date", "Ship Date"]].head())

# Сохранение файла
output_path = r"d:\Gut_proekt\train_ddmmyyyy.csv"
df.to_csv(output_path, index=False, encoding="utf-8")

print(f"Файл сохранен: {output_path}")