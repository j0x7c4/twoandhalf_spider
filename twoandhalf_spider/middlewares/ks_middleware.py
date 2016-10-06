# encoding=utf-8
import random
import json
from twoandhalf_spider.cookie_manager.ks_cookies import cookies
from twoandhalf_spider.user_agents import pc_agents

class PcUserAgentMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(pc_agents)
        request.headers["User-Agent"] = agent
        request.headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        request.headers["Accept-Encoding"] = "gzip, deflate, sdch, br"
        request.headers["Accept-Language"] = "en-US,en;q=0.8"
        request.headers["Connection"] = "keep-alive"
        request.headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"

class KsCookiesMiddleware(object):
    """ 换Cookie """

    def process_request(self, request, spider):
        cookie = random.choice(cookies)
        request.cookies = cookie

class BeforeStartDownloadMiddleware(object):

    def process_request(self, request, spider):
        print "before start to download"
        print request.headers
        print request.cookies