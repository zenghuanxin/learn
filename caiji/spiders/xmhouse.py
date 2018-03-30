# -*- coding: utf-8 -*-
import scrapy


class XmhouseSpider(scrapy.Spider):
    name = 'xmhouse'
    allowed_domains = ['m.xmhouse.com']
    start_urls = ['http://m.xmhouse.com/house/xf_psalev2.aspx?siteid=1&lptype=1']

    def parse(self, response):
        pass
