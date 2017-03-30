# -*- coding: utf-8 -*-
import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class BaseCookieManager(object):

    def __init__(self):
        self.cookies = {}