# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Video(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field()
    designation = scrapy.Field()
    description = scrapy.Field()
    video_length = scrapy.Field()
    distribution_date = scrapy.Field()
    cover_path = scrapy.Field()
    stars_text = scrapy.Field()
    genres_text = scrapy.Field()

class Artist(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()

class Company(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()

class Genre(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()

