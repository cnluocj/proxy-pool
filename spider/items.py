# coding:utf-8

import json


class Proxy(object):
    def __init__(self, ip='', port='', faceless='', type=''):
        self.ip = ip
        self.port = port
        self.faceless = faceless
        self.type = type

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
        }

    @classmethod
    def to_object(cls, object_dict):
        if type(object_dict) != dict:
            object_dict = json.loads(object_dict)

        proxy = cls()
        proxy.ip = object_dict['ip']
        proxy.port = object_dict['port']
        proxy.faceless = object_dict['faceless']
        proxy.type = object_dict['type']
        return proxy
