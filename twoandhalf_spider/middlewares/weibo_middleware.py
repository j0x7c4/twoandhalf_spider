# encoding=utf-8
from twoandhalf_spider.cookie_manager.weibo_cookies import WeiboCookieManager
from twoandhalf_spider.user_agents import mobile_agents
import random
import logging
import os
from scrapy.exceptions import IgnoreRequest
from scrapy.utils.response import response_status_message
from scrapy.downloadermiddlewares.retry import RetryMiddleware

logger = logging.getLogger(__name__)

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
    def __init__(self):
        self.cookieManager = WeiboCookieManager()

    def process_request(self, request, spider):
        key, request.cookies = self.cookieManager.pick()
        request.meta["accountText"] = key

    def process_response(self, request, response, spider):
        if response.status in [300, 301, 302, 303]:
            try:
                redirect_url = response.headers["location"]
                if "login.weibo" in redirect_url or "login.sina" in redirect_url:  # Cookie失效
                    logger.warning("One Cookie need to be updating...")
                    self.cookieManager.update_cookie(request.meta['accountText'])
                elif "weibo.cn/security" in redirect_url:  # 账号被限
                    logger.warning("One Account is locked! Remove it!")
                    self.cookieManager.remove_cookie(request.meta["accountText"])
                elif "weibo.cn/pub" in redirect_url:
                    logger.warning(
                        "Redirect to 'http://weibo.cn/pub'!( Account:%s )" % request.meta["accountText"].split("--")[0])
                reason = response_status_message(response.status)
                return self._retry(request, reason, spider) or response  # 重试
            except Exception, e:
                raise IgnoreRequest
        elif response.status in [403, 414]:
            logger.error("%s! Stopping..." % response.status)
            os.system("pause")
        else:
            return response