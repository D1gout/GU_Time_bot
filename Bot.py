import asyncio
import json
import logging
import sqlite3
import threading
from datetime import datetime

import pendulum
import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import TOKEN, MY_ID


def TimeList(index):
    __URL = 'https://gu-ural.ru/wp-admin/admin-ajax.php'

    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    connect.commit()

    group = ''
    error = ''

    for group_num in cursor.execute(
            f"SELECT group_id FROM login_id WHERE id = {index}"):
        group += str(group_num)[1:4]

    for group_error in cursor.execute(
            f"SELECT group_id FROM login_id WHERE id = {index}"):
        error += str(group_error)[1]

    text = ''

    if error == '0':
        text = "Пожалуйста пересоздайте аккаунт\n\n" \
               "P.S. скорее всего я что-то обновил)"
        return text

    col = {'form': '1',
           'group': group,
           'teacher': '',
           'action': 'lau_shedule_students_show'
           }
    req = requests.post(__URL, data=col).text

    list = json.loads(req)
    list_speed = list["current"]["data"]
    day = pendulum.today().format('DD.MM.YYYY')
    nextDay = pendulum.tomorrow().format('DD.MM.YYYY')
    weekday = str(datetime.today().isoweekday())
    for i in range(len(list_speed)):
        if list_speed[i]["discipline"] != "" or list_speed[i][
            "discipline"] is not None:
            if list_speed[i]["place"] != "" or list_speed[i][
                "place"] is not None:
                if list_speed[i]["date"] == day:
                    if list_speed[i]["notes"] != "":
                        if list_speed[i]["place"] is not None:
                            if list_speed[i]["classroom"] == "" or \
                                    list_speed[i]["classroom"] is None:
                                text += list_speed[i]["discipline"] + " (" + \
                                        list_speed[i]["notes"] + ")\n" \
                                        + list_speed[i]["place"] \
                                        + "\n" + list_speed[i]["time"] \
                                        + "\n\n"
                            else:
                                text += list_speed[i]["discipline"] + " (" + \
                                        list_speed[i]["notes"] + ")\n" \
                                        + list_speed[i]["place"] \
                                        + "\n" + "ауд. " + list_speed[i][
                                            "classroom"] \
                                        + "\n" + list_speed[i]["time"] \
                                        + "\n\n"
                        else:
                            if list_speed[i]["classroom"] == "" or \
                                    list_speed[i]["classroom"] is None:
                                text += list_speed[i]["discipline"] + " (" + \
                                        list_speed[i]["notes"] + ")\n" \
                                        + list_speed[i]["time"] \
                                        + "\n\n"
                            else:
                                text += list_speed[i]["discipline"] + " (" + \
                                        list_speed[i]["notes"] + ")\n" \
                                        + "ауд. " + list_speed[i]["classroom"] \
                                        + "\n" + list_speed[i]["time"] \
                                        + "\n\n"
                    else:
                        if list_speed[i]["place"] is not None:
                            if list_speed[i]["classroom"] == "" or \
                                    list_speed[i]["classroom"] is None:
                                text += list_speed[i]["discipline"] + "\n" + \
                                        list_speed[i]["place"] + "\n" \
                                        + list_speed[i]["time"] \
                                        + "\n\n"
                            else:
                                text += list_speed[i]["discipline"] + "\n" + \
                                        list_speed[i]["place"] + "\n" \
                                        + "ауд. " + list_speed[i]["classroom"] \
                                        + "\n" + list_speed[i]["time"] \
                                        + "\n\n"
                        else:
                            if list_speed[i]["classroom"] == "" or \
                                    list_speed[i]["classroom"] is None:
                                text += list_speed[i]["discipline"] + "\n" + \
                                        list_speed[i]["time"] + "\n\n"

                            else:
                                text += list_speed[i]["discipline"] + "\n" + \
                                        list_speed[i]["time"] + "\n" + "\n\n"

    text += "Завтра:\n\n"

    list_speed = list["next"]["data"]

    if weekday != "7":
        list_speed = list["current"]["data"]

    for i in range(len(list_speed)):
        if list_speed[i]["discipline"] != "" or list_speed[i][
            "discipline"] is not None:
            if list_speed[i]["place"] != "" or list_speed[i][
                "place"] is not None:
                if list_speed[i]["date"] == nextDay:
                    if list_speed[i]["notes"] != "":
                        if list_speed[i]["place"] is not None:
                            if list_speed[i]["classroom"] == "" or \
                                    list_speed[i]["classroom"] is None:
                                text += list_speed[i]["discipline"] + " (" + \
                                        list_speed[i]["notes"] + ")\n" \
                                        + list_speed[i]["place"] \
                                        + "\n" + list_speed[i]["time"] \
                                        + "\n\n"
                            else:
                                text += list_speed[i]["discipline"] + " (" + \
                                        list_speed[i]["notes"] + ")\n" \
                                        + list_speed[i]["place"] \
                                        + "\n" + "ауд. " + list_speed[i][
                                            "classroom"] \
                                        + "\n" + list_speed[i]["time"] \
                                        + "\n\n"
                        else:
                            if list_speed[i]["classroom"] == "" or \
                                    list_speed[i]["classroom"] is None:
                                text += list_speed[i]["discipline"] + " (" + \
                                        list_speed[i]["notes"] + ")\n" \
                                        + list_speed[i]["time"] \
                                        + "\n\n"
                            else:
                                text += list_speed[i]["discipline"] + " (" + \
                                        list_speed[i]["notes"] + ")\n" \
                                        + "ауд. " + list_speed[i]["classroom"] \
                                        + "\n" + list_speed[i]["time"] \
                                        + "\n\n"
                    else:
                        if list_speed[i]["place"] is not None:
                            if list_speed[i]["classroom"] == "" or \
                                    list_speed[i]["classroom"] is None:
                                text += list_speed[i]["discipline"] + "\n" + \
                                        list_speed[i]["place"] + "\n" \
                                        + list_speed[i]["time"] \
                                        + "\n\n"
                            else:
                                text += list_speed[i]["discipline"] + "\n" + \
                                        list_speed[i]["place"] + "\n" \
                                        + "ауд. " + list_speed[i]["classroom"] \
                                        + "\n" + list_speed[i]["time"] \
                                        + "\n\n"
                        else:
                            if list_speed[i]["classroom"] == "" or \
                                    list_speed[i]["classroom"] is None:
                                text += list_speed[i]["discipline"] + "\n" + \
                                        list_speed[i]["time"] + "\n\n"

                            else:
                                text += list_speed[i]["discipline"] + "\n" + \
                                        list_speed[i]["time"] + "\n" + "\n\n"

    return text


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

