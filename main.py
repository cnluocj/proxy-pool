# coding:utf-8


from spider.validator import ProxyValidator
from spider.validator import ProxyReValidator
from spider.getter import ProxyGetter
from api import proxy_api


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
    proxy_api.app.run()


if __name__ == '__main__':
    run()

