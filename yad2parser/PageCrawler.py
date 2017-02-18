#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import time
from abc import ABCMeta, abstractmethod
import requests
import CrawlerExceptions
import config

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

import os
prefs = {"download.default_directory" : "C:\\temp", "plugins.plugins_disabled": ["Adobe Flash Player"] }
chrome_options = Options()
chrome_options.add_experimental_option("prefs",prefs)

#driver = webdriver.Remote(command_executor="http://10.0.0.2:9515", desired_capabilities= chrome_options.to_capabilities())

def request_url_selenium(url, params, headers, proxies):
    prepared_url = requests.Request('GET',url, params=params).prepare().url
    log.debug("GET(selenium) url=%s" % prepared_url)
    driver = webdriver.Chrome(os.path.join(os.path.dirname(__file__), 'chrome2.exe'),
                              chrome_options=chrome_options)
    driver.get(prepared_url)
    page_source, url = driver.page_source, prepared_url
    driver.close()
    return page_source, url

def request_url(url, params, headers, proxies):
        proxy_dict = None
        if proxies != None:
            http_proxy = random.choice(proxies)
            proxy_dict = {
                "http": http_proxy
            }
        log.debug("GET url=%s, proxy=%s" % (url,str(proxy_dict)))
        req = requests.get(url, params=params, headers=headers, proxies=proxy_dict)
        return req.text

class PageCrawler(object):

    __metaclass__ = ABCMeta

    def __init__(self,url, params, proxy_list = None, page='Page', page_num = 1):
        self.url = url
        self.proxy_list = proxy_list
        self.headers = { 'User-Agent': config.USER_AGENT_HEADER}
        self.params = params
        self.page = page
        if self.page:
            self.page_num = page_num
            self.params['Page'] = 1

    def get_page(self, num_of_retry = config.NUM_OF_RETRY, time_to_sleep = config.SLEEP):
        for i in xrange(num_of_retry):
            try:
                log.debug("trying to get page: %s ,try: %d" % (str(self.params.get("Page","only-page")), i))
                data, prepared_url= request_url_selenium(self.url, self.params, self.headers, self.proxy_list)
                self._is_crawler_page(data)
                return data, prepared_url
            except (CrawlerExceptions.CrawlerExceptionProblem, requests.exceptions.ProxyError):
                #time.sleep(random.randint(1,time_to_sleep))
                time.sleep(time_to_sleep)
        raise CrawlerExceptions.NumOfRetryExceeded()

    @staticmethod
    @abstractmethod
    def _is_last_page(data):
        pass

    @staticmethod
    @abstractmethod
    def _is_crawler_page(data):
        pass

    def __iter__(self):
        if self.page:
            self.params[self.page] = self.page_num
            return self
        else:
            return CrawlerExceptions.NoPaginig("call to get_page method instead")

    def next(self):
        try:
            data, _ = self.get_page()
            self._is_last_page(data)
            self.params[self.page] += 1
            return data
        except CrawlerExceptions.NumOfRetryExceeded:
            raise StopIteration()