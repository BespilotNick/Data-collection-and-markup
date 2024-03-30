from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import json

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36'
url = 'https://www.youtube.com/@progliveru/videos'

chrome_options = Options()
chrome_options.add_argument(f'user-agent={USER_AGENT}')
browser = webdriver.Chrome()
browser.get(url)

WebDriverWait(browser, 10).until(ec.presence_of_all_elements_located((By.TAG_NAME, 'body')))

page_height = browser.execute_script("return document.documentElement.scrollHeight")
print(f'{page_height = }')

pause_time = 3
time.sleep(pause_time)

last_height = page_height
while True:
    browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(pause_time)
    new_page_height = page_height = browser.execute_script("return document.documentElement.scrollHeight")
    if new_page_height == last_height:
        break
    last_height = new_page_height
print(f'{last_height = }')

