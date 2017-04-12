# coding:utf-8


import json
from spider.ProxySpiderFactory import ProxySpiderFactory
from spider.ProxyValidator import ProxyValidator
from spider.ProxyGetter import ProxyGetter
from db.RedisClient import RedisClient


def run():
    # 启动验证器
    validator = ProxyValidator()
    validator.start()

    getter = ProxyGetter()
    for x in range(0, 100):
        print x
        print json.dumps(getter.get())


if __name__ == '__main__':
    run()

