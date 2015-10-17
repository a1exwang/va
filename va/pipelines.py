# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from va.items import VaItem
import dblite

class VaPipeline(object):
    def __init__(self):
        self.ds = None

    def open_spider(self, spider):
        self.ds = dblite.open(VaItem, 'sqlite://./db.sqlite3:items', autocommit=True)

    def close_spider(self, spider):
        self.ds.commit()
        self.ds.close()

    def process_item(self, item, spider):
        if isinstance(item, VaItem):
            try:
                self.ds.put(item)
            except dblite.DuplicateItem:
                raise DropItem("Duplicate item found")
        else:
            raise DropItem("Unkown item type ")

        return item
