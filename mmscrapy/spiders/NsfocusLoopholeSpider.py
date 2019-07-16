#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/16 17:13
# @Author  : ganliang
# @File    : NsfocusLoopholeSpider.py
# @Desc    : nsfocus漏洞爬虫
from datetime import datetime

from lxml import etree
from scrapy import Request
from scrapy_redis import defaults
from scrapy_redis.spiders import RedisSpider

from mmscrapy.utils.ElementUtil import getElement


class NsfocusLoopholeSpider(RedisSpider):
    """
    采用redis分布式爬虫爬取绿盟漏洞数据
    """
    name = "nsfocus_loophole_spider"
    base_url = "http://www.nsfocus.net/index.php?act=sec_bug"
    allowed_domains = ['nsfocus.net']

    basic_settings = {
        "ITEM_PIPELINES": {
            'mmscrapy.pipelines.ConsolePipeline.ConsolePipeline': 300,
            'mmscrapy.pipelines.JsonFilePipeline.JsonFilePipeline': 302
        },
        "DOWNLOADER_MIDDLEWARES": {
            'mmscrapy.middlewares.MmscrapyDownloaderMiddleware': 543,
        },
        "DUPEFILTER_DEBUG": True,
    }
    # 分布式爬虫配置
    distribute_settings = {
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
    custom_settings = distribute_settings

    def __init__(self, *args, **kwargs):
        super(NsfocusLoopholeSpider, self).__init__()

    # def start_requests(self):
    #     yield Request(self.base_url, dont_filter=False, callback=self.parse)

    def make_requests_from_url(self, url):
        return Request(url, dont_filter=False, callback=self.parse)

    def parse(self, response):
        # 漏洞列表
        nsfocus_loopholes = response.css("ul.vul_list li a::attr(href)").getall()
        for nsfocus_loophole in nsfocus_loopholes:
            yield response.follow(nsfocus_loophole, dont_filter=False, callback=self.parse_nsfocus_loophole,
                                  priority=10)

        # 漏洞分页
        nsfocus_pages = response.css("div.page a::attr(href)").getall()
        for nsfocus_page in nsfocus_pages:
            yield response.follow(nsfocus_page, dont_filter=False, callback=self.parse, priority=20)

    def parse_nsfocus_loophole(self, response):
        result = {}
        res_html = etree.HTML(response.body)
        loophole_title = getElement(res_html, "//div[@class='title']/text()")
        result.setdefault("loophole_title", loophole_title)

        vulbar_content_element = res_html.xpath("//div[@class='vulbar']")[0]

        title = getElement(vulbar_content_element, "//div[@align='center']/b/text()")

        result.setdefault("title", title)

        refect_product = getElement(vulbar_content_element, "//blockquote/text()")
        result.setdefault("refect_product", str(refect_product))

        links = vulbar_content_element.xpath("a/@href")
        cve_link, vender_link, advisory_link = None, None, None
        if len(links) == 3:
            cve_link, vender_link, advisory_link = links
        elif len(links) == 2:
            cve_link, advisory_link = links
        elif len(links) == 1:
            cve_link = links
        cve_id = getElement(vulbar_content_element, "a/text()")
        result.setdefault("cve_link", cve_link)
        result.setdefault("cve_id", cve_id)
        result.setdefault("vender_link", vender_link)
        result.setdefault("advisory_link", advisory_link)

        main_content = etree.tostring(vulbar_content_element, encoding="utf-8")
        main_content = str(main_content)

        pubdate_index = main_content.find("发布日期")
        pubdate_before_index = main_content.find(">", pubdate_index) + 1
        pubdate_after_index = main_content.find("<", pubdate_before_index)
        pubdate = main_content[pubdate_before_index:pubdate_after_index]
        result.setdefault("pubdate", pubdate)

        update_index = main_content.find("更新日期")
        update_before_index = main_content.find(">", update_index) + 1
        update_after_index = main_content.find("<", update_before_index)
        update_date = main_content[update_before_index:update_after_index]
        result.setdefault("update_date", update_date)

        desc_index = main_content.find("描述：")
        desc_before_index = main_content.find("<br/>", desc_index) + 12
        desc_after_index = main_content.find("<br/>&#13;", desc_before_index)
        desc = main_content[desc_before_index:desc_after_index]

        desc_before_index = main_content.find("<br/>&#13;", desc_after_index) + 23
        desc_after_index = main_content.find("<br/>", desc_before_index)
        desc2 = main_content[desc_before_index:desc_after_index]
        result.setdefault("desc", desc + desc2)

        advisory_begin_index = main_content.rfind("厂商补丁：<br/>") + len("厂商补丁：<br/>") + 6
        advisory_end_index = main_content.rfind("&#13;")
        advisory = main_content[advisory_begin_index:advisory_end_index]
        result.setdefault("advisory", advisory)

        result.setdefault("url", response.request.url)
        result.setdefault("create_time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        yield result
