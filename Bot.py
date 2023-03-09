import asyncio
import json
import logging
import sqlite3
from datetime import datetime

import pendulum
import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import BotBlocked
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardButton, InlineKeyboardMarkup

from config import TOKEN
from weekday import WEEKDAYS


def TimeList(index):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    connect.commit()

    if asyncio.sleep(3600):
        TimeListUpdate(index)

    text = cursor.execute(
        "SELECT list_text FROM login_id WHERE id = {}"
        .format(index)).fetchone()

    return text[0]


def TimeListUpdate(index):
    __URL = 'https://gu-ural.ru/wp-admin/admin-ajax.php'

    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    connect.commit()

    group = ''
    error = ''

    for group_num in cursor.execute(
            "SELECT group_id FROM login_id WHERE id = {}".format(index)):
        group += str(group_num)[1:4]

    for group_error in cursor.execute(
            "SELECT group_id FROM login_id WHERE id = {}".format(index)):
        error += str(group_error)[1]

    text = WEEKDAYS[datetime.today().weekday()]

    if error == '0':
        text = "Пожалуйста пересоздайте аккаунт\n\n" \
               "P.S. скорее всего я что-то обновил и ваш аккаунт потерялся("
        return text

    col = {'form': '1',
           'group': group,
           'teacher': '',
           'action': 'lau_shedule_students_show'
           }
    req = requests.post(__URL, data=col).text
    try:
        list = json.loads(req)
    except json.decoder.JSONDecodeError:
        text = 'Ошибка получения расписания'
        return text
    text_old = text
    list_speed = list["current"]["data"]
    day = pendulum.today().format('DD.MM.YYYY')
    nextDay = pendulum.tomorrow().format('DD.MM.YYYY')
    weekday = str(datetime.today().isoweekday())
    for i in range(len(list_speed)):
        if list_speed[i]["discipline"] != "" or \
                list_speed[i]["discipline"] is not None:
            if list_speed[i]["place"] != "" or \
                    list_speed[i]["place"] is not None:
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
                                        + "ауд. " \
                                        + list_speed[i]["classroom"] \
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
                                        + "ауд. " \
                                        + list_speed[i]["classroom"] \
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

    text_new = text

    if text_old == text_new:
        text = WEEKDAYS[datetime.today().weekday()]
        text += "Расписание отсутствует\n\n"

    text += "Завтра:\n\n"

    text_old = text

    if weekday == "7":
        list_speed = list["next"]["data"]

    for i in range(len(list_speed)):
        if list_speed[i]["discipline"] != "" or \
                list_speed[i]["discipline"] is not None:
            if list_speed[i]["place"] != "" or \
                    list_speed[i]["place"] is not None:
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
                                        + "ауд. " + \
                                        list_speed[i]["classroom"] + \
                                        "\n" + list_speed[i]["time"] \
                                        + "\n\n"
                    else:
                        if list_speed[i]["place"] is not None:
                            if list_speed[i]["classroom"] == "" or \
                                    list_speed[i]["classroom"] is None:
                                text += list_speed[i]["discipline"] + \
                                        "\n" + list_speed[i]["place"] + \
                                        "\n" \
                                        + list_speed[i]["time"] \
                                        + "\n\n"
                            else:
                                text += list_speed[i]["discipline"] + "\n" + \
                                        list_speed[i]["place"] + "\n" \
                                        + "ауд. " + \
                                        list_speed[i]["classroom"] + \
                                        "\n" + list_speed[i]["time"] \
                                        + "\n\n"
                        else:
                            if list_speed[i]["classroom"] == "" or \
                                    list_speed[i]["classroom"] is None:
                                text += list_speed[i]["discipline"] + "\n" + \
                                        list_speed[i]["time"] + "\n\n"

                            else:
                                text += list_speed[i]["discipline"] + "\n" + \
                                        list_speed[i]["time"] + "\n" + "\n\n"

    text_new = text
    if text_old == text_new and text_new != "Расписание отсутствует\n\n" \
                                            "Завтра:\n\n":
        text += "Расписание отсутствует"

    if text_new == "Расписание отсутствует\n\nЗавтра:\n\n":
        text = "Расписание отсутствует"

    data = (text, index)

    cursor.execute(
        "UPDATE login_id SET list_text = ? WHERE id = ?", data)
    connect.commit()

    return text


