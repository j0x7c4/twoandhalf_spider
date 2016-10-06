# encoding=utf-8
import random

from twoandhalf_spider.cookie_manager.weibo_cookies import cookies as webo_cookies
from twoandhalf_spider.cookie_manager.ks_cookies import cookies as ks_cookies
from user_agents import mobile_agents, pc_agents

class PcUserAgentMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(pc_agents)
        request.headers["User-Agent"] = agent
        request.headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        request.headers["Accept-Encoding"] = "gzip, deflate, sdch, br"
        request.headers["Accept-Language"] = "en-US,en;q=0.8"
        request.headers["Connection"] = "keep-alive"
        request.headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        print request.headers


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
        cookie = random.choice(webo_cookies)
        request.cookies = cookie


class KsCookiesMiddleware(object):
    """ 换Cookie """

    def process_request(self, request, spider):
        cookie = random.choice(ks_cookies)
        request.cookies = cookie