from aiogram import executor
from telegram_bot.bot import dp
from data.config import get_json_data

from telegram_bot.bot import storage

if __name__ == '__main__':
    get_json_data()
    storage.push()
    executor.start_polling(dp, skip_updates=True)