async def FullList(index):
    __URL = 'https://gu-ural.ru/wp-admin/admin-ajax.php'

    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    connect.commit()

    group = ''
    error = ''

    weekday = str(datetime.today().isoweekday())

    for group_num in cursor.execute(
            "SELECT group_id FROM login_id WHERE id = {}".format(index)):
        group += str(group_num)[1:4]

    for group_error in cursor.execute(
            "SELECT group_id FROM login_id WHERE id = {}".format(index)):
        error += str(group_error)[1]

    col = {'form': '1',
           'group': group,
           'teacher': '',
           'action': 'lau_shedule_students_show'
           }
    req = requests.post(__URL, data=col).text
    try:
        list = json.loads(req)
    except json.decoder.JSONDecodeError:
        text = 'Ошибка получения расписания'
        return text
    await bot.send_message(index, 'Расписание на неделю')

    check = 0

    list_speed = list["current"]["data"]

    if weekday == "7":
        list_speed = list["next"]["data"]

    for j in range(1, 8):
        text = WEEKDAYS[j - 1]

        text_old = text
        for i in range(len(list_speed)):
            if list_speed[i]["discipline"] != "" or \
                    list_speed[i]["discipline"] is not None:
                if list_speed[i]["place"] != "" or \
                        list_speed[i]["place"] is not None:
                    if list_speed[i]["weekday"] == str(j):
                        if list_speed[i]["notes"] != "":
                            if list_speed[i]["place"] is not None:
                                if list_speed[i]["classroom"] == "" or \
                                        list_speed[i]["classroom"] is None:
                                    text += list_speed[i]["discipline"] \
                                            + " (" + list_speed[i]["notes"] \
                                            + ")\n" \
                                            + list_speed[i]["place"] \
                                            + "\n" + list_speed[i]["time"] \
                                            + "\n\n"
                                else:
                                    text += list_speed[i]["discipline"] \
                                            + " (" + list_speed[i]["notes"] \
                                            + ")\n" \
                                            + list_speed[i]["place"] \
                                            + "\n" + "ауд. " + list_speed[i][
                                                "classroom"] \
                                            + "\n" + list_speed[i]["time"] \
                                            + "\n\n"
                            else:
                                if list_speed[i]["classroom"] == "" or \
                                        list_speed[i]["classroom"] is None:
                                    text += list_speed[i]["discipline"] \
                                            + " (" \
                                            + list_speed[i]["notes"] + ")\n" \
                                            + list_speed[i]["time"] \
                                            + "\n\n"
                                else:
                                    text += list_speed[i]["discipline"] \
                                            + " (" + list_speed[i]["notes"] \
                                            + ")\n" \
                                            + "ауд. " \
                                            + list_speed[i]["classroom"] \
                                            + "\n" + list_speed[i]["time"] \
                                            + "\n\n"
                        else:
                            if list_speed[i]["place"] is not None:
                                if list_speed[i]["classroom"] == "" or \
                                        list_speed[i]["classroom"] is None:
                                    text += list_speed[i]["discipline"] \
                                            + "\n" + list_speed[i]["place"] \
                                            + "\n" \
                                            + list_speed[i]["time"] \
                                            + "\n\n"
                                else:
                                    text += list_speed[i][
                                                "discipline"] + "\n" + \
                                            list_speed[i]["place"] + "\n" \
                                            + "ауд. " \
                                            + list_speed[i]["classroom"] \
                                            + "\n" + list_speed[i]["time"] \
                                            + "\n\n"
                            else:
                                if list_speed[i]["classroom"] == "" or \
                                        list_speed[i]["classroom"] is None:
                                    text += list_speed[i]["discipline"] + \
                                            "\n" + list_speed[i]["time"] + \
                                            "\n\n"

                                else:
                                    text += list_speed[i]["discipline"] + \
                                            "\n" + list_speed[i]["time"] + \
                                            "\n" + "\n\n"

        text_new = text
        if text_old == text_new and text_new != "Расписание отсутствует\n\n" \
                                                "Завтра:\n\n":
            if check == 0 and j == 7:
                await bot.send_message(index, 'Расписание отсутствует')
                check += 1
        else:
            await bot.send_message(index, text)
            check += 1


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
button_start = ReplyKeyboardMarkup(resize_keyboard=True,
                                   one_time_keyboard=True).add(start)

