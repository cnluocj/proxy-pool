# coding:utf-8


from flask import Flask
from spider.ProxyGetter import ProxyGetter

app = Flask(__name__)

@app.route('/getproxy')
def getproxy():
    proxy_getter = ProxyGetter()
    return proxy_getter.get().to_string()

if __name__ == '__main__':
    app.run()

