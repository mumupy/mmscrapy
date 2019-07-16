#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/16 20:13
# @Author  : ganliang
# @File    : SinaNewsSpider.py
# @Desc    : 新浪新闻爬虫程序
from scrapy import Request
from scrapy_redis import defaults
from scrapy_redis.spiders import RedisSpider


class SinaNewsSpider(RedisSpider):
    """
    采用redis分布式爬虫爬取绿盟漏洞数据
    """
    name = "news_loophole_spider"
    base_url = "http://hb.sina.com.cn/news/"
    allowed_domains = ["sina.com.cn"]

    # 分布式爬虫配置
    custom_settings = {
        "ITEM_PIPELINES": {
            'mmscrapy.pipelines.ConsolePipeline.ConsolePipeline': 300,
            'mmscrapy.pipelines.JsonFilePipeline.JsonFilePipeline': 302,
            'scrapy_redis.pipelines.RedisPipeline': 303,
        },
        "DOWNLOADER_MIDDLEWARES": {
            'mmscrapy.middlewares.MmscrapyDownloaderMiddleware': 543,
        },
        "SCHEDULER": "scrapy_redis.scheduler.Scheduler",
        "DUPEFILTER_CLASS": "scrapy_redis.dupefilter.RFPDupeFilter",
        "DUPEFILTER_DEBUG": True,
        "REDIS_START_URLS_KEY": defaults.START_URLS_KEY,
        "REDIS_PARAMS": {
            'host': '172.31.134.225',
            'port': '6379',
            'db': 15
        }
    }

    def __init__(self, *args, **kwargs):
        super(SinaNewsSpider, self).__init__()

    def make_requests_from_url(self, url):
        return Request(url, dont_filter=False, callback=self.parse)

    def parse(self, response):
        pass
