# coding:utf-8

import time
import json
import requests
from spider.BaseProxySpider import *
from spider.items import Proxy
from selenium import webdriver
from lxml import etree


class KuaidailiProxySpider(BaseProxySpider):
    """
    快代理爬虫
    """

    start_urls = map(lambda x: 'http://www.kuaidaili.com/proxylist/%s/' % str(x), [x for x in range(1, 11)])

    def load_proxies(self):
        for url in self.start_urls:
            driver = webdriver.PhantomJS()
            driver.get(url)
            time.sleep(0.5)
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


class XicidailiProxySpider(BaseProxySpider):
    """
    西刺代理爬虫
    """

    # 高匿一天有近10页,透明一天只有不到2页
    start_urls = ['http://www.xicidaili.com/nn/{}'.format(x) for x in range(1, 11)] + \
                 ['http://www.xicidaili.com/nt/{}'.format(x) for x in range(1, 3)]

    def load_proxies(self):
        for url in self.start_urls:
            content = requests.get(url, headers=self.headers).content
            tree = etree.HTML(content)
            for sel in tree.xpath('//table[@id="ip_list"]/tr'):
                proxy = Proxy()
                ip_html = sel.xpath('td[2]/text()')
                if (ip_html is None) or (len(ip_html) == 0):
                    continue
                proxy.ip = ip_html[0]
                proxy.port = sel.xpath('td[3]/text()')[0]
                proxy.faceless = sel.xpath('td[5]/text()')[0]
                proxy.type = sel.xpath('td[6]/text()')[0]
                yield json.dumps(proxy.to_dict())


class GoubanjiaProxySpider(BaseProxySpider):
    """
    www.goubanjia.com


<p style="display: none;">1</p><span>1</span><span style="display: inline-block;">7</span>
<div style="display: inline-block;"></div>
<div style="display: inline-block;"></div><span style="display: inline-block;">5.</span>
<div style="display: inline-block;">3</div><span style="display: inline-block;">0</span><span style="display: inline-block;">.</span>
<div style="display: inline-block;">12</div>
<p style="display: none;">4.</p><span>4.</span>
<p style="display: none;">12</p><span>12</span>
<p style="display: none;"></p><span></span><span style="display: inline-block;">8</span>:<span class="port GEA">8615</span>

    长这样...
    """

    # 国内匿名代理到270页之后就没验证时间了,国内透明代理一共就15页
    start_urls = ['http://www.goubanjia.com/free/gngn/index{}.shtml'.format(x) for x in range(1, 270)] + \
                 ['http://www.goubanjia.com/free/gnpt/index{}.shtml'.format(x) for x in range(1, 15)]

    def load_proxies(self):
        for url in self.start_urls:
            content = requests.get(url, headers=self.headers).content
            tree = etree.HTML(content)
            for sel in tree.xpath('//tr/td[@class="ip"]'):
                proxy = Proxy()
                proxy.port = sel.xpath('span[contains(@class, "port")]/text()')[0]
                ip_slices = sel.xpath('*[contains(@style, "display: inline-block;") or contains(@style, "") and not(contains(@class, "port"))]/text()')
                ip = ''
                for sli in ip_slices:
                    ip += sli
                proxy.ip = ip
                yield json.dumps(proxy.to_dict())


if __name__ == '__main__':
    # spider = KuaidailiProxySpider()
    # spider = XicidailiProxySpider()
    spider = GoubanjiaProxySpider()
    proxies = spider.load_proxies()
    for proxy in proxies:
        print proxy