route = KeyboardButton('Направление')
button_route = ReplyKeyboardMarkup(resize_keyboard=True).add(route)

qurs = KeyboardButton('Курс')
button_qurs = ReplyKeyboardMarkup(resize_keyboard=True).add(qurs)

info = KeyboardButton('/info')
button_info = ReplyKeyboardMarkup(resize_keyboard=True).add(qurs)

start = KeyboardButton('/start')
button_start = ReplyKeyboardMarkup(resize_keyboard=True).add(start)

on = KeyboardButton('/on')
off = KeyboardButton('/off')

restart = KeyboardButton('Обновить')
button_restart = ReplyKeyboardMarkup(resize_keyboard=True).row(
    restart, on, off
)

help_comands = ReplyKeyboardMarkup(resize_keyboard=True).row(
    qurs, start, route, restart, info
)

button1 = KeyboardButton('1️⃣')
button2 = KeyboardButton('2️⃣')
button3 = KeyboardButton('3️⃣')
button4 = KeyboardButton('4️⃣')

nup1 = KeyboardButton('Юриспруденция')
nup2 = KeyboardButton('Экономика')
nup3 = KeyboardButton('Менеджмент')
nup4 = KeyboardButton('Прикладная информатика')
nup6 = KeyboardButton('Реклама и связи с общественностью')
nup7 = KeyboardButton('Сервис')
nup8 = KeyboardButton('Хореографическое искусство')
nup9 = KeyboardButton("Управление персоналом")
nup10 = KeyboardButton('Журналистика')
nup11 = KeyboardButton('Гостиничное дело')
nup12 = KeyboardButton('Психология')
nup13 = KeyboardButton('Туризм')

gr1 = KeyboardButton('ФиК 3')
gr2 = KeyboardButton('ЦЭ 3')
gr3 = KeyboardButton('ФиК 4')
gr4 = KeyboardButton('ЦЭ 4')

skip1 = KeyboardButton('2 стр')
skip2 = KeyboardButton('3 стр')
skip3 = KeyboardButton('4 стр')

