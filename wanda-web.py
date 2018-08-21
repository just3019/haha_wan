import datetime
import sqlite3

import requests
from flask import Flask

app = Flask(__name__)
conn = sqlite3.connect('wanda.db')


@app.route('/')
def hello_world():
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    return 'Hello Flask!'


# 登录万达飞凡管理员
@app.route('/loginWandaGuanli')
def login_wanda_guanli():
    headers = {
        'Content-Type': 'application/json;chartset=utf-8',
    }
    data = '{"username":"chentinghuang","password":"a66abb5684c45962d887564f08346e8d"}'
    session = requests.session()
    response = session.post('http://wanda.ffan.com/sail/merchant/users/login', headers=headers, data=data)
    return response.text


@app.route('/getUserInfo')
def get_user_info():
    print("hahah")


if __name__ == '__main__':
    print("开始")
# app.run(port=8888)
# 非凡管理后台登录记录用户
# 非凡商家模拟登录记录用户
# 提供万达广场id对照表
# 微信客户端登录万达小程序的WXFFANTOKEN
