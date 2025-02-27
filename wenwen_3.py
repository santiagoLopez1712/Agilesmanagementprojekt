import pandas as pd
import urllib.request
url_2_csv = "https://raw.githubusercontent.com/santiagoLopez1712/Agilesmanagementprojekt/refs/heads/wenwen/train_cleaned.csv"
file_2_csv = "train_cleaned.csv"
urllib.request.urlretrieve(url_2_csv, file_2_csv)
df_train = pd.read_csv(file_2_csv)   # train.csv neue Version importieren und lesen

print(df_train.head(7))   
## Result: zeig die erste 7 Zeile der neue saubere Dataset, test gut

# Aufgabe 9: Erstellung interaktiver Diagramme (Balken-, Linien- und Kreisdiagramme)
import matplotlib.pyplot as plt

# Convert 'Order Date' to datetime format
df_train['Order Date'] = pd.to_datetime(df_train['Order Date'], format="%d/%m/%Y")

## Balkendiagramme: Plot Bar Chart with Different Colors for Each Year
# Extract Year & Month-Year
df_train['Year'] = df_train['Order Date'].dt.year
df_train['Month-Year'] = df_train['Order Date'].dt.strftime('%m/%Y')

# Aggregate Sales by Month-Year
sales_by_month = df_train.groupby(['Year', 'Month-Year'])['Sales'].sum().reset_index()

# Define colors for different years
year_colors = {2015: "#FFA500", 2016: "#00008B", 2017: "#90EE90", 2018: "#006400"}

# Plot Bar Chart
plt.figure(figsize=(12, 6))
for year in sales_by_month['Year'].unique():
    subset = sales_by_month[sales_by_month['Year'] == year]
    plt.bar(subset['Month-Year'], subset['Sales'], color=year_colors[year], label=str(year))

# Rotate X-axis labels
plt.xticks(rotation=90)

# Labels & Title
plt.xlabel("Month-Year")
plt.ylabel("Total Sales")
plt.title("Total Sales by Month-Year (Colored by Year)")
plt.legend(title="Year")

# Show Plot
plt.show()


## Liniendiagramme: Plot Line Chart with Different Colors for Each Year

# Ensure 'Order Date' is in datetime format
df_train['Order Date'] = pd.to_datetime(df_train['Order Date'], format='%d/%m/%Y')

# Extract Year and Year-Month
df_train['Year'] = df_train['Order Date'].dt.year
df_train['Year-Month'] = df_train['Order Date'].dt.to_period('M')

# Aggregate Sales by Year-Month
sales_by_month = df_train.groupby(['Year', 'Year-Month'])['Sales'].sum().reset_index()

# Convert 'Year-Month' to string for plotting
sales_by_month['Year-Month'] = sales_by_month['Year-Month'].astype(str)

# Define Colors for Each Year
year_colors = {2015: 'orange', 2016: 'darkblue', 2017: 'lightgreen', 2018: 'darkgreen'}

# Plot Line Chart with Different Colors for Each Year
plt.figure(figsize=(12, 6))

for year, color in year_colors.items():
    year_data = sales_by_month[sales_by_month['Year'] == year]
    plt.plot(year_data['Year-Month'], year_data['Sales'], marker='o', linestyle='-', color=color, label=str(year))

# Formatting
plt.xlabel("Month-Year")
plt.ylabel("Total Sales")
plt.title("Monthly Sales Trend by Year")
plt.xticks(rotation=90)  # Rotate labels for better readability
plt.legend(title="Year")
plt.grid(True)

# Show Plot
plt.show()


## Kreisdiagramme (Pie Chart)
# Extract the year
df_train['Year'] = df_train['Order Date'].dt.year

# Aggregate sales by Year
sales_by_year = df_train.groupby('Year')['Sales'].sum()

# Create the pie chart
plt.figure(figsize=(8, 6))
plt.pie(
    sales_by_year, 
    labels=sales_by_year.index, 
    autopct='%1.1f%%', 
    startangle=140, 
    colors=plt.cm.Paired.colors
)

# Add title
plt.title('Total Sales Distribution by Year')

# Show the plot
plt.show()