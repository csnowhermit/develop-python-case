# -*- coding:utf-8 -*-

import json
from flask import Flask, request

'''
    flask服务端：模拟应用交互模块，被PostConsumer调用
'''

app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def call():
    try:
        user_agent = request.headers.get('User-Agent')  # 获取浏览器头部信息
        if request.method == "GET":
            forward = request.args.get('forward')
            actions = request.args.get('actions')
            print('<p>GET %s, %s, %s</p>' % (forward, actions, user_agent))
        elif request.method == "POST":
            get_data = json.loads(request.get_data(as_text=True))
            print('<p>POST %s</p>' % (get_data))
        else:      # 其他方式的请求不予处理
            pass
        return '0'
    except:
        return '1'

if __name__ == '__main__':
    app.run(host="localhost", port=80, debug=True)

