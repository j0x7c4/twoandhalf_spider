# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class ProfileItem(Item):
    """ 个人信息 """
    _id = Field()  # 用户ID
    nick_name = Field()  # 昵称
    gender = Field()  # 性别
    province = Field()  # 所在省
    city = Field()  # 所在城市
    signature = Field()  # 个性签名
    birthday = Field()  # 生日
    num_post = Field()  # 微博数
    num_follow = Field()  # 关注数
    num_fan = Field()  # 粉丝数
    url = Field()  # 首页链接


class PostItem(Item):
    """ 微博信息 """
    _id = Field()  # 用户ID-微博ID
    userid = Field()  # 用户ID
    body = Field()  # 微博内容
    pub_time = Field()  # 发表时间
    location = Field()  # 定位坐标
    source = Field()  # 发表工具/平台
    num_like = Field()  # 点赞数
    num_comment = Field()  # 评论数
    num_repost = Field()  # 转载数


class FollowItem(Item):
    """ 关注人列表 """
    _id = Field()  # 用户ID
    follow = Field()  # 关注


class FanItem(Item):
    """ 粉丝列表 """
    _id = Field()  # 用户ID
    fan = Field()  # 粉丝
