# -*- coding: utf-8 -*-
from scrapy import signals
import random
import pymysql
from settings import USER_AGENT_LIST
from get_ip import getip

class IPProxydownloadermiddleware(object):
    def process_request(self,request,spider):
        ua = random.choice(USER_AGENT_LIST)
        if ua:
            request.headers['User-Agent'] = ua
        while True:
            proxy = getip()
            if proxy:
                request.meta["proxy"] = 'http://'+proxy
                break
            else:
                continue

