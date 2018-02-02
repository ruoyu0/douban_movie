#!/usr/bin/env python
# !encoding=utf-8
# author: zhuyuan

import time
import conf
import urllib, requests
from common import order
from scrapy.selector import Selector

proxy_ip = None

def get_proxy_ip(spider):
    # 全局唯一
    global proxy_ip  # pylint: disable=global-statement
    if proxy_ip is None:
        proxy_ip = ProxyIp(spider)
    return proxy_ip


class ProxyIp(object):
    def __init__(self, spider):
        self.spider = spider
        self.ip_port = None
        self.last_ip = None
        self.time_record = None
        self.ip_port_use_count = 1
        self._test_url = conf.test_url
        self._select_new_proxy_ip()

    # 使用IP代理池的中间件
    def get_one_proxy_ip(self):
        if self.ip_port_use_count == 0 or time.time() > self.time_record + 60:
            self._select_new_proxy_ip()
        self.spider.logger.info("********** 第 {} 次使用该ip_port: {} **********".format(self.ip_port_use_count, self.ip_port))
        self.ip_port_use_count = (self.ip_port_use_count + 1) % 16  # 若超过20次，便换下一个可用ip的实现
        return self.ip_port

    def _select_new_proxy_ip(self):
        time_record = time.time()
        # 获取IP的API接口
        apiUrl = "http://dynamic.goubanjia.com/dynamic/get/{}.html".format(order.order)
        # 请求数据
        new_ip_port = urllib.urlopen(apiUrl).read().strip("\n")
        if new_ip_port == self.ip_port or new_ip_port == self.last_ip:
            self._select_new_proxy_ip()
        elif self._url_is_available(new_ip_port):
            self.ip_port = new_ip_port
            self.time_record = time_record
            self.ip_port_use_count = 1
            self.spider.logger.info("********** select new ip_port: {} **********".format(new_ip_port))
        else:
            self.last_ip = new_ip_port
            self._select_new_proxy_ip()

    def _url_is_available(self, ip_port):
        try:
            res = requests.get(url=self._test_url, headers=conf.HEADERS, timeout=10, proxies={"https": "http://" + ip_port})
            if res.status_code == 200:
                movie_name = Selector(response=res).xpath(".//div[@id='content']/h1/span[1]/text()").extract_first()
                if movie_name.strip() == u"请以你的名字呼唤我 Call Me by Your Name":
                    return True
        except:
            self.spider.logger.exception("url_test error:\n")
        self.spider.logger.warning("########## 被禁止的IP: {}".format(ip_port))
        return False
