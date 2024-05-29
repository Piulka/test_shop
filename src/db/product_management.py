# product_management.py
from telebot import types
from src.db.models.product import Product
from src.db.database import Session


def add_product(message, bot):
    bot.send_message(message.chat.id, 'Введите название продукта:', reply_markup=get_cancel_button())
    bot.register_next_step_handler(message, get_product_name, bot)


def get_product_name(message, bot):
    if message.text.lower() == "отмена":
        bot.send_message(message.chat.id, 'Добавление продукта отменено.')
        return
    product_name = message.text
    bot.send_message(message.chat.id, 'Введите описание продукта:', reply_markup=get_cancel_button())
    bot.register_next_step_handler(message, get_product_description, bot, product_name)


def get_product_description(message, bot, product_name):
    if message.text.lower() == "отмена":
        bot.send_message(message.chat.id, 'Добавление продукта отменено.')
        return
    product_description = message.text
    bot.send_message(message.chat.id, 'Введите цену продукта:', reply_markup=get_cancel_button())
    bot.register_next_step_handler(message, get_product_price, bot, product_name, product_description)


def get_product_price(message, bot, product_name, product_description):
    if message.text.lower() == "отмена":
        bot.send_message(message.chat.id, 'Добавление продукта отменено.')
        return
    try:
        product_price = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, 'Цена должна быть числом. Попробуйте снова.')
        bot.register_next_step_handler(message, get_product_price, bot, product_name, product_description)
        return
    session = Session()
    new_product = Product(name=product_name, description=product_description, price=product_price)
    session.add(new_product)
    session.commit()
    session.close()
    bot.send_message(message.chat.id, 'Продукт успешно добавлен в базу данных.')


def get_cancel_button():
    cancel_button = types.InlineKeyboardButton("Отмена", callback_data="cancel_adding_product")
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(cancel_button)
    return keyboard
