import logging
import sqlite3
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

# Токен, ID создателя, Имя базы данных
TOKEN = '5975391066:AAEHxpuSeVYz4fidfGbV61zuKN4zOrxGvDY'
MY_ID = '706967790'
DB_FILENAME = 'db_bot'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
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
        users_id = [message.chat.id, '1', '3']

        cursor.execute(f"INSERT INTO login_id VALUES({people_id}, 4, 1, 792);")

        connect.commit()

        for speciality_num in cursor.execute(f"SELECT speciality_id FROM login_id WHERE id = {people_id}"):
            print(str(speciality_num)[1])
        for course_num in cursor.execute(f"SELECT course_id FROM login_id WHERE id = {people_id}"):
            print(str(course_num)[1])
        for group_num in cursor.execute(f"SELECT group_id FROM login_id WHERE id = {people_id}"):
            print(str(group_num)[1:4])
    else:
        await bot.send_message(message.chat.id, 'Уже зареганы')


@dp.message_handler(commands=['delete'])
async def delete(message: types.Message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    people_id = message.chat.id
    cursor.execute(f"DELETE FROM login_id WHERE id = {people_id}")
    connect.commit()



if __name__ == '__main__':
    executor.start_polling(dp)
