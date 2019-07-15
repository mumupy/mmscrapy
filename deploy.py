#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/14 0:08
# @Author  : ganliang
# @File    : deploy.py
# @Desc    : 自动化部署

import os
import sys
from sys import argv
import subprocess

def scrapyd_deploy():
    """
    scrapy打包运行
    :return:
    """
    # 打包
    os.popen("scrapyd-deploy.cmd --build-egg mmscrapy.egg")

    # 启动服务
    os.popen("scrapyd")

    # 将本地的egg包添加到scrapyd
    os.popen("scrapyd-deploy.cmd -a -p mmscrapy")


def spiderkeeper_deploy():
    """
    spiderkeeper运行
    :return:
    """
    os.system("spiderkeeper")


if __name__ == "__main__":
    args = argv[1:]
    if len(args) < 1:
        print ("usage python deploy.py scrapyd|spiderkeeper")
        sys.exit(-1)

    deploy_tool = args[0]

    if deploy_tool == "spiderkeeper":
        spiderkeeper_deploy()
    elif deploy_tool == "scrapyd":
        scrapyd_deploy()
    else:
        scrapyd_deploy()
