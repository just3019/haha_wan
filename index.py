import requests

headers = {
    'Host': 'api.ffan.com',
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15G77 MicroMessenger/6.7.1 NetType/WIFI Language/zh_CN',
    'Referer': 'https://servicewechat.com/wx07dfb5d79541eca9/83/page-frame.html',
    'Accept-Language': 'zh-cn',
}

params = (
    ('cookieStr', 'psid=b59def45289ca608e824c0343cce3957; puid=01D132E5F32343EEB9F7D08C1B400102; up=bup; sid=6c395e0d3184f3a7d1b2d30695cbaf3f; uid=15000000371775781; uniqkey2=RZhczLgfkoQJoTrJRhGcRs+uCdOz+AtZ29UP8LP8D1b11t5Znk7AQ2Nn+8jBUyzzmK7d4I8KAlNbEgSS9HMSwG7gWwdTxpyBCBxZcwkzeXb1Xz13f4tkjXHYigxXB2RqRJwgz29iHKqfT9xI6wHsYTiGBaDnKGf/pQzn8rg9y4qFHWn7cPoTW9+rqruUiKQbhdLw; puid=01D132E5F32343EEB9F7D08C1B400102; uid=15000000371775781; ploginToken=b59def45289ca608e824c0343cce3957; '),
)

data = [
  ('plazaId', '1102223'),
]

response = requests.post('https://api.ffan.com/wechatxmt/v1/coupons-package/', headers=headers, params=params, data=data)
print(response.text)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.post('https://api.ffan.com/wechatxmt/v1/coupons-package/?cookieStr=psid%3Db59def45289ca608e824c0343cce3957%3B%20puid%3D01D132E5F32343EEB9F7D08C1B400102%3B%20up%3Dbup%3B%20sid%3D6c395e0d3184f3a7d1b2d30695cbaf3f%3B%20uid%3D15000000371775781%3B%20uniqkey2%3DRZhczLgfkoQJoTrJRhGcRs%2BuCdOz%2BAtZ29UP8LP8D1b11t5Znk7AQ2Nn%2B8jBUyzzmK7d4I8KAlNbEgSS9HMSwG7gWwdTxpyBCBxZcwkzeXb1Xz13f4tkjXHYigxXB2RqRJwgz29iHKqfT9xI6wHsYTiGBaDnKGf%2FpQzn8rg9y4qFHWn7cPoTW9%2BrqruUiKQbhdLw%3B%20puid%3D01D132E5F32343EEB9F7D08C1B400102%3B%20uid%3D15000000371775781%3B%20ploginToken%3Db59def45289ca608e824c0343cce3957%3B%20', headers=headers, data=data)