markup1 = ReplyKeyboardMarkup(resize_keyboard=True,
                              one_time_keyboard=True).row(
    button1, button2, button3, button4
)
markup2 = ReplyKeyboardMarkup(one_time_keyboard=True).row(
    nup1, nup2, nup3, nup4, skip1
)
markup3 = ReplyKeyboardMarkup(one_time_keyboard=True).row(
    nup6, nup7, nup8, nup9, skip2
)
markup4 = ReplyKeyboardMarkup(one_time_keyboard=True).row(
    nup10, nup11, nup12, nup13
)
markup5 = ReplyKeyboardMarkup(one_time_keyboard=True).row(
    button1, button2, gr1, gr2, gr3, gr4
)


async def AutoTime():
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    connect.commit()

    auto = [x[0] for x in cursor.execute(
        f"SELECT id FROM login_id WHERE auto_time = {1}")]

    check = 1
    while auto:
        if datetime.now().strftime("%H:%M") == '09:00':
            check = 1

        i = 0
        await asyncio.sleep(20)
        if datetime.now().strftime("%H:%M") == '21:00' and check == 1:
            for _ in auto:
                await bot.send_message(auto[i], TimeList(auto[i]))
                check = 0
                i += 1


async def on_startup(_):
    asyncio.create_task(AutoTime())


