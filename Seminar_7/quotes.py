from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://quotes.toscrape.com")

quotes = []

while True:
    quote_elements = driver.find_element(By.XPATH, '//div[@class="quote"]')

    for quote_element in quote_elements:
        quote = quote_element.find_element(By.XPATH, '//span[@class="text"]')
        author = 

