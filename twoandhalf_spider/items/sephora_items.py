# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class CategoryItem(Item):
    """ category """
    name = Field()
    parent = Field()


class ProductItem(Item):
    """ product """
    name = Field()
    en_name = Field()
    brand = Field()
    category = Field()
    price = Field()
    img_sm_url = Field()
    img_lg_url = Field()
    brand_img_url = Field()
    info = Field()
    url = Field()
