# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider

class DangSpider(RedisSpider):
    name = 'dang'
    allowed_domains = ['dangdang.com']
    # start_urls = ['http://dangdang.com/']
    redis_key = "dd"
    # def start_requests(self):
    #     url = "http://category.dangdang.com/?ref=www-0-C"
    #     yield scrapy.Request(url,callback=self.parse,dont_filter=True)

    def parse(self, response):
        hrefs = response.xpath("//div[@class = 'classify_kind']//a/@href").extract()
        for href in hrefs:
            yield scrapy.Request(href,callback=self.parse_nxt)

    def parse_nxt(self,response):
        li_list = response.xpath("//div[@id = 'search_nature_rg']//li")
        cat = response.xpath("//div[@class = 'select_frame']/a[@class = 'a diff']/text()").extract_first()
        for li in li_list:
            item = {}
            item["href"] = li.xpath("./a[1]/@href").extract_first()
            item["name"] = li.xpath("./a[1]/@title").extract_first()
            item["img"] = li.xpath("./a[1]/img/@src").extract_first()
            item["cat"] = cat
            item["price"] = li.xpath("./p[@class = 'price']/span/text()").extract_first().replace("\xa5","")
            item["book_detail"] = li.xpath("./p[@class = 'detail']/text()").extract_first()
            item["book_comments_num"] = li.xpath("./p[@class = 'search_star_line']//a/text()").extract_first()
            item["book_comments_href"] = li.xpath("./p[@class = 'search_star_line']//a/@href").extract_first()
            item["book_author"] = li.xpath("./p[@class = 'search_book_author']/span[1]/a/text()").extract_first()
            item["book_pub"] = li.xpath("./p[@class = 'search_book_author']/span[3]/a/text()").extract_first()
            item["book_pub_time"] = li.xpath("./p[@class = 'search_book_author']/span[2]/text()").extract_first()
            item["comments"] = li.xpath("./p[@class = 'star']/a/text()").extract_first()
            item["home"] = li.xpath("./p[@class = 'link']/a/text()").extract_first()
            item["home_link"] = li.xpath("./p[@class = 'link']/a/@href").extract_first()
            yield scrapy.Request(item["href"],callback=self.parse_details,meta={"item":item})
        nxt_tmp = response.xpath("//div[@class = 'paging']//li[@class = 'next']/a/@href").extract_first()
        if nxt_tmp is not None:
            nxt_page = "http://category.dangdang.com"+nxt_tmp
            print(nxt_page)
            yield scrapy.Request(nxt_page,callback=self.parse_nxt)

    def parse_details(self,response):
        item = response.meta["item"]
        item["book_more_info"] = response.xpath("//div[@class = 'pro_content']/ul[@class ='key clearfix']/li/text()").extract()
        item["book_jud"] = response.xpath("//div[@id = 'mediaFeedback']//span[@id = 'mediaFeedback-show']/text()").extract()
        item["book_abs_jud"] = response.xpath("//div[@id = 'abstract-show']/text()").extract()
        item["book_content"] = response.xpath("//div[@id = 'content']//span/text()").extract()
        item["all_more"] = response.xpath("//div[@id = 'detail_describe']//li/text()").extract()
        yield item






