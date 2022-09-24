from aiogram import executor
from telegram_bot.bot import dp
from data.config import get_json_data

if __name__ == '__main__':
    get_json_data()
    executor.start_polling(dp, skip_updates=True)
