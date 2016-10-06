# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

from twoandhalf_spider.items.weibo_items import ProfileItem, PostItem, FollowItem, FanItem


class TwoandhalfSpiderPipeline(object):
    def process_item(self, item, spider):
        return item



class MongoDBPipleline(object):
    def __init__(self):
        clinet = pymongo.MongoClient("localhost", 27017)
        db = getattr(clinet, 'weibo')
        self.profile = getattr(db, "profile")
        self.post = getattr(db, "post")
        self.follow = getattr(db, "follow")
        self.fan = getattr(db, "fan")

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, ProfileItem):
            try:
                self.profile.insert(dict(item))
            except Exception:
                pass
        elif isinstance(item, PostItem):
            try:
                self.post.insert(dict(item))
            except Exception:
                pass
        elif isinstance(item, FollowItem):
            follow_items = dict(item)
            follows = follow_items.pop("follow")
            for i in range(len(follows)):
                follow_items[str(i + 1)] = follows[i]
            try:
                self.follow.insert(follow_items)
            except Exception:
                pass
        elif isinstance(item, FanItem):
            fan_items = dict(item)
            fans = fan_items.pop("fan")
            for i in range(len(fans)):
                fan_items[str(i + 1)] = fans[i]
            try:
                self.fan.insert(fan_items)
            except Exception:
                pass
        return item
