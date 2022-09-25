from aiogram import Bot, Dispatcher, types
import json
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

TOKEN = "5738031171:AAEBv4hUujqqpRpApztI0ay29IsvQYt4JQM"

# session_storage = {}
# parsed_data = {}
# current_state = 0
# is_on_edit = 0
# editing_task = ''

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

    def set_task(self, val):
        self.tasks[self.editing_task] = val

    def set_name(self, name):
        self.name = name

    def set_grade(self, grade):
        self.grade = grade

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
            result.update({user: data.create_dict()})
        with open('telegram_bot/params.json', 'a') as f:
            f.write(json.dumps(result))


storage = Storage()


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
    await send_message(user, 'Давайте начнем!')
    await send_message(user, 'Введите ФИО')
    data = storage.get_user(user)
    data.set_state(1)


@dp.message_handler(commands=['push', 'send', 'отправить', 'пуш', 'закончил', 'да'])
async def push(message: types.Message):
    user = message.from_user.id
    data = storage.get_user(user)
    current_state = data.get_state()
    parsed_data = data.get_dict()
    if current_state >= 20:
        print(parsed_data)
        send_to_sheets(data.get_dict())
        await send_message(user, 'Ваши баллы были загружены. Хорошего дня!')
        data.set_state(0)
        data.clear_all()
    else:
        await send_message(user, 'Сначала заполните все поля варианта')


@dp.message_handler(commands=["check", 'баллы', 'чекнуть'])
async def check(message: types.Message):
    user = message.from_user.id
    data = storage.get_user(user)
    parsed_data = data.get_tasks()
    await send_message(message.from_user.id, reformat_dict(parsed_data))
    print(reformat_dict(parsed_data))


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
    print(user, message.from_user.first_name, text)
    print()
    data = storage.get_user(user)
    current_state = data.get_state()
    is_on_edit = data.get_edit_state()
    if is_on_edit == 1:
        data.set_editing_task_number(text)
        data.set_edit_state(2)
        await send_message(user, 'Введите правильное количество баллов')
    elif is_on_edit == 2:
        data.set_task(text)
        await send_message(user, 'Ваше задание исправлено(посмотреть текущие баллы можно функцией "/check")')
        if current_state < 20:
            await send_message(user, f'Введите баллы за {current_state - 2} задание')
        else:
            await send_message(user, f'Если все правильно, напишите: "да"')
        data.set_edit_state(0)
    else:
        if current_state == 1:
            data.set_name(text)
            await send_message(user, f'Теперь введите свой класс(11А или 11Б)')
            data.set_state(data.get_state() + 1)
        elif current_state == 2:
            data.set_grade(text)
            await send_message(user, f'Введите баллы за {current_state - 1} задание')
            data.set_state(data.get_state() + 1)
        elif current_state == 3:
            await ask_task(user, text)
        elif current_state == 4:
            await ask_task(user, text)
        elif current_state == 5:
            await ask_task(user, text)
        elif current_state == 6:
            await ask_task(user, text)
        elif current_state == 7:
            await ask_task(user, text)
        elif current_state == 8:
            await ask_task(user, text)
        elif current_state == 9:
            await ask_task(user, text)
        elif current_state == 10:
            await ask_task(user, text)
        elif current_state == 11:
            await ask_task(user, text)
        elif current_state == 12:
            await ask_task(user, text)
        elif current_state == 13:
            await ask_task(user, text)
        elif current_state == 14:
            await ask_task(user, text)
        elif current_state == 15:
            await ask_task(user, text)
        elif current_state == 16:
            await ask_task(user, text)
        elif current_state == 17:
            await ask_task(user, text)
        elif current_state == 18:
            await ask_task(user, text)
        elif current_state == 19:
            await ask_task(user, text)
        elif current_state == 20:
            data.update_task(str(current_state - 2), text)
            await send_message(user,
                               f'Данные введены верно?\n\n{data.name}\n{data.grade}\n{reformat_dict(data.get_tasks())}\n'
                               f'\nЕсли все правильно, '
                               f'напишите: "да"')
            data.set_state(data.get_state() + 1)
        elif current_state == 21 and text.lower() == 'да':
            await push(message)


def send_to_sheets(dct):
    pass


async def ask_task(user, text):
    data = storage.get_user(user)
    current_state = data.get_state()
    data.update_task(str(current_state - 2), text)
    await send_message(user, f'Введите баллы за {current_state - 1} задание')
    data.set_state(data.get_state() + 1)


def reformat_dict(dct):
    res = ''
    for key, val in dct.items():
        res += f'{key} : {val} \n'
    return res.replace('name', 'ФИО').replace('grade', 'Класс')


async def send_message(user, message):
    await bot.send_message(user, message)
