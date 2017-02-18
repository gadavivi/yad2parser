#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import datetime
logging.basicConfig()

USER_AGENT_HEADER = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
SLEEP = 7
NUM_OF_RETRY = 3

HTTP_PROXIS = [
    "http://82.81.213.153:8088",
    "http://81.218.174.175:8088",
    "http://80.179.196.126:8088",
    "http://31.168.230.194:8080",
    "http://81.218.131.96:8088",
    "http://31.168.202.59:8088",
    "http://213.57.89.62:18000",
    "http://31.168.80.106:8088",
    "http://213.57.89.97:18000",
    "http://79.177.100.251:8080",
    "http://82.80.144.132:8088",
    "http://82.81.213.153:8088",
    "http://82.80.63.94:8088",
    "http://62.219.118.198:8088"
]

HTTP_PROXIS = None
BASE_URL = ur'http://www.yad2.co.il'
RENT_PARAMS = (ur'/Nadlan/rent.php',{
                'multiSearch':1,
                'arrArea':r'9,11,3,4,71,10,98,12',
                'arrHomeTypeID':1,
                'fromRooms':3,
                'untilRooms':3,
                'fromPrice':3500,
                'untilPrice':4500,
                'PriceType':1,
                'Elevator':1,
                'PriceOnly':1
})


SALES_PARAMS = (ur'/Nadlan/sales.php', {
                'multiSearch':1,
                'arrArea':r'9,11,3,4,71,10,98,12',
                'arrHomeTypeID':1,
                'fromRooms':3,
                'untilRooms':3,
                'fromPrice':1000000,
                'untilPrice':1500000,
                'PriceType':1,
                'Elevator':1,
                'PriceOnly':1
},True)

RENT_COLOMS = {
    u'ישוב:':0,       # city
    u'<td>שכונה:</td>':1, # neighborhood
    u'כתובת:':2, # address
    u'חדרים:':3, # rooms
    u'קומה:':4,       # floor
    u'גודל במ"ר:':5 #size
}

KONES_PARAM = {
    'areaId':  3,
    'typeId': 1,
    'fromDate': (datetime.datetime.now() + datetime.timedelta(-30)).strftime("%d/%m/%Y"),
    'toDate': (datetime.datetime.now() + datetime.timedelta(60)).strftime("%d/%m/%Y"),
    'adv': 1
}