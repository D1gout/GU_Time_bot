import json

import requests

__URL = 'https://gu-ural.ru/wp-admin/admin-ajax.php'

speciality_num = '4'
course_num = '2'
group_num = '793'


col = {'form': '1',
       'speciality': speciality_num,
       'course': course_num,
       'group': group_num,
       'teacher': '',
       'action': 'lau_shedule_students_show'
       }

req = requests.post(__URL, data=col).text

list = json.loads(req)

#print(list)
print(list)
