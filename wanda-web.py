import datetime
import json
import socket

from bs4 import BeautifulSoup
from flask import Flask, request
import requests
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect('/Users/demon/Desktop/wanda.db')


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
    request.data


if __name__ == '__main__':
    print("开始")
# app.run(port=8888)
