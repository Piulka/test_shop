from models.product import Product
from database import Session


def delete_product(product_id):
    print(product_id)
    session = Session()
    product = session.query(Product).get(product_id)
    print(product)
    if product:
        print(product.id)
        session.delete(product)
        print(product)
        session.commit()
        return True
    session.close()
    return False
