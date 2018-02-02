#!/usr/bin/env python
# !encoding=utf-8
# author: zhuyuan

import conf
from common import redis_client

if __name__ == '__main__':
    redis_client = redis_client.get_redis_client()
    url2mark = redis_client.hgetall(conf.redis_table)
    print "total url count:", len(url2mark)
    print "get url data count:", len([url for url, mark in url2mark.iteritems() if mark=='1'])
    print "un get url data count:", len([url for url, mark in url2mark.iteritems() if mark=='0'])