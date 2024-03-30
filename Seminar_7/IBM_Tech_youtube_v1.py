# 
# Выберите веб-сайт, который содержит информацию, представляющую интерес для извлечения данных. Это может быть новостной сайт, 
# платформа для электронной коммерции или любой другой сайт, который позволяет осуществлять скрейпинг (убедитесь в соблюдении условий обслуживания сайта).
# Используя Selenium, напишите сценарий для автоматизации процесса перехода на нужную страницу сайта.
# Определите элементы HTML, содержащие информацию, которую вы хотите извлечь (например, заголовки статей, названия продуктов, цены и т.д.).
# Используйте BeautifulSoup для парсинга содержимого HTML и извлечения нужной информации из идентифицированных элементов.
# Обработайте любые ошибки или исключения, которые могут возникнуть в процессе скрейпинга.
# Протестируйте свой скрипт на различных сценариях, чтобы убедиться, что он точно извлекает нужные данные.
# Предоставьте ваш Python-скрипт вместе с кратким отчетом (не более 1 страницы), который включает следующее: URL сайта. Укажите URL сайта, 
# который вы выбрали для анализа. Описание. Предоставьте краткое описание информации, которую вы хотели извлечь из сайта. 
# Подход. Объясните подход, который вы использовали для навигации по сайту, определения соответствующих элементов и извлечения нужных данных. 
# Трудности. Опишите все проблемы и препятствия, с которыми вы столкнулись в ходе реализации проекта, и как вы их преодолели. 
# Результаты. Включите образец извлеченных данных в выбранном вами структурированном формате (например, CSV или JSON). 
# Примечание: Обязательно соблюдайте условия обслуживания сайта и избегайте чрезмерного скрейпинга, который может нарушить нормальную работу сайта.



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup as bs
import time
import json

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36'
url = 'https://www.youtube.com/@IBMTechnology/videos'

chrome_options = Options()
chrome_options.add_argument(f'user-agent={USER_AGENT}')
browser = webdriver.Chrome()
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

    video_titles_xpath = '//*[@id="video-title"]'
    metadata_views_xpath = '//*[@id="metadata-line"]/span[1]'
    metadata_published_xpath = '//*[@id="metadata-line"]/span[2]'

    video_titles = browser.find_elements(By.XPATH, video_titles_xpath)
    metadata_views = browser.find_elements(By.XPATH, metadata_views_xpath)
    metadata_published = browser.find_elements(By.XPATH, metadata_published_xpath)

    video_data = {}

    for i in range(len(video_titles)):
        title = video_titles[i].text
        views = metadata_views[i].text
        published = metadata_published[i].text

        video_data[title] = {"views": views, "published": published}

        with open('IBMTech_youtube.json', 'w', encoding='utf-8') as file:
            json.dump(video_data, file, ensure_ascii=False, indent=4)

except Exception as E:
    print(f'Произошла ошибка, {E}')
finally:
    browser.quit()

