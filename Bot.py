import logging
import json
import sqlite3
from datetime import datetime

import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


def TimeList(index):
    __URL = 'https://gu-ural.ru/wp-admin/admin-ajax.php'

    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    connect.commit()

    s = ''
    c = ''
    g = ''

    for speciality_num in cursor.execute(f"SELECT speciality_id FROM login_id WHERE id = {index}"):
        s += (str(speciality_num)[1])
    for course_num in cursor.execute(f"SELECT course_id FROM login_id WHERE id = {index}"):
        c += (str(course_num)[1])
    for group_num in cursor.execute(f"SELECT group_id FROM login_id WHERE id = {index}"):
        g += str(group_num)[1:4]

    col = {'form': '1',
           'speciality': s,
           'course': c,
           'group': g,
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
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
            id INTEGER,
            speciality_id STRING NOT NULL DEFAULT '4',
            course_id STRING NOT NULL DEFAULT '1',
            group_id STRING NOT NULL DEFAULT '792'
        )""")

    connect.commit()

    people_id = message.chat.id

    cursor.execute(f"SELECT id FROM login_id WHERE id = {people_id}")
    data = cursor.fetchone()

    if data is None:
        cursor.execute(f"INSERT INTO login_id VALUES({people_id}, 4, 1, 792);")
        connect.commit()

    if message.text == '1️⃣':
        cursor.execute(f"UPDATE login_id SET course_id = 1, group_id = 792 WHERE id = {people_id};")
        connect.commit()
        await message.answer(TimeList(people_id), reply_markup=button_restart)

    if message.text == '2️⃣':
        cursor.execute(f"UPDATE login_id SET course_id = 2, group_id = 793 WHERE id = {people_id};")
        connect.commit()
        await message.answer(TimeList(people_id), reply_markup=button_restart)

    if message.text == '3️⃣':
        cursor.execute(f"UPDATE login_id SET course_id = 3, group_id = 795 WHERE id = {people_id};")
        connect.commit()
        await message.answer(TimeList(people_id), reply_markup=button_restart)

    if message.text == '4️⃣':
        cursor.execute(f"UPDATE login_id SET course_id = 4, group_id = 794 WHERE id = {people_id};")
        connect.commit()
        await message.answer(TimeList(people_id), reply_markup=button_restart)

    if message.text == '5️⃣':
        cursor.execute(f"UPDATE login_id SET course_id = 5 WHERE id = {people_id};")
        connect.commit()
        await message.answer(TimeList(people_id), reply_markup=button_restart)

    if message.text == nup1.text:
    if message.text == nup2.text:
    if message.text == nup3.text:
    if message.text == nup4.text:
    if message.text == nup5.text:
    if message.text == nup6.text:
    if message.text == nup7.text:
    if message.text == nup8.text:
    if message.text == nup9.text:
    if message.text == nup10.text:
    if message.text == nup11.text:
    if message.text == nup12.text:
    if message.text == nup13.text:



    if message.text == 'Обновить':
        await message.answer(TimeList(people_id), reply_markup=button_restart)

    if message.text == 'Курс':
        await message.answer('Ваш курс', reply_markup=markup1)

    if message.text == 'Направление':
        await message.answer('Ваше направление', reply_markup=markup2)

    if message.text == '2 стр':
        await message.answer('.', reply_markup=markup3)
    if message.text == '3 стр':
        await message.answer('.', reply_markup=markup4)

    # await message.answer(TimeList(people_id), reply_markup=button_restart)


if __name__ == '__main__':
    executor.start_polling(dp)
