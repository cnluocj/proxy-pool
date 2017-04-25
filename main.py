# coding:utf-8


from spider.ProxyValidator import ProxyValidator
from spider.ProxyValidator import ProxyReValidator
from spider.ProxyGetter import ProxyGetter
from api import ProxyApi


def run():
    # 启动验证器,开20个线程去验证
    for i in range(20):
        validator = ProxyValidator()
        validator.start()

    revalidator = ProxyReValidator()
    revalidator.start()

    # 触发爬虫
    ProxyGetter().get()

    # 启动 Flask 服务器
    ProxyApi.app.run()


if __name__ == '__main__':
    run()

