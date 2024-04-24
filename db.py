from sqlalchemy import Boolean, Column, Enum, Integer, String, ForeignKey, Float, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import enum

class StatusEnum(enum.Enum):
    on_sale = 1
    pending = 2
    sold = 3

class TransmissionEnum(enum.Enum):
    manual = 1
    automatic = 2
    unknown = 3

'''
car { brand, model, year, price/currentbid, status: on sale/sold, miles?, time_left?, transmission?, featured: true|false, 
     inspected: true|false, location: { city, state/province, zip}, reserve: true|false }
     '''

class Car:
    __tablename__ = 'cars'
    sale_id = Column(Integer, primary_key=True)
    model = Column(String)
    brand = Column(String)
    price = Column(Float)
    status = Column(StatusEnum)
    miles = Column(Integer, nullable=True)
    transmission = Column(TransmissionEnum, nullable=True)
    featured = Column(Boolean, nullable=True, default=False)
    inspected = Column(Boolean, nullable=True, default=False)
    location = Column(String, nullable=True)
    reserve = Column(Boolean, nullable=True)
    #def __init__(self, data):

