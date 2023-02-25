import sqlite3
import traceback
import sys

try:
    sqlite_connection = sqlite3.connect('sqlite_python.db')
    cursor = sqlite_connection.cursor()
    print("База данных подключена к SQLite")

    sqlite_insert_query = """INSERT INTO resources
                          (RESOURCE_NAME, RESOURCE_URL, top_tag,
                          bottom_tag, title_cut, date_cut)
                            VALUES  ('Nur.kz', 'https://www.nur.kz/society/', 
                            'top tag', 'bottom tag', 'title cut', '2019-03-17')"""

    count = cursor.execute(sqlite_insert_query)
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