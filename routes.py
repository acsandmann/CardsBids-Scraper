import json
import os
from xml.dom import ValidationErr
from flask import Blueprint, jsonify, make_response, render_template, request, Response 
from models import Car
from sqlalchemy.exc import SQLAlchemyError
from db import db_session as session
from sqlalchemy import text
import pandas as pd
from joblib import load

main = Blueprint("main", __name__)
# model = Blueprint("model", __name__)

from flask.views import MethodView

def root_dir():  
    return os.path.abspath(os.path.dirname(__file__))

def get_file(filename): 
    try:
        return open(os.path.join(root_dir(), filename)).read()
    except IOError as exc:
        return str(exc)

def predict_car_price(new_data, model):
    input_data = pd.DataFrame([new_data])

    prediction = model.predict(input_data)
    return prediction[0]


class IndexSite(MethodView):

    def get(self):
        content = get_file('./index.html')
        return Response(content, mimetype="text/html")


class ShowCars(MethodView):

    def get(self):
        cars = Car.query.all()
        return jsonify([car.to_dict() for car in cars])
    
class CarDetail(MethodView):
    def get(self, sale_id):
        car = Car.query.get(sale_id)
        if car:
            return jsonify(car.to_dict())
        else:
            return make_response(jsonify({"error": "Car not found"}), 404)

    def post(self):
        data = request.json
        try:
            car = Car(**data)
            session.add(car)
            session.commit()
            return make_response(jsonify(car.to_dict()), 201)
        except SQLAlchemyError as e:
            session.rollback()
            return make_response(jsonify({"error": str(e)}), 400)

    def put(self, sale_id):
        car = Car.query.get(sale_id)
        if not car:
            return make_response(jsonify({"error": "Car not found"}), 404)

        data = request.json
        print(data)
        try:
            for key, value in data.items():
                setattr(car, key, value)
            print(car)
            session.commit()
            return jsonify(car.to_dict())
        except SQLAlchemyError as e:
            session.rollback()
            return make_response(jsonify({"error": str(e)}), 400)

    def delete(self, sale_id):
        car = Car.query.get(sale_id)
        if not car:
            return make_response(jsonify({"error": "Car not found"}), 404)

        try:
            session.delete(car)
            session.commit()
            return make_response(jsonify({"message": "Car deleted"}), 204)
        except SQLAlchemyError as e:
            session.rollback()
            return make_response(jsonify({"error": str(e)}), 400)

class Brands(MethodView):
    def get(self):
        brands = session.execute(text("SELECT DISTINCT brand FROM cars")).all()
        return jsonify(list(map(lambda x: x[0], brands)))
    
class Brand(MethodView):
    def get(self, brand):
        cars = session.query(Car).where(Car.brand.ilike(brand)).all()
        return jsonify([car.to_dict() for car in cars])
    
class Predict(MethodView):
    def __init__(self):
        super().__init__()
        self.model = load("best_model_pipeline.joblib")

    def post(self):
        data = request.get_json()
        print(data)
        try:
            prediction = predict_car_price({
                "model": data["model"],
                "brand": data["make"],
                "transmission": data["transmission"].lower(),
                "year": int(data["year"]),
                "miles": int(data["mileage"]),
                "featured": bool(data["featured"]),
                "inspected": bool(data["inspected"]),
                "car_age": 2024 - int(data["year"]),
                "status": "sold"
            
            }, self.model)
            print(prediction)
            return jsonify({"price": prediction}), 200
        except ValidationErr as err:
            return jsonify(err.messages), 400

    
    def get(self):
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
        predicted_price = predict_car_price(new_car, self.model)
        return f"Predicted Price: ${predicted_price:.2f}"


main.add_url_rule('/', view_func=IndexSite.as_view('index'))
main.add_url_rule("/cars/", view_func=ShowCars.as_view("show_users"))
main.add_url_rule("/car/", view_func=CarDetail.as_view("create_car"), methods=['POST'])
main.add_url_rule("/car/<int:sale_id>", view_func=CarDetail.as_view("car_details"), methods=['GET', 'PUT', 'DELETE'])
main.add_url_rule("/brands/", view_func=Brands.as_view("brands"))
main.add_url_rule("/brand/<string:brand>", view_func=Brand.as_view("brand"))
main.add_url_rule("/predict/", view_func=Predict.as_view("predict"), methods=['GET', 'POST'])
