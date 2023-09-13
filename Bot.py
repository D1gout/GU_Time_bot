import asyncio
import json
import logging
import re
import sqlite3
import configparser
from datetime import datetime
from decouple import config

import pendulum
import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import BotBlocked
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardButton, InlineKeyboardMarkup

from utils.bd import create_bd, update_bd, select_bd

from utils.weekday import WEEKDAYS
from utils.auto_task import AutoTask

path = "utils/settings.ini"
configs = configparser.ConfigParser()
configs.read(path)

TOKEN = configs.get("Settings", "token")
SLEEP = configs.get("Settings", "sleep_mode")
STOP = configs.get("Settings", "stop")
if TOKEN == "YOUR_TOKEN_HERE":
    TOKEN = config('BOT_TOKEN')
    SLEEP = config('sleep_mode')
    STOP = config('stop')


def TimeList(index):
    error = select_bd('list_text', 'login_id', 'id', index, 1)[0]

    text = select_bd('list_text', 'login_id', 'id', index, 1)

    if error == '0':
        text = "Пожалуйста пересоздайте аккаунт\n\n" \
               "P.S. скорее всего я что-то обновил и ваш аккаунт потерялся("
        return text
    elif text[0] == "None":
        text = "Подождите пару минут, расписание обновляется"
        return text

    return text[0]


def TimeListUpdate(index):
    __URL = 'https://gu-ural.ru/wp-admin/admin-ajax.php'

    group = select_bd('group_id', 'login_id', 'id', index, 1)[0]
    error = select_bd('group_id', 'login_id', 'id', index, 1)[0]

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

    req = re.sub('<[^<]+?>', '', req)
    req = req.replace('&quot;', '')
    req = req.replace('open.gu', 'open.gu-ural.ru')
    try:
        req_list = json.loads(req)
    except json.decoder.JSONDecodeError:
        text = 'Ошибка получения расписания'
        return text
    list_speed = req_list["current"]["data"]
    day = pendulum.today().format('DD.MM.YYYY')
    next_day = pendulum.tomorrow().format('DD.MM.YYYY')
    weekday = str(datetime.today().isoweekday())
    for speed in list_speed:
        if speed["date"] != day:
            continue

        text += f"{speed['discipline']}"

        if speed.get('notes'):
            text += f" ({speed['notes']})"

        text += "\n"

        if speed.get('type'):
            text += f"{speed['type']}\n"

        if speed.get('place'):
            text += f"{speed['place']}\n"

        if speed.get('classroom'):
            text += f"ауд. {speed['classroom']}\n"

        text += f"{speed['time']}\n\n"

    text += "Завтра:\n\n"

    text_old = text

    if weekday == "7":
        list_speed = req_list["next"]["data"]

    for speed in list_speed:
        if speed["date"] != next_day:
            continue

        text += f"{speed['discipline']}"

        if speed.get('notes'):
            text += f" ({speed['notes']})"

        text += "\n"

        if speed.get('type'):
            text += f"{speed['type']}\n"

        if speed.get('place'):
            text += f"{speed['place']}\n"

        if speed.get('classroom'):
            text += f"ауд. {speed['classroom']}\n"

        text += f"{speed['time']}\n\n"

    text_new = text
    if text_old == text_new and text_new != "Расписание отсутствует\n\n" \
                                            "Завтра:\n\n":
        text += "Расписание отсутствует"

    if text_new == "Расписание отсутствует\n\nЗавтра:\n\n":
        text = "Расписание отсутствует"

    update_bd('login_id', 'list_text', text, 'id', index)

    return text


