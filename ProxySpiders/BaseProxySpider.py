# coding:utf-8


class Proxy(object):
    def __init__(self, ip='', port='', faceless='', type='', address=''):
        self.ip = ip
        self.port = port
        self.faceless = faceless
        self.type = type
        self.address = address

    def __setattr__(self, key, value):
        if 'faceless' == key:
            self.set_faceless(value);
        elif 'type' == key:
            self.set_type(value)
        else:
            self.__dict__[key] = value

    def set_faceless(self, value):
        if u'透明' in value:
            self.__dict__['faceless'] = u'透明'
        elif u'高匿' in value:
            self.__dict__['faceless'] = u'高匿'
        else:
            self.__dict__['faceless'] = value

    def set_type(self, value):
        if 'HTTPS' in value or 'https' in value:
            self.__dict__['type'] = 'HTTPS'
        elif 'HTTP' in value or 'http' in value:
            self.__dict__['type'] = 'HTTP'
        else:
            self.__dict__['type'] = value

    def to_dict(self):
        return {
            'ip': self.ip,
            'port': self.port,
            'faceless': self.faceless,
            'type': self.type,
            'address': self.address,
        }


class BaseProxySpider(object):

    def getProxies(self):
        """
        返回代理的 json 结构
        :return:
        """
        raise NotImplementedError('subclasses of BaseCache must provide a getProxy() method')


