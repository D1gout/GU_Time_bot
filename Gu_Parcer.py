import logging
import json
import sqlite3
from datetime import datetime

import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

#
#
# def TimeList(speciality_num, course_num, group_num):
#     __URL = 'https://gu-ural.ru/wp-admin/admin-ajax.php'
#
#     if course_num != 0:
#         k_time = course_num
#
#     col = {'form': '1',
#            'speciality': speciality_num,
#            'course': k_time,
#            'group': group_num,
#            'teacher': '',
#            'action': 'lau_shedule_students_show'
#            }
#     req = requests.post(__URL, data=col).text
#     list = json.loads(req)
#     list_speed = list["current"]["data"]
#     text = ''
#     day = datetime.today().isoweekday()
#     for i in range(len(list_speed)):
#         #text += \
#         if list_speed[i]["weekday"] == str(day):
#             if list_speed[i]["notes"] != "":
#                 if list_speed[i]["place"] is not None:
#                     print(list_speed[i]["discipline"] + " ("
#                           + list_speed[i]["notes"] + ")\n "
#                           + list_speed[i]["place"] + "\n")
#                 else:
#                     print(list_speed[i]["discipline"] + " ("
#                           + list_speed[i]["notes"] + ")\n" + "\n")
#             else:
#                 if list_speed[i]["place"] is not None:
#                     print(list_speed[i]["discipline"] +
#                           + list_speed[i]["place"] + "\n")
#                 else:
#                     print(list_speed[i]["discipline"] + " ("
#                           + list_speed[i]["notes"] + ")\n" + "\n")
#
#         # if list_speed[i]["weekday"] == str(day+1):
#         #     print(list_speed[i]["discipline"] + " (" + list_speed[i]["notes"] + ")\n" + list_speed[i]["time"] + "\n")
#
#     return text
#
#
# print(TimeList(4, 2, 793))
#
# __URL = 'https://gu-ural.ru/wp-admin/admin-ajax.php'
#
# connect = sqlite3.connect('users.db')
# cursor = connect.cursor()
#
# connect.commit()
#
# s = ''
# c = ''
# g = ''
#
# for speciality_num in cursor.execute(f"SELECT speciality_id FROM login_id WHERE id = {706967790}"):
#     s += str(speciality_num)[1]
# for course_num in cursor.execute(f"SELECT course_id FROM login_id WHERE id = {706967790}"):
#     c += str(course_num)[1]
# for group_num in cursor.execute(f"SELECT group_id FROM login_id WHERE id = {706967790}"):
#     g += str(group_num)[1:4]
#
# col = {'form': '1',
#        'speciality': s,
#        'course': c,
#        'group': g,
#        'teacher': '',
#        'action': 'lau_shedule_students_show'
#        }
# req = requests.post(__URL, data=col).text
# list = json.loads(req)
# list_speed = list["current"]["data"]
# text = ''
# day = datetime.today().isoweekday()
# for i in range(len(list_speed)):
#     if list_speed[i]["weekday"] == str(day):
#         if list_speed[i]["notes"] != "":
#             if list_speed[i]["place"] is not None:
#                 text += list_speed[i]["discipline"] + " (" + list_speed[i]["notes"] + ")\n" \
#                         + list_speed[i]["place"] \
#                         + "\n" + list_speed[i]["time"] + "\n\n"
#             else:
#                 text += list_speed[i]["discipline"] + " (" + list_speed[i]["notes"] + ")\n" + list_speed[i]["time"] \
#                         + "\n\n"
#         else:
#             if list_speed[i]["place"] is not None:
#                 text += list_speed[i]["discipline"] + "\n" + list_speed[i]["place"] + "\n" + list_speed[i]["time"] \
#                         + "\n\n"
#             else:
#                 text += list_speed[i]["discipline"] + list_speed[i]["time"] + "\n\n"
#
# print(text)

nup13 = KeyboardButton('Туризм')

print(nup13.text)
