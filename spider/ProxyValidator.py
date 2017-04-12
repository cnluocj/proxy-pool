# coding:utf-8

import threading
import socket
from db.RedisClient import RedisClient
from spider.items import Proxy
from db.DBClientFactory import DBClientFactory


class ProxyValidator(threading.Thread):

    def __init__(self, wait_queue=None, pass_queue=None):
        if not wait_queue:
            wait_queue = DBClientFactory.create_wait_validate_db_client(RedisClient)
        if not pass_queue:
            pass_queue = DBClientFactory.create_active_db_client(RedisClient)
        threading.Thread.__init__(self)
        self.wait_queue = wait_queue
        self.pass_queue = pass_queue

    def run(self):
        while True:
            proxy_dict = self.wait_queue.blpop()[1]
            proxy = Proxy.to_object(proxy_dict)
            is_active = ProxyValidator.scan(proxy.ip, int(proxy.port))
            if is_active:
                self.pass_queue.put(proxy_dict)

    @classmethod
    def scan(cls, ip, port):
        port = int(port)
        s = socket.socket()
        s.settimeout(5)
        if s.connect_ex((ip, port)) == 0:
            return True
        else:
            return False


if __name__ == '__main__':

    wait_queue = RedisClient(name='wait_validate_proxies')
    pass_queue = RedisClient(name='active_proxies')

    for i in range(20):
        validator = ProxyValidator(wait_queue=wait_queue, pass_queue=pass_queue)
        # validator.setDaemon(True) # 不能用守护进程,因为如果发生异常 phantomjs 会无法退出,从而狂占内存
        validator.start()

