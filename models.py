import sqlite3


def create_models():
    try:
        sqlite_connection = sqlite3.connect('sqlite_python.db')
        sqlite_create_tables_queries = '''CREATE TABLE IF NOT EXISTS resources (
                                    RESOURCE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                    RESOURCE_NAME TEXT NOT NULL,
                                    RESOURCE_URL  text NOT NULL,
                                    top_tag  text,
                                    bottom_tag  text,
                                    title_cut text,
                                    date_cut datetime );'''
        items = '''CREATE TABLE IF NOT EXISTS items (
                                        id  INTEGER PRIMARY KEY AUTOINCREMENT,
                                        res_id  INTEGER NOT NULL,
                                        link   text NOT NULL,
                                        title   text,
                                        content   text,
                                        nd_date  datetime,
                                        s_date  datetime,
                                        not_date text );'''
        cursor = sqlite_connection.cursor()
        print("База данных подключена к SQLite")
        cursor.execute(sqlite_create_tables_queries)
        sqlite_connection.commit()
        cursor.execute(items)
        sqlite_connection.commit()
        print("Таблица SQLite создана")
        cursor.close()


    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
