# coding:utf-8

from spider.ProxySpider import *


class ProxySpiderFactory(object):

    proxy_clss = [
        # KuaidailiProxySpider,
        XicidailiProxySpider,
        GoubanjiaProxySpider,
    ]

    @classmethod
    def create_spider(cls, spider_class):
        """
        生成代理爬虫实例
        :return:
        """
        spider_ins = spider_class()
        return spider_ins


if __name__ == '__main__':
    pass
    # spider = ProxySpiderFactory.create_spider(KuaidailiProxySpider)
    # proxies = spider.loadProxies()
    # for proxy in proxies:
    #     print proxy