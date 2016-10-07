# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class ProjectItem(Item):
    """ ks project """
    name = Field()
    location = Field()
    category = Field()
    category_tag = Field()
    content = Field()
    creator = Field()
    backers_count = Field()
    pledged = Field()
    url = Field()
