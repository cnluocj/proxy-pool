# coding:utf-8


import redis
import json
from spider.items import Proxy


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

    def getAll(self):
        return self.__connect.smembers(self.name)

    def getCount(self):
        return self.__connect.scard(self.name)

    def changeTable(self, name):
        self.name = name


if __name__ == '__main__':
    proxy = Proxy('127.0.0.1', '8080', u'透明', 'HTTPS')
    client = RedisClient('testpy', 'localhost', 6379)
    client.put(proxy)
    proxy = Proxy.to_object(client.get())
    print 'ip: {}, port: {}'.format(proxy.ip, proxy.port)

