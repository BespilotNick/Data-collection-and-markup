import scrapy


class CountriesSpider(scrapy.Spider):
    name = "countries"
    allowed_domains = ["traidingeconomics.com"]
    start_urls = ["https://traidingeconomics.com/country-list/inflation-rate?continent=world"]
 
    def parse(self, response):
        pass
