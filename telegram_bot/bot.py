from aiogram import Bot, Dispatcher, types
import json
from data.config import logger
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from google_sheets.google_sheets_handlers import add_data_to_personal_table

TOKEN = "5738031171:AAEBv4hUujqqpRpApztI0ay29IsvQYt4JQM"

button0 = KeyboardButton('0')
button1 = KeyboardButton('1')
button2 = KeyboardButton('2')
button3 = KeyboardButton('3')
button4 = KeyboardButton('4')
button_accept = KeyboardButton('Да')
button_11a = KeyboardButton('11А')
button_11b = KeyboardButton('11Б')
students = {}
try:
    with open("telegram_bot/students.json") as f:
        students = json.load(f)
except:
    pass

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


class UserData:
    def __init__(self):
        self.name = ''
        self.grade = ''
        self.state = 0
        self.is_on_edit = 0
        self.editing_task = ''
        self.tasks = {}

    def clear_all(self):
        self.name = ''
        self.grade = ''
        self.state = 0
        self.is_on_edit = 0
        self.editing_task = ''
        self.tasks = {}

    def set_editing_task_number(self, val):
        self.editing_task = val

    def get_editing_task_number(self):
        return self.editing_task

    def set_task(self, val):
        self.tasks[self.editing_task] = val

    def set_name(self, name):
        self.name = name

    def set_grade(self, grade):
        self.grade = grade.upper()

    def update_task(self, key, val):
        self.tasks.update({key: val})

    def get_tasks(self):
        return self.tasks

    def set_state(self, val):
        self.state = val

    def get_state(self):
        return self.state

    def set_edit_state(self, val):
        self.is_on_edit = val

    def get_edit_state(self):
        return self.is_on_edit

    def get_dict(self):
        return {'name': self.name, "grade": self.grade, "parsed_data": self.tasks}

    def get_sheets_format(self):
        res = {}
        res.update({'name': self.name})
        res.update({"grade": self.grade})
        for key, value in self.tasks.items():
            res.update({key: value})
        return res


class Storage:
    def __init__(self):
        self.dct = {}

    def add_user(self, user):
        self.dct[user] = UserData()

    def get_user(self, user) -> UserData:
        return self.dct.get(user)

    def push(self):
        result = {}
        for user, data in self.dct.items():
            result.update({user: data.get_sheets_format})
        with open('telegram_bot/params.json', 'a') as f:
            f.write(json.dumps(result))


storage = Storage()


@dp.message_handler(commands=['skip'])
async def skip(message: types.Message):
    user = message.from_user.id
    data = storage.get_user(user)
    data.set_state(21)


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    user = message.from_user.id
    storage.add_user(user)
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
    user = message.from_user.id
    try:
        name = students[user]
        name_btn = KeyboardButton(name)
        markup = ReplyKeyboardMarkup(resize_keyboard=True).add(name_btn)
    except:
        markup = None
    if storage.get_user(user) is None:
        storage.add_user(user)
    await send_message(user, 'Давайте начнем!')
    await send_message(user, 'Введите ФИ', markup)
    data = storage.get_user(user)
    data.set_state(1)


@dp.message_handler(commands=['push', 'send', 'да'])
async def push(message: types.Message):
    user = message.from_user.id
    data = storage.get_user(user)
    current_state = data.get_state()
    if current_state >= 20:
        # storage.push()
        reply_markup = ReplyKeyboardRemove()
        # print(data.get_sheets_format())
        send_to_sheets(data.get_sheets_format())
        await bot.send_message(user, 'Ваши баллы были загружены. Хорошего дня!', reply_markup=reply_markup)
        data.set_state(0)
        data.clear_all()
    else:
        await send_message(user, 'Сначала заполните все поля варианта')


@dp.message_handler(commands=["check"])
async def check(message: types.Message):
    user = message.from_user.id
    data = storage.get_user(user)
    parsed_data = data.get_tasks()
    await send_message(message.from_user.id, reformat_dict(parsed_data))
    # print(reformat_dict(parsed_data))


