from data.config import logger
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

TOKEN = "5738031171:AAEBv4hUujqqpRpApztI0ay29IsvQYt4JQM"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    button_hi = KeyboardButton('Привет! 👋')

    greet_kb = ReplyKeyboardMarkup()
    greet_kb.add(button_hi)
    await bot.send_message(message.from_user.id,
                           "Это бот для учета результатов по пробникам ЕГЭ по математике.\n"
                           "Ваши данные будут заноситься в таблицу преподавателя.\n\n"
                           "*Комманды*:\n\t\t"
                           r"/help - помощь"
                           "\n\t\t"
                           r"/addnewvariant - добавить результаты нового варианта"
                           "\n\t\t"
                           r"/editvariant - изменить результаты существующего варианта",
                           parse_mode="Markdown")


@dp.message_handler(commands=["addnewvariant"])
async def add_new_variant(message: types.Message):
    pass


@dp.message_handler(commands=["editvariant"])
async def edit_existing_variant(message: types.Message):
    pass
