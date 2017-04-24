# coding:utf-8


import json
from flask import Flask
from spider.ProxyGetter import ProxyGetter

app = Flask(__name__)

@app.route('/getproxy')
def getproxy():
    proxy_getter = ProxyGetter()
    proxy = proxy_getter.get()
    if proxy:
        return proxy.to_string()
    else:
        result = {'error': '无结果'}
        return json.dumps(result)

if __name__ == '__main__':
    app.run()
