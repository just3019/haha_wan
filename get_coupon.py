# -*- coding: utf-8 -*-
# python3.6

import requests


def get_coupon(memberId, productId, mobile, cookieStr, puid):
    productInfos = '[{"productId":"' + productId + '","count":1}]'
    headers = {
        'Host': 'api.ffan.com',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15F79 MicroMessenger/6.7.1 NetType/4G Language/zh_CN',
        'Referer': 'https://servicewechat.com/wx07dfb5d79541eca9/81/page-frame.html',
        'Accept-Language': 'zh-cn',
    }

    params = (
        ('cookieStr', cookieStr),
    )

    data = [
        ('memberId', memberId),
        ('actionType', 'create'),
        ('remark', '{"orderType":"coupon","plazaId":1000769,"adSpaceId":"couponList"}'),
        ('productInfos', productInfos),
        ('clientInfo', '{"clientVersion":"wx07dfb5d79541eca9","ipAddr":"","clientType":"11"}'),
        ('tradeCode', '7010'),
        ('phoneNo', mobile),
        ('paymentFlag', '0'),
        ('orderSrc', '2010'),
        ('puid', puid),
        ('totalPrice', '0'),
        ('word_cup_2018', ''),
    ]

    response = requests.post('https://api.ffan.com/wechatxmt/v1/order/create/proxy', headers=headers, params=params,
                             data=data)
    result = response.text
    print('=========>' + result)
    return result


    # NB. Original query string below. It seems impossible to parse and
    # reproduce query strings 100% accurately so the one below is given
    # in case the reproduced version is not "correct".
    # response = requests.post('https://api.ffan.com/wechatxmt/v1/order/create/proxy?cookieStr=psid%3D82d04808433a3ac132d9034959970696%3B%20puid%3DA283D45AD75941FAA1B3AC7BB8A26D18%3B%20up%3Dbup%3B%20sid%3D29faaf25d689308a2fa89143406d8101%3B%20uid%3D15000000275022050%3B%20uniqkey2%3DRZhczLgfkoQJoTrJQkvJHputC4Lk%2FwtUjtZWpuWrDFyo1Npck0uVRTow%2BJ%2FBUyzzmK7d4I8KAlNbEgWS8HQXx2ntWgdTxpyBCBwDdFRnKCjxUjt8dYk22iLR3AYBCjdpQ5EmlTUwH6WTTtxI6wHsYTj3BtzlX2GP0Q7j9bI9yYmBHmH%2FdP9gVN7Y0M6WjtEaj9Lw%3B%20puid%3DA283D45AD75941FAA1B3AC7BB8A26D18%3B%20uid%3D15000000275022050%3B%20ploginToken%3D82d04808433a3ac132d9034959970696%3B%20', headers=headers, data=data)
