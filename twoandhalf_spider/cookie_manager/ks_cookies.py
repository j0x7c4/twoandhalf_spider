# encoding=utf-8
import json
import requests

def getCookies():
    """ 获取Cookies """
    cookies = []
    url = r'https://www.kickstarter.com/'
    session = requests.Session()
    r = session.get(url)
    jsonStr = r.content
    info = json.loads(jsonStr)
    if info["retcode"] == "0":
        print "Get Cookie Success!"
        cookie = session.cookies.get_dict()
        cookies.append(cookie)
    else:
        print "Failed!( Reason:%s )" % info['reason']
    return cookies


cookies = getCookies()
print "Get Cookies Finish!( Num:%d)" % len(cookies)