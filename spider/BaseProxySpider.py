# coding:utf-8


class BaseProxySpider(object):

    def getProxies(self):
        """
        返回代理的 json 结构
        :return:
        """
        raise NotImplementedError('subclasses of BaseCache must provide a getProxy() method')


