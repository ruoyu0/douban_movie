#!/usr/bin/env python
# !encoding=utf-8
# author: zhuyuan

mongo_host = "127.0.0.1"
mongo_port = 27017
mongo_dbname = "douban_movie"

redis_host = "127.0.0.1"
redis_port = 6379
redis_dbnum = 5
redis_table = "douban_movie"

test_url = "https://movie.douban.com/subject/26799731/"

HEADERS = {
    "Connection": "keep-alive",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
}
