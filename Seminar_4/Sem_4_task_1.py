import requests
from lxml import html

url = 'https://worldathletics.org/records/toplists/sprints/60-metres/indoor/women/senior/2023?page=1'

response = requests.get(url, 
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36'})

page = html.fromstring(response.content)
rows = page.xpath('//table[@class="records-table"]/tbody/tr')
first_row = rows[0].xpath('.//td/text()')
for el in first_row:
    print(el.strip())