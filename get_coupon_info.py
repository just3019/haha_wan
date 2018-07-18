# -*- coding: utf-8 -*-
# python3.6

import requests


# 获取优惠券明细
def get_couponNo(cookieStr, oid):
    headers = {
        'Host': 'api.ffan.com',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15F79 MicroMessenger/6.7.1 NetType/WIFI Language/zh_CN',
        'Referer': 'https://servicewechat.com/wx07dfb5d79541eca9/81/page-frame.html',
        'Accept-Language': 'zh-cn',
    }

    params = (
        ('cookieStr', cookieStr),
        ('oid', oid),
    )

    response = requests.get('https://api.ffan.com/wechatxmt/v1/order', headers=headers, params=params)
    result = response.text
    # print('===>\n' + result)
    return result

    # NB. Original query string below. It seems impossible to parse and
    # reproduce query strings 100% accurately so the one below is given
    # in case the reproduced version is not "correct".
    # response = requests.get('https://api.ffan.com/wechatxmt/v1/order?cookieStr=SESSIONID%3D99d4c1ab11c69f31484e14670b2c7a07%3B%20up%3Dbup%3B%20uniqkey2%3DRZhczLgfkoQJoTrJS0naFp72CIKw%2BwNZjN5e9uX8XVWi3dtUnAvQSGY88c3NXWqiyqfZ4o1YAFdbGlKV8SURkT3gCF9Q192JDxMAfUAidXT8KD0NdNE2%2FQKirXdSB0FpM%2BkqmjlFa6WZOqJAq0O2QESNDw%3B%20uid%3D15020418012101385%3B%20SESSIONID%3D99d4c1ab11c69f31484e14670b2c7a07%3B%20puid%3DB2B293FCBBC74F3DA965BD63BE3073EA%3Buid%3D15020418012101385%3BploginToken%3D9c753864572b2408e04a4dd8bc8a2ac2%3B&oid=51878725821385', headers=headers)
