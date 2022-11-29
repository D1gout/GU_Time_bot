import logging

from aiogram import Bot, Dispatcher, executor, types

# Токен, выданный BotFather в телеграмме
TOKEN = '5975391066:AAEHxpuSeVYz4fidfGbV61zuKN4zOrxGvDY'
MY_ID = '706967790'
DB_FILENAME = 'db_bot'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отправлю этот текст тебе в ответ!")


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне что-нибудь!")


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
