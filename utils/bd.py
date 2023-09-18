import sqlite3


def create_bd():
    """
    Создает базу данных
    """
    connect = sqlite3.connect('users.db')
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


def update_bd(column: str, field: str, field_num: int or str, search: str, search_num: int):
    """
    :param column: Колонка
    :type column: str
    :param field: Обновляемое поле
    :type field: str
    :param field_num: Значение обновляемого поля
    :type field_num: int or str
    :param search: Поле фильтр
    :type search: str
    :param search_num: Значение поля фильтра
    :type search_num: int
    """
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute(
        f"UPDATE {column} SET {field} = ? WHERE {search} = ?;", [field_num, search_num])
    connect.commit()


def select_bd(field: str, column: str, search_field: str, search_num: int, method=0):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    if method == 0:
        cursor.execute(
            f"SELECT {field} FROM {column} WHERE {search_field} = {search_num};")
        connect.commit()
    if method == 1:
        data = cursor.execute(
            f"SELECT {field} FROM {column} WHERE {search_field} = {search_num};").fetchone()
        connect.commit()
        return data
