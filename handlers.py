# handlers.py
import telebot
from keyboard_main import create_inline_keyboard
from models.product import Product
from database import Session
from product_management import add_product, get_cancel_button
import product_selection


def register_handlers(bot):
    @bot.callback_query_handler(func=lambda call: call.data == 'cancel_adding_product')
    def handle_cancel_adding_product(call):
        bot.answer_callback_query(call.id, text="Добавление продукта отменено.")
        bot.send_message(call.message.chat.id, 'Добавление продукта отменено.')
        bot.clear_step_handler_by_chat_id(call.message.chat.id)  # Очищаем шаги, чтобы прервать процесс добавления

    @bot.callback_query_handler(func=lambda call: call.data.startswith('confirm_delete_'))
    def handle_confirm_delete__button(call):
        product_selection.handle_confirmation_button(bot, call)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('delete_'))
    def handle_delete_button(call):
        print(call.data)
        product_selection.handle_delete_button(bot, call)
        print(call.data)

    @bot.message_handler(commands=['start'])
    def create_reply_keyboard(message):
        rkb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = telebot.types.KeyboardButton('Показать меню')
        rkb.add(btn)
        bot.send_message(message.chat.id, 'Привет, я тестовый бот-магазин', reply_markup=rkb)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('next_'))
    def handle_next_button(call):
        offset = int(call.data.split('_')[1])
        session = Session()
        products = session.query(Product).all()
        kb_products = product_selection.create_products_keyboard(products, offset)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите товар',
                              reply_markup=kb_products)
        session.close()

    @bot.message_handler(func=lambda message: message.text == 'Показать меню')
    def show_inline_keyboard(message):
        kb = create_inline_keyboard(message)
        bot.send_message(message.chat.id, 'Вот ваша инлайн-клавиатура:', reply_markup=kb)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_worker(call):
        if call.data == 'shop':
            bot.send_message(call.message.chat.id, 'Это тестовый магазин')
        elif call.data == 'add_product':
            add_product(call.message, bot)
        elif call.data == 'contacts':
            bot.send_message(call.message.chat.id, 'Телеграмм: @xPiul, Телефон: +7 (800) 555-35-35')
        elif call.data == 'products':
            product_selection.handle_products_command(bot, call.message)
        else:
            product_selection.handle_product_selection(bot, call)
