# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class VaItem(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    designation = scrapy.Field()
    description = scrapy.Field()
    artist = scrapy.Field()
    image = scrapy.Field()


