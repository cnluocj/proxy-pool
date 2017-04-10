# coding:utf-8


class BaseProxySpider(object):

    def load_proxies(self):
        """
        返回代理的 json 结构
        :return:
        """
        raise NotImplementedError('subclasses of BaseCache must provide a getProxy() method')


