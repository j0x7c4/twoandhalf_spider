# encoding=utf-8
import random

from twoandhalf_spider.cookie_manager.weibo_cookies import cookies
from twoandhalf_spider.user_agents import mobile_agents

class MobileUserAgentMiddleware(object):
    """ 换User-Agent """

    def process_request(self, request, spider):
        agent = random.choice(mobile_agents)
        request.headers["User-Agent"] = agent
        request.headers["Accept"] = "*/*"
        request.headers["Accept-Encoding"] = "gzip,deflate"
        request.headers["Accept-Language"] = "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4"
        request.headers["Connection"] = "keep-alive"
        request.headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"


class WeiboCookiesMiddleware(object):
    """ 换Cookie """

    def process_request(self, request, spider):
        cookie = random.choice(cookies)
        request.cookies = cookie
