# coding:utf-8


import redis
import json
from spider.items import Proxy
from spider.ProxySpiderFactory import ProxySpiderFactory


class RedisClient(object):

    def __init__(self, name, host, port):
        self.name = name
        self.__connect = redis.Redis(host=host, port=port, db=0)

    def get(self):
        return self.__connect.srandmember(name=self.name)

    def put(self, value):
        value = json.dumps(value.to_dict()) if type(value) == Proxy else value
        return self.__connect.sadd(self.name, value)

    def pop(self):
        return self.__connect.spop(self.name)

    def get_all(self):
        return self.__connect.smembers(self.name)

    def get_count(self):
        return self.__connect.scard(self.name)

    def change_table(self, name):
        self.name = name


if __name__ == '__main__':
    client = RedisClient(name='testpy', host='localhost', port=6379)
    for cls in ProxySpiderFactory.proxy_clss:
        spider = ProxySpiderFactory.create_spider(cls)
        proxies = spider.load_proxies()
        for proxy in proxies:
            client.put(proxy)
            print 'ip: {}, port: {}, type: {}'.format(proxy.ip, proxy.port, proxy.type)


