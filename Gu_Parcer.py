import json
from datetime import datetime

import requests


def TimeList(speciality_num, course_num, group_num):
    __URL = 'https://gu-ural.ru/wp-admin/admin-ajax.php'

    if course_num != 0:
        k_time = course_num

    col = {'form': '1',
           'speciality': speciality_num,
           'course': k_time,
           'group': group_num,
           'teacher': '',
           'action': 'lau_shedule_students_show'
           }
    req = requests.post(__URL, data=col).text
    list = json.loads(req)
    list_speed = list["current"]["data"]
    text = ''
    day = datetime.today().isoweekday()
    for i in range(len(list_speed)):
        #text += \
        if list_speed[i]["weekday"] == str(day):
            if list_speed[i]["notes"] != "":
                if list_speed[i]["place"] is not None:
                    print(list_speed[i]["discipline"] + " ("
                          + list_speed[i]["notes"] + ")\n "
                          + list_speed[i]["place"] + "\n")
                else:
                    print(list_speed[i]["discipline"] + " ("
                          + list_speed[i]["notes"] + ")\n" + "\n")
            else:
                if list_speed[i]["place"] is not None:
                    print(list_speed[i]["discipline"] +
                          + list_speed[i]["place"] + "\n")
                else:
                    print(list_speed[i]["discipline"] + " ("
                          + list_speed[i]["notes"] + ")\n" + "\n")

        # if list_speed[i]["weekday"] == str(day+1):
        #     print(list_speed[i]["discipline"] + " (" + list_speed[i]["notes"] + ")\n" + list_speed[i]["time"] + "\n")

    return text


print(TimeList(4, 2, 793))
