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


import requests
from lxml import html
from pymongo import MongoClient
import time
from random import uniform

url = 'https://finance.yahoo.com/screener/predefined/sec-ind_sec-largest-equities_healthcare/?count=100&offset=0'
url2 = 'https://finance.yahoo.com/screener/predefined/sec-ind_sec-largest-equities_healthcare/?count=100&offset=100'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36'}

# def scrape_page(url, headers=headers):
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
print(my_list)


# def save_to_mongodb(list):
#     client = MongoClient("mongodb://localhost:27017/")
#     db = client['world_athletics']
#     collection = db['60_metres_women']
#     collection.insert_many(list)

# def main_func():
#     main_url = 'https://finance.yahoo.com/screener/predefined/sec-ind_sec-largest-equities_healthcare/?count=100&offset='
#     for number in range(100, 501, 100):
#         print(f'Page in progress: {number}')
#         work_url = main_url + str(number)
#         work_list = scrape_page(work_url)
#         save_to_mongodb(work_list)
#         time.sleep(uniform(3,6))


# if __name__ == "__main__":
#     main()
