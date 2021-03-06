# coding:utf-8


import redis
import json
from spider.items import Proxy
from spider.spider_factory import ProxySpiderFactory
from db.db_factory import DBClientFactory


class RedisClient(object):

    def __init__(self, name, host='localhost', port=6379):
        self.name = name
        pool = redis.ConnectionPool(host=host, port=port, db=0)
        self.__connect = redis.StrictRedis(connection_pool=pool)

    def put(self, value):
        value = json.dumps(value.to_dict()) if type(value) == Proxy else value
        return self.__connect.rpush(self.name, value)

    def lpop(self):
        return self.__connect.lpop(self.name)

    def blpop(self):
        return self.__connect.blpop(self.name)

    def delete(self, value):
        self.__connect.srem(self.name, value)

    def get_all(self):
        return self.__connect.smembers(self.name)

    def get_count(self):
        return self.__connect.llen(self.name)

    def change_table(self, name):
        self.name = name


if __name__ == '__main__':
    # client = RedisClient(name='http_proxies', host='localhost', port=6379)
    client = DBClientFactory.create_active_db_client(RedisClient)
    for cls in ProxySpiderFactory.proxy_clss:
        spider = ProxySpiderFactory.create_spider(cls)
        proxies = spider.load_proxies()
        for proxy in proxies:
            client.put(proxy)
            proxy = Proxy.to_object(proxy)
            print 'ip: {}, port: {}, type: {}'.format(proxy.ip, proxy.port, proxy.type)

    # client = RedisClient()
    # print client.lpop()


