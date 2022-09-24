from aiogram import executor
from telegram_bot.bot import dp

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
