import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import re

# Load the data
df = pd.read_json('./scraped_data.json')

# Preprocess the data
df['sold_price'] = df['sold_price'].replace('[\$,]', '', regex=True).astype(float)
df['year'] = df['title'].apply(lambda x: re.findall(r'\b(19[0-9][0-9]|20[0-2][0-9]|202[0-3])\b', x)[0] if re.findall(r'\b(19[0-9][0-9]|20[0-2][0-9]|202[0-3])\b', x) else 0).astype(int)

# Assuming 'title' contains a consistent format "[year] [make] [model]"
df['make'] = df['title'].apply(lambda x: x.split()[1] if len(x.split()) > 1 else 'Unknown')
df['model'] = df['title'].apply(lambda x: ' '.join(x.split()[2:]) if len(x.split()) > 2 else 'Unknown')

# Select features and target
X = df[['year', 'make', 'model']]  # This assumes categorical data will be processed correctly
y = df['sold_price']

# Convert categorical data to numeric
X = pd.get_dummies(X, columns=['make', 'model'])

# Splitting the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model training
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predicting and Evaluating the model
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f'Mean Absolute Error: {mae}')

# Saving the model for future use (optional)
import joblib
joblib.dump(model, './model.pkl')
