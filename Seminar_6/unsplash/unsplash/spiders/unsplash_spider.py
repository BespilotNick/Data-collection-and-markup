import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class UnsplashSpider(CrawlSpider):
    name = "unsplash_spider"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com/"]

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class = "zmDAx"]'), callback="parse_item", follow=True),
        )

    def parse_item(self, response):
        print(response.url)
