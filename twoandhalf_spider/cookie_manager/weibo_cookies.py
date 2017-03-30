# -*- coding: utf-8 -*-
import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging
import time
import os
import random
import sys
from twoandhalf_spider.account import myWeiBo
from twoandhalf_spider.cookie_manager.base_cookies import BaseCookieManager
import traceback

IDENTIFY = 1
dcap = dict(DesiredCapabilities.PHANTOMJS)  # PhantomJS需要使用老版手机的user-agent，不然验证码会无法通过
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"
)
logger = logging.getLogger(__name__)
logging.getLogger("selenium").setLevel(logging.WARNING)


class WeiboCookieManager(BaseCookieManager):
    def __init__(self):
        super(WeiboCookieManager, self).__init__()
        self.accounts = myWeiBo
        for weibo in self.accounts:
            cookie = self.get_cookie(weibo['no'], weibo['psw'])
            if len(cookie)>0:
                self.cookies[self.encode_key(weibo['no'], weibo['psw'])] = cookie
        self.cookieNum = len(self.cookies.items())
        logger.warning("The num of the cookies is %s" % self.cookieNum)
        if self.cookieNum == 0:
            logger.warning('Stopping...')
            sys.exit(1)

    def pick(self):
        k, v = random.choice(self.cookies.items())
        return k, v

    def encode_key(self, account, password):
        return account+"--"+password

    def decode_key(self, key):
        return (key.split("--")[0], key.split("--")[1])

    def get_cookie(self, account, password):
        """ 获取一个账号的Cookie """
        try:
            logger.info("*********")
            browser = webdriver.PhantomJS(desired_capabilities=dcap)
            browser.get("https://weibo.cn/login/")
            logger.info("##########%s" % browser.title)
            #time.sleep(1)

            failure = 0
            while u"微博" in browser.title and failure < 5:
                failure += 1
                logger.info("failure %d" % failure)
                browser.save_screenshot("/tmp/aa.png")
                username = browser.find_element_by_name("mobile")
                username.clear()
                username.send_keys(account)
                logger.info("send username %s" %account)
                psd = browser.find_element_by_xpath('//input[@type="password"]')
                psd.clear()
                psd.send_keys(password)
                logger.info("send password ***")
                try:
                    code = browser.find_element_by_name("code")
                    code.clear()
                    code_txt = raw_input("请查看路径下新生成的aa.png，然后输入验证码:")  # 手动输入验证码
                    code.send_keys(code_txt.decode('utf8'))
                except Exception, e:
                    traceback.print_exc()

                commit = browser.find_element_by_name("submit")
                commit.click()
                time.sleep(3)
                if u"我的首页" not in browser.title:
                    time.sleep(4)
                if u'未激活微博' in browser.page_source:
                    print '账号未开通微博'
                    return {}

            cookie = {}
            if u"我的首页" in browser.title:
                for elem in browser.get_cookies():
                    cookie[elem["name"]] = elem["value"]
                logger.warning("Get Cookie Success!( Account:%s )" % account)
            return cookie
        except Exception, e:
            logger.warning("Failed %s!" % account)
            traceback.print_exc()
            return {}
        finally:
            try:
                browser.quit()
            except Exception, e:
                traceback.print_exc()



    def update_cookie(self, key):
        """ 更新一个账号的Cookie """
        account, password = self.decode_key(key)
        cookie = self.getCookie(account, password)
        if len(cookie) > 0:
            logger.warning("The cookie of %s has been updated successfully!" % account)
            self.cookies[key] = cookie
        else:
            logger.warning("The cookie of %s updated failed! Remove it!" % key)
            self.remove_cookie(key)


    def remove_cookie(self, key):
        """ 删除某个账号的Cookie """
        del self.cookies[key]
        self.cookieNum = len(self.cookies)
        logger.warning("The num of the cookies left is %s" % self.cookieNum)
        if self.cookieNum == 0:
            logger.warning("Stopping...")
            sys.exit(1)