from app import create_product, get_products

if __name__ == '__main__':
    create_product('Бургер12',
                   'Две мясные котлеты грилль, специальный соус сыр, огурцы салат и лук, все на булочке с кунжутом',
                   120)
    product = get_products(1)
    print(product.name)
