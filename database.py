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
    def __init__(self, brand, model, year, price, current_bid, status,
                 miles, transmission, featured, inspected, city, state, zip_code, is_province, province, reserve):

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
        return self.session.query(Cars).filter(Cars.current_bid == self.current_bid).all()
    
    def get_status(self):
        return self.session.query(Cars).filter(Cars.status == self.status).all()
    
    def get_miles(self):
        return self.session.query(Cars).filter(Cars.miles == self.miles).all()
    
    def get_trans(self):
        return self.session.query(Cars).filter(Cars.tranmisson == self.transmission).all()
    
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
        return self.session.query(Cars).filter(Cars.is_provice == self.is_province).all()
    
    def get_province(self):
        return self.session.query(Cars).filter(Cars.get_province == self.get_province).all()
    
    def get_reserve(self):
        return self.session.query(Cars).filter(Cars.is_provice == self.get_reserve).all()
    
    
    



def main():

    Instance1 = Cars("Honda" ,"S2000", 2005, 2000, 500, "not sold", 30000, "manual", True, True, "Seattle", False, None)


    cars_honda = Instance1.get_brand("honda")
    print("Honda Cars")
    for car in cars_honda:
        print(car)

    cars_year = Instance1.get_year(1996)
    print("Years in 1996")
    for car in cars_year:
        print(car)

    
    cars_model = Instance1.get_model("S2000")
    print("S2000 Listings")
    for car in cars_model:
        print(car)



if __name__ == 'main':
    main()