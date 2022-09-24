from data.config import logger
from aiogram import Bot, Dispatcher, types

from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

TOKEN = "5738031171:AAEBv4hUujqqpRpApztI0ay29IsvQYt4JQM"
session_storage = {}
is_on_dialog = 0
is_on_edit = 0
editing_task = ''
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await bot.send_message(message.from_user.id,
                           "Это бот для учета результатов по пробникам ЕГЭ по математике.\n"
                           "Ваши данные будут заноситься в таблицу преподавателя.\n\n"
                           "*Комманды*:\n\t\t"
                           r"/help - помощь"
                           "\n\t\t"
                           r"/addnewvariant - добавить результаты нового варианта"
                           "\n\t\t"
                           r"/editvariant - изменить результаты существующего варианта"
                           "\n\t\t"
                           r"/push - залить данные в таблицу"
                           "\n\t\t"
                           r"/check - узнать текущее количество введенных баллов",
                           parse_mode="Markdown")


@dp.message_handler(commands=["addnewvariant"])
async def add_new_variant(message: types.Message):
    global is_on_dialog
    user = message.from_user.id
    await send_message(user, 'Давайте начнем!')
    await send_message(user, 'Введите ФИО')
    is_on_dialog = 1


@dp.message_handler(commands=['push', 'send', 'отправить', 'пуш', 'закончил', 'да'])
async def push(message: types.Message):
    global is_on_dialog
    if is_on_dialog >= 20:
        print(session_storage)
        await send_message(message.from_user.id, 'Ваши баллы были загружены. Хорошего дня!')
        is_on_dialog = 0
    else:
        await send_message(message.from_user.id, 'Сначала заполните все поля варианта')


@dp.message_handler(commands=["check", 'баллы', 'чекнуть'])
async def check(message: types.Message):
    await send_message(message.from_user.id, reformat_dict(session_storage))
    print(reformat_dict(session_storage))


@dp.message_handler(commands=["editvariant"])
async def edit_existing_variant(message: types.Message):
    global is_on_edit
    global editing_task
    user = message.from_user.id
    editing_task = ''
    await send_message(user, 'Введите номер задания, которое хотите исправить')
    is_on_edit = 1


@dp.message_handler()
async def handle(message: types.Message):
    global is_on_dialog
    global is_on_edit
    global editing_task
    text = message.text
    user = message.from_user.id
    if is_on_edit == 1:
        editing_task = text
        is_on_edit = 2
        await send_message(user, 'Введите правильное количество баллов')
    elif is_on_edit == 2:
        session_storage[editing_task] = text
        await send_message(user, 'Ваше задание исправлено(посмотреть текущие баллы можно функцией "/check")')
        if is_on_dialog < 20:
            await send_message(user, f'Введите баллы за {is_on_dialog - 2} задание')
        else:
            await send_message(user, f'Если все правильно, напишите: "да"')
        is_on_edit = 0
    else:
        if is_on_dialog == 1:
            session_storage.update({'name': text})
            await send_message(user, f'Теперь введите свой класс(11А или 11Б)')
            is_on_dialog += 1
        elif is_on_dialog == 2:
            session_storage.update({'grade': text})
            await send_message(user, f'Введите баллы за {is_on_dialog - 1} задание')
            is_on_dialog += 1
        elif is_on_dialog == 3:
            session_storage.update({str(is_on_dialog - 2): text})
            await send_message(user, f'Введите баллы за {is_on_dialog - 1} задание')
            is_on_dialog += 1
        elif is_on_dialog == 4:
            session_storage.update({str(is_on_dialog - 2): text})
            await send_message(user, f'Введите баллы за {is_on_dialog - 1} задание')
            is_on_dialog += 1
        elif is_on_dialog == 5:
            session_storage.update({str(is_on_dialog - 2): text})
            await send_message(user, f'Введите баллы за {is_on_dialog - 1} задание')
            is_on_dialog += 1
        elif is_on_dialog == 6:
            session_storage.update({str(is_on_dialog - 2): text})
            await send_message(user, f'Введите баллы за {is_on_dialog - 1} задание')
            is_on_dialog += 1
        elif is_on_dialog == 7:
            session_storage.update({str(is_on_dialog - 2): text})
            await send_message(user, f'Введите баллы за {is_on_dialog - 1} задание')
            is_on_dialog += 1
        elif is_on_dialog == 8:
            session_storage.update({str(is_on_dialog - 2): text})
            await send_message(user, f'Введите баллы за {is_on_dialog - 1} задание')
            is_on_dialog += 1
        elif is_on_dialog == 9:
            session_storage.update({str(is_on_dialog - 2): text})
            await send_message(user, f'Введите баллы за {is_on_dialog - 1} задание')
            is_on_dialog += 1
        elif is_on_dialog == 10:
            session_storage.update({str(is_on_dialog - 2): text})
            await send_message(user, f'Введите баллы за {is_on_dialog - 1} задание')
            is_on_dialog += 1
        elif is_on_dialog == 11:
            session_storage.update({str(is_on_dialog - 2): text})
            await send_message(user, f'Введите баллы за {is_on_dialog - 1} задание')
            is_on_dialog += 1
        elif is_on_dialog == 12:
            session_storage.update({str(is_on_dialog - 2): text})
            await send_message(user, f'Введите баллы за {is_on_dialog - 1} задание')
            is_on_dialog += 1
        elif is_on_dialog == 13:
            session_storage.update({str(is_on_dialog - 2): text})
            await send_message(user, f'Введите баллы за {is_on_dialog - 1} задание')
            is_on_dialog += 1
        elif is_on_dialog == 14:
            session_storage.update({str(is_on_dialog - 2): text})
            await send_message(user, f'Введите баллы за {is_on_dialog - 1} задание')
            is_on_dialog += 1
        elif is_on_dialog == 15:
            session_storage.update({str(is_on_dialog - 2): text})
            await send_message(user, f'Введите баллы за {is_on_dialog - 1} задание')
            is_on_dialog += 1
        elif is_on_dialog == 16:
            session_storage.update({str(is_on_dialog - 2): text})
            await send_message(user, f'Введите баллы за {is_on_dialog - 1} задание')
            is_on_dialog += 1
        elif is_on_dialog == 17:
            session_storage.update({str(is_on_dialog - 2): text})
            await send_message(user, f'Введите баллы за {is_on_dialog - 1} задание')
            is_on_dialog += 1
        elif is_on_dialog == 18:
            session_storage.update({str(is_on_dialog - 2): text})
            await send_message(user, f'Введите баллы за {is_on_dialog - 1} задание')
            is_on_dialog += 1
        elif is_on_dialog == 19:
            session_storage.update({str(is_on_dialog - 2): text})
            await send_message(user, f'Введите баллы за {is_on_dialog - 1} задание')
            is_on_dialog += 1
        elif is_on_dialog == 20:
            await send_message(user,
                               f'Данные введены верно?\n\n{reformat_dict(session_storage)}\n\nЕсли все правильно '
                               f'напишите: "да"')
            is_on_dialog += 1
        elif is_on_dialog == 21 and text.lower() == 'да':
            await push(message)


def reformat_dict(dct):
    res = ''
    for key, val in dct.items():
        res += f'{key} : {val} \n'
    return res.replace('name', 'ФИО').replace('grade', 'Класс')


async def send_message(user, message):
    await bot.send_message(user, message)
