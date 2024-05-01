import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from joblib import dump


engine = create_engine('sqlite:///cars.db')
data = pd.read_sql("SELECT * FROM cars", engine)

data['car_age'] = 2024 - data['year']  


categorical_features = ['model', 'brand', 'status', 'transmission']
numerical_features = ['miles', 'car_age'] 


categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])


preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_features),
        ('cat', categorical_transformer, categorical_features)
    ])


model = RandomForestRegressor(random_state=42)
pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('classifier', model)])

X = data.drop('price', axis=1)  
y = data['price']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

dump(pipeline, 'model_pipeline.joblib')


from sklearn.model_selection import RandomizedSearchCV

# Define parameter grid for RandomizedSearchCV
param_grid = {
    'classifier__n_estimators': [100, 200, 300],
    'classifier__max_depth': [None, 10, 20, 30],
    'classifier__min_samples_leaf': [1, 2, 4],
    'classifier__min_samples_split': [2, 5, 10]
}


search = RandomizedSearchCV(pipeline, param_grid, n_iter=10, cv=5, verbose=2, random_state=42, scoring='neg_mean_absolute_error')

search.fit(X_train, y_train)

best_model = search.best_estimator_

dump(best_model, 'best_model_pipeline.joblib')

print("Best model parameters:", search.best_params_)

def predict_car_price(new_data, model):
    """
    Predicts the car price using the trained model pipeline.
    
    Args:
        new_data (dict): A dictionary containing the new car attributes.
        model (Pipeline): The trained model pipeline including preprocessing steps.
    
    Returns:
        float: The predicted price of the car.
    """
    input_data = pd.DataFrame([new_data])

    prediction = model.predict(input_data)
    return prediction[0]

new_car = {
    'model': 'MX-5',
    'brand': 'Mazda',
    'status': 'sold',
    'transmission': 'manual',
    #'location': 'california',
    'year': 2021,
    'miles': 30000,
    'featured': False,
    'inspected': False,
    'car_age': 2024 - 2021  
}

predicted_price = predict_car_price(new_car, best_model)
print(f"Predicted Price: ${predicted_price:.2f}")