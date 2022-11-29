import logging
import json
from datetime import datetime

import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

k_time = 0


def TimeList(speciality_num, course_num, group_num):
    __URL = 'https://gu-ural.ru/wp-admin/admin-ajax.php'

    col = {'form': '1',
           'speciality': speciality_num,
           'course': course_num,
           'group': group_num,
           'teacher': '',
           'action': 'lau_shedule_students_show'
           }
    req = requests.post(__URL, data=col).text
    list = json.loads(req)
    list_speed = list["current"]["data"]
    text = ''
    day = datetime.today().isoweekday()
    for i in range(len(list_speed)):
        if list_speed[i]["weekday"] == str(day):
            if list_speed[i]["notes"] != "":
                if list_speed[i]["place"] is not None:
                    text += list_speed[i]["discipline"] + " (" + list_speed[i]["notes"] + ")\n" \
                            + list_speed[i]["place"] \
                            + "\n" + list_speed[i]["time"] + "\n\n"
                else:
                    text += list_speed[i]["discipline"] + " (" + list_speed[i]["notes"] + ")\n" + list_speed[i]["time"] \
                            + "\n\n"
            else:
                if list_speed[i]["place"] is not None:
                    text += list_speed[i]["discipline"] + "\n" + list_speed[i]["place"] + "\n" + list_speed[i]["time"] \
                            + "\n\n"
                else:
                    text += list_speed[i]["discipline"] + list_speed[i]["time"] + "\n\n"

    return text


# Токен, ID создателя, Имя базы данных
TOKEN = '5975391066:AAEHxpuSeVYz4fidfGbV61zuKN4zOrxGvDY'
MY_ID = '706967790'
DB_FILENAME = 'db_bot'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

route = KeyboardButton('Направление')
button_route = ReplyKeyboardMarkup(resize_keyboard=True).add(route)

qurs = KeyboardButton('Курс')
button_qurs = ReplyKeyboardMarkup(resize_keyboard=True).add(qurs)

start = KeyboardButton('/start')
button_start = ReplyKeyboardMarkup(resize_keyboard=True).add(start)

restart = KeyboardButton('Обновить')
button_restart = ReplyKeyboardMarkup(resize_keyboard=True).add(restart)

help_comands = ReplyKeyboardMarkup(resize_keyboard=True).row(
    qurs, start, route, restart
)

button1 = KeyboardButton('1️⃣')
button2 = KeyboardButton('2️⃣')
button3 = KeyboardButton('3️⃣')
button4 = KeyboardButton('4️⃣')
button5 = KeyboardButton('5️⃣')

nup1 = KeyboardButton('Юриспруденция')
nup2 = KeyboardButton('Экономика')
nup3 = KeyboardButton('Менеджмент')
nup4 = KeyboardButton('Прикладная информатика')
nup5 = KeyboardButton('Конструирование изделий легкой промышленности')
nup6 = KeyboardButton('Реклама и связи с общественностью')
nup7 = KeyboardButton('Сервис')
nup8 = KeyboardButton('Хореографическое искусство')
nup9 = KeyboardButton('Управление персоналом')
nup10 = KeyboardButton('Журналистика')
nup11 = KeyboardButton('Гостиничное дело')
nup12 = KeyboardButton('Психология')
nup13 = KeyboardButton('Туризм')

skip1 = KeyboardButton('2 стр')
skip2 = KeyboardButton('3 стр')
skip3 = KeyboardButton('4 стр')

markup1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(
    button1, button2, button3, button4, button5
)
markup2 = ReplyKeyboardMarkup(one_time_keyboard=True).row(
    nup1, nup2, nup3, nup4, skip1
)
markup3 = ReplyKeyboardMarkup(one_time_keyboard=True).row(
    nup5, nup6, nup7, nup8, skip2
)
markup4 = ReplyKeyboardMarkup(one_time_keyboard=True).row(
    nup9, nup10, nup11, nup12, nup13
)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.answer('Мои команды', reply_markup=help_comands)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer("Привет, я бот который скидывает расписание\n\nby Ащев Даниил", reply_markup=button_route)


@dp.message_handler()
async def echo(message: types.Message):
    if message.text == '1️⃣':
        await message.answer(TimeList(4, 1, 792), reply_markup=button_restart)

    if message.text == '2️⃣':
        await message.answer(TimeList(4, 2, 793), reply_markup=button_restart)

    if message.text == '3️⃣':
        await message.answer(TimeList(4, 3, 795), reply_markup=button_restart)

    if message.text == '4️⃣':
        await message.answer(TimeList(4, 4, 794), reply_markup=button_restart)

    if message.text == '5️⃣':
        await message.answer(TimeList(4, 5, 0), reply_markup=button_restart)

    if message.text == 'Обновить':
        await message.answer(TimeList(4, 1, 792), reply_markup=button_restart)

    if message.text == 'Курс':
        await message.answer('Ваш курс', reply_markup=markup1)

    if message.text == 'Направление':
        await message.answer('Ваше направление', reply_markup=markup2)

    if message.text == '2 стр':
        await message.answer('.', reply_markup=markup3)
    if message.text == '3 стр':
        await message.answer('.', reply_markup=markup4)


if __name__ == '__main__':
    executor.start_polling(dp)
