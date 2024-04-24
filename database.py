""" https://docs.sqlalchemy.org/en/20/
model is primary key

car { brand, model, year, price/currentbid, status: on sale/sold, miles?, time_left?, transmission?, featured: true|false, 
     inspected: true|false, location: { city, state/province, zip}, reserve: true|false }

add query to get all cars by brand (select * from cars where brand = f'${brand}')
all cars by year
filter by price
filter by model """

"""CREATE TABLE cars IF NOT EXIST (
    brand VARCHAR(255) NOT NULL,
    model VARCHAR(255) NOT NULL,
    year INT NOT NULL,
    price DECIMAL (10,2) NOT NULL,
    current_bid DECIMAL (10,2),
    status ENUM("not sold", "sold"),
    miles INT NOT NULL,
    transmission ENUM ("none", "manual"),
    featured BOOLEAN,
    inspected BOOLEAN,
    city VARCHAR(255) NOT NULL,
    is_province BOOLEAN,
    province VARCHAR(255) NOT NULL,
    reserve BOOLEAN,

);

# GET Cars by brand

SELECT * FROM cars WHERE brand = f'${BRAND}';

# GET Cars by Year
SELECT * FROM cars WHERE year = f'${YEAR}';

# GET cars by price
SELECT * FROM cars WHERE price = f'${PRICE}';

# GET cars by model

SELECT * FROM cars WHERE model = f'${MODEL}';"""


class Cars:
    def __init__(
        self,
        brand,
        model,
        year,
        price,
        current_bid,
        status,
        miles,
        transmission,
        featured,
        inspected,
        city,
        state,
        zip_code,
        is_province,
        province,
        reserve,
    ):

        self.brand = brand
        self.model = model
        self.year = year
        self.price = price
        self.current_bid = current_bid
        self.status = status
        self.miles = miles
        self.transmission = transmission
        self.featured = featured
        self.inspected = inspected
        self.city = city
        self.state = state
        self.zip = zip_code
        self.is_province = is_province
        self.province = province
        self.reserve = reserve

    def get_brand(self):
        return self.session.query(Cars).filter(Cars.brand == self.brand).all()

    def get_model(self):
        return self.session.query(Cars).filter(Cars.model == self.model).all()

    def get_year(self):
        return self.session.query(Cars).filter(Cars.year == self.year).all()

    def get_price(self):
        return self.session.query(Cars).filter(Cars.price == self.price).all()

    def get_current_bid(self):
        return (
            self.session.query(Cars).filter(Cars.current_bid == self.current_bid).all()
        )

    def get_status(self):
        return self.session.query(Cars).filter(Cars.status == self.status).all()

    def get_miles(self):
        return self.session.query(Cars).filter(Cars.miles == self.miles).all()

    def get_trans(self):
        return (
            self.session.query(Cars).filter(Cars.tranmisson == self.transmission).all()
        )

    def get_featured_status(self):
        return self.session.query(Cars).filter(Cars.featured == self.featured).all()

    def get_inspection_status(self):
        return self.session.query(Cars).filter(Cars.inspected == self.inspected).all()

    def get_city(self):
        return self.session.query(Cars).filter(Cars.city == self.city).all()

    def get_state(self):
        return self.session.query(Cars).filter(Cars.state == self.state).all()

    def get_zip(self):
        return self.session.query(Cars).filter(Cars.zip == self.zip).all()

    def get_is_province_status(self):
        return (
            self.session.query(Cars).filter(Cars.is_provice == self.is_province).all()
        )

    def get_province(self):
        return (
            self.session.query(Cars)
            .filter(Cars.get_province == self.get_province)
            .all()
        )

    def get_reserve(self):
        return (
            self.session.query(Cars).filter(Cars.is_provice == self.get_reserve).all()
        )


from sqlalchemy import (
    create_engine,
    exists,
)
from sqlalchemy.orm import sessionmaker, declarative_base
import json
import re
from models import Car, StatusEnum

Base = declarative_base()


