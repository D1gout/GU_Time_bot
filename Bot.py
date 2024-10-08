import asyncio
import json
import logging
import re
import sqlite3
import configparser
from datetime import datetime

from bs4 import BeautifulSoup
from decouple import config
from utils.groups import groups

import pendulum
import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import RetryAfter, TelegramAPIError
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

    text = WEEKDAYS[datetime.today().weekday()]

    if group == '0':
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

delete = KeyboardButton('/delete')
button_delete = ReplyKeyboardMarkup(resize_keyboard=True,
                                    one_time_keyboard=True).add(delete)

on = KeyboardButton('/on')
off = KeyboardButton('/off')

restart = KeyboardButton('Обновить')
button_restart = ReplyKeyboardMarkup(resize_keyboard=True).row(
    restart, on, off
)

help_commands = ReplyKeyboardMarkup(resize_keyboard=True).row(
    qurs, start, delete, route, restart, info
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
    nup1_2, nup2_2, nup12_2
)
user_group_selection = {}


async def on_startup(_):
    tsk = AutoTask(bot, configs, path, TimeList, TimeListUpdate)
    asyncio.create_task(tsk.AutoTime())
    asyncio.create_task(tsk.ListUpdate())
    if STOP == "1":
        asyncio.create_task(tsk.StopMessage())

    await bot.send_message(706967790, "INFO:aiogram.dispatcher.dispatcher:Start polling")


async def process_group_selection(message, speciality, people_id):
    group_data = groups.get(speciality, {}).get(message.text)

    if isinstance(group_data, list):
        user_group_selection[people_id] = group_data
        markup = ReplyKeyboardMarkup(resize_keyboard=True)

        buttons = [KeyboardButton(str(group_id)) for group_id in group_data]
        markup.add(*buttons)

        await message.answer('Выберите вашу группу:', reply_markup=markup)

    elif group_data:  # Если только один вариант group_id
        update_bd('login_id', 'group_id', group_data, 'id', people_id)
        await message.answer(TimeList(people_id), reply_markup=button_restart)

    else:  # Если группа не найдена
        await message.answer('Группа не найдена, попробуйте еще раз.')


async def handle_group_choice(message, people_id):
    if people_id in user_group_selection:
        selected_group = int(message.text)
        if selected_group in user_group_selection[people_id]:
            update_bd('login_id', 'group_id', selected_group, 'id', people_id)
            await message.answer(TimeList(people_id), reply_markup=button_restart)
        else:
            await message.answer('Неверный выбор группы, попробуйте еще раз.')

        # Очищаем выбор группы после обработки
        del user_group_selection[people_id]
    else:
        await message.answer('Произошла ошибка, выберите группу снова.')


@dp.callback_query_handler(lambda c: c.data == 'typ1_click')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    try:
        await bot.send_message(callback_query.from_user.id, 'Ваше направление',
                               reply_markup=markup2)
    except ():
        await asyncio.sleep(0.1)


@dp.callback_query_handler(lambda c: c.data == 'typ2_click')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    try:
        await bot.send_message(callback_query.from_user.id, 'Ваше направление',
                               reply_markup=markup5)
    except ():
        await asyncio.sleep(0.1)


@dp.message_handler(commands=['on'])
async def process_autotime_on(message: types.Message):
    auto = select_bd('auto_time', 'login_id', 'id', message.chat.id, 1)[0]

    if str(auto) == '0':
        await message.answer('Включено авто-расписание в 21:00',
                             reply_markup=button_restart)
        update_bd('login_id', 'auto_time', 1, 'id', message.chat.id)


@dp.message_handler(commands=['off'])
async def process_autotime_off(message: types.Message):
    auto = select_bd('auto_time', 'login_id', 'id', message.chat.id, 1)[0]

    if str(auto) == '1':
        await message.answer('Выключено авто-расписание',
                             reply_markup=button_restart)
        update_bd('login_id', 'auto_time', 0, 'id', message.chat.id)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.answer('Мои команды', reply_markup=help_commands)


@dp.message_handler(commands=['info'])
async def process_info_command(message: types.Message):
    url = 'https://github.com/D1gout/GU_Time_bot/releases'

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        pre_tag = soup.find('pre', class_='text-small color-fg-muted ws-pre-wrap')

        if pre_tag:
            text = pre_tag.get_text(strip=True)
            await message.answer(text,
                                 reply_markup=button_restart)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer(
        "Привет!",
        reply_markup=link_button)
    await message.answer(
        "Я бот который скидывает расписание\n\nВыбери уровень обучения",
        reply_markup=typ_buttons)


@dp.message_handler(commands=['delete'])
async def process_start_command(message: types.Message):
    update_bd('login_id', 'list_text', "None", 'id', message.chat.id)
    update_bd('login_id', 'group_id', 0, 'id', message.chat.id)
    await message.answer(
        "Аккаунт удален",
        reply_markup=button_start)


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

    if message.text in ['1️⃣', '2️⃣', '3️⃣', '4️⃣']:
        await process_group_selection(message, speciality, people_id)

    elif message.text.isdigit() and people_id in user_group_selection:
        await handle_group_choice(message, people_id)

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
        await message.answer('Ваш курс', reply_markup=markup1)
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


def start_bot():
    try:
        executor.start_polling(dp, on_startup=on_startup, timeout=20)
    except RetryAfter as e:
        retry_after = e.timeout
        print(f"Превышен лимит запросов. Повтор через {retry_after} секунд.")
        asyncio.sleep(retry_after)
        start_bot()
    except TelegramAPIError as e:
        print(f"Ошибка Telegram API: {e}. Повторная попытка через 5 секунд.")
        asyncio.sleep(5)
        start_bot()
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        asyncio.sleep(5)
        start_bot()


if __name__ == '__main__':
    if SLEEP == "False":
        start_bot()
