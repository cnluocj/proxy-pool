# coding:utf-8


import json
from flask import Flask
from spider.getter import ProxyGetter

app = Flask(__name__)

@app.route('/getproxy')
def getproxy():
    proxy_getter = ProxyGetter()
    proxy = proxy_getter.get()
    if proxy:
        proxy_dict = proxy.to_dict()
        proxy_dict['is_success'] = True
        return json.dumps(proxy_dict)
    else:
        result = {'is_success': False}
        return json.dumps(result)

@app.route('/gethttpsproxy')
def gethttpsproxy():
    proxy_getter = ProxyGetter()
    proxy = proxy_getter.get(protocol='HTTPS')
    if proxy:
        proxy_dict = proxy.to_dict()
        proxy_dict['is_success'] = True
        return json.dumps(proxy_dict)
    else:
        result = {'is_success': False}
        return json.dumps(result)

if __name__ == '__main__':
    app.run()
