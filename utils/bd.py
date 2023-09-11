import sqlite3


def create_bd():
    """
    Создает базу данных
    """
    connect = sqlite3.connect('./../users.db')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
                    id INTEGER,
                    speciality_id STRING NOT NULL DEFAULT '0',
                    course_id STRING NOT NULL DEFAULT '0',
                    group_id STRING NOT NULL DEFAULT '0',
                    auto_time STRING NOT NULL DEFAULT '0',
                    list_text TEXT NOT NULL DEFAULT 'None'
                )""")

    connect.commit()


def update_bd(column: str, field: str, field_num: int or str, value: str, value_num: int):
    """
    :param column: Колонка
    :type column: str
    :param field: Поле
    :type field: str
    :param field_num: Значение поля
    :type field_num: int or str
    :param value: Обновляемое поле
    :type value: str
    :param value_num: Значение для обновления
    :type value_num: int
    """
    connect = sqlite3.connect('./../users.db')
    cursor = connect.cursor()

    cursor.execute(
        f"UPDATE {column} SET {field} = {field_num} WHERE {value} = {value_num};")
    connect.commit()


def select_bd(field: str, column: str, search_field: str, search_num: int):
    connect = sqlite3.connect('./../users.db')
    cursor = connect.cursor()

    cursor.execute(
        f"SELECT {field} FROM {column} WHERE {search_field} = {search_num};")
    connect.commit()
