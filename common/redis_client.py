#!/usr/bin/env python
# !encoding=utf-8
# author: zhuyuan

import conf
import redis

redis_client = None


def get_redis_client():
    # 全局唯一
    global redis_client
    if redis_client is None:
        redis_client = redis.StrictRedis(host=conf.redis_host, port=conf.redis_port, db=conf.redis_db)
    return redis_client

if __name__ == '__main__':
    redis_client = get_redis_client()
    print redis_client.hget(conf.redis_table, "http://www.baidu.com")

