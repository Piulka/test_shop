# main.py
from dotenv import load_dotenv
load_dotenv()

from telebot import TeleBot
from src import handlers
from os import getenv

# Инициализация бота
bot = TeleBot(getenv("TOKEN"))


# Перемещение регистрации обработчиков в main.py
handlers.register_handlers(bot)

bot.polling(none_stop=True)
