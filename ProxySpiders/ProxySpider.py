# coding:utf-8

import time
import json
from BaseProxySpider import BaseProxySpider
from BaseProxySpider import Proxy
from selenium import webdriver
from lxml import etree


class KuaidailiProxySpider(BaseProxySpider):

    start_urls = map(lambda x: 'http://www.kuaidaili.com/proxylist/%s/' % str(x), [x for x in range(1, 11)])

    def getProxies(self):
        for url in self.start_urls:
            driver = webdriver.PhantomJS()
            driver.get(url)
            time.sleep(3)
            js = "console.log('')"
            driver.execute_script(js)
            resp = etree.HTML(driver.page_source)
            for sel in resp.xpath("//tbody/tr"):
                proxy = Proxy()
                proxy.ip = sel.xpath("td[@data-title='IP']/text()")[0]
                proxy.port = sel.xpath("td[@data-title='PORT']/text()")[0]
                proxy.faceless = sel.xpath("td[@data-title='%s']/text()" % u'匿名度')[0]
                proxy.type = sel.xpath("td[@data-title='%s']/text()" % u'类型')[0]
                proxy.address = sel.xpath("td[@data-title='%s']/text()" % u'位置')[0]
                yield json.dumps(proxy.to_dict())
            driver.close()


if __name__ == '__main__':
    spider = KuaidailiProxySpider()
    proxies = spider.getProxies()
    for proxy in proxies:
        print proxy



