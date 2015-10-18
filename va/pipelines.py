# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from va.items import Video, Artist, Company, Genre
import dblite

class VaPipeline(object):
    def __init__(self):
        self.videos = None
        self.artists = None
        self.companies = None

    def open_spider(self, spider):
        self.videos = dblite.open(Video, 'sqlite://./db.sqlite3:videos', autocommit=True)
        self.artists = dblite.open(Artist, 'sqlite://./db.sqlite3:artists', autocommit=True)
        self.companies = dblite.open(Company, 'sqlite://./db.sqlite3:companies', autocommit=True)
        self.genres = dblite.open(Genre, 'sqlite://./db.sqlite3:genres', autocommit=True)

    def close_spider(self, spider):
        self.videos.commit()
        self.videos.close()

    def process_item(self, item, spider):
        if isinstance(item, Video):
            try:
                self.videos.put(item)
            except dblite.DuplicateItem:
                raise DropItem("Duplicate videos found")
        elif isinstance(item, Artist):
            try:
                self.artists.put(item)
            except dblite.DuplicateItem:
                raise DropItem("Duplicate artists found")
        elif isinstance(item, Company):
            try:
                self.companies.put(item)
            except dblite.DuplicateItem:
                raise DropItem("Duplicate companies found")
        elif isinstance(item, Genre):
            try:
                self.genres.put(item)
            except dblite.DuplicateItem:
                raise DropItem("Duplicate genres found")
        else:
            raise DropItem("Unkown item type ")

        return item
