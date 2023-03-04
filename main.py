import sqlite3
import getting_data_from_site
import db
import models
import inserts

db.create_database()
models.create_models()
inserts.insert_data_ro_resources()
try:
    sqlite_connection = sqlite3.connect('sqlite_python.db')
    cursor = sqlite_connection.cursor()
    print("База данных подключена к SQLite")
    cursor.execute('SELECT * FROM resources;')
    resources = cursor.fetchall()
    print(resources)
    getting_data_from_site.get_data(resources[0][0], resources[0][2])
except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)

finally:
    if (sqlite_connection):
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")
