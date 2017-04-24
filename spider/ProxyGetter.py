# coding:utf-8


import json
from db.DBClientFactory import DBClientFactory
from db.RedisClient import RedisClient
from spider.ProxySpiderFactory import ProxySpiderFactory
from spider.items import Proxy
from spider.ProxyValidator import ProxyValidator


class ProxyGetter(object):

    def __init__(self, db_client_class=RedisClient):
        self.db_client = DBClientFactory.create_active_db_client(db_client_class)
        self.wait_db_client = DBClientFactory.create_wait_validate_db_client(db_client_class)

    def get(self):
        """
        如果能获取代理则返回代理,否则返回 False
        :return:
        """
        proxy_count = self.db_client.get_count()
        wait_proxy_count = self.wait_db_client.get_count()
        if proxy_count < 10 and not wait_proxy_count:
            self.__crawl_proxy()

        proxy_json = self.db_client.lpop()
        if not proxy_json:
            return False
        self.db_client.put(proxy_json)
        proxy = Proxy.to_object(proxy_json)
        return proxy

    def __crawl_proxy(self):
        for cl in ProxySpiderFactory.proxy_clss:
            spider = ProxySpiderFactory.create_spider(cl)
            proxies = spider.load_proxies()
            for proxy in proxies:
                self.wait_db_client.put(proxy)


if __name__ == '__main__':
    getter = ProxyGetter()
    for x in range(0, 100):
        print json.dumps(getter.get())
