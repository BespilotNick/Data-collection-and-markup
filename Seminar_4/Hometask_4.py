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
from random import randint

url = 'https://finance.yahoo.com/screener/predefined/sec-ind_sec-largest-equities_healthcare/?count=100&offset=0'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36'}

# def scrape_page(url, headers=headers):
response = requests.get(url, headers)

page = html.fromstring(response.content)
rows = page.xpath('//table[@class="W(100%)"]/tbody/tr')

my_list = []
for row in rows:
    every_row = row.xpath(".//td/text()")
    my_list.append({
        'Symbol': row.xpath(".//td[1]/a/text()")[0].strip(),
        'Name': every_row[0].strip(),
        # 'Price (Intrady)': every_row[2].strip() if every_row[2].strip() != "" else 0.0,
        # 'Change': row.xpath(".//td[4]/a/text()")[0].strip(),
        # '% Change': every_row[5].strip(),
        # 'Volume': every_row[7].strip(),
        'AVG Vol (3 month)': every_row[1].strip(),
        # 'Market Cap': every_row[9].strip(),
        'PE Ratio (TTM)': every_row[2].strip()
    })
print(my_list)



# if __name__ == "__main__":
#     main()
