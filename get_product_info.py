import json

import requests


def get_product_info():
    headers = {
        'Host': 'api.ffan.com',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15F79 MicroMessenger/6.7.1 NetType/WIFI Language/zh_CN',
        'Referer': 'https://servicewechat.com/wx07dfb5d79541eca9/83/page-frame.html',
        'Accept-Language': 'zh-cn',
    }

    params = (
        ('adSpaceId', 'couponList'),
        ('plazaId', '1000769'),
        ('channelId', '1003'),
        ('type', '1001'),
        ('pageNum', '1'),
        ('pageSize', '10'),
    )

    response = requests.get('https://api.ffan.com/wechatxmt/v5/plaza/coupons', headers=headers, params=params)

    result = response.text
    print('===>\n' + result)
    return result


if __name__ == '__main__':
    num = 0
    result = json.loads(get_product_info())
    a = result['data']['resource'][num - 1]['couponNo']
    print(a)
