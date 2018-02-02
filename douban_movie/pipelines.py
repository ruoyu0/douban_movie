# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import conf
from common import mongo_client


class DoubanMoviePipeline(object):
    def open_spider(self, spider):
        self.coll_name = spider.name
        self.mongo_client = mongo_client.get_mongo_client()
        # self.mongo_coll = self.mongo_client[conf.mongo_dbname][self.coll_name]

    def process_item(self, item, spider):
        item_dict = dict(item)
        movie_country = item_dict.get("movie_country", "")
        # spider.logger.info("movie_country: {}".format(movie_country))
        if movie_country:
            insert_result = self.mongo_client[conf.mongo_dbname][movie_country].insert(item_dict)
            return "insert_data_id: {}".format(insert_result)
        return "no fount data!"
