from bs4 import BeautifulSoup
import requests

url = 'https://www.boxofficemojo.com/intl/?ref_=bo_nb_hm_tab'

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

print(soup.prettify())