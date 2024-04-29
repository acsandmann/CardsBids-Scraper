import os
from flask import Blueprint, jsonify, make_response, render_template, request, Response
from models import Car
from sqlalchemy.exc import SQLAlchemyError
from db import db_session as session

main = Blueprint("main", __name__)

from flask.views import MethodView

def root_dir():  
    return os.path.abspath(os.path.dirname(__file__))

def get_file(filename): 
    try:
        return open(os.path.join(root_dir(), filename)).read()
    except IOError as exc:
        return str(exc)


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


main.add_url_rule('/', view_func=IndexSite.as_view('index'))
main.add_url_rule("/cars/", view_func=ShowCars.as_view("show_users"))
main.add_url_rule("/car/", view_func=CarDetail.as_view("create_car"), methods=['POST'])
main.add_url_rule("/car/<int:sale_id>", view_func=CarDetail.as_view("car_details"), methods=['GET', 'PUT', 'DELETE'])
