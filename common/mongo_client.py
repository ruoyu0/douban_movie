#!/usr/bin/env python
# !encoding=utf-8
# author: zhuyuan

import conf
from pymongo import MongoClient, InsertOne, ReplaceOne

mongo_client = None


def get_mongo_client():
    # 全局唯一
    global mongo_client
    if mongo_client is None:
        mongo_client = MongoClient(conf.mongo_host, conf.mongo_port, connect=False)
    return mongo_client


if __name__ == '__main__':
    mongo_client = get_mongo_client()
    mongo_db = mongo_client[conf.mongo_dbname]
    print mongo_db
    # mongo_coll = mongo_db["douban_movie"]


