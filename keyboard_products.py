import telebot
import sqlalchemy
from db.db import Session


def get_names_from_db():
    session = Session()
    names = [product.name for product in session.query(Product).all()]
    session.close()
    return names
def products():
    names = get_names_from_db()
    kb_products = telebot.types.InlineKeyboardMarkup()
    for name in names:
        kb_products.add(telebot.types.InlineKeyboardButton(text=name, callback_data=name))
    bot.send_message(message.chat.id, 'Выберите товар', reply_markup=kb_products)
