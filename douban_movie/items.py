# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanMovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    douban_url = scrapy.Field()  # 豆瓣上该电影的url
    movie_name = scrapy.Field()  # 电影名称
    movie_rename = scrapy.Field()  # 电影又名
    movie_time = scrapy.Field()  # 电影时长
    movie_release_date = scrapy.Field()  # 上映日期
    movie_imdb_link = scrapy.Field()  # 电影IMDb链接
    movie_language = scrapy.Field()  # 电影语言
    movie_type = scrapy.Field()  # 电影类型
    movie_official_site = scrapy.Field()  # 电影官方网址
    movie_country = scrapy.Field()  # 导演所属国家
    movie_product_contries = scrapy.Field()  # 电影制作地区

    movie_douban_score = scrapy.Field()  # 豆瓣评分

    movie_synopsis = scrapy.Field()  # 电影剧情简介

    movie_director = scrapy.Field()  # 电影导演
    movie_screenwriter = scrapy.Field()  # 电影编剧
    movie_actor = scrapy.Field()  # 电影主要演员

    movie_duanping = scrapy.Field()  # 电影短评
    movie_yingping = scrapy.Field()  # 电影影评
    movie_awards = scrapy.Field()  # 电影获奖情况
