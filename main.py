from aiogram import executor
from telegram_bot.bot import dp
import data.config


if __name__ == '__main__':
    print("БОТ ВЫШЕЛ В ОНЛАЙН!!!")
    data.config.logger.warning("БОТ ВЫШЕЛ В ОНЛАЙН!!!")
    data.config.get_json_data()
    executor.start_polling(dp, skip_updates=True)
