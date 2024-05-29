import telebot

from src.admin_list import add_admin, is_admin


def create_inline_keyboard(message):
    kb = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton(text='О магазине', callback_data='shop')
    btn2 = telebot.types.InlineKeyboardButton(text='Товары', callback_data='products')
    btn3 = telebot.types.InlineKeyboardButton(text='Контакты', callback_data='contacts')
    add_admin(message.from_user.id)
    if is_admin(message.from_user.id):
        btn4 = telebot.types.InlineKeyboardButton(text='Добавить продукт', callback_data='add_product')
        kb.add(btn4)
    kb.add(btn1, btn2, btn3)
    return kb

