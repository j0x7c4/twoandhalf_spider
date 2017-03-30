# encoding=utf-8
import datetime
import re

from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider

from twoandhalf_spider.items.weibo_items import ProfileItem, PostItem, FollowItem, FanItem


class Spider(CrawlSpider):
    name = "weibo"
    host = "http://weibo.cn"
    start_urls = [
        5032401317
        # 5235640836, 5676304901, 5871897095, 2139359753, 5579672076, 2517436943, 5778999829, 5780802073, 2159807003,
        # 1756807885, 3378940452, 5762793904, 1885080105, 5778836010, 5722737202, 3105589817, 5882481217, 5831264835,
        # 2717354573, 3637185102, 1934363217, 5336500817, 1431308884, 5818747476, 5073111647, 5398825573, 2501511785,
    ]
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "twoandhalf_spider.middlewares.weibo_middleware.MobileUserAgentMiddleware": 401,
            "twoandhalf_spider.middlewares.weibo_middleware.WeiboCookiesMiddleware": 402,
        }
    }

    p_url_follows = "http://weibo.cn/%s/follow"
    p_url_fans = "http://weibo.cn/%s/fans"
    p_url_posts = "http://weibo.cn/%s/profile?filter=1&page=1"
    p_url_profile0 = "http://weibo.cn/attgroup/opening?uid=%s"

    def start_requests(self):
        for id in self.start_urls:
            id = str(id)
            follows = []
            follow_items = FollowItem()
            follow_items["_id"] = id
            follow_items["follow"] = follows
            fans = []
            fan_items = FanItem()
            fan_items["_id"] = id
            fan_items["fan"] = fans

            url_follows = self.p_url_follows % id
            url_fans = self.p_url_fans % id
            url_posts = self.p_url_posts % id
            url_profile0 = self.p_url_profile0 % id
            #yield Request(url=url_follows, meta={"item": follow_items, "result": follows}, callback=self.parse3)  # 去爬关注人
            #yield Request(url=url_fans, meta={"item": fan_items, "result": fans}, callback=self.parse3)  # 去爬粉丝
            yield Request(url=url_profile0, meta={"id": id}, callback=self.parse0)  # 去爬个人信息
            yield Request(url=url_posts, meta={"id": id}, callback=self.parse2)  # 去爬微博


    def parse0(self, response):
        """ 抓取个人信息1 """
        profile_items = ProfileItem()
        selector = Selector(response)
        text0 = selector.xpath('body/div[@class="u"]/div[@class="tip2"]').extract_first()
        if text0:
            num_post = re.findall(u'\u5fae\u535a\[(\d+)\]', text0)  # 微博数
            num_follow = re.findall(u'\u5173\u6ce8\[(\d+)\]', text0)  # 关注数
            num_fan = re.findall(u'\u7c89\u4e1d\[(\d+)\]', text0)  # 粉丝数
            if num_post:
                profile_items["num_post"] = int(num_post[0])
            if num_follow:
                profile_items["num_follow"] = int(num_follow[0])
            if num_fan:
                profile_items["num_fan"] = int(num_fan[0])
            profile_items["_id"] = response.meta["id"]
            url_profile1 = "http://weibo.cn/%s/info" % response.meta["id"]
            yield Request(url=url_profile1, meta={"item": profile_items}, callback=self.parse1)

    def parse1(self, response):
        """ 抓取个人信息2 """
        profile_items = response.meta["item"]
        selector = Selector(response)
        text1 = ";".join(selector.xpath('body/div[@class="c"]/text()').extract())  # 获取标签里的所有text()
        nickname = re.findall(u'\u6635\u79f0[:|\uff1a](.*?);', text1)  # 昵称
        gender = re.findall(u'\u6027\u522b[:|\uff1a](.*?);', text1)  # 性别
        place = re.findall(u'\u5730\u533a[:|\uff1a](.*?);', text1)  # 地区（包括省份和城市）
        signature = re.findall(u'\u7b80\u4ecb[:|\uff1a](.*?);', text1)  # 个性签名
        birthday = re.findall(u'\u751f\u65e5[:|\uff1a](.*?);', text1)  # 生日
        #sexorientation = re.findall(u'\u6027\u53d6\u5411[:|\uff1a](.*?);', text1)  # 性取向
        #marriage = re.findall(u'\u611f\u60c5\u72b6\u51b5[:|\uff1a](.*?);', text1)  # 婚姻状况
        url = re.findall(u'\u4e92\u8054\u7f51[:|\uff1a](.*?);', text1)  # 首页链接

        if nickname:
            profile_items["nick_name"] = nickname[0]
        if gender:
            profile_items["gender"] = gender[0]
        if place:
            place = place[0].split(" ")
            profile_items["province"] = place[0]
            if len(place) > 1:
                profile_items["city"] = place[1]
        if signature:
            profile_items["signature"] = signature[0]
        if birthday:
            try:
                birthday = datetime.datetime.strptime(birthday[0], "%Y-%m-%d")
                profile_items["birthday"] = birthday - datetime.timedelta(hours=8)
            except Exception:
                pass
        # if sexorientation:
        #     if sexorientation[0] == gender[0]:
        #         informationItems["Sex_Orientation"] = "gay"
        #     else:
        #         informationItems["Sex_Orientation"] = "Heterosexual"
        # if marriage:
        #     informationItems["Marriage"] = marriage[0]
        if url:
            profile_items["url"] = url[0]
        yield profile_items

    def parse2(self, response):
        """ 抓取微博数据 """
        selector = Selector(response)
        posts = selector.xpath('body/div[@class="c" and @id]')
        for post in posts:
            post_items = PostItem()
            id = post.xpath('@id').extract_first()  # 微博ID
            content = post.xpath('div/span[@class="ctt"]/text()').extract_first()  # 微博内容
            cooridinates = post.xpath('div/a/@href').extract_first()  # 定位坐标
            like = re.findall(u'\u8d5e\[(\d+)\]', post.extract())  # 点赞数
            transfer = re.findall(u'\u8f6c\u53d1\[(\d+)\]', post.extract())  # 转载数
            comment = re.findall(u'\u8bc4\u8bba\[(\d+)\]', post.extract())  # 评论数
            others = post.xpath('div/span[@class="ct"]/text()').extract_first()  # 求时间和使用工具（手机或平台）

            post_items["userid"] = response.meta["id"]
            post_items["_id"] = response.meta["id"] + "-" + id
            if content:
                post_items["body"] = content.strip(u"[\u4f4d\u7f6e]")  # 去掉最后的"[位置]"
            if cooridinates:
                cooridinates = re.findall('center=([\d|.|,]+)', cooridinates)
                if cooridinates:
                    post_items["location"] = cooridinates[0]
            if like:
                post_items["num_like"] = int(like[0])
            if transfer:
                post_items["num_repost"] = int(transfer[0])
            if comment:
                post_items["num_comment"] = int(comment[0])
            if others:
                others = others.split(u"\u6765\u81ea")
                post_items["pub_time"] = others[0]
                if len(others) == 2:
                    post_items["source"] = others[1]
            yield post_items
        url_next = selector.xpath(
            u'body/div[@class="pa" and @id="pagelist"]/form/div/a[text()="\u4e0b\u9875"]/@href').extract()
        if url_next:
            yield Request(url=self.host + url_next[0], meta={"id": response.meta["id"]}, callback=self.parse2)

    def parse3(self, response):
        """ 抓取关注或粉丝 """
        items = response.meta["item"]
        selector = Selector(response)
        text2 = selector.xpath(
            u'body//table/tr/td/a[text()="\u5173\u6ce8\u4ed6" or text()="\u5173\u6ce8\u5979"]/@href').extract()
        for elem in text2:
            elem = re.findall('uid=(\d+)', elem)
            if elem:
                response.meta["result"].append(elem[0])
                id = int(elem[0])
                id = str(id)
                follows = []
                follow_items = FollowItem()
                follow_items["_id"] = id
                follow_items["follow"] = follows
                fans = []
                fan_items = FanItem()
                fan_items["_id"] = id
                fan_items["fan"] = fans

                url_follows = self.p_url_follows % id
                url_fans = self.p_url_fans % id
                url_posts = self.p_url_posts % id
                url_profile0 = self.p_url_profile0 % id
                yield Request(url=url_follows, meta={"item": follow_items, "result": follows},
                              callback=self.parse3)  # 去爬关注人
                yield Request(url=url_fans, meta={"item": fan_items, "result": fans}, callback=self.parse3)  # 去爬粉丝
                yield Request(url=url_profile0, meta={"id": id}, callback=self.parse0)  # 去爬个人信息
                yield Request(url=url_posts, meta={"id": id}, callback=self.parse2)  # 去爬微博

        url_next = selector.xpath(
            u'body//div[@class="pa" and @id="pagelist"]/form/div/a[text()="\u4e0b\u9875"]/@href').extract()
        if url_next:
            yield Request(url=self.host + url_next[0], meta={"item": items, "result": response.meta["result"]},
                          callback=self.parse3)
        else:  # 如果没有下一页即获取完毕
            yield items