on = KeyboardButton('/on')
off = KeyboardButton('/off')

restart = KeyboardButton('Обновить')
button_restart = ReplyKeyboardMarkup(resize_keyboard=True).row(
    restart, on, off
)

help_comands = ReplyKeyboardMarkup(resize_keyboard=True).row(
    qurs, start, route, restart, info
)

typ1 = InlineKeyboardButton('Бакалавриат', callback_data='typ1_click')
typ2 = InlineKeyboardButton('Магистратура', callback_data='typ2_click')

link_button = InlineKeyboardMarkup().add(InlineKeyboardButton(
    'Написать мне',
    url='https://t.me/Aweyout'))

typ_buttons = InlineKeyboardMarkup().row(
    typ1, typ2
)

button1 = KeyboardButton('1️⃣')
button2 = KeyboardButton('2️⃣')
button3 = KeyboardButton('3️⃣')
button4 = KeyboardButton('4️⃣')

nup1 = KeyboardButton('Юриспруденция')
nup1_2 = KeyboardButton('Юриспруденция\n(М)')  # (Магистратура)
nup2 = KeyboardButton('Экономика')
nup2_2 = KeyboardButton('Экономика\n(М)')  # (Магистратура)
nup3 = KeyboardButton('Менеджмент')
nup4 = KeyboardButton('Прикладная информатика')
nup6 = KeyboardButton('Реклама и связи с общественностью')
nup7 = KeyboardButton('Сервис')
nup8 = KeyboardButton('Хореографическое искусство')
nup9 = KeyboardButton("Управление персоналом")
nup10 = KeyboardButton('Журналистика')
nup11 = KeyboardButton('Гостиничное дело')
nup12 = KeyboardButton('Психология')
nup12_2 = KeyboardButton('Психология\n(М)')  # (Магистратура)
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
markup2 = ReplyKeyboardMarkup(resize_keyboard=True,
                              one_time_keyboard=True).row(
    nup1, nup2, nup3, nup4, skip1
)
markup3 = ReplyKeyboardMarkup(resize_keyboard=True,
                              one_time_keyboard=True).row(
    nup6, nup7, nup8, nup9, skip2
)
markup4 = ReplyKeyboardMarkup(resize_keyboard=True,
                              one_time_keyboard=True).row(
    nup10, nup11, nup12, nup13
)
markup5 = ReplyKeyboardMarkup(resize_keyboard=True,
                              one_time_keyboard=True).row(
    button1, button2, gr1, gr2, gr3, gr4
)
markup6 = ReplyKeyboardMarkup(resize_keyboard=True,
                              one_time_keyboard=True).row(
    nup1_2, nup2_2, nup12_2
)


