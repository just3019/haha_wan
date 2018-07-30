import requests

headers = {
    'Host': 'api.ffan.com',
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15F79 MicroMessenger/6.7.1 NetType/WIFI Language/zh_CN',
    'Referer': 'https://servicewechat.com/wx07dfb5d79541eca9/83/page-frame.html',
    'Accept-Language': 'zh-cn',
}

response = requests.get('https://api.ffan.com/wechatxmt/v1/cities', headers=headers)
print(response.text)


import requests

headers = {
    'Host': 'api.ffan.com',
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15G77 MicroMessenger/6.7.1 NetType/WIFI Language/zh_CN',
    'Referer': 'https://servicewechat.com/wx07dfb5d79541eca9/83/page-frame.html',
    'Accept-Language': 'zh-cn',
}

response = requests.get('https://api.ffan.com/wechatxmt/v1/cities', headers=headers)
