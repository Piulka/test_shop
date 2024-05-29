from app import create_product, get_products

if __name__ == '__main__':
    create_product('Бургер41253',
                   'Две мя3сные котлеты грилль, специальный соус сыр, огурцы салат и лук, все на булочке с кунжутом',
                   1220)
    product = get_products(1)
    print(product.name)
