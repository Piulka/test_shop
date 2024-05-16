from sqlalchemy.orm import sessionmaker
from models.product import Product
from database import engine

# Создаем сессию для взаимодействия с базой данных
Session = sessionmaker(bind=engine)
session = Session()

# Идентификатор продукта, который нужно обновить
product_id = 10  # Замените на реальный идентификатор продукта

# Находим продукт по идентификатору
product = session.query(Product).get(product_id)

# Если продукт найден, обновляем его поля
if product:
    product.name = 'Салат'
    product.description = 'Вкусный'
    product.price = 19.99  # Новая цена продукта
    session.commit()  # Сохраняем изменения в базе данных
    print('Продукт успешно обновлен')
else:
    print('Продукт не найден')

# Закрываем сессию
session.close()