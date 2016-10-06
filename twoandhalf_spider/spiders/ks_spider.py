#
# encoding=utf-8

# encoding=utf-8
import datetime
import re

from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider

from twoandhalf_spider.items.ks_items import ProjectItem


class Spider(CrawlSpider):
    name = "ks"
    category_id_list = [1]
    page_range = range(1, 2)
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "twoandhalf_spider.middleware.MobileUserAgentMiddleware": 401,
            "twoandhalf_spider.middleware.KsCookiesMiddleware": 402,
        }
    }
    p_url_list = "https://www.kickstarter.com/discover/advanced?category_id=%d&sort=popularity&page=%d"
    p_url_projects = "https://www.kickstarter.com/projects/%s"

    def start_requests(self):
        for category_id in self.category_id_list:
            for page in self.page_range:
                url_list = self.p_url_list % (category_id, page)
                yield Request(url=url_list, callback=self.parse_list)

    def parse_list(self, res):
        """
        parse project list
        """
        selector = Selector(res)
        print selector.xpath('//a/text()').extract_first()
        project_urls = selector.xpath('//h6[@class="project-card-content"]/a/@href').extract()
        for project_url in project_urls:
            yield Request(url=project_url, callback=self.parse_project)

    def parse_project(self, res):
        """
        parse project
        :param res:
        :return:
        """
        selector = Selector(res)
        backers_count = selector.xpath('//div[@id="backers_count"]/text()').extract_first()
        pledged = selector.xpath('//div[@id=""]/div/text()').extract_first()
        project_title = selector.xpath('//div[@class="NS_projects__header"]//a/text()').extract_first()
        project_content = selector.xpath('//div[@class="NS_projects__description_section"]//text()').extract_first()

        creator_name = selector.xpath('//div[@class="NS_projects__creator"]')
        project_location_category = selector.xpath('//div[@class="NS_projects__category_location"]/a/text()').extract()
        project_location, project_tag = "", ""
        if project_location_category and len(project_location_category)>0:
            project_location = project_location_category[0]
        if project_location_category and len(project_location_category)>1:
            project_tag = project_location_category[1]

        item = ProjectItem()
        item.name = project_title
        item.content = project_content
        item.creator = creator_name
        item.location = project_location
        item.category_tag = project_tag
        item.backers_count = backers_count
        item.pledged = pledged
        yield item
