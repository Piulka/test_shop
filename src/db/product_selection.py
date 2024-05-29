# product_selection.py
from telebot import types
from src.db.models.product import Product
from src.db.database import Session
from src.admin_list import is_admin
from src.db.product_del import delete_product


def create_products_keyboard(products, offset=0):
    kb_products = types.InlineKeyboardMarkup()
    # Разбиваем товары на две колонки по 5 штук
    for i in range(offset, min(len(products), offset + 10), 2):
        row = []
        if i < len(products):
            row.append(types.InlineKeyboardButton(text=products[i].name, callback_data=f'product_{products[i].id}'))
        if i + 1 < len(products):
            row.append(
                types.InlineKeyboardButton(text=products[i + 1].name, callback_data=f'product_{products[i + 1].id}'))
        kb_products.row(*row)

    # Добавляем кнопку "Назад" в конце первого столбца
    if offset > 0:
        kb_products.row(types.InlineKeyboardButton(text='Назад', callback_data=f'prev_{max(0, offset - 10)}'))

    # Добавляем кнопку "Далее" в конце второго столбца
    if len(products) > offset + 10:
        kb_products.row(types.InlineKeyboardButton(text='Далее', callback_data=f'next_{offset + 10}'))

    return kb_products


def handle_products_command(bot, message):
    session = Session()
    products = session.query(Product).all()
    kb_products = create_products_keyboard(products)
    bot.send_message(message.chat.id, 'Выберите товар', reply_markup=kb_products)
    session.close()


def create_product_buttons(product_id, user_id, product_message_id):
    markup = types.InlineKeyboardMarkup()
    buy_button = types.InlineKeyboardButton('Купить', callback_data=f'buy_{product_id}')
    markup.add(buy_button)

    # Проверяем, является ли пользователь администратором
    if is_admin(user_id):
        delete_button = types.InlineKeyboardButton('Удалить товар',
                                                   callback_data=f'delete_{product_id}_{product_message_id}')
        markup.add(delete_button)

    return markup


# Обработчик для кнопки удаления продукта
def handle_delete_button(bot, call):
    if call.data.startswith('delete_'):
        parts = call.data.split('_')
        product_id = int(parts[1])
        product_message_id = int(parts[2])
        reply_markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("Да",
                                          callback_data=f"confirm_delete_yes_{product_id}_{call.message.message_id}_{product_message_id}")
        btn2 = types.InlineKeyboardButton("Нет",
                                          callback_data=f"confirm_delete_no_{call.message.message_id}_{product_message_id}")
        reply_markup.add(btn1, btn2)
        bot.send_message(call.message.chat.id, 'Вы действительно хотите удалить этот товар?', reply_markup=reply_markup)


def handle_confirmation_button(bot, call):
    if call.data.startswith('confirm_delete_yes_'):
        parts = call.data.split('_')
        product_id = int(parts[3])
        original_message_id = int(parts[4])
        product_message_id = int(parts[5])
        delete_product(product_id)
        bot.send_message(call.message.chat.id, 'Товар успешно удален.')
        try:
            bot.delete_message(call.message.chat.id, original_message_id)
        except Exception as e:
            print(f"Error deleting message {original_message_id}: {e}")
        try:
            bot.delete_message(call.message.chat.id, product_message_id)
        except Exception as e:
            print(f"Error deleting message {product_message_id}: {e}")
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception as e:
            print(f"Error deleting message {call.message.message_id}: {e}")
    elif call.data.startswith('confirm_delete_no_'):
        parts = call.data.split('_')
        product_message_id = int(parts[3])
        bot.send_message(call.message.chat.id, 'Удаление отменено.')
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception as e:
            print(f"Error deleting message {call.message.message_id}: {e}")
        try:
            bot.delete_message(call.message.chat.id, product_message_id)
        except Exception as e:
            print(f"Error deleting message {product_message_id}: {e}")


def handle_product_selection(bot, call):
    if call.data.startswith('product_'):
        product_id = int(call.data.split('_')[1])
        session = Session()
        product = session.query(Product).get(product_id)
        if product:
            product_message = f"{product.name}\n\n{product.description}\n\nЦена: {product.price}"
            bot.send_message(call.message.chat.id, product_message,
                             reply_markup=create_product_buttons(product_id, call.from_user.id,
                                                                 call.message.message_id))
            # Удаляем старое сообщение
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except Exception as e:
                print(f"Error deleting message {call.message.message_id}: {e}")
        else:
            bot.send_message(call.message.chat.id, 'Товар не найден')
        session.close()
    elif call.data.startswith('next_'):
        offset = int(call.data.split('_')[1])
        session = Session()
        products = session.query(Product).all()
        kb_products = create_products_keyboard(products, offset)
        try:
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=kb_products)
        except Exception as e:
            print(f"Error editing message {call.message.message_id}: {e}")
        session.close()
    elif call.data.startswith('prev_'):
        offset = int(call.data.split('_')[1])
        session = Session()
        products = session.query(Product).all()
        kb_products = create_products_keyboard(products, offset)
        try:
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=kb_products)
        except Exception as e:
            print(f"Error editing message {call.message.message_id}: {e}")
        session.close()


def handle_buy_button(bot, call):
    if call.data.startswith('buy_'):
        product_id = int(call.data.split('_')[1])
        session = Session()
        product = session.query(Product).get(product_id)
        if product:
            # Здесь должна быть логика покупки, например, изменение количества товара в базе данных
            bot.send_message(call.message.chat.id, f'Вы успешно купили {product.name}')
        else:
            bot.send_message(call.message.chat.id, 'Товар не найден')
        session.close()
