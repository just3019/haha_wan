# -*- coding: utf-8 -*-
# python3.6

import requests


# 获取验证码
def get_code(mobile):
    headers = {
        'Host': 'api.ffan.com',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15F79 MicroMessenger/6.7.1 NetType/WIFI Language/zh_CN',
        'Referer': 'https://servicewechat.com/wx07dfb5d79541eca9/81/page-frame.html',
        'Accept-Language': 'zh-cn',
    }

    params = (
        ('sign', 'xcx'),
    )

    data = [
        ('mobile', mobile),
    ]

    response = requests.post('https://api.ffan.com/wechatxmt/v1/member/verifyCode', headers=headers, params=params,
                             data=data)
    # print('获取验证码接口返回参数：\n' + response.text)

    # NB. Original query string below. It seems impossible to parse and
    # reproduce query strings 100% accurately so the one below is given
    # in case the reproduced version is not "correct".
    # response = requests.post('https://api.ffan.com/wechatxmt/v1/member/verifyCode?sign=xcx', headers=headers, data=data)
