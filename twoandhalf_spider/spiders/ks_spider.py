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
    p_url_list = "https://www.kickstarter.com/discover/advanced?category_id=%d&sort=popularity&page=%d"
    host = 'https://www.kickstarter.com'

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
        project_urls = selector.xpath('//div[@class="project-card-content"]//a/@href').extract()
        for project_url in project_urls:
            project_url = self.host + project_url
            yield Request(url=project_url, callback=self.parse_project)

    def parse_project(self, res):
        """
        parse project
        :param res:
        :return:
        """
        project_url = res.url
        selector = Selector(res)
        backers_count = selector.xpath('//div[@id="backers_count"]/text()').extract_first()
        pledged = selector.xpath('//div[contains(@class,"stat-item")]//div[@class="js-pledged"]/text()').extract_first()
        project_title = selector.xpath('//div[contains(@class, "NS_projects__header")]//a/text()').extract_first()
        project_content = selector.xpath('//div[@class="NS_projects__description_section"]//div[contains(@class, "description-container")]//text()').extract()
        project_content = "".join([x.strip() for x in project_content])
        creator_name = selector.xpath('//div[@class="NS_projects__creator"]//h5/a/text()').extract_first()
        project_location_category = selector.xpath('//div[contains(@class, "NS_projects__category_location")]/a/text()').extract()
        project_location, project_tag = "", ""
        if project_location_category and len(project_location_category)>0:
            project_location = project_location_category[0]
        if project_location_category and len(project_location_category)>1:
            project_tag = project_location_category[1]

        item = ProjectItem()
        item["name"] = project_title.strip()
        item["content"] = project_content.strip()
        item["creator"] = creator_name.strip()
        item["location"] = project_location.strip()
        item["category_tag"] = project_tag.strip()
        item["backers_count"] = backers_count.strip()
        item["pledged"] = pledged.strip()
        item["url"] = project_url
        yield item
