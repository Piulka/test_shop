from database import Session
from models.product import Product


def get_names_from_db():
    session = Session()
    names = [product.name for product in session.query(Product).all()]
    session.close()
    return names

