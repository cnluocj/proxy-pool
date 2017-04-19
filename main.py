# coding:utf-8


from spider.ProxyValidator import ProxyValidator
from api import ProxyApi


def run():
    # 启动验证器
    validator = ProxyValidator()
    validator.start()

    # 启动 Flask 服务器
    ProxyApi.app.run()


if __name__ == '__main__':
    run()