async def FullList(index):
    __URL = 'https://gu-ural.ru/wp-admin/admin-ajax.php'

    weekday = str(datetime.today().isoweekday())

    group = select_bd('group_id', 'login_id', 'id', index, 1)[0]

    col = {'form': '1',
           'group': group,
           'teacher': '',
           'action': 'lau_shedule_students_show'
           }
    req = requests.post(__URL, data=col).text

    req = re.sub('<[^<]+?>', '', req)
    req = req.replace('&quot;', '')
    req = req.replace('open.gu', 'open.gu-ural.ru')
    try:
        req_list = json.loads(req)
    except json.decoder.JSONDecodeError:
        text = 'Ошибка получения расписания'
        return text
    await bot.send_message(index, 'Расписание на неделю')

    check = 0

    list_speed = req_list["current"]["data"]

    if weekday == "7":
        list_speed = req_list["next"]["data"]

    for j in range(1, 8):
        text = WEEKDAYS[j - 1]

        text_old = text
        for i in range(len(list_speed)):
            if list_speed[i]["discipline"] != "" or \
                    list_speed[i]["discipline"] is not None:
                if list_speed[i]["place"] != "" or \
                        list_speed[i]["place"] is not None:
                    if list_speed[i]["weekday"] == str(j):
                        if list_speed[i]["type"] != "":
                            if list_speed[i]["notes"] != "":
                                if list_speed[i]["place"] is not None:
                                    if list_speed[i]["classroom"] == "" or \
                                            list_speed[i]["classroom"] is None:
                                        text += list_speed[i]["discipline"] \
                                                + " (" \
                                                + list_speed[i]["notes"] \
                                                + ")\n" \
                                                + list_speed[i]["type"] + "\n" \
                                                + list_speed[i]["place"] \
                                                + "\n" \
                                                + list_speed[i]["time"] \
                                                + "\n\n"
                                    else:
                                        text += list_speed[i]["discipline"] \
                                                + " (" \
                                                + list_speed[i]["notes"] \
                                                + ")\n" \
                                                + list_speed[i]["type"] \
                                                + "\n" \
                                                + list_speed[i]["place"] \
                                                + "\n" + "ауд. " \
                                                + list_speed[i]["classroom"] \
                                                + "\n" \
                                                + list_speed[i]["time"] \
                                                + "\n\n"
                                else:
                                    if list_speed[i]["classroom"] == "" or \
                                            list_speed[i]["classroom"] is None:
                                        text += list_speed[i]["discipline"] \
                                                + " (" \
                                                + list_speed[i]["notes"] \
                                                + ")\n" \
                                                + list_speed[i]["type"] \
                                                + "\n" \
                                                + list_speed[i]["time"] \
                                                + "\n\n"
                                    else:
                                        text += list_speed[i]["discipline"] \
                                                + " (" \
                                                + list_speed[i]["notes"] \
                                                + ")\n" \
                                                + list_speed[i]["type"] \
                                                + "\n" \
                                                + "ауд. " \
                                                + list_speed[i]["classroom"] \
                                                + "\n" \
                                                + list_speed[i]["time"] \
                                                + "\n\n"
                            else:
                                if list_speed[i]["place"] is not None:
                                    if list_speed[i]["classroom"] == "" or \
                                            list_speed[i]["classroom"] is None:
                                        text += list_speed[i]["discipline"] \
                                                + "\n" \
                                                + list_speed[i]["type"] \
                                                + "\n" \
                                                + list_speed[i]["place"] \
                                                + "\n" \
                                                + list_speed[i]["time"] \
                                                + "\n\n"
                                    else:
                                        text += list_speed[i][
                                                    "discipline"] + "\n" + \
                                                list_speed[i]["type"] + "\n" \
                                                + list_speed[i]["place"] \
                                                + "\n" \
                                                + "ауд. " \
                                                + list_speed[i]["classroom"] \
                                                + "\n" \
                                                + list_speed[i]["time"] \
                                                + "\n\n"
                                else:
                                    if list_speed[i]["classroom"] == "" or \
                                            list_speed[i]["classroom"] is None:
                                        text += list_speed[i]["discipline"] + \
                                                "\n" \
                                                + list_speed[i]["type"] \
                                                + "\n" \
                                                + list_speed[i]["time"] + \
                                                "\n\n"

                                    else:
                                        text += list_speed[i]["discipline"] + \
                                                "\n" \
                                                + list_speed[i]["type"] \
                                                + "\n" \
                                                + list_speed[i]["time"] + \
                                                "\n" + "\n\n"
                        else:
                            if list_speed[i]["notes"] != "":
                                if list_speed[i]["place"] is not None:
                                    if list_speed[i]["classroom"] == "" or \
                                            list_speed[i]["classroom"] is None:
                                        text += list_speed[i]["discipline"] \
                                                + " (" \
                                                + list_speed[i]["notes"] \
                                                + ")\n" \
                                                + list_speed[i]["place"] \
                                                + "\n" \
                                                + list_speed[i]["time"] \
                                                + "\n\n"
                                    else:
                                        text += list_speed[i]["discipline"] \
                                                + " (" \
                                                + list_speed[i]["notes"] \
                                                + ")\n" \
                                                + list_speed[i]["place"] \
                                                + "\n" + "ауд. " + \
                                                list_speed[i][
                                                    "classroom"] \
                                                + "\n" \
                                                + list_speed[i]["time"] \
                                                + "\n\n"
                                else:
                                    if list_speed[i]["classroom"] == "" or \
                                            list_speed[i]["classroom"] is None:
                                        text += list_speed[i]["discipline"] \
                                                + " (" \
                                                + list_speed[i][
                                                    "notes"] + ")\n" \
                                                + list_speed[i]["time"] \
                                                + "\n\n"
                                    else:
                                        text += list_speed[i]["discipline"] \
                                                + " (" \
                                                + list_speed[i]["notes"] \
                                                + ")\n" \
                                                + "ауд. " \
                                                + list_speed[i]["classroom"] \
                                                + "\n" \
                                                + list_speed[i]["time"] \
                                                + "\n\n"
                            else:
                                if list_speed[i]["place"] is not None:
                                    if list_speed[i]["classroom"] == "" or \
                                            list_speed[i]["classroom"] is None:
                                        text += list_speed[i]["discipline"] \
                                                + "\n" \
                                                + list_speed[i]["place"] \
                                                + "\n" \
                                                + list_speed[i]["time"] \
                                                + "\n\n"
                                    else:
                                        text += list_speed[i][
                                                    "discipline"] + "\n" + \
                                                list_speed[i]["place"] + "\n" \
                                                + "ауд. " \
                                                + list_speed[i]["classroom"] \
                                                + "\n" \
                                                + list_speed[i]["time"] \
                                                + "\n\n"
                                else:
                                    if list_speed[i]["classroom"] == "" or \
                                            list_speed[i]["classroom"] is None:
                                        text += list_speed[i]["discipline"] + \
                                                "\n" \
                                                + list_speed[i]["time"] + \
                                                "\n\n"

                                    else:
                                        text += list_speed[i]["discipline"] + \
                                                "\n" \
                                                + list_speed[i]["time"] + \
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

