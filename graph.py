import pandas as pd
import matplotlib.pyplot as plt
import json

# Load JSON data
with open('./scraped_data.json', 'r') as file:
    data = json.load(file)

# Create a DataFrame
df = pd.DataFrame(data)

# Convert sold prices to numerical values and handle missing values
df['sold_price'] = df['sold_price'].replace('[\$,]', '', regex=True).astype(float)

# Fill missing values if necessary
df['transmission'].fillna('Unknown', inplace=True)
df['modifications'].fillna('Unknown', inplace=True)

# Convert mileage to a clean format and handle unknowns
df['mileage'] = df['mileage'].str.extract('(\d+,\d+|\d+)')[0].str.replace(',', '').astype(float)
df['mileage'].fillna(df['mileage'].mean(), inplace=True)  # Example: fill with the mean

plt.figure(figsize=(10, 6))
plt.hist(df['sold_price'].dropna(), bins=30, color='blue', alpha=0.7)
plt.title('Distribution of Sold Prices')
plt.xlabel('Price ($)')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

plt.figure(figsize=(7, 7))
df['transmission'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.title('Transmission Types Distribution')
plt.ylabel('')
plt.show()

plt.figure(figsize=(8, 5))
mod_counts = df['modifications'].value_counts()
plt.bar(mod_counts.index, mod_counts.values, color=['red', 'green'])
plt.title('Modifications Status')
plt.xlabel('Modification Type')
plt.ylabel('Count')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
