import json

import requests


def cities():
    headers = {
        'Host': 'api.beyonds.com',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16B92 MicroMessenger/6.7.4(0x1607042c) NetType/WIFI Language/zh_CN',
        'Referer': 'https://servicewechat.com/wx07dfb5d79541eca9/109/page-frame.html',
        'Accept-Language': 'zh-cn',
    }
    response = requests.get('https://api.beyonds.com/wdmp/plaza/v1/city/cities', headers=headers)
    print(response.text)
    return response.text


def plazas(cityId):
    headers = {
        'Host': 'api.beyonds.com',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16B92 MicroMessenger/6.7.4(0x1607042c) NetType/WIFI Language/zh_CN',
        'Referer': 'https://servicewechat.com/wx07dfb5d79541eca9/109/page-frame.html',
        'Accept-Language': 'zh-cn',
    }
    params = (
        ('cityId', cityId),
        ('longitude', '120.1198501586914'),
        ('latitude', '30.299083709716797'),
    )
    response = requests.get('https://api.beyonds.com/wdmp/plaza/v1/city/plazas', headers=headers, params=params)
    print(response.text)
    return response.text


def write(s):
    f = open("广场明细.txt", "a")
    f.write('%s\n' % s.strip())
    f.close()


if __name__ == '__main__':
    r = json.loads(cities())
    cities = r["data"]
    size = len(cities)
    for i in range(0, size):
        rr = json.loads(plazas(cities[i]["cityId"]))
        list = rr["data"]
        for j in range(0, len(list)):
            plazaId = list[j]["plazaId"]
            plazaName = list[j]["plazaName"]
            p = "%s|%s" % (plazaId, plazaName)
            write(p)
