
import os.path
import random
import time
import sqlite3
import traceback
import sys
import requests
from bs4 import BeautifulSoup
import datetime
from test import get_not_date


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



def get_data(res_id, url):
    headers = {
        "user - agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / "
                        "110.0.0.0 Safari / 537.36 "
    }
    pagination = 1
    while requests.get(url + f'/{pagination}', headers):

        req = requests.get(url + f'/{pagination}', headers)
        folder_name = f"data/data_{pagination}"

        if os.path.exists(folder_name):
            print("The folder already exist")
        else:
            os.mkdir(folder_name)

        with open(f"{folder_name}/projects_{pagination}.html", "w", encoding="utf-8") as file:
            file.write(req.text)

        with open(f"{folder_name}/projects_{pagination}.html", encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        articles = soup.find_all("article", class_="block-infinite__item-content")
        project_urls = []
        for article in articles:
            project_url = article.find("a").get("href")
            project_urls.append(project_url)

        for project_url in project_urls:
            req = requests.get(project_url, headers)
            project_name = project_url.split("/")[-2]

            with open(f"{folder_name}/{project_name}.html", "w", encoding="utf-8") as file:
                file.write(req.text)

            with open(f"{folder_name}/{project_name}.html", encoding="utf-8") as file:
                src = file.read()

            soup = BeautifulSoup(src, "lxml")
            project_data = soup.find("div", class_="page__container")
            try:
                project_headline = project_data.find('h1', class_="main-headline js-main-headline").text
            except:
                project_headline = "No project headline"
            try:
                project_date = project_data.find("div", class_="layout-content-type-page__wrapper-block").find(
                    "time").text.strip()
            except:
                project_date = "No project date"

            project_content = ""
            try:

                project_paragraphs = project_data.find("div", class_="formatted-body io-article-body").find_all("p")
                for paragraph in project_paragraphs:
                    project_content += paragraph.text
                project_content = project_content.replace(f"Оригинал статьи: {project_url}", "").strip()
            except:
                project_content = "No content"

            insert_to_items_db(res_id=res_id, project_url=project_url, project_headline=project_headline,
                               project_content=project_content, project_date=project_date)



        print(f"Page #{pagination}")
        # Так как при скролле сайта, новостей становиться больше я здесь сделал break (т.к. очень долго ждать)
        # Но можете закоментировать, если нужно все проверить!
        # if pagination == 5:
        #     break
        pagination += 1
        time.sleep(random.randrange(2, 4))

    print(f'Number of pages {pagination}')




try:
    sqlite_connection = sqlite3.connect('sqlite_python.db')
    cursor = sqlite_connection.cursor()
    print("База данных подключена к SQLite")
    cursor.execute('SELECT * FROM resources;')
    resources = cursor.fetchall()
    print(resources)
    get_data(resources[0][0], resources[0][2])
except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)

finally:
    if (sqlite_connection):
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")

