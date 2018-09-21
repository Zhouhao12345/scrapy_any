# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WorkImageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    image_urls = scrapy.Field()
    image_paths = scrapy.Field()
    pass

class ProductionItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    image_url = scrapy.Field()
    price = scrapy.Field()
    status = scrapy.Field()
    keywords = scrapy.Field()
    pass
