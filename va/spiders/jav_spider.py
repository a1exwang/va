
import scrapy
from functools import *
from va.items import *

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
            content = video.xpath('a')[0]

            title = content.xpath("div[@class='title']/text()")[0].extract()
            link = response.urljoin(content.xpath('@href')[0].extract())

            print page
            yield scrapy.Request(link, partial(self.parse_inner, title=title))

            url = JavSpider.base_url + str(page+1)
            yield(scrapy.Request(url, callback=partial(self.parse, page=page+1)))

    def parse_inner(self, response, title):
        content = response.selector.xpath(
            "//body/div[@id='content']/div[@id='rightcolumn']")

        item = Video()

        code_tmp = content.xpath(
            "div[@class='post-body']/table/tr/td/div[@id='video_info']/div[@id='video_id']/table/tr/td/text()").extract()
        if len(code_tmp) > 1:
            code = code_tmp[1]
        else:
            return

        cover_path_tmp = content.xpath(
            "div[@class='post-body']/table/tr/td/div/img/@src").extract()
        cover_path = cover_path_tmp[0] if len(cover_path_tmp) > 0 else ""

        distribution_date_tmp = content.xpath(
            "div[@class='post-body']/table/tr/td/div[@id='video_info']/div[@id='video_date']/table/tr/td[@class='text']/text()").extract()
        distribution_date = distribution_date_tmp[0] if len(distribution_date_tmp) > 0 else ""

        length_tmp = content.xpath(
            "div[@class='post-body']/table/tr/td/div[@id='video_info']/div[@id='video_length']/table/tr/td/span/text()").extract()
        length = length_tmp[0] if len(length_tmp) > 0 else ""

        director_path_tmp = content.xpath(
            "div[@class='post-body']/table/tr/td/div[@id='video_info']/div[@id='video_director']/table/tr/td/span/a/@href").extract()
        director_path = director_path_tmp[0] if len(director_path_tmp)> 0 else ""

        maker_path_tmp = content.xpath(
            "div[@class='post-body']/table/tr/td/div[@id='video_info']/div[@id='video_maker']/table/tr/td/span/a/@href").extract()
        maker_path = maker_path_tmp[0] if len(maker_path_tmp) > 0 else ""

        distributor_path_tmp = content.xpath(
            "div[@class='post-body']/table/tr/td/div[@id='video_label']/div[@id='video_maker']/table/tr/td/span/a/@href").extract()
        distributor_path = distributor_path_tmp[0] if len(distributor_path_tmp) > 0 else ""

        genres = content.xpath(
            "div[@class='post-body']/table/tr/td/div[@id='video_info']/div[@id='video_genres']/table/tr/td/span/a")
        stars = content.xpath(
            "div[@class='post-body']/table/tr/td/div[@id='video_info']/div[@id='video_cast']/table/tr/td/span/span/a")

        genres_str = ""
        for genre in genres:
            genre_str = genre.xpath("text()").extract()[0]
            genres_str += genre_str + "  "

            genre_item = Genre()
            genre_item['name'] = genre_str
            yield genre_item

        stars_str = ""
        for star in stars:
            star_str= star.xpath("text()").extract()[0]
            stars_str += star_str + "  "

            star_item = Artist()
            star_item['name'] = star_str
            yield star_item

        print(code)

        item['title'] = title
        item['video_length'] = length
        item['designation'] = code
        item['cover_path'] = cover_path
        item['distribution_date'] = distribution_date
        item['stars_text'] = stars_str
        item['genres_text'] = genres_str
        yield item

