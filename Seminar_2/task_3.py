from bs4 import BeautifulSoup
import requests
import urllib.parse
import pandas

url = 'https://www.boxofficemojo.com/intl/?ref_=bo_nb_hm_tab'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

table = soup.find('table', {'class': 'a-bordered'})
headers = [header.text.strip() for header in table.find_all('th') if header.text]

data = []
for row in table.find_all('tr'):
    rowdata = {}
    cells = row.find_all('td')
    if cells:
      # rowdata[headers[0]] = cells[0].find('a').text if cells[0].find('a') else ''
        rowdata[headers[0]] = cells[0].text if cells[0].find('a') else ''
        rowdata[headers[1]] = cells[1].text
        rowdata[headers[2]] = cells[2].text
        rowdata[headers[3]] = cells[3].text
        rowdata[headers[4]] = cells[4].text.strip()
        rowdata[headers[5]] = cells[5].text.replace('$', '')
        data.append(rowdata)

df = pandas.DataFrame(data)
print(df)
