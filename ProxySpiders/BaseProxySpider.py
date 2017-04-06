# coding:utf-8


class Proxy(object):
    def __init__(self, ip='', port='', faceless='', type='', address=''):
        self.ip = ip
        self.port = port
        self.faceless = faceless
        self.type = type
        self.address = address

    def toDict(self):
        return {
            'ip': self.ip,
            'port': self.port,
            'faceless': self.faceless,
            'type': self.type,
            'address': self.address,
        }


class BaseProxySpider(object):

    def getProxys(self):
        """
        返回代理的 json 结构
        :return:
        """
        raise NotImplementedError('subclasses of BaseCache must provide a getProxy() method')


