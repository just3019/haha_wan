import json
import random

import requests
import time


def get_local_user(index):
    cookies = {
        'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22adminkmxs%22%2C%22%24device_id%22%3A%22164c642c5b7407-048ae012493e02-163b6952-1296000-164c642c5b837%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22164c642c5b7407-048ae012493e02-163b6952-1296000-164c642c5b837%22%7D',
        'JSESSIONID': '72A10896DC92AE7E5B81A31F492197F5',
    }
    headers = {
        'orgname': '%E6%98%86%E6%98%8E%E8%A5%BF%E5%B1%B1%E4%B8%87%E8%BE%BE%E5%B9%BF%E5%9C%BA',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6',
        'orgTypeName': '%E5%B9%BF%E5%9C%BA',
        'userid': '124184006076923904',
        'orgcode': '1000744',
        'orgTypeCode': '10003',
        'Connection': 'keep-alive',
        'workingOrgCode': '1000744',
        'code': '1000744',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'tenantId': '2017092600001',
        'Accept': 'application/json, text/plain, */*',
        'username': '%E6%98%86%E6%98%8E%E8%A5%BF%E5%B1%B1%E4%B8%87%E8%BE%BE%E5%B9%BF%E5%9C%BA%E7%AE%A1%E7%90%86%E5%91%98',
        'Referer': 'http://wanda.ffan.com/',
        'token': 'MjQzMzcwMDk3ODE5Nzc5MDcy',
    }

    params = (
        ('pageIndex', index),
        ('pageSize', '1000'),
        ('scopes/[/]', '1000744'),
        ('scope', '1000744'),
        ('orgType', '10003'),
        ('regStartTime', '2018-01-01'),
        ('regEndTime', '2018-01-06'),
        ('wechatBind', '3'),
        ('drainageTypeshow', 'false'),
        ('drainagedateshow', 'false'),
        ('timestr', '1535959506056'),
    )

    # pro = ["http://101.27.20.15:39276", "http://101.27.21.132:14270"]
    # server = random.choice(pro)
    # proxy = {
    #     "http": server,
    #     "https": server
    # }

    response = requests.get('http://wanda.ffan.com/sail/member/list', headers=headers, params=params, cookies=cookies)
    result = response.text
    print("====>" + result)
    return result


if __name__ == '__main__':
    index = 1
    while True:
        file_write = open("昆明西山万达.txt", "a")
        result = json.loads(get_local_user(index))
        if result["status"] == "0500":
            print(result["message"])
            time.sleep(5)
            continue
        list_data = result['data']
        count = len(list_data)
        if count == 0:
            print("拉取完毕")
            break
        # 遍历查询出来的所有手机号 检验手机号
        for j in range(0, count):
            timeStamp = list_data[j]["regTime"]
            timeArray = time.localtime(timeStamp / 1000)
            fromOrg = list_data[j]["fromOrg"]
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            phone = list_data[j]['mobileNo']
            p = list_data[j]['mobileNo'] + "  " + otherStyleTime
            print(p)
            file_write.write('%s\n' % p)
        file_write.close()
        index += 1
        time.sleep(1)