async def AutoTime():       # Авто расписание
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
            id INTEGER,
            speciality_id STRING NOT NULL DEFAULT '0',
            course_id STRING NOT NULL DEFAULT '0',
            group_id STRING NOT NULL DEFAULT '0',
            auto_time STRING NOT NULL DEFAULT '0',
            list_text TEXT NOT NULL DEFAULT 'None'
        )""")

    connect.commit()

    auto = [x[0] for x in cursor.execute(
        "SELECT id FROM login_id WHERE auto_time = {}".format(1))]

    while not auto:
        await asyncio.sleep(10)

        auto = [x[0] for x in cursor.execute(
            "SELECT id FROM login_id WHERE auto_time = {}".format(1))]

    check = 1
    while auto:
        auto = [x[0] for x in cursor.execute(
            "SELECT id FROM login_id WHERE auto_time = {}".format(1))]

        if datetime.now().strftime("%H:%M") == '20:55':
            check = 1

        i = 0
        await asyncio.sleep(20)
        if datetime.now().strftime("%H:%M") == '21:00' and check == 1:
            for _ in auto:
                try:
                    await bot.send_message(auto[i], TimeList(auto[i]))
                except BotBlocked:
                    await asyncio.sleep(0.1)

                check = 0
                i += 1


async def ListUpdate():     # Авто обновление расписания
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
            id INTEGER,
            speciality_id STRING NOT NULL DEFAULT '0',
            course_id STRING NOT NULL DEFAULT '0',
            group_id STRING NOT NULL DEFAULT '0',
            auto_time STRING NOT NULL DEFAULT '0',
            list_text TEXT NOT NULL DEFAULT 'None'
        )""")

    connect.commit()

    index_count = [x[0] for x in cursor.execute(
        "SELECT id FROM login_id WHERE group_id != {}".format(0))]

    while not index_count:
        await asyncio.sleep(10)

        index_count = [x[0] for x in cursor.execute(
            "SELECT id FROM login_id WHERE group_id != {}".format(0))]

    while index_count:
        index_count = cursor.execute(
            "SELECT id FROM login_id WHERE group_id != {}"
            .format(0)).fetchall()

        for index in index_count:
            old_text = [x[0] for x in cursor.execute(
                "SELECT list_text FROM login_id WHERE id = {}"
                .format(index[0]))]

            TimeList(index[0])

            now_text = [x[0] for x in cursor.execute(
                "SELECT list_text FROM login_id WHERE id = {}".
                format(index[0]))]

            if now_text[0] != old_text[0]:
                try:
                    await bot.send_message(index[0], now_text[0])
                except BotBlocked:
                    await asyncio.sleep(0.1)

            await asyncio.sleep(0.1)

        await asyncio.sleep(240)


async def on_startup(_):
    asyncio.create_task(AutoTime())
    asyncio.create_task(ListUpdate())


@dp.callback_query_handler(lambda c: c.data == 'typ1_click')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    try:
        await bot.send_message(callback_query.from_user.id, 'Ваше направление',
                               reply_markup=markup2)
    except BotBlocked:
        await asyncio.sleep(0.1)


@dp.callback_query_handler(lambda c: c.data == 'typ2_click')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    try:
        await bot.send_message(callback_query.from_user.id, 'Ваше направление',
                               reply_markup=markup6)
    except BotBlocked:
        await asyncio.sleep(0.1)


