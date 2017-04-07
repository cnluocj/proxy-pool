# coding:utf-8

from db.RedisClient import RedisClient
from ProxySpider import KuaidailiProxySpider


class ProxySpiderFactory(object):

    @classmethod
    def create_spider(cls, spider_class):
        """
        生成代理爬虫实例
        :return:
        """
        spider_ins = spider_class()
        return spider_ins


if __name__ == '__main__':
    spider = ProxySpiderFactory.create_spider(KuaidailiProxySpider)
    proxies = spider.loadProxies()
    for proxy in proxies:
        print proxy