help_commands = ReplyKeyboardMarkup(resize_keyboard=True).row(
    qurs, start, route, restart, info
)

typ1 = InlineKeyboardButton(
    'Бакалавриат', callback_data='typ1_click')
typ2 = InlineKeyboardButton(
    'Магистратура', callback_data='typ2_click')

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
# (Магистратура)
nup1_2 = KeyboardButton('Юриспруденция\n(М)')
nup2 = KeyboardButton('Экономика')
# (Магистратура)
nup2_2 = KeyboardButton('Экономика\n(М)')
nup3 = KeyboardButton('Менеджмент')
nup4 = KeyboardButton('Прикладная информатика')
nup6 = KeyboardButton(
    'Реклама и связи с общественностью')
nup7 = KeyboardButton('Сервис')
nup8 = KeyboardButton('Хореографическое искусство')
nup9 = KeyboardButton("Управление персоналом")
nup10 = KeyboardButton('Журналистика')
nup11 = KeyboardButton('Гостиничное дело')
nup12 = KeyboardButton('Психология')
# (Магистратура)
nup12_2 = KeyboardButton('Психология\n(М)')
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


async def on_startup(_):
    asyncio.create_task(AutoTask(bot, configs, path, TimeList, TimeListUpdate).AutoTime())
    asyncio.create_task(AutoTask(bot, configs, path, TimeList, TimeListUpdate).ListUpdate())
    asyncio.create_task(AutoTask(bot, configs, path, TimeList, TimeListUpdate).ListTimeUpdater())
    if STOP == "1":
        asyncio.create_task(AutoTask(bot, configs, path, TimeList, TimeListUpdate).StopMessage())


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
    auto = select_bd('auto_time', 'login_id', 'id', message.chat.id, 1)[0]

    if auto == '0':
        await message.answer('Включено авто-расписание в 21:00',
                             reply_markup=button_restart)
        update_bd('login_id', 'auto_time', 1, 'id', message.chat.id)


