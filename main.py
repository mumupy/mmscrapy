#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/10 17:29
# @Author  : ganliang
# @File    : main.py
# @Desc    : 程序入口
import os
import sys


def start_nodel_spider():
    os.system("scrapy crawl novel_spider -a category=finish -a cate=1234 -o novel1.json")


def start_image_spider():
    os.system("scrapy crawl image_spider")


def start_quotes_spider():
    os.system("scrapy crawl quotes_spider -o quotes.json -a tag=humor")


def start_author_spider():
    os.system("scrapy crawl author_spider -o author.json")


def start_xiaohuar_image_spider():
    # os.system("scrapy crawl xiaohuar_image_spider -a category=meinv -a type=image -s IMAGES_STORE=D:/data/mmscrapy/xiaohua/imagemeinv")
    # os.system("scrapy crawl xiaohuar_image_spider -a category=meinv -a type=info -s JSONFILE_BASEDIR=D:/data/mmscrapy/xiaohua/infomeinv")
    os.system(
        "scrapy crawl xiaohuar_image_spider -a category=hua -a type=image -s JSONFILE_BASEDIR=D:/data/mmscrapy/xiaohua/hua")


def start_cnvd_loophole_spider():
    """
    爬取cnvd漏洞
    :return:
    """
    os.system("scrapy crawl cnvd_loophole_spider -a typeId=29 -s JSONFILE_BASEDIR=D:/data/mmscrapy/cnvd")


def start_xicidaili_proxy_spider():
    """
    爬取cnvd漏洞
    :return:
    """
    os.system("scrapy crawl xicidaili_proxy_spider -a type=nn -s JSONFILE_BASEDIR=D:/data/mmscrapy/xicidaili")


if __name__ == "__main__":
    args = sys.argv[1:]

    args.append("xicidaili")

    if len(args) < 1:
        print ("usage [python main.py cnvd|xiaohuar|author ]")
        sys.exit(-1)

    spider = args[0]
    if spider == "nodel":
        start_nodel_spider()
    elif spider == "image":
        start_image_spider()
    elif spider == "quotes":
        start_quotes_spider()
    elif spider == "author":
        start_author_spider()
    elif spider == "xiaohuar":
        start_xiaohuar_image_spider()
    elif spider == "cnvd":
        start_cnvd_loophole_spider()
    elif spider == "xicidaili":
        start_xicidaili_proxy_spider()
