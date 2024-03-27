# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UnsplashItem(scrapy.Item):
    name = scrapy.Field()
    image_url = scrapy.Field()
    images = scrapy.Field()
    categories = scrapy.Field()
    local_path = scrapy.Field()
