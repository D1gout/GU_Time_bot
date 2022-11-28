import logging

from aiogram import Bot, Dispatcher, executor, types
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MediaIds(Base):
    __tablename__ = 'Media ids'
    id = Column(Integer, primary_key=True)
    file_id = Column(Sastring(255))
    filename = Column(String(255))


# Токен, выданный BotFather в телеграмме
API_TOKEN = '5975391066:AAEHxpuSeVYz4fidfGbV61zuKN4zOrxGvDY'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне что-нибудь!")


@dp.message_handler(commands=['photo'])
async def process_photo_command(message: types.Message):
    caption = 'Какие глазки! :eyes:'
    await bot.send_photo(message.from_user.id, CAT_BIG_EYES,
                         caption=emojize(caption),
                         reply_to_message_id=message.message_id)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
