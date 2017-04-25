# coding:utf-8


from spider.ProxyValidator import ProxyValidator
from spider.ProxyValidator import ProxyReValidator
from api import ProxyApi


def run():
    # 启动验证器,开10个线程去验证
    for i in range(10):
        validator = ProxyValidator()
        validator.start()

    revalidator = ProxyReValidator()
    revalidator.start()

    # 启动 Flask 服务器
    ProxyApi.app.run()


if __name__ == '__main__':
    run()

