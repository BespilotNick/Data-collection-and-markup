import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapy.loader import ItemLoader
from ..items import UnsplashItem
from itemloaders.processors import MapCompose
import requests
import os


class UnsplashSpider(CrawlSpider):
    name = "unsplash_spider"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com/"]

    rules = (
        Rule(LinkExtractor(restrict_xpaths=('//div[@class = "zmDAx"]/a')), callback="parse_item", follow=True),
        )

    def parse_item(self, response):

        loader = ItemLoader(item=UnsplashItem(), response=response)
        loader.default_input_processor = MapCompose(str.strip)

        loader.add_xpath('name', '//h1/text()')

        cat_list = []
        for i in range(1, len(response.xpath('//*[@id="app"]/div/div/div/div/div/div/div/div[@class = "VZRk3 rLPoM"]/a'))+1):
            cat_list.append(response.xpath(f'//*[@id="app"]/div/div/div/div/div/div/div/div[@class = "VZRk3 rLPoM"]/a[{i}]/text()').get())
        
        loader.add_value('categories', cat_list)

        image_link = response.xpath('//button/div/div[@class="MorZF"]/img/@src').getall()
        loader.add_value('image_urls', image_link)
        # Или так:
        # loader.add_xpath('image_urls', '//button/div/div[@class="MorZF"]/img/@src')
        
        pic = requests.get(image_link[0]).content
        pic_name = f'images/{response.xpath("//h1/text()").get()}.jpg'

        with open(pic_name, "wb") as img:
            img.write(pic)

        loc_path = os.path.abspath(pic_name)
        loader.add_value('local_path', loc_path)

        yield loader.load_item()
