from flask import Blueprint, jsonify
from models import Car

main = Blueprint("main", __name__)

from flask.views import MethodView


class ShowCars(MethodView):

    def get(self):
        cars = Car.query.all()
        return jsonify([car.to_dict() for car in cars])


main.add_url_rule("/cars/", view_func=ShowCars.as_view("show_users"))
