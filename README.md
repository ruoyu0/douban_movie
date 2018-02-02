#### 爬虫 - 获取豆瓣电影数据
* 该爬虫使用scrapy框架
* 该爬虫使用了redis(docker) - 用作url判重
* 该爬虫使用了mongodb(docker) - 用作数据存储
* 该爬虫使用了请求延时的中间件(在./douban_movie/middlewares.py文件中)
* 该爬虫使用了动态代理
* ```./common/order.py```文件没有上传，内含动态代理的order值(该值能获取动态代理IP)
* 由于豆瓣网站的数据不需要动态加载, 该爬虫没有使用splash(docker)工具
* 在当前目录下，直接执行```./main.py```就能运行该爬虫
