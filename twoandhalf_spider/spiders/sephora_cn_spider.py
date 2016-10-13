# encoding=utf-8
import datetime
import re
import time
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider

from twoandhalf_spider.items.sephora_items import CategoryItem, ProductItem


class Spider(CrawlSpider):
    name = "sephora_cn"
    category_id_list = [1]
    page_range = range(1, 2)
    start_urls = ['http://www.sephora.cn']
    host = 'http://www.sephora.cn/'

    def parse(self, res):
        """
        select parse
        """
        selector = Selector(res)
        urls = selector.xpath('//a/@href').extract()
        for url in urls:
            if re.search("/category/([0-9a-zA-Z]|\-)+", url):
                yield Request(url=url, callback=self.parse_category)
            elif re.search("/product/([0-9a-zA-Z]|\-)+", url):
                yield Request(url=url, callback=self.parse_product)

    def parse_category(self, res):
        """
        parse category
        """
        if not re.search("/page/[0-9]+", res.url):
            d = datetime.datetime.fromtimestamp(time.time())
            selector = Selector(res)
            bread_crumb = selector.xpath('//div[@id="breadCrumb"]/div[@id="widget_breadcrumb"]/ul/a/text()').extract()
            bread_crumb.append(selector.xpath('//div[@id="breadCrumb"]/div[@id="widget_breadcrumb"]/ul/span/text()').extract_first())
            parent_category = None
            category = bread_crumb[-1]
            if len(bread_crumb)>2:
                parent_category = bread_crumb[-2]
            item = CategoryItem()
            item['name'] = category
            item['parent'] = parent_category
            item['ts'] = d.strftime("%Y-%m-%d %H:%M:%S")
            yield item
        for url in selector.xpath('//div[@id="main"]//a/@href').extract():
            if re.search("/product/([0-9a-zA-Z]|\-)+", url):
                yield Request(url=url, callback=self.parse_product)
        page_list = selector.xpath('//div[@class="pageList"]/span/a/@href').extract()
        if page_list and len(page_list) > 0:
            yield Request(url=page_list[-1], callback=self.parse_category)

    def parse_product(self, res):
        """parse product"""
        d = datetime.datetime.fromtimestamp(time.time())
        selector = Selector(res)
        bread_crumb = selector.xpath('//div[@id="breadCrumb"]/div[@id="widget_breadcrumb"]/ul/a/text()').extract()
        bread_crumb.append(
            selector.xpath('//div[@id="breadCrumb"]/div[@id="widget_breadcrumb"]/ul/span/text()').extract_first())

        name = bread_crumb[-1]
        brand = bread_crumb[-2]
        category = bread_crumb[-3]

        brand_img_url =selector.xpath('//div[@id="productDetail_up"]//a[@class="proBrandImg"]/img/@src').extract_first()
        en_name = selector.xpath('//div[@id="productDetail_up"]//p[@id="enName"]/text()').extract_first().strip()
        price = selector.xpath('//div[@id="productDetail_up"]//div[@class="promotion-container"]/p[@class="proPrice"]/span/text()').extract()[-1]
        info = selector.xpath('//div[@id="skuInfo"]/li/p/text()').extract()
        img_sm = selector.xpath('//div[@class="skuImgItems"]//img/@src').extract()
        img_lg = [x.replace("50x50", "350x350") for x in img_sm]

        item = ProductItem()
        item['name'] = name
        item['brand'] = brand
        item['category'] = category
        item['brand_img_url'] = brand_img_url
        item['en_name'] = en_name
        item['price'] = price
        item['img_sm_url'] = img_sm
        item['img_lg_url'] = img_lg
        item['info'] = info
        item['url'] = res.url
        item['ts'] = d.strftime("%Y-%m-%d %H:%M:%S")
        yield item
