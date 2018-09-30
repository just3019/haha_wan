import requests

headers = {
    'Host': 'api.ffan.com',
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A366 MicroMessenger/6.7.3(0x16070321) NetType/WIFI Language/zh_CN',
    'Referer': 'https://servicewechat.com/wx07dfb5d79541eca9/92/page-frame.html',
    'Accept-Language': 'zh-cn',
}

params = (
    ('sign', 'xcx'),
)

data = {
  'mobile': '13675822154'
}

response = requests.post('https://api.ffan.com/wechatxmt/v1/member/verifyCode', headers=headers, params=params, data=data)

print(response.text)
#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.post('https://api.ffan.com/wechatxmt/v1/member/verifyCode?sign=xcx', headers=headers, data=data)
