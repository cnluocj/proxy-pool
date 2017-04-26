# coding:utf-8


from spider.validator import ProxyValidator
from spider.validator import ProxyReValidator
from spider.getter import ProxyGetter
from db.db_factory import DBClientFactory
from api import proxy_api
from db.db_clients import RedisClient


def run():
    # 启动验证器,开20个线程去验证
    for i in range(20):
        validator = ProxyValidator()
        validator.start()

    # 重复验证
    http_db_client = DBClientFactory.create_active_db_client(db_client_class=RedisClient, protocol='HTTP')
    https_db_client = DBClientFactory.create_active_db_client(db_client_class=RedisClient, protocol='HTTPS')

    http_revalidator = ProxyReValidator(pass_queue=http_db_client)
    http_revalidator.start()

    https_revalidator = ProxyReValidator(pass_queue=https_db_client)
    https_revalidator.start()

    # 触发爬虫
    ProxyGetter().get()

    # 启动 Flask 服务器
    proxy_api.app.run()


if __name__ == '__main__':
    run()

