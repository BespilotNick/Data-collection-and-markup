from bs4 import BeautifulSoup
import requests
import urllib.parse

url = 'https://www.boxofficemojo.com/intl/?ref_=bo_nb_hm_tab'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

release_link = []
for link in soup.find_all('td', {'class': "a-text-left mojo-field-type-release mojo-cell-wide"}):
     atag = link.find('a')
     if atag:
          release_link.append(atag.get('href'))

url_join = [urllib.parse.urljoin('https://www.boxofficemojo.com', link) for link in release_link]
print(url_join)
