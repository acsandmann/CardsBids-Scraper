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
        image_url,
        end_date,
        miles=None,
        transmission=None,
        horsepower=None,
        modifications=None,
        ownership=None,
        extra=None,
        featured=False,
        inspected=False,
        location=None,
        reserve=None,
    ):
        try:
            d = Car.extract_car_details(title)
            year, brand, model = d["year"], d["brand"], d["model"]    

            c = Car(
                sale_id=Car.generate_id(url),
                model=model,
                brand=brand,
                year=year,
                price=float(re.sub(r"[,$]", "", str(price)).strip("$")),
                status=StatusEnum.sold,
                miles=Car.parse_mileage(miles),
                transmission=Car.parse_trans(transmission),
                featured=featured,
                inspected=inspected,
                location=location,
                reserve=reserve,
                url=url,
                image_url=image_url,
                end_date=end_date,
                horsepower=horsepower,
                modifications=modifications,
                ownership=ownership,
                extra=extra,
            )
            return c
        except Exception as e:
            print(url, price)
            print("create car:", url)
            print(e)
            return None

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
                        c = self.create_car(
                            data["title"],
                            data["sold_price"],
                            0,
                            data["url"],
                            data["image_url"],
                            data["end_date"],
                            data["mileage"],
                            data["transmission"],
                            data["engine"],
                            data["modifications"],
                            data["ownership"],
                            data["extra"]
                        )
                        if c:
                            new_cars.append(c)
                else:
                    print("batch:", data["url"])
        self.session.add_all(new_cars)
        self.session.commit()

        return f"Batch processed: Added {len(new_cars)} new cars."


def main():
    manager = CarsManager("sqlite:///./cars.db")

    cars = json.load(open("./scraped_data.g.json"))
    print(len(cars))
    manager.batch_create_cars(cars)


if __name__ == "__main__":
    main()
