# main.py
from telebot import TeleBot
from Token import TOKEN
from src import handlers

# Инициализация бота
bot = TeleBot(TOKEN)


# Перемещение регистрации обработчиков в main.py
handlers.register_handlers(bot)

bot.polling(none_stop=True)
