import scrapy


class BestsellersSpider(scrapy.Spider):
    name = "bestsellers_spider"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["http://en.wikipedia.org/"]

    def parse(self, response):
        pass
