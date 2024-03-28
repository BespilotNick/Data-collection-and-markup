# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UnsplashItem(scrapy.Item):
    name = scrapy.Field()
    categories = scrapy.Field()
    image_urls = scrapy.Field()
    local_path = scrapy.Field()
    images = scrapy.Field()
