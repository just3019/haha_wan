# -*- coding: utf-8 -*-
# python3.6

import requests


# 获取验证码
def get_code(mobile):
    import requests

    headers = {
        'Host': 'api.ffan.com',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15G77 MicroMessenger/6.7.1 NetType/4G Language/zh_CN',
        'Referer': 'https://servicewechat.com/wx07dfb5d79541eca9/83/page-frame.html',
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
    print('获取验证码接口返回参数：\n' + response.text)


if __name__ == '__main__':
    get_code("13675822154")
