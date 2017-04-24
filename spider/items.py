# coding:utf-8

import json


class Proxy(object):
    def __init__(self, ip='', port='', faceless='', ty=''):
        self.ip = ip
        self.port = port
        self.faceless = faceless
        self.type = ty
        self.valid_at = ''

    @property
    def faceless(self):
        return self._faceless

    @faceless.setter
    def faceless(self, value):
        if u'透明' in value:
            self._faceless = u'透明'
        elif u'高匿' in value:
            self._faceless = u'高匿'
        elif u'匿名' in value:
            self._faceless = u'匿名'
        else:
            self._faceless = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if 'HTTPS' in value or 'https' in value:
            self._type = 'HTTPS'
        elif 'HTTP' in value or 'http' in value:
            self._type = 'HTTP'
        else:
            self._type = value

    def to_dict(self):
        return {
            'ip': self.ip,
            'port': self.port,
            'faceless': self.faceless,
            'type': self.type,
            'valid_at': self.valid_at,
        }

    def to_string(self):
        return json.dumps(self.to_dict())

    @classmethod
    def to_object(cls, object_dict):
        if type(object_dict) != dict:
            object_dict = json.loads(object_dict)

        proxy = cls()
        proxy.ip = object_dict['ip']
        proxy.port = object_dict['port']
        proxy.faceless = object_dict['faceless']
        proxy.type = object_dict['type']
        proxy.valid_at = object_dict['valid_at']
        return proxy

if __name__ == '__main__':
    proxy = Proxy(faceless=u'透明', ty='https')
    # proxy.faceless = u'透明'
    # proxy.type = 'http'
    print proxy.to_string()