
import scrapy
from functools import *
from va.items import VaItem

class JavSpider(scrapy.Spider):
    name = "jav"
    allowed_domains = ["www.javlibrary.com"]
    base_url = "http://www.javlibrary.com/cn/vl_newrelease.php?mode=&page="
    start_urls = [
        base_url + "1"
    ]

    def parse(self, response, page=1):
        video_tags = response.selector.xpath(
            "/html/body/div[@id='content']/div[@id='rightcolumn']/div[@class='videothumblist']/div[@class='videos']/div")
        for video in video_tags:
            item = VaItem()
            content = video.xpath('a')[0]

            item['title'] = content.xpath("div[@class='title']/text()")[0].extract()
            item['link'] = response.urljoin(content.xpath('@href')[0].extract())
            item['designation'] = content.xpath("div[@class='id']/text()")[0].extract()
            item['image'] = content.xpath("img/@src")[0].extract()

            print page
            yield item

            url = JavSpider.base_url + str(page+1)
            yield(scrapy.Request(url, callback=partial(self.parse, page=page+1)))

