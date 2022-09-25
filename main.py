from aiogram import executor
from telegram_bot.bot import dp
import data.config


if __name__ == '__main__':
    data.config.get_json_data()
    executor.start_polling(dp, skip_updates=True)