@dp.message_handler(commands=['off'])
async def process_autotime_off(message: types.Message):
    auto = select_bd('auto_time', 'login_id', 'id', message.chat.id, 1)[0]

    if auto == '1':
        await message.answer('Выключено авто-расписание',
                             reply_markup=button_restart)
        update_bd('login_id', 'auto_time', 0, 'id', message.chat.id)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.answer('Мои команды', reply_markup=help_commands)


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

    create_bd()

    people_id = message.chat.id

    data = select_bd('id', 'login_id', 'id', people_id, 1)

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
        if speciality == '1':
            update_bd('login_id', 'group_id', 962, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        # if speciality == '2':
        #     update_bd('login_id', 'group_id', 797, 'id', people_id)
        #     await message.answer(TimeList(people_id),
        #                          reply_markup=button_restart)

        if speciality == '3':
            update_bd('login_id', 'group_id', 956, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '4':
            update_bd('login_id', 'group_id', 934, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '6':
            update_bd('login_id', 'group_id', 943, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        # if speciality == '7':
        #     update_bd('login_id', 'group_id', 789, 'id', people_id)
        #     await message.answer(TimeList(people_id),
        #                          reply_markup=button_restart)
        if speciality == '8':
            update_bd('login_id', 'group_id', 835, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        # if speciality == '9':
        #     update_bd('login_id', 'group_id', 786, 'id', people_id)
        #     await message.answer(TimeList(people_id),
        #                          reply_markup=button_restart)
        if speciality == '10':
            update_bd('login_id', 'group_id', 923, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '11':
            update_bd('login_id', 'group_id', 916, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '12':
            update_bd('login_id', 'group_id', 920, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '13':
            update_bd('login_id', 'group_id', 922, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '14':
            update_bd('login_id', 'group_id', 913, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '15':
            update_bd('login_id', 'group_id', 815, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)

    if message.text == '2️⃣':
        # if speciality == '1':
        #     update_bd('login_id', 'group_id', 962, 'id', people_id)
        #     await message.answer(TimeList(people_id),
        #                          reply_markup=button_restart)
        if speciality == '2':
            update_bd('login_id', 'group_id', 957, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '3':
            update_bd('login_id', 'group_id', 956, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '4':
            update_bd('login_id', 'group_id', 917, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '6':
            update_bd('login_id', 'group_id', 944, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '7':
            update_bd('login_id', 'group_id', 949, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '8':
            update_bd('login_id', 'group_id', 836, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '9':
            update_bd('login_id', 'group_id', 933, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '10':
            update_bd('login_id', 'group_id', 924, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '11':
            update_bd('login_id', 'group_id', 947, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '11':
            update_bd('login_id', 'group_id', 939, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)

        if speciality == '13':
            update_bd('login_id', 'group_id', 948, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '15':
            update_bd('login_id', 'group_id', 842, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)

    if message.text == '3️⃣':
        if speciality == '1':
            update_bd('login_id', 'group_id', 911, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '2':
            update_bd('login_id', 'group_id', 958, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        # if speciality == '3':
        #     update_bd('login_id', 'group_id', 801, 'id', people_id)
        #     await message.answer(TimeList(people_id),
        #                          reply_markup=button_restart)
        if speciality == '4':
            update_bd('login_id', 'group_id', 918, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '6':
            update_bd('login_id', 'group_id', 941, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '7':
            update_bd('login_id', 'group_id', 951, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '8':
            update_bd('login_id', 'group_id', 837, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        # if speciality == '9':
        #     update_bd('login_id', 'group_id', 819, 'id', people_id)
        #     await message.answer(TimeList(people_id),
        #                          reply_markup=button_restart)
        if speciality == '10':
            update_bd('login_id', 'group_id', 925, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '11':
            update_bd('login_id', 'group_id', 950, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        # if speciality == '12':
        #     update_bd('login_id', 'group_id', 810, 'id', people_id)
        #     await message.answer(TimeList(people_id),
        #                          reply_markup=button_restart)
        if speciality == '13':
            update_bd('login_id', 'group_id', 952, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)

    if message.text == '4️⃣':
        if speciality == '1':
            update_bd('login_id', 'group_id', 912, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '3':
            update_bd('login_id', 'group_id', 814, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '4':
            update_bd('login_id', 'group_id', 919, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '6':
            update_bd('login_id', 'group_id', 945, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '7':
            update_bd('login_id', 'group_id', 953, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '8':
            update_bd('login_id', 'group_id', 838, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '9':
            update_bd('login_id', 'group_id', 946, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '10':
            update_bd('login_id', 'group_id', 926, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '11':
            update_bd('login_id', 'group_id', 955, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '12':
            update_bd('login_id', 'group_id', 940, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)
        if speciality == '13':
            update_bd('login_id', 'group_id', 954, 'id', people_id)
            await message.answer(TimeList(people_id),
                                 reply_markup=button_restart)

    if message.text == 'Обновить':
        if TimeList(people_id) == "Пожалуйста пересоздайте аккаунт\n\n" \
                                  "P.S. скорее всего я что-то обновил и ваш аккаунт потерялся(":
            await message.answer("Пожалуйста пересоздайте аккаунт\n\n"
                                 "P.S. скорее всего я что-то обновил и ваш аккаунт потерялся(",
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
        update_bd('login_id', 'speciality_id', 1, 'id', people_id)
        await message.answer('Ваш курс', reply_markup=markup1)
    if message.text == nup2.text:
        update_bd('login_id', 'speciality_id', 2, 'id', people_id)
        await message.answer('Ваш курс и группа', reply_markup=markup5)
    if message.text == nup3.text:
        update_bd('login_id', 'speciality_id', 3, 'id', people_id)
        await message.answer('Ваш курс', reply_markup=markup1)
    if message.text == nup4.text:
        update_bd('login_id', 'speciality_id', 4, 'id', people_id)
        await message.answer('Ваш курс', reply_markup=markup1)
    if message.text == nup6.text:
        update_bd('login_id', 'speciality_id', 6, 'id', people_id)
        await message.answer('Ваш курс', reply_markup=markup1)
    if message.text == nup7.text:
        update_bd('login_id', 'speciality_id', 7, 'id', people_id)
        await message.answer('Ваш курс', reply_markup=markup1)
    if message.text == nup8.text:
        update_bd('login_id', 'speciality_id', 8, 'id', people_id)
        await message.answer('Ваш курс', reply_markup=markup1)
    if message.text == nup9.text:
        update_bd('login_id', 'speciality_id', 9, 'id', people_id)
        await message.answer('Ваш курс', reply_markup=markup1)
    if message.text == nup10.text:
        update_bd('login_id', 'speciality_id', 10, 'id', people_id)
        await message.answer('Ваш курс', reply_markup=markup1)
    if message.text == nup11.text:
        update_bd('login_id', 'speciality_id', 11, 'id', people_id)
        await message.answer('Ваш курс', reply_markup=markup1)
    if message.text == nup12.text:
        update_bd('login_id', 'speciality_id', 12, 'id', people_id)
        await message.answer('Ваш курс', reply_markup=markup1)
    if message.text == nup13.text:
        update_bd('login_id', 'speciality_id', 13, 'id', people_id)
        await message.answer('Ваш курс', reply_markup=markup1)
    if message.text == nup1_2.text:
        update_bd('login_id', 'speciality_id', 14, 'id', people_id)
        await message.answer('Ваш курс', reply_markup=markup1)
    if message.text == nup2_2.text:
        update_bd('login_id', 'speciality_id', 15, 'id', people_id)
        await message.answer('Ваш курс', reply_markup=markup1)
    if message.text == nup12_2.text:
        update_bd('login_id', 'speciality_id', 16, 'id', people_id)
        await message.answer('Ваш курс', reply_markup=markup1)

    if message.text == gr1.text:
        update_bd('login_id', 'group_id', 802, 'id', people_id)
        await message.answer(TimeList(people_id),
                             reply_markup=button_restart)

    if message.text == gr2.text:
        update_bd('login_id', 'group_id', 799, 'id', people_id)
        await message.answer(TimeList(people_id),
                             reply_markup=button_restart)

    if message.text == gr3.text:
        update_bd('login_id', 'group_id', 817, 'id', people_id)
        await message.answer(TimeList(people_id),
                             reply_markup=button_restart)

    if message.text == gr4.text:
        update_bd('login_id', 'group_id', 816, 'id', people_id)
        await message.answer(TimeList(people_id),
                             reply_markup=button_restart)


if __name__ == '__main__':
    if SLEEP == "False":
        executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
