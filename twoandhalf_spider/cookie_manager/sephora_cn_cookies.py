# encoding=utf-8
import json
import requests
import logging

logger = logging.getLogger('sephora_cn_cookies')

def getCookies():
    """ 获取Cookies """
    cookies = []
    url = r'http://www.sephora.cn/'
    headers = {}
    headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"
    headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    headers["Accept-Encoding"] = "gzip, deflate, sdch, br"
    headers["Accept-Language"] = "en-US,en;q=0.8"
    headers["Connection"] = "keep-alive"
    headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
    try:
        session = requests.Session()
        r = session.get(url, headers=headers)
        if session.cookies is not None and session.cookies.get_dict() is not None:
            logger.info("Get Cookie Success!")
            cookie = session.cookies.get_dict()
            cookies.append(cookie)
        else:
            logger.error("Get Cookie Failed!")
    except Exception, e:
        print e
    return cookies


cookies = getCookies()
logger.info("Get Cookies Finish!( Num:%d)" % len(cookies))