import sqlalchemy
from sqlalchemy import Column
from base import Base


class Product(Base):
    __tablename__ = 'products'
    id = Column(sqlalchemy.Integer, primary_key=True)
    name = Column(sqlalchemy.String)
    description = Column(sqlalchemy.String)
    price = Column(sqlalchemy.Float)