class CarsManager:
    def __init__(self, database_url):
        self.engine = create_engine(database_url)
        Car.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_car(
        self,
        title,
        price,
        status,
        url,
        miles=None,
        transmission=None,
        featured=False,
        inspected=False,
        location=None,
        reserve=None,
    ):
        try:
            year, (brand, model) = Car.extract_car_details(title)

            if miles is not None:
                miles = int(
                    re.match(r"(\d{1,3}(?:,\d{3})*|\~\d+)", miles)
                    .group(0)
                    .replace(",", "")
                    .strip("~")
                )

            c = Car(
                sale_id=Car.generate_id(url),
                model=model,
                brand=brand,
                year=year,
                price=float(re.sub(r"[,$]", "", price).strip("$")),
                status=StatusEnum.sold,
                miles=miles,
                transmission=Car.parse_trans(transmission),
                # featured=featured,
                # inspected=inspected,
                # location=location,
                # reserve=reserve,
                url=url,
            )
            return c
        except:
            print(url)

    def batch_create_cars(self, car_data_list):
        new_cars = []
        ids = []

        for data in car_data_list:
            id_ = Car.generate_id(data["url"])
            if not self.session.query(exists().where(Car.sale_id == id_)).scalar():
                if id_ not in ids:
                    ids.append(id_)

                    if isinstance(data, Car):
                        new_cars.append(data)
                    else:
                        if "sold_price" not in data.keys():
                            data["sold_price"] = 0

                        new_cars.append(
                            self.create_car(
                                data["title"],
                                data["sold_price"],
                                0,
                                data["url"],
                                data["mileage"],
                                data["transmission"],
                            )
                        )
                else:
                    print(data["url"])
        self.session.add_all(new_cars)
        self.session.commit()

        return f"Batch processed: Added {len(new_cars)} new cars."

    def get_cars_by_brand(self, brand):
        return self.session.query(Car).filter(Car.brand == brand).all()

    def get_cars_by_year(self, year):
        return self.session.query(Car).filter(Car.year == year).all()

    def get_cars_by_price(self, price):
        return self.session.query(Car).filter(Car.price == price).all()

    def get_cars_by_model(self, model):
        return self.session.query(Car).filter(Car.model == model).all()

    def get_current_bid(self, current_bid):
        return (
            self.session.query(Cars).filter(Cars.current_bid == self.current_bid).all()
        )

    def get_status(self, status):
        return self.session.query(Cars).filter(Cars.status == self.status).all()

    def get_miles(self, miles):
        return self.session.query(Cars).filter(Cars.miles == self.miles).all()

    def get_trans(self, transmission):
        return (
            self.session.query(Cars).filter(Cars.tranmisson == self.transmission).all()
        )

    def get_featured_status(self, featured):
        return self.session.query(Cars).filter(Cars.featured == self.featured).all()

    def get_inspection_status(self, inspected):
        return self.session.query(Cars).filter(Cars.inspected == self.inspected).all()

    def get_city(self, city):
        return self.session.query(Cars).filter(Cars.city == self.city).all()

    def get_state(self, state):
        return self.session.query(Cars).filter(Cars.state == self.state).all()

    def get_zip(self, zip_code):
        return self.session.query(Cars).filter(Cars.zip == self.zip).all()

    def get_is_province_status(self, is_province):
        return (
            self.session.query(Cars).filter(Cars.is_provice == self.is_province).all()
        )

    def get_province(self, province):
        return (
            self.session.query(Cars)
            .filter(Cars.get_province == self.get_province)
            .all()
        )

    def get_reserve(self, reserve):
        return (
            self.session.query(Cars).filter(Cars.is_provice == self.get_reserve).all()
        )


def main():
    manager = CarsManager("sqlite:///./cars.db")

    cars = json.load(open("./scraped_data.json"))
    print(len(cars))

    manager.batch_create_cars(cars)
    # Example tests
    cars_honda = manager.get_cars_by_brand("Honda")
    print("Honda Cars:")
    for car in cars_honda:
        print(car)

    cars_year = manager.get_cars_by_year(1996)
    print("\nYears in 1996:")
    for car in cars_year:
        print(car)

    cars_model = manager.get_cars_by_model("S2000")
    print("\nS2000 Listings:")
    for car in cars_model:
        print(car)


if __name__ == "__main__":
    main()