@dp.message_handler(commands=['on'])
async def process_autotime_on(message: types.Message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    connect.commit()

    auto = ''
    for auto_num in cursor.execute(
            f"SELECT auto_time FROM login_id WHERE id = {message.chat.id}"):
        auto += str(auto_num)[1]

    if auto == '0':
        await message.answer('Включено авто-расписание в 21:00',
                             reply_markup=button_restart)
        cursor.execute(
            f"UPDATE login_id SET auto_time = 1 WHERE id = {message.chat.id};")
        connect.commit()

        auto = ''
        for auto_num in cursor.execute(
                f"SELECT auto_time FROM login_id WHERE id = {message.chat.id}"):
            auto += str(auto_num)[1]


@dp.message_handler(commands=['off'])
async def process_autotime_off(message: types.Message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    connect.commit()

    auto = ''
    for auto_num in cursor.execute(
            f"SELECT auto_time FROM login_id WHERE id = {message.chat.id}"):
        auto += str(auto_num)[1]

    if auto == '1':
        await message.answer('Выключено авто-расписание',
                             reply_markup=button_restart)
        cursor.execute(
            f"UPDATE login_id SET auto_time = 0 WHERE id = {message.chat.id};")
        connect.commit()


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.answer('Мои команды', reply_markup=help_comands)


@dp.message_handler(commands=['info'])
async def process_info_command(message: types.Message):
    await message.answer('Версия 1.2\n\nДобавил авто-расписание в 21:00',
                         reply_markup=button_restart)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer(
        "Привет, я бот который скидывает расписание\n\nby @Aweyout",
        reply_markup=button_route)


@dp.message_handler()
async def echo(message: types.Message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
            id INTEGER,
            speciality_id STRING NOT NULL DEFAULT '0',
            course_id STRING NOT NULL DEFAULT '0',
            group_id STRING NOT NULL DEFAULT '0',
            auto_time STRING NOT NULL DEFAULT '0'
        )""")

    connect.commit()

    people_id = message.chat.id
    cursor.execute(f"SELECT id FROM login_id WHERE id = {people_id}")
    data = cursor.fetchone()

    if data is None:
        cursor.execute(
            f"INSERT INTO login_id VALUES({people_id}, 0, 0, 0, 0);")
        connect.commit()

    speciality = ''
    for speciality_num in cursor.execute(
            f"SELECT speciality_id FROM login_id WHERE id = {people_id}"):
        if str(speciality_num)[2] != ',':
            speciality += (str(speciality_num)[1:3])
        else:
            speciality += (str(speciality_num)[1])

    connect.commit()

    if message.text == '1️⃣':
        # if speciality == '1':
        #     cursor.execute
        #     (f"UPDATE login_id SET group_id = 0 WHERE id = {people_id};")
        #     connect.commit()
        #     await message.answer
        #     (TimeList(people_id), reply_markup=button_restart)
        if speciality == '2':
            cursor.execute(
                f"UPDATE login_id SET group_id = 797 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '3':
            cursor.execute(
                f"UPDATE login_id SET group_id = 783 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '4':
            cursor.execute(
                f"UPDATE login_id SET group_id = 792 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '6':
            cursor.execute(
                f"UPDATE login_id SET group_id = 787 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '7':
            cursor.execute(
                f"UPDATE login_id SET group_id = 789 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '8':
            cursor.execute(
                f"UPDATE login_id SET group_id = 835 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '9':
            cursor.execute(
                f"UPDATE login_id SET group_id = 786 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '10':
            cursor.execute(
                f"UPDATE login_id SET group_id = 791 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '11':
            cursor.execute(
                f"UPDATE login_id SET group_id = 788 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '12':
            cursor.execute(
                f"UPDATE login_id SET group_id = 782 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '13':
            cursor.execute(
                f"UPDATE login_id SET group_id = 790 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)

    if message.text == '2️⃣':
        if speciality == '1':
            cursor.execute(
                f"UPDATE login_id SET group_id = 804 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '2':
            cursor.execute(
                f"UPDATE login_id SET group_id = 798 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        # if speciality == '3':
        #     cursor.execute
        #     (f"UPDATE login_id SET group_id = 0 WHERE id = {people_id};")
        #     connect.commit()
        #     await message.answer
        #     (TimeList(people_id), reply_markup=button_restart)
        if speciality == '4':
            cursor.execute(
                f"UPDATE login_id SET group_id = 793 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '6':
            cursor.execute(
                f"UPDATE login_id SET group_id = 820 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '7':
            cursor.execute(
                f"UPDATE login_id SET group_id = 822 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '8':
            cursor.execute(
                f"UPDATE login_id SET group_id = 836 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        # if speciality == '9':
        #     cursor.execute
        #     (f"UPDATE login_id SET group_id = 0 WHERE id = {people_id};")
        #     connect.commit()
        #     await message.answer
        #     (TimeList(people_id), reply_markup=button_restart)
        if speciality == '10':
            cursor.execute(
                f"UPDATE login_id SET group_id = 803 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '11':
            cursor.execute(
                f"UPDATE login_id SET group_id = 823 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        # if speciality == '12':
        #     cursor.execute
        #     (f"UPDATE login_id SET group_id = 782 WHERE id = {people_id};")
        #     connect.commit()
        #     await message.answer
        #     (TimeList(people_id), reply_markup=button_restart)
        if speciality == '13':
            cursor.execute(
                f"UPDATE login_id SET group_id = 824 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)

    if message.text == '3️⃣':
        if speciality == '1':
            cursor.execute(
                f"UPDATE login_id SET group_id = 806 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '3':
            cursor.execute(
                f"UPDATE login_id SET group_id = 801 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '4':
            cursor.execute(
                f"UPDATE login_id SET group_id = 795 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '6':
            cursor.execute(
                f"UPDATE login_id SET group_id = 821 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '7':
            cursor.execute(
                f"UPDATE login_id SET group_id = 825 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '8':
            cursor.execute(
                f"UPDATE login_id SET group_id = 837 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '9':
            cursor.execute(
                f"UPDATE login_id SET group_id = 819 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '10':
            cursor.execute(
                f"UPDATE login_id SET group_id = 805 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '11':
            cursor.execute(
                f"UPDATE login_id SET group_id = 827 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '12':
            cursor.execute(
                f"UPDATE login_id SET group_id = 810 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '13':
            cursor.execute(
                f"UPDATE login_id SET group_id = 826 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)

    if message.text == '4️⃣':
        if speciality == '1':
            cursor.execute(
                f"UPDATE login_id SET group_id = 808 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '3':
            cursor.execute(
                f"UPDATE login_id SET group_id = 814 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '4':
            cursor.execute(
                f"UPDATE login_id SET group_id = 794 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        # if speciality == '6':
        #     cursor.execute
        #     (f"UPDATE login_id SET group_id = 821 WHERE id = {people_id};")
        #     connect.commit()
        #     await message.answer
        #     (TimeList(people_id), reply_markup=button_restart)
        # if speciality == '7':
        #     cursor.
        #     (f"UPDATE login_id SET group_id = 825 WHERE id = {people_id};")
        #     connect.commit()
        #     await message.answer
        #     (TimeList(people_id), reply_markup=button_restart)
        if speciality == '8':
            cursor.execute(
                f"UPDATE login_id SET group_id = 838 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '9':
            cursor.execute(
                f"UPDATE login_id SET group_id = 818 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '10':
            cursor.execute(
                f"UPDATE login_id SET group_id = 807 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        # if speciality == '11':
        #     cursor.execute
        #     (f"UPDATE login_id SET group_id = 827 WHERE id = {people_id};")
        #     connect.commit()
        #     await message.answer
        #     (TimeList(people_id), reply_markup=button_restart)
        if speciality == '12':
            cursor.execute(
                f"UPDATE login_id SET group_id = 811 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        # if speciality == '13':
        #     cursor.execute
        #     (f"UPDATE login_id SET group_id = 826 WHERE id = {people_id};")
        #     connect.commit()
        #     await message.answer
        #     (TimeList(people_id), reply_markup=button_restart)

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

    if message.text == nup1.text:
        cursor.execute(
            f"UPDATE login_id SET speciality_id = 1 WHERE id = {people_id};")
        connect.commit()
        await message.answer('Ваш курс', reply_markup=markup1)
    if message.text == nup2.text:
        cursor.execute(
            f"UPDATE login_id SET speciality_id = 2 WHERE id = {people_id};")
        connect.commit()
        await message.answer('Ваш курс и группа', reply_markup=markup5)
    if message.text == nup3.text:
        cursor.execute(
            f"UPDATE login_id SET speciality_id = 3 WHERE id = {people_id};")
        connect.commit()
        await message.answer('Ваш курс', reply_markup=markup1)
    if message.text == nup4.text:
        cursor.execute(
            f"UPDATE login_id SET speciality_id = 4 WHERE id = {people_id};")
        connect.commit()
        await message.answer('Ваш курс', reply_markup=markup1)
    if message.text == nup6.text:
        cursor.execute(
            f"UPDATE login_id SET speciality_id = 6 WHERE id = {people_id};")
        connect.commit()
        await message.answer('Ваш курс', reply_markup=markup1)
    if message.text == nup7.text:
        cursor.execute(
            f"UPDATE login_id SET speciality_id = 7 WHERE id = {people_id};")
        connect.commit()
        await message.answer('Ваш курс', reply_markup=markup1)
    if message.text == nup8.text:
        cursor.execute(
            f"UPDATE login_id SET speciality_id = 8 WHERE id = {people_id};")
        connect.commit()
        await message.answer('Ваш курс', reply_markup=markup1)
    if message.text == nup9.text:
        cursor.execute(
            f"UPDATE login_id SET speciality_id = 9 WHERE id = {people_id};")
        connect.commit()
        await message.answer('Ваш курс', reply_markup=markup1)
    if message.text == nup10.text:
        cursor.execute(
            f"UPDATE login_id SET speciality_id = 10 WHERE id = {people_id};")
        connect.commit()
        await message.answer('Ваш курс', reply_markup=markup1)
    if message.text == nup11.text:
        cursor.execute(
            f"UPDATE login_id SET speciality_id = 11 WHERE id = {people_id};")
        connect.commit()
        await message.answer('Ваш курс', reply_markup=markup1)
    if message.text == nup12.text:
        cursor.execute(
            f"UPDATE login_id SET speciality_id = 12 WHERE id = {people_id};")
        connect.commit()
        await message.answer('Ваш курс', reply_markup=markup1)
    if message.text == nup13.text:
        cursor.execute(
            f"UPDATE login_id SET speciality_id = 13 WHERE id = {people_id};")
        connect.commit()
        await message.answer('Ваш курс', reply_markup=markup1)

    if message.text == gr1.text:
        cursor.execute(
            f"UPDATE login_id SET group_id = 802 WHERE id = {people_id};")
        connect.commit()
        await message.answer(TimeList(people_id),
                             reply_markup=button_restart)

    if message.text == gr2.text:
        cursor.execute(
            f"UPDATE login_id SET group_id = 799 WHERE id = {people_id};")
        connect.commit()
        await message.answer(TimeList(people_id),
                             reply_markup=button_restart)

    if message.text == gr3.text:
        cursor.execute(
            f"UPDATE login_id SET group_id = 817 WHERE id = {people_id};")
        connect.commit()
        await message.answer(TimeList(people_id),
                             reply_markup=button_restart)

    if message.text == gr4.text:
        cursor.execute(
            f"UPDATE login_id SET group_id = 816 WHERE id = {people_id};")
        connect.commit()
        await message.answer(TimeList(people_id),
                             reply_markup=button_restart)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
