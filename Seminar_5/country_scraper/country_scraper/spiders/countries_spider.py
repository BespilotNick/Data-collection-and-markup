import scrapy


class CountriesSpiderSpider(scrapy.Spider):
    name = "countries_spider"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/List_of_sovereign_states"]

    def parse(self, response):
        for country in response.css('table.wikitable.sortable tbody tr'):
            name = country.css('td:nth-child(1) b a::text').get()
            if name:
                yield {'Country': name}
