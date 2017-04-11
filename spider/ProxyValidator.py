# coding:utf-8

import threading
import requests
import socket
from db.RedisClient import RedisClient
from spider.items import Proxy


class ProxyValidator(threading.Thread):

    def __init__(self, wait_queue, pass_queue):
        threading.Thread.__init__(self)
        self.wait_queue = wait_queue
        self.pass_queue = pass_queue

    def run(self):
        while True:
            print 'in'
            proxy_dict = self.wait_queue.blpop()[1]
            proxy = Proxy.to_object(proxy_dict)
            is_active = self.__scan(proxy.ip, int(proxy.port))
            if is_active:
                self.pass_queue.put(proxy_dict)

    def __scan(self, ip, port):
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
        # validator.setDaemon(True)
        validator.start()

