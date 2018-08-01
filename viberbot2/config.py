from enum import Enum
from peewee import PostgresqlDatabase, Model
import json

token = '47f9342a0767d358-7be9201a856b9132-dd0645dd704dc0c'

db = PostgresqlDatabase(
    database='d9r2fbaqjqm03n',
    user='nvpxjyazjaukzl',
    password='3bc6d35180897c67d46391aa7a32941fc46f53c1029cd57601cb8a31f0bb920d',
    host='ec2-54-235-252-23.compute-1.amazonaws.com',
    port=5432
)

temp_addr = 'ОШИБКА. НАЖМИТЕ "НЕТ"'

class States(Enum):
    S_START_BOOKING = '0'
    S_ADDITION = '1'
    S_CONFIRM_ORDER = '2'
    S_DONE = '3'

main_kb = json.loads("""
{
    "Type":"keyboard",
    "Buttons":[
        {
            "Columns":6,
            "Rows":1,
            "Text":"<font color='#ffffff' size='20'>Заказать такси</font>",
            "ActionBody":"order_taxi",
            "BgColor":"#C77306"
        },
        {
            "Columns":3,
            "Rows":1,
            "Text":"<font color='#C77306'>Контакты</font>",
            "ActionBody":"contacts",
            "BgColor":"#ffffff"
        },
        {
            "Columns":3,
            "Rows":1,
            "Text":"<font color='#C77306'>Написать отзыв</font>",
            "ActionBody":"feedback",
            "BgColor":"#ffffff"
        }
    ]
}""")

cancel_kb = json.loads("""
{
    "Type":"keyboard",
    "Buttons":[
        {
            "Columns":6,
            "Rows":1,
            "Text":"<font color='#ffffff' size='20'>Назад</font>",
            "ActionBody":"cancel_answer",
            "BgColor":"#000000"
        }
    ]
}
""")

yes_no_kb = json.loads("""
{
    "Type":"keyboard",
    "Buttons":[
        {
            "Columns":3,
            "Rows":1,
            "Text":"<font color='#ffffff' size='20'>Нет</font>",
            "ActionBody":"no_answer",
            "BgColor":"#ff776d"
        },
        {
            "Columns":3,
            "Rows":1,
            "Text":"<font color='#ffffff' size='20'>Да</font>",
            "ActionBody":"yes_answer",
            "BgColor":"#8bffae"
        }
    ]
}
""")

back_pass_kb = json.loads("""
{
    "Type":"keyboard",
    "Buttons":[
        {
            "Columns":3,
            "Rows":1,
            "Text":"<font color='#C77306' size='20'>Назад</font>",
            "ActionBody":"back_answer",
            "BgColor":"#ffffff"
        },
        {
            "Columns":3,
            "Rows":1,
            "Text":"<font color='#ffffff'>Пропустить</font>",
            "ActionBody":"pass_answer",
            "BgColor":"#C77306"
        }
    ]
}
""")