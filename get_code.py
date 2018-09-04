# -*- coding: utf-8 -*-
# python3.6

import requests


# 获取验证码
def get_code(mobile):
    params = (
        ('sign', 'xcx'),
    )
    data = [
        ('mobile', mobile),
    ]
    response = requests.post('https://api.ffan.com/wechatxmt/v1/member/verifyCode', params=params, data=data)
    print('获取验证码接口返回参数：\n' + response.text)


if __name__ == '__main__':
    get_code("13675822154")