@dp.message_handler(commands=["editvariant"])
async def edit_existing_variant(message: types.Message):
    user = message.from_user.id
    data = storage.get_user(user)
    parsed_data = data.get_tasks()
    if parsed_data != {}:
        await send_message(user, 'Введите номер задания, которое хотите исправить')
        data.set_edit_state(1)
    else:
        await send_message(user, 'Нет данных для правки, может запишем?\n\nВозможно, /addnewvariant вам поможет')


@dp.message_handler()
async def handle(message: types.Message):
    text = message.text
    user = message.from_user.id
    logger.info((user, message.from_user.first_name, text))
    data = storage.get_user(user)
    current_state = data.get_state()
    is_on_edit = data.get_edit_state()
    if is_on_edit == 1:
        data.set_editing_task_number(text)
        data.set_edit_state(2)
        await send_message(user, 'Введите правильное количество баллов')
    elif is_on_edit == 2:
        try:
            int(text)
            data.set_task(text)
            await send_message(user, 'Ваше задание исправлено(посмотреть текущие баллы можно функцией "/check")')
            if current_state < 20:
                await send_message(user, f'Введите баллы за {current_state - 2} задание')
            else:
                reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)
                reply_markup.add(button_accept)
                await bot.send_message(user, f'Если все правильно, напишите: "да"', reply_markup=reply_markup)
            data.set_edit_state(0)
        except TypeError:
            await send_message(user, f'Введите целое число из допустимого регистра')
    else:
        if current_state == 1:
            data.set_name(text)
            students.update({user: text})
            # print(students)
            with open("telegram_bot/students.json", 'w') as f:
                json.dump(students, f)
            # print('done')
            reply_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            reply_markup.add(button_11a)
            reply_markup.add(button_11b)
            await bot.send_message(user, f'Теперь введите свой класс(11А или 11Б)', reply_markup=reply_markup)
            data.set_state(data.get_state() + 1)
        elif current_state == 2:
            reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)
            reply_markup.add(button0, button1)
            data.set_grade(text)
            await bot.send_message(user, f'Введите баллы за {current_state - 1} задание', reply_markup=reply_markup)
            data.set_state(data.get_state() + 1)
        elif current_state in range(3, 20):
            reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)
            up = 10
            if current_state in range(3, 13):
                reply_markup.add(button0, button1)
                up = 1
            elif current_state in range(13, 16):
                reply_markup.add(button0, button1, button2)
                up = 2
            elif current_state in range(16, 18):
                reply_markup.add(button0, button1, button2, button3)
                up = 3
            else:
                reply_markup.add(button0, button1, button2, button3, button4)
                up = 4
            await ask_task(user, text, markup=reply_markup, up=up)
        elif current_state == 20:
            data.update_task(str(current_state - 2), text)
            reply_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            reply_markup.add(button_accept)
            await bot.send_message(user,
                                   f'Данные введены верно?\n\n{data.name}; Класс: {data.grade}\n'
                                   f'{reformat_dict(data.get_tasks())}\n'
                                   f'\nЕсли все правильно, '
                                   f'напишите: "да"', reply_markup=reply_markup)
            data.set_state(data.get_state() + 1)
        elif current_state == 21 and text.lower() == 'да':
            await send_message(user, "Таблица заполняется, минуточку...")
            await push(message)


def send_to_sheets(dct):
    add_data_to_personal_table(dct)


async def ask_task(user, text, markup, up):
    data = storage.get_user(user)
    current_state = data.get_state()
    try:
        int(text)
        if 0 <= int(text) <= up:
            data.update_task(str(current_state - 2), str(text))
            await send_message(user, f'Введите баллы за {current_state - 1} задание', markup=markup)
            data.set_state(data.get_state() + 1)
        else:
            await send_message(user, f'Введите целое число из допустимого регистра', markup=markup)
    except TypeError:
        await send_message(user, f'Введите целое число из допустимого регистра', markup=markup)


def reformat_dict(dct):
    res = ''
    for key, val in dct.items():
        res += f'{key} : {val} \n'
    return res.replace('name', 'ФИО').replace('grade', 'Класс')


async def send_message(user, message, markup=None):
    if markup:
        await bot.send_message(user, message, reply_markup=markup)
    else:
        await bot.send_message(user, message)
