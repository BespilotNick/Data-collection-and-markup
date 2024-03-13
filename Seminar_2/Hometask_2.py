# Задание:
# Выполнить скрейпинг данных в веб-сайта http://books.toscrape.com/ и извлечь информацию о всех книгах на сайте во всех категориях: 
# название, цену, количество товара в наличии (In stock (19 available)) в формате integer, описание.
# Затем сохранить эту информацию в JSON-файле.



from bs4 import BeautifulSoup
import requests
import urllib.parse
import pandas
import json
import re

print(__name__)


def scraping_to_dict():
    book = []
    price = []
    amount = []
    description = []
    res_dict = {}

    url_m = 'http://books.toscrape.com'
    url_p = 'http://books.toscrape.com/catalogue/page-1.html'

    
    while True:
        page = requests.get(url_p)
        soup = BeautifulSoup(page.content, 'html.parser')
        next_page_link = soup.find('li', ('class', 'next'))
        result = soup.find_all('li', {'class': "col-xs-6 col-sm-4 col-md-3 col-lg-3"})

        url_2 = []
        for i in result:
            for link in i.find_all('div', {'class': 'image_container'}):
                url_2.append(link.find('a').get('href'))
        
        url_joined = []

        for link in url_2:
            url_joined.append(urllib.parse.urljoin(url_m, link))

        for i in url_joined:
            response = requests.get(i)

        soup = BeautifulSoup(response.content, 'html.parser')

        try:
            book.append(soup.find('div', {'class': 'col-sm-6 product_main'}).find('h1').text)
        except:
            book.append('')

        try:
            price.append(soup.find('div', {'class': 'col-sm-6 product_main'}).find('p', {'class': 'price_color'}).text)
        except:
            price.append('')

        # try:
        #     amount.append(soup.find('p', {'class': 'instock availability'}).text)
        # except:
        #     amount.append('')

        try:
            description.append(soup.find('article', {'class': 'prodct_page'}).find('p').text)
        except:
            description.append('')
        
            res_dict = {'Book': book, 'Price': price, 'Amount': amount, 'Description': description}

        if not next_page_link:
            break
        
        url_p = url_m + next_page_link['href']


    return res_dict


def save_to_json(dict, filename='books_scraped.json'):
    with open(filename, 'w') as f:
        json.dump(dict, f, indent=4)


def main():
    res_dict = scraping_to_dict()
    save_to_json(res_dict)


if __name__ == '__main__':
    main()
