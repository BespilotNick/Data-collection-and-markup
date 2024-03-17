import requests
from lxml import html
from pymongo import MongoClient
import time

url = 'https://worldathletics.org/records/toplists/sprints/60-metres/indoor/women/senior/2023?page=1'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36'}

def scrape_page(url, headers=headers):
    response = requests.get(url, headers=headers) 
        
    page1 = html.fromstring(response.content)
    rows = page1.xpath('//table[@class="records-table"]/tbody/tr')

    my_list = []
    for row in rows:
        every_row = row.xpath(".//td/text()")
        my_list.append({
            'Rank': every_row[0].strip(),
            'Mark': every_row[1].strip(),
            'Wind': every_row[2].strip() if every_row[2].strip() != "" else 0.0,
            'Competitior': row.xpath(".//td[4]/a/text()")[0].strip(),
            'DOB': every_row[5].strip(),
            'Nat': every_row[7].strip(),
            'Pos': every_row[8].strip(),
            'Venue': every_row[9].strip(),
            'Date': every_row[10].strip(),
            'Results Score': every_row[11].strip()
        })
    return my_list

def save_to_mongodb(list):
    client = MongoClient("mongodb://localhost:27017/")
    db = client['world_athletics']
    collection = db['60_metres_women']
    collection.insert_many(list)

def main_func():
    main_url = 'https://worldathletics.org/records/toplists/sprints/60-metres/indoor/women/senior/2023?page='
    for number in range(1,5):
        print(f'Page in progress: {number}')
        work_url = main_url + str(number)
        work_list = scrape_page(work_url)
        save_to_mongodb(work_list)
        time.sleep(3)

if __name__ == "__main__":
    main_func()