from src.db.database import get_session
from models.product import Product


def create_product(name, description, price):
    session = get_session()
    existing_product = session.query(Product).filter_by(name=name).first()
    if existing_product:
        print(f"Продукт '{name}' уже существует")
        return
    product = Product(name=name, description=description, price=price)
    session.add(product)
    session.commit()
    print(f"Продукт '{name}' added")
    session.close()


def get_products(prodict_id):
    session = get_session()
    products = session.query(Product).get(prodict_id)
    session.close()
    return products
