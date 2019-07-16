#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/10 22:47
# @Author  : ganliang
# @File    : ConsolePipeline.py
# @Desc    : 控制台打印输出
import json
import logging


class ConsolePipeline(object):
    logger = logging.getLogger(__name__)

    def process_item(self, item, spider):
        try:
            itemdict = dict(item.iteritems())
            self.logger.info(json.dumps(itemdict))
        except Exception as ex:
            self.logger.error(ex)
        return item
