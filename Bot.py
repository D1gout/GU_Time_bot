import logging

from aiogram import Bot, Dispatcher, executor, types

# Токен, выданный BotFather в телеграмме
API_TOKEN = '5975391066:AAEHxpuSeVYz4fidfGbV61zuKN4zOrxGvDY'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer('Ты пидор')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
