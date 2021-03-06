# coding:utf-8


import json
import threading
from db.db_factory import DBClientFactory
from db.db_clients import RedisClient
from spider.spider_factory import ProxySpiderFactory
from spider.items import Proxy


class ProxyGetter(object):

    def __init__(self, db_client_class=RedisClient):
        self.http_db_client = DBClientFactory.create_active_db_client(db_client_class)
        self.https_db_client = DBClientFactory.create_active_db_client(db_client_class, protocol='HTTPS')
        self.wait_db_client = DBClientFactory.create_wait_validate_db_client(db_client_class)

    def get(self, protocol='HTTP'):
        """
        如果能获取代理则返回代理,否则返回 False
        :return:
        """
        if protocol == 'HTTPS':
            db_client = self.https_db_client
        else:
            db_client = self.http_db_client
        proxy_count = db_client.get_count()
        wait_proxy_count = self.wait_db_client.get_count()
        # 如果可用代理数少于10,并且没有等待验证的代理,那么就重新爬取代理
        if proxy_count < 10 and not wait_proxy_count:
            self.__crawl_proxy()

        proxy_json = db_client.lpop()
        if not proxy_json:
            return False
        # 用过一次之后又回到验证列表
        self.wait_db_client.put(proxy_json)
        proxy = Proxy.to_object(proxy_json)
        return proxy

    def __crawl_proxy(self):
        ProxyCrawler(self.wait_db_client).start()


class ProxyCrawler(threading.Thread):

    def __init__(self, db_client):
        super(ProxyCrawler, self).__init__()
        self.db_client = db_client

    def run(self):
        for cl in ProxySpiderFactory.proxy_clss:
            spider = ProxySpiderFactory.create_spider(cl)
            proxies = spider.load_proxies()
            for proxy in proxies:
                self.db_client.put(proxy)


if __name__ == '__main__':
    getter = ProxyGetter()
    # for x in range(0, 100):
    #     print json.dumps(getter.get())
    getter.get()
