#!/usr/bin/env python
# !encoding=utf-8
# author: zhuyuan

import sys

reload(sys)
sys.setdefaultencoding('utf8')

from scrapy import cmdline

cmdline.execute("scrapy crawl douban_movie_spider".split())
