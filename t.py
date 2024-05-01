from joblib import load
import pandas as pd


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


def main():

    # Load the model from the file
    model = load("best_model_pipeline.joblib")
    new_car = {
        "model": "MX-5",
        "brand": "Mazda",
        "status": "sold",
        "transmission": "manual",
        #'location': 'california',
        "year": 2021,
        "miles": 15000,
        "featured": False,
        "inspected": False,
        "car_age": 2024 - 2021,
    }

    predicted_price = predict_car_price(new_car, model)
    print(f"Predicted Price: ${predicted_price:.2f}")


if __name__ == "__main__":
    main()
