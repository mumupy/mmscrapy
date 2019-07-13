#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/11 0:14
# @Author  : ganliang
# @File    : setup.py.py
# @Desc    : 安装包

from setuptools import setup, find_packages

setup(
    name='mmscrapy',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = mmscrapy.settings']}
)
