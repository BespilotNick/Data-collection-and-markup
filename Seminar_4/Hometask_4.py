# Задание.

# Выберите веб-сайт с табличными данными, который вас интересует.
# Напишите код Python, использующий библиотеку requests для отправки HTTP GET-запроса на сайт и получения HTML-содержимого страницы.
# Выполните парсинг содержимого HTML с помощью библиотеки lxml, чтобы извлечь данные из таблицы.
# Сохраните извлеченные данные в CSV-файл с помощью модуля csv.

# Ваш код должен включать следующее:
# Строку агента пользователя в заголовке HTTP-запроса, чтобы имитировать веб-браузер и избежать блокировки сервером.
# Выражения XPath для выбора элементов данных таблицы и извлечения их содержимого.
# Обработка ошибок для случаев, когда данные не имеют ожидаемого формата.
# Комментарии для объяснения цели и логики кода.
# Примечание: Пожалуйста, не забывайте соблюдать этические и юридические нормы при веб-скреппинге.


# Импортируем необходимые модули
import requests
from lxml import html
from pymongo import MongoClient
import csv
import time
from random import uniform

# url страницы которую будем использовать (первоначальная страница)
url = 'https://finance.yahoo.com/screener/predefined/sec-ind_sec-largest-equities_healthcare/?count=25&offset=25'

# Строка агента пользователя, чтобы имитировать веб-браузер и избежать блокировки сервером.
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36'}

# Функция для скрейпинга вэб-страницы и получения интересующей нас информации:
# функция получает в качестве аргумента url-адрес страницы и производит get-запрос.
# В дальнейшем, полученные данные используются для извлечения информации и записи её в список словарей.
# Функция возвращает список словарей

def scrape_page(url: str, headers: dict = headers) -> list:
    '''This function is getting information from the HTML document (web-page) 
    that is passed as an argument "url", save data as a list of dictionaries
    and returns that list'''

    response = requests.get(url, headers)

    page = html.fromstring(response.content)
    rows = page.xpath('//table[@class="W(100%)"]/tbody/tr')

    my_list = []
    for row in rows:
        my_list.append({
            'Symbol': row.xpath(".//td/a/text()")[0].strip(),
            'Name': row.xpath(".//td/text()")[0].strip(),
            'Price (Intrady)': row.xpath(".//td/fin-streamer/text()")[0].strip(),
            'Change': row.xpath(".//td[@aria-label='Change']/fin-streamer/span/text()")[0].strip(),
            '% Change': row.xpath(".//td[@aria-label='% Change']/fin-streamer/span/text()")[0].strip(),
            'Volume': row.xpath(".//td/fin-streamer/text()")[1].strip(),
            'AVG Vol (3 month)': row.xpath(".//td/text()")[1].strip(),
            'Market Cap': row.xpath(".//td/fin-streamer/text()")[2].strip(),
            'PE Ratio (TTM)': row.xpath(".//td/text()")[2].strip()
        })
    return my_list


# Функция для записи полученной информации в файл .csv

def write_to_csv(list: list) -> None:
    '''Creates csv-file and write "list" into it'''

    with open('Largest_Healthcare_Companies.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, 
                                fieldnames=list[0],
                                dialect='excel-tab')                                   
        writer.writeheader()        
        writer.writerows(list)


# Функция для записи полученной информации в базу данных СУБД Mongo DB

def save_to_mongodb(list: list) -> None:
    '''Function creates a new database and collection if they do not exist, or updates existing ones 
    and adds data from the argument "list" to them using the database management system - Mongo DB'''

    client = MongoClient("mongodb://localhost:27017/")
    db = client['yahoo_finance']
    collection = db['largest_healthcare_companies']
    collection.insert_many(list)


# Основная функция генерирующая url-адрес и вызывающая функции для скрейпинга вэб-страниц и записи данных в БД и файл .csv

def main_func() -> None:
    '''Generates url-address and calling functions to scrape web-pages and writing information to database and csv-file'''

    lower_limit = 0
    upper_limit = 537       # Цифра взята с сайта - общее количество строк (на 18.03.2024)
    step = 25

    full_list = []          # Дополнительный список необходим для избежания повторных записей заголовка 
                            #  в csv-файле при каждом вызове функции в цикле

    main_url = 'https://finance.yahoo.com/screener/predefined/sec-ind_sec-largest-equities_healthcare/?count=25&offset='
    for number in range(lower_limit, upper_limit, step):
        print(f'Page in progress: {int(number/25 + 1)}')
        work_url = main_url + str(number)
        work_list = scrape_page(work_url)
        save_to_mongodb(work_list)
        for dict in work_list:
            full_list.append(dict)
        time.sleep(uniform(3,6))

    write_to_csv(full_list)


if __name__ == "__main__":
    main_func()
