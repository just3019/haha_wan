import json

import requests
import time

headers = {
    'Host': 'api.ffan.com',
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15G77 MicroMessenger/6.7.1 NetType/WIFI Language/zh_CN',
    'Referer': 'https://servicewechat.com/wx07dfb5d79541eca9/83/page-frame.html',
    'Accept-Language': 'zh-cn',
}


def get_park(cityId):
    params = (
        ('cityId', cityId),
    )

    while True:
        response = requests.get('https://api.ffan.com/wechatxmt/v1/plazas', headers=headers, params=params)
        print(response.text)
        result = json.loads(response.text)
        if result["status"] != 200:
            print("请求错误，等待5s重试")
            time.sleep(5)
            continue
        return response.text


def get_cities():
    response = requests.get('https://api.ffan.com/wechatxmt/v1/cities', headers=headers)
    print("==" + response.text)
    return response.text


if __name__ == '__main__':

    f = open("广场信息.txt", "w")

    cities = json.loads(get_cities())
    for c in cities['data']:
        park = json.loads(get_park(c['cityId']))
        for pp in park['data']:
            p = str(pp['plazaId']) + " " + pp['plazaName'] + " " + c["cityName"]
            print(p)
            f.write('%s\n' % p)

    f.close()
