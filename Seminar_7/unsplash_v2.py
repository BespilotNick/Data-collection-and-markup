import requests
import os
import shutil
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import json
import csv

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36'
main_page_url = "https://unsplash.com"
chrome_options = Options()
chrome_options.add_argument(f'user-agent={USER_AGENT}')
browser = webdriver.Chrome()

def main() -> None:
    pages_urls = getting_category_urls(main_page_url)
    category_names = getting_category_names(main_page_url)
    
    save_data_to_json(parse_category_page(category_names=category_names, category_urls=pages_urls))
    save_data_to_csv(parse_category_page(category_names=category_names, category_urls=pages_urls))


def getting_category_urls(main_page_url: str) -> list:
    cat_urls = []
    page = BeautifulSoup(requests.get(main_page_url).content, 'html.parser')
    categories = page.find("div", {'class': 'pRk2s'}).find_all('ul')
    unwanted = page.find("div", {'class': 'pRk2s'}).find('ul').find_all('li', {'class': 'jTN_l'})
    for row in categories:
        for el in row.find_all('li'):        
            if el in unwanted:
                continue
            else:
                cat_urls.append(urljoin(main_page_url, el.find('a').get('href')))
    return cat_urls


def getting_category_names(main_page_url: str) -> list:
    cat_names = []
    page = BeautifulSoup(requests.get(main_page_url).content, 'html.parser')
    categories = page.find("div", {'class': 'pRk2s'}).find_all('ul')
    unwanted = page.find("div", {'class': 'pRk2s'}).find('ul').find_all('li', {'class': 'jTN_l'})
    for row in categories:
        for el in row.find_all('li'):        
            if el in unwanted:
                continue
            else:
                cat_names.append(el.find('a').text)
    return cat_names


def parse_category_page(category_names: list, category_urls: list) -> dict:
    for indx, link in enumerate(category_urls):
        data_dict = {
            category_names[indx]: [parse_photo_page(p_url) for p_url in get_full_page(link)]
        }
    return data_dict


def get_full_page(url: str):
    try:
        browser.get(url)
        WebDriverWait(browser, 10).until(ec.presence_of_all_elements_located((By.TAG_NAME, 'body')))
        page_height = browser.execute_script("return document.documentElement.scrollHeight")

        PAUSE_TIME = 2
        time.sleep(PAUSE_TIME)

        SCROLL_PAUSE_TIME = 1
        last_height = page_height
        while True:
            browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = browser.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        cat_page = BeautifulSoup(requests.get(url).content, 'html.parser')

        links = []
        page_path = cat_page.find("div", {'class': 'ripi6'}).find_all('figure')
        for row in page_path:
            for el in row.find_all('a', {'itemprop':  "contentUrl"}):
                links.append(urljoin(url.split("/t")[0], el.get('href')))

    except Exception as E:
        print(f'Произошла ошибка, {E}')
    finally:
        browser.quit()
    return links


def parse_photo_page(url: str) -> dict:
    photo_page = requests.get(url)
    page = BeautifulSoup(photo_page.content, 'html.parser')
    name = page.find('h1').text
    sub_list = []
    subcategories = page.find("div", {"class": "MbPKr M5vdR"}).find_all("div", {"class": "VZRk3 rLPoM"})
    for sub in subcategories:
        for el in sub.find_all("a"):
            sub_list.append(el.get("title"))
    image_url = page.find_all("div", {"class": "MorZF"})[0].find("img").get("src")

    page_dict = {
        "Name": name,
        "Subcategories": sub_list,
        "Image_url": image_url,
        "Local_path": saving_image(image_url, name)
    }

    return page_dict


def saving_image(img_url: str, name: str) -> str:

    pic = requests.get(img_url).content
    pic_name = f'{name}.jpg'

    if not os.path.isdir("Unsplash_images"):
        os.mkdir("Unsplash_images")
    
    os.chdir("Unsplash_images")
    
    with open(f'{pic_name}', "wb") as img:
        img.write(pic)

    local_path = os.path.abspath(pic_name)

    os.chdir("..")

    return local_path


def save_data_to_json(data: dict) -> None:
    with open('Usplash_v2.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def save_data_to_csv(data: dict) -> None:
    with open("Unsplash_v2.csv", "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["quote", "author"])
        writer.writeheader()
        writer.writerows(data)


if __name__ == "__main__":
    main()