import asyncio
import sqlite3
from icecream.icecream import ic
from datetime import datetime

from aiogram.utils.exceptions import BotBlocked, UserDeactivated
from utils.bd import create_bd
connect = sqlite3.connect('users.db')
cursor = connect.cursor()


class AutoTask:
    def __init__(self, bot, configs, path, time_list, time_list_update):
        create_bd()
        self.bot = bot
        self.configs = configs
        self.path = path
        self.time_list = time_list
        self.time_list_update = time_list_update

    async def AutoTime(self):  # Авто расписание
        auto = [x[0] for x in cursor.execute(
            "SELECT id FROM login_id WHERE auto_time = {}".format(1))]

        while not auto:
            await asyncio.sleep(10)

            auto = [x[0] for x in cursor.execute(
                "SELECT id FROM login_id WHERE auto_time = {}".format(1))]

        check = 1
        while auto:
            auto_people = [x[0] for x in cursor.execute(
                "SELECT id FROM login_id WHERE auto_time = {}".format(1))]

            if datetime.now().strftime("%H:%M") == '20:55':
                check = 1

            i = 0
            await asyncio.sleep(20)
            if datetime.now().strftime("%H:%M") == '21:00' and check == 1:
                for _ in auto_people:
                    try:
                        await self.bot.send_message(auto_people[i],
                                                    self.time_list(auto_people[i]))
                    except BotBlocked as e:
                        ic(e)
                        await asyncio.sleep(0.1)
                    except UserDeactivated as e:
                        ic(e)
                        await asyncio.sleep(0.1)

                    check = 0
                    i += 1

    async def ListUpdate(self):  # Авто обновление расписания
        index_count = [x[0] for x in cursor.execute(
            "SELECT id FROM login_id WHERE group_id != {}".format(0))]

        while not index_count:
            await asyncio.sleep(10)

            index_count = [x[0] for x in cursor.execute(
                "SELECT id FROM login_id WHERE group_id != {}".format(0))]

        while True:
            index = [x[0] for x in cursor.execute(
                "SELECT id FROM login_id WHERE group_id != {}".format(0))]

            i = 0
            for _ in index:
                old_text = [x[0] for x in cursor.execute(
                    "SELECT list_text FROM login_id WHERE id = {}"
                    .format(index[i]))]

                try:
                    self.time_list_update(index[i])
                except BotBlocked as e:
                    ic(e)
                    await asyncio.sleep(0.1)
                except UserDeactivated as e:
                    ic(e)
                    await asyncio.sleep(0.1)

                now_text = [x[0] for x in cursor.execute(
                    "SELECT list_text FROM login_id WHERE id = {}".
                    format(index[i]))]

                if now_text[0] != old_text[0]:
                    try:
                        await self.bot.send_message(index[i], now_text[0])
                    except BotBlocked as e:
                        ic(e)
                        await asyncio.sleep(0.1)
                    except UserDeactivated as e:
                        ic(e)
                        await asyncio.sleep(0.1)

                i += 1

            await asyncio.sleep(120)

    async def ListTimeUpdater(self):  # Обновление расписания в БД раз в час
        index_count = [x[0] for x in cursor.execute(
            "SELECT id FROM login_id WHERE group_id != {}".format(0))]

        while index_count:
            index_count = [x[0] for x in cursor.execute(
                "SELECT id FROM login_id WHERE group_id != {}".format(0))]

            i = 0
            for _ in index_count:
                try:
                    self.time_list_update(index_count[i])
                except BotBlocked as e:
                    ic(e)
                    await asyncio.sleep(0.1)
                except UserDeactivated as e:
                    ic(e)
                    await asyncio.sleep(0.1)

                i += 1

            await asyncio.sleep(3600)

    async def StopMessage(self):  # Сообщение о начале каникул
        index_count = [x[0] for x in cursor.execute(
            "SELECT id FROM login_id WHERE group_id != {}".format(0))]

        i = 0
        for _ in index_count:
            try:
                await self.bot.send_message(index_count[i], 'Спасибо, что пользовались ботом\n'
                                                            'ФКТ желает хороших каникул тем,\nу кого они уже начались!')
            except BotBlocked as e:
                ic(e)
                await asyncio.sleep(0.1)
            except UserDeactivated as e:
                ic(e)
                await asyncio.sleep(0.1)

            i += 1

        self.configs.set("Settings", "sleep_mode", "True")

        with open(self.path, "w") as config_file:
            self.configs.write(config_file)
