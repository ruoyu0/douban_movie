#!/usr/bin/env python
# !encoding=utf-8
# author: zhuyuan

import conf
from common import mongo_client

if __name__ == '__main__':
    mongo_client = mongo_client.get_mongo_client()
    mongo_db = mongo_client[conf.mongo_dbname]
    collection_names =  mongo_db.collection_names()
    for collection_name in collection_names:
        query_result = mongo_db[collection_name].find({}).count()
        print u"{}: {}".format(collection_name, query_result)