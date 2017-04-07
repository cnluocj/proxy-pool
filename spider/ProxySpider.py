# coding:utf-8

import time
import json
from spider.BaseProxySpider import *
from spider.items import Proxy
from spider.ProxySpiderFactory import ProxySpiderFactory as psFactory
from selenium import webdriver
from lxml import etree


class KuaidailiProxySpider(BaseProxySpider):

    start_urls = map(lambda x: 'http://www.kuaidaili.com/proxylist/%s/' % str(x), [x for x in range(1, 11)])

    def load_proxies(self):
        for url in self.start_urls:
            driver = webdriver.PhantomJS()
            driver.get(url)
            time.sleep(3)
            js = 'console.log("")'
            driver.execute_script(js)
            resp = etree.HTML(driver.page_source)
            for sel in resp.xpath('//tbody/tr'):
                proxy = Proxy()
                proxy.ip = sel.xpath('td[@data-title="IP"]/text()')[0]
                proxy.port = sel.xpath('td[@data-title="PORT"]/text()')[0]
                proxy.faceless = sel.xpath('td[@data-title="%s"]/text()' % u'匿名度')[0]
                proxy.type = sel.xpath('td[@data-title="%s"]/text()' % u'类型')[0]
                yield json.dumps(proxy.to_dict())
            driver.close()


if __name__ == '__main__':
    # spider = KuaidailiProxySpider()
    # proxies = spider.loadProxies()
    spider = psFactory.create_spider(KuaidailiProxySpider)
    proxies = spider.load_proxies()
    for proxy in proxies:
        print proxy



