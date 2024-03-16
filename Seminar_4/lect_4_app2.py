import requests
from lxml import html

resp = requests.get(url = 'https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm', 
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36'})

tree = html.fromstring(html = resp.content)
print(resp.status_code)
