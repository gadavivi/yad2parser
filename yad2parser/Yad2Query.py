#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from PageCrawler import PageCrawler
import CrawlerExceptions
import time
from config import SLEEP

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def convert_to_int(num):
    try:
        return int(num)
    except Exception:
        return -1

class Yad2Crawler(PageCrawler):
    @staticmethod
    def _is_last_page(data):
        index = data.find(" ")
        if index != -1:
            if data[index + len("no_ads_title"):].find("no_ads_title") != -1:
                raise StopIteration()

    @staticmethod
    def _is_crawler_page(data):
        if "(bot,spider, crawler etc)" in data or "Incident Id" in data:
            log.info("yad2 crawler found - go to sleep")
            raise CrawlerExceptions.CrawlerExceptionProblem()


class Yad2Query(object):
    def __init__(self, base_url, search_query, params, coloms_dict, proxy_list = None, page_num = 1):
        self.base_url = base_url
        self.proxy_list = proxy_list
        self.page_crawler = Yad2Crawler(self.base_url + search_query, params, self.proxy_list, page_num=page_num)
        self.coloms_dict = coloms_dict



    @staticmethod
    def extract_items(page):
        id_list = re.findall('onclick="show_ad\((.*)\);', page)
        id_list = [id for id in id_list if "'platinum_'" not in id]
        id_list = [re.findall("(/.*php)','(.*?)','([a-z\d]+)'",id)[0] for id in id_list]
        id_list = set(id_list)
        for site, param,id in id_list:
            yield site, param, id

    @staticmethod
    def extract_item(data, coloms_dict):
        details_index_s = data.find('<table class="innerDetailsDataGrid"')
        details_index_e = details_index_s + data[details_index_s:].find('</table>') + len('</table>')
        details_text = data[details_index_s: details_index_e]
        price_index_s = data[details_index_e:].find('<table class="price"') + details_index_e
        price_index_e = price_index_s + data[price_index_s:].find('</table>') + len('</table>')
        price_text = data[price_index_s: price_index_e]
        price_text = price_text[price_text.find('<td>') + len('<td>'):]
        price_text = price_text[:price_text.find('<script')]
        price = int(re.findall('([,\d]+)',price_text)[0].replace(',',''))
        lines = details_text.split('<tr>')
        result = ["None"] * 6
        for line in lines[1:]:
            for colom in coloms_dict:
                if colom in line:
                    result[coloms_dict[colom]] = re.findall('<b>(.*)</b>', line.replace("\n", ""))[0].rstrip().lstrip()
                    break
        #city ,neighborhood, address, rooms, floor, size  = lines[1], lines[2], lines[4], lines[6], lines[7], lines[8]
        city, neighborhood, address, rooms, floor, size = tuple(result)
        if address == str(None):
            address = neighborhood
        return price, city ,neighborhood, address, convert_to_int(rooms), floor, convert_to_int(size)


    def get_items(self, exist_ids = list()):
        for page in self.page_crawler:
            for site, param, id in self.extract_items(page):
                try:
                    if id not in exist_ids:
                        time.sleep(SLEEP)
                        log.info("start extract id: %s" % id)
                        yield self.get_item(site, {param : id}) + (id,)
                    else:
                        log.info('id: %s already got inserted' % id)
                except Exception as ex:
                    log.error("failed to parse site=%s, id=%s" % (self.base_url + site, id))
                    log.exception(ex)


    def get_item(self, site, param):
        data, prepared_url = Yad2Crawler(self.base_url + site, param, self.proxy_list, page=None).get_page()
        return self.extract_item(data, self.coloms_dict) + (prepared_url, )