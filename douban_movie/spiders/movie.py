#!/usr/bin/env python
# !encoding=utf-8
# author: zhuyuan

import re
import conf
import time
import json
import scrapy
from common import redis_client
from douban_movie.items import DoubanMovieItem


class MovieSpider(scrapy.Spider):
    start_urls = []
    name = "douban_movie_spider"
    redis_client = redis_client.get_redis_client()

    def start_requests(self):
        self.start_urls.append(conf.test_url)
        if self.redis_client.hgetall(conf.redis_table):
            self.start_urls += [url for url, mark in self.redis_client.hgetall(conf.redis_table).iteritems() if mark == '0']
        self.logger.info("********** start_urls:\n{}".format("\n".join("%4d %s" % (i, urls) for i, urls in enumerate(self.start_urls))))
        for one_url in self.start_urls:
            yield scrapy.Request(one_url, self.parse_one_movie_page, dont_filter=True)

    def parse_one_movie_page(self, response):
        data_mapping = {}
        data_mapping[u"豆瓣url"] = response.url
        movie_name = response.xpath(".//div[@id='content']/h1/span[1]/text()").extract_first()
        data_mapping[u"电影名称"] = movie_name.strip().split(" ")[0] if movie_name else ""

        info_html = response.xpath(".//div[@id='info']").extract_first()
        if info_html:
            data_mapping.update(self.parse_part_info(info_html))
            if data_mapping.get(u'制片国家/地区', ""):
                if isinstance(data_mapping[u'制片国家/地区'], list):
                    data_mapping[u"所属国家"] = data_mapping[u'制片国家/地区'][0].split(' ')[0]
                else:
                    data_mapping[u"所属国家"] = data_mapping[u'制片国家/地区'].strip().split(' ')[0]

        inte_selector_list = response.xpath(".//div[@id='interest_sectl']")
        if inte_selector_list:
            score = inte_selector_list[0].xpath(".//div[@class='rating_self clearfix']/strong/text()").extract_first()
            data_mapping[u"豆瓣评分"] = score.strip() if score else ""

        rela_selector_list = response.xpath(".//div[@class='related-info']")
        if rela_selector_list:
            synopsis = rela_selector_list[0].xpath(".//div[@class='indent']/span/text()").extract_first()
            data_mapping[u"剧情简介"] = synopsis.strip() if synopsis else ""

        mod_selector_list = response.xpath(".//div[@class='mod']")
        if mod_selector_list:
            data_mapping[u"获奖情况"] = self.parse_part_huojiang(mod_selector_list[0])

        comm_selector_list = response.xpath(".//div[@id='comments-section']")
        if comm_selector_list:
            data_mapping[u"电影短评"] = self.parse_part_duanping(comm_selector_list[0])

        review_selector_list = response.xpath(".//section[@class='reviews mod movie-content']")
        if review_selector_list:
            data_mapping[u"电影影评"] = self.parse_part_yingping(review_selector_list[0])

        # 获取新的电影的url
        new_movie_urls = re.findall(u"https://movie.douban.com/subject/\d*/", response.text)
        new_movie_urls = list(set(new_movie_urls))
        new_movie_urls = [one_url for one_url in new_movie_urls if not self.redis_client.hget(conf.redis_table, one_url)]
        self.logger.info("********** new_urls:\n{}".format("\n".join("%4d %s" % (i, urls) for i, urls in enumerate(new_movie_urls))))
        for one_url in new_movie_urls:
            self.redis_client.hset(conf.redis_table, one_url, 0)
            yield scrapy.Request(one_url, self.parse_one_movie_page, dont_filter=True)

        if data_mapping[u"电影名称"] and self.redis_client.hget(conf.redis_table, response.url) == '0':
            self.redis_client.hset(conf.redis_table, response.url, 1)
            yield self._data_to_item(data_mapping)

    def parse_part_info(self, info_html):
        data_mapping = {}
        html_list = info_html.split("<br>")
        for one_line in html_list:
            one_line = re.sub("<.*?>", "", one_line).strip()
            if one_line.find(": ") == -1:
                continue
            key, value = one_line.split(": ", 1)
            if value.find(" / ") != -1:
                value = [i.strip() for i in value.split(" / ") if i.strip()]
            data_mapping[key] = value
        return data_mapping

    def parse_part_huojiang(self, root_selector):
        # 获奖
        award_list = []
        ul_selector_list = root_selector.xpath(".//ul[@class='award']")

        for one_selector in ul_selector_list:
            award = one_selector.xpath(".//text()").extract()
            award = award if award else []
            award = " / ".join([i.strip() for i in award if i.strip()])
            award_list.append(award)
        return award_list

    def parse_part_duanping(self, root_selector):
        # 短评
        comment_list = []
        comment_item_list = root_selector.xpath(".//div[@class='comment-item']")
        for one_comment in comment_item_list:
            comment_user = one_comment.xpath(".//span[@class='comment-info']/a/text()").extract_first()
            comment_user = comment_user.strip() if comment_user else ""
            comment_time = one_comment.xpath(".//span[@class='comment-info']/span[@class='comment-time ']/text()").extract_first()
            comment_time = comment_time.strip() if comment_time else ""
            comment_star = one_comment.xpath(".//span[@class='comment-vote']/span[@class='votes']/text()").extract_first()
            comment_star = comment_star.strip() if comment_star else ""
            comment_text = one_comment.xpath(".//div[@class='comment']/p/text()").extract_first()
            comment_text = comment_text.strip() if comment_text else ""
            if comment_user:
                comment_data = "({} / {} / {}) - {}".format(comment_user, comment_star, comment_time, comment_text)
                comment_list.append(comment_data)
        return comment_list

    def parse_part_yingping(self, root_selector):
        # 影评
        comment_list = []
        comment_item_list = root_selector.xpath(".//div[@class='review-list  ']/div")
        for one_comment in comment_item_list:
            comment_user = one_comment.xpath(".//header[@class='main-hd']/a[@class='name']/text()").extract_first()
            comment_user = comment_user.strip() if comment_user else ""
            comment_time = one_comment.xpath(".//header[@class='main-hd']/span[@class='main-meta']/text()").extract_first()
            comment_time = comment_time.strip() if comment_time else ""
            comment_text = one_comment.xpath(".//div[@class='main-bd']/div[@class='review-short']/div[@class='short-content']/text()").extract()
            comment_text = "".join([i.strip().split("...")[0].strip() for i in comment_text if i.strip()])
            comment_data = "({} / {}) - {}".format(comment_user, comment_time, comment_text)
            comment_list.append(comment_data)
        return comment_list

    def _data_to_item(self, data_mapping):
        data_item = DoubanMovieItem(
            douban_url=data_mapping.get(u"豆瓣url", None),  # 豆瓣上该电影的url
            movie_name=data_mapping.get(u"电影名称", None),  # 电影名称
            movie_rename=data_mapping.get(u"又名", None),  # 电影又名
            movie_time=data_mapping.get(u'片长', None),  # 电影时长
            movie_release_date=data_mapping.get(u'上映日期', None),  # 上映日期
            movie_imdb_link=data_mapping.get(u'IMDb链接', None),  # 电影IMDb链接
            movie_language=data_mapping.get(u'语言', None),  # 电影语言
            movie_type=data_mapping.get(u'类型', None),  # 电影类型
            movie_official_site=data_mapping.get(u'官方网站', None),  # 电影官方网址
            movie_country=data_mapping.get(u'所属国家', None),  # 导演所属国家
            movie_product_contries=data_mapping.get(u'制片国家/地区', None),  # 电影制作地区

            movie_douban_score=data_mapping.get(u'豆瓣评分', None),  # 豆瓣评分

            movie_synopsis=data_mapping.get(u'剧情简介', None),  # 电影剧情简介

            movie_director=data_mapping.get(u'导演', None),  # 电影导演
            movie_screenwriter=data_mapping.get(u'编剧', None),  # 电影编剧
            movie_actor=data_mapping.get(u'主演', None),  # 电影主要演员

            movie_duanping=data_mapping.get(u'电影短评', None),  # 电影短评
            movie_yingping=data_mapping.get(u'电影影评', None),  # 电影影评
            movie_awards=data_mapping.get(u'获奖情况', None),  # 电影获奖情况
        )
        return data_item
