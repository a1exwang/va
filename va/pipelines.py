# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline
from va.items import *
import dblite

class VaPipeline(object):
    def __init__(self):
        self.videos = None
        self.artists = None
        self.companies = None
        self.genres = None

    def open_spider(self, spider):
        self.videos = dblite.open(Video, 'sqlite://./db.sqlite3:videos', autocommit=True)
        self.artists = dblite.open(Artist, 'sqlite://./db.sqlite3:artists', autocommit=True)
        self.companies = dblite.open(Company, 'sqlite://./db.sqlite3:companies', autocommit=True)
        self.genres = dblite.open(Genre, 'sqlite://./db.sqlite3:genres', autocommit=True)

    def close_spider(self, spider):
        self.videos.commit()
        self.videos.close()
        self.artists.commit()
        self.artists.close()
        self.companies.commit()
        self.companies.close()
        self.genres.commit()
        self.genres.close()

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
        elif isinstance(item, CoverPicture):
            pass
        #     try:
        #         pass
        #     except dblite.DuplicateItem:
        #         raise DropItem("Duplicate covor found")
        #else:
        #    raise DropItem("Unkown item type ")

        return item

class CoverFilePipeline(FilesPipeline):
    def __init__(self, store_uri):
        super(CoverFilePipeline, self).__init__(store_uri)
        self.covers = None

    def open_spider(self, spider):
        super(CoverFilePipeline, self).open_spider(spider)
        self.covers = dblite.open(CoverPicture, 'sqlite://./db.sqlite3:covers', autocommit=True)

    def close_spider(self, spider):
        super(CoverFilePipeline, self).close_spider(spider)
        self.covers.commit()
        self.covers.close()

    def get_media_requests(self, item, info):
        if isinstance(item, CoverPicture):
            yield scrapy.Request(item['file_url'])

    def item_completed(self, results, item, info):
        if isinstance(item, CoverPicture):
            result = results[0]
            if not result[0]:
                raise DropItem("Item contains no files")
            item['file_path'] = result[1]['path']
            try:
                self.covers.put(item)
            except:
                raise DropItem("Duplicate covor found")
            return item
        else:
            return None
