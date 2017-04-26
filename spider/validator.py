# coding:utf-8

import threading
import socket
import time
from db.db_clients import RedisClient
from spider.items import Proxy
from db.db_factory import DBClientFactory


class ProxyValidator(threading.Thread):

    def __init__(self, wait_queue=None, http_queue=None, https_queue=None):
        if not wait_queue:
            wait_queue = DBClientFactory.create_wait_validate_db_client(RedisClient)
        if not http_queue:
            http_queue = DBClientFactory.create_active_db_client(RedisClient)
        if not https_queue:
            https_queue = DBClientFactory.create_active_db_client(RedisClient, protocol='HTTPS')
        threading.Thread.__init__(self)
        self.wait_queue = wait_queue
        self.http_queue = http_queue
        self.https_queue = https_queue

    def run(self):
        while True:
            proxy_dict = self.wait_queue.blpop()[1]
            proxy = Proxy.to_object(proxy_dict)
            proxy.valid_at = time.time()
            is_active = ProxyValidator.scan(proxy.ip, int(proxy.port))
            if is_active:
                if proxy.type == 'HTTPS':
                    self.https_queue.put(proxy.to_string())
                elif proxy.type == 'HTTP':
                    self.http_queue.put(proxy.to_string())
                else:
                    continue

    @classmethod
    def scan(cls, ip, port):
        port = int(port)
        s = socket.socket()
        s.settimeout(5)
        if s.connect_ex((ip, port)) == 0:
            return True
        else:
            return False


class ProxyReValidator(threading.Thread):
    """
    如果已经验证过的代理,每隔1分钟检查一遍,把验证时间超过5分钟的重新检验
    """

    def __init__(self, pass_queue, wait_queue=None):
        if not wait_queue:
            wait_queue = DBClientFactory.create_wait_validate_db_client(RedisClient)
        threading.Thread.__init__(self)
        self.wait_queue = wait_queue
        self.pass_queue = pass_queue

    def run(self):
        while True:
            proxy_dict = self.pass_queue.blpop()[1]
            proxy = Proxy.to_object(proxy_dict)
            now = time.time()
            if now - proxy.valid_at > 5 * 60:
                self.wait_queue.put(proxy_dict)
            else:
                self.pass_queue.put(proxy_dict)
                time.sleep(60)


if __name__ == '__main__':

    for i in range(20):
        validator = ProxyValidator()
        # validator.setDaemon(True) # 不能用守护进程,因为如果发生异常 phantomjs 会无法退出,从而狂占内存
        validator.start()

    revalidator = ProxyReValidator()
    revalidator.start()



