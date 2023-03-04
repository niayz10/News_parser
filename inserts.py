import sqlite3
import traceback
import sys
import datetime
from format_functions import get_not_date


def insert_data_ro_resources():
    try:
        sqlite_connection = sqlite3.connect('sqlite_python.db')
        cursor = sqlite_connection.cursor()
        print("База данных подключена к SQLite")
        cursor.execute('SELECT * FROM resources;')
        resources = cursor.fetchall()
        if len(resources) != 0:
            return
        sqlite_insert_query = """INSERT INTO resources
                              (RESOURCE_NAME, RESOURCE_URL, top_tag,
                              bottom_tag, title_cut, date_cut)
                                VALUES  ('Nur.kz', 'https://www.nur.kz/society/', 
                                'top tag', 'bottom tag', 'title cut', '2019-03-17')"""

        cursor.execute(sqlite_insert_query)
        sqlite_connection.commit()
        print("Запись успешно вставлена в таблицу resouces ", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Не удалось вставить данные в таблицу sqlite")
        print("Класс исключения: ", error.__class__)
        print("Исключение", error.args)
        print("Печать подробноcтей исключения SQLite: ")
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def insert_to_items_db(res_id, project_url, project_headline, project_content, project_date):
    try:
        sqlite_connection = sqlite3.connect('sqlite_python.db')
        cursor = sqlite_connection.cursor()
        print("База данных подключена к SQLite")
        insert_query = """INSERT INTO items (res_id, link, title, content, nd_date, s_date, not_date) 
                            VALUES  (?,?,?,?,?,?,?)"""
        now = datetime.datetime.now()
        data_tuple = (res_id, project_url, project_headline, project_content, project_date, now,
                      get_not_date(project_date))
        cursor.execute(insert_query, data_tuple)
        sqlite_connection.commit()
        print("Запись успешно вставлена в таблицу items ")
        cursor.close()

    except sqlite3.Error as error:
        print("Не удалось вставить данные в таблицу items")
        print("Класс исключения: ", error.__class__)
        print("Исключение", error.args)
        print("Печать подробноcтей исключения SQLite: ")
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))

    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