@dp.message_handler(commands=['on'])
async def process_autotime_on(message: types.Message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    connect.commit()

    auto = ''
    for auto_num in cursor.execute(
            "SELECT auto_time FROM login_id WHERE id = {}"
                    .format(message.chat.id)):
        auto += str(auto_num)[1]

    if auto == '0':
        await message.answer('Включено авто-расписание в 21:00',
                             reply_markup=button_restart)
        cursor.execute(
            "UPDATE login_id SET auto_time = 1 WHERE id = {};"
            .format(message.chat.id))
        connect.commit()

        auto = ''
        for auto_num in cursor.execute(
                "SELECT auto_time FROM login_id "
                "WHERE id = {}".format(message.chat.id)):
            auto += str(auto_num)[1]


@dp.message_handler(commands=['off'])
async def process_autotime_off(message: types.Message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    connect.commit()

    auto = ''
    for auto_num in cursor.execute(
            "SELECT auto_time FROM login_id WHERE id = {}"
                    .format(message.chat.id)):
        auto += str(auto_num)[1]

    if auto == '1':
        await message.answer('Выключено авто-расписание',
                             reply_markup=button_restart)
        cursor.execute(
            "UPDATE login_id SET auto_time = 0 WHERE id = {};"
            .format(message.chat.id))
        connect.commit()


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.answer('Мои команды', reply_markup=help_comands)


@dp.message_handler(commands=['info'])
async def process_info_command(message: types.Message):
    await message.answer('Версия 1.9.0\n\n'
                         'Новые кнопки, скоро глобальное обновление',
                         reply_markup=button_restart)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer(
        "Привет!",
        reply_markup=link_button)
    await message.answer(
        "Я бот который скидывает расписание\n\nВыбери уровень обучения",
        reply_markup=typ_buttons)


@dp.message_handler(commands=['full'])
async def process_info_command(message: types.Message):
    await FullList(message.chat.id)


@dp.message_handler()
async def echo(message: types.Message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
            id INTEGER,
            speciality_id STRING NOT NULL DEFAULT '0',
            course_id STRING NOT NULL DEFAULT '0',
            group_id STRING NOT NULL DEFAULT '0',
            auto_time STRING NOT NULL DEFAULT '0',
            list_text TEXT NOT NULL DEFAULT 'None'
        )""")

    connect.commit()

    people_id = message.chat.id
    cursor.execute("SELECT id FROM login_id WHERE id = {}"
                   .format(people_id))
    data = cursor.fetchone()

    if data is None:
        cursor.execute(
            "INSERT INTO login_id VALUES({}, 0, 0, 0, 0, 'None');"
            .format(people_id))
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
        #     (f"UPDATE login_id SET group_id = 0 WHERE id = {};"
        #     .format(people_id))
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
        if speciality == '14':
            cursor.execute(
                f"UPDATE login_id SET group_id = 796 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '15':
            cursor.execute(
                f"UPDATE login_id SET group_id = 815 WHERE id = {people_id};")
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
        #     (f"UPDATE login_id SET group_id = 0 WHERE id = {};"
        #     .format(people_id))
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
        #     (f"UPDATE login_id SET group_id = 0 WHERE id = {};"
        #     .format(people_id))
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
        #     (f"UPDATE login_id SET group_id = 782 WHERE id = {};"
        #     .format(people_id))
        #     connect.commit()
        #     await message.answer
        #     (TimeList(people_id), reply_markup=button_restart)
        if speciality == '13':
            cursor.execute(
                f"UPDATE login_id SET group_id = 824 WHERE id = {people_id};")
            connect.commit()
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '15':
            cursor.execute(
                f"UPDATE login_id SET group_id = 842 WHERE id = {people_id};")
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
        #     (f"UPDATE login_id SET group_id = 821 WHERE id = {};"
        #     .format(people_id))
        #     connect.commit()
        #     await message.answer
        #     (TimeList(people_id), reply_markup=button_restart)
        # if speciality == '7':
        #     cursor.
        #     (f"UPDATE login_id SET group_id = 825 WHERE id = {};"
        #     .format(people_id))
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
        #     (f"UPDATE login_id SET group_id = 827 WHERE id = {};"
        #     .format(people_id))
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
        #     (f"UPDATE login_id SET group_id = 826 WHERE id = {};"
        #     .format(people_id))
        #     connect.commit()
        #     await message.answer
        #     (TimeList(people_id), reply_markup=button_restart)

    if message.text == 'Обновить':
        if TimeList(people_id) == "Пожалуйста пересоздайте аккаунт\n\n" \
                                  "P.S. скорее всего я что-то " \
                                  "обновил и ваш аккаунт потерялся(":
            await message.answer(TimeList(people_id),
                                 reply_markup=button_start)
        else:
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)

    if message.text == 'Курс':
        await message.answer('Ваш курс', reply_markup=markup1)

    if message.text == '2 стр':
        await message.answer('2 стр', reply_markup=markup3)
    if message.text == '3 стр':
        await message.answer('3 стр', reply_markup=markup4)

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
    if message.text == nup1_2.text:
        cursor.execute(
            f"UPDATE login_id SET speciality_id = 14 WHERE id = {people_id};")
        connect.commit()
        await message.answer('Ваш курс', reply_markup=markup1)
    if message.text == nup2_2.text:
        cursor.execute(
            f"UPDATE login_id SET speciality_id = 15 WHERE id = {people_id};")
        connect.commit()
        await message.answer('Ваш курс', reply_markup=markup1)
    if message.text == nup12_2.text:
        cursor.execute(
            f"UPDATE login_id SET speciality_id = 16 WHERE id = {people_id};")
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
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
