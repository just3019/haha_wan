import json
import random
import time

import requests

import ip138check_phone

cookies = {
    'CITY_ID': '110100',
    'SESSIONID': '8402089fb985f3a007cd7e6091b02d28',
    'U_UID': '899fbab7-0f94-44ea-8df4-2c7ef055f257',
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22chentinghuang%22%2C%22%24device_id%22%3A%22164c642c5b7407-048ae012493e02-163b6952-1296000-164c642c5b837%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22164c642c5b7407-048ae012493e02-163b6952-1296000-164c642c5b837%22%7D',
    'JSESSIONID': 'B2C6E7BDEAB2D40BAB8727F0A9440265',
}

headers = {
    'orgname': '%E6%B8%A9%E5%B7%9E%E5%B9%B3%E9%98%B3%E4%B8%87%E8%BE%BE%E5%B9%BF%E5%9C%BA',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6',
    'orgTypeName': '%E5%B9%BF%E5%9C%BA',
    'userid': '131737550254505984',
    'orgcode': '1000769',
    'orgTypeCode': '10003',
    'Connection': 'keep-alive',
    'workingOrgCode': '1000769',
    'code': '1000769',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'tenantId': '2017092600001',
    'Accept': 'application/json, text/plain, */*',
    'username': '%E9%99%88%E5%BB%B7%E7%9A%87',
    'Referer': 'http://wanda.ffan.com/',
    'token': 'MjQxNDkwMTM1MDA1MjY1OTIw',
}

params = (
    ('pageIndex', '1'),
    ('pageSize', '10'),
    ('scopes/[/]', '1000769'),
    ('scope', '1000769'),
    ('orgType', '10003'),
    ('wechatBind', '3'),
    ('drainageTypeshow', 'false'),
    ('drainagedateshow', 'false'),
    ('timestr', '1535505355760'),
)


def getUser(index, scope):
    params = (
        ('regStartTime', '2018-09-09'),
        ('regEndTime', '2018-09-09'),
        ('pageIndex', index),
        ('pageSize', '1000'),
        ('scopes/[/]', scope),
        ('scope', scope),
        ('orgType', '10003'),
        ('wechatBind', '3'),
        ('drainageTypeshow', 'false'),
        ('drainagedateshow', 'false'),
        ('timestr', time.time()),
    )

    response = requests.get('http://wanda.ffan.com/sail/member/list', headers=headers, params=params, cookies=cookies)
    result = response.text
    print("====>" + result)
    return result


def get_one_guangchang(id, guangchangname, localname):
    place_name = "910/" + guangchangname + ".txt"
    file_write = open(place_name, "a")
    total_count = 0
    ip138check_phone.init(localname)
    for i in range(1, 100):
        result = json.loads(getUser(i, id))
        list_data = result['data']
        count = len(list_data)
        if count == 0:
            total_count = result["_metadata"]["totalCount"]
            break
        # 遍历查询出来的所有手机号 检验手机号
        for j in range(0, count):
            timeStamp = list_data[j]["regTime"]
            timeArray = time.localtime(timeStamp / 1000)
            # fromOrg = list_data[j]["fromOrg"]
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            phone = list_data[j]['mobileNo']
            # 获取手机号地区
            ip138_result = ip138check_phone.check(phone)
            p = list_data[j]['mobileNo'] + "  " + otherStyleTime + ip138_result
            print(p)
            file_write.write('%s\n' % p)
            # time.sleep(random.randint(0, 1))
    r = "总量：" + str(total_count) + " 非本地号：" + str(ip138check_phone.get_not_local()) + " 虚拟号：" + str(
        ip138check_phone.get_virtual())
    file_write.write("%s \n" % r)
    file_write.close()


def get_all_guangchang():
    file_read = open("广场信息.txt", "r")
    index = 0
    while True:
        index += 1
        mystr = file_read.readline()
        if not mystr:
            break
        result = mystr.split(" ")
        print(result)
        org_id = result[0]
        place_name = "908/" + result[1] + ".txt"
        file_write = open(place_name, "a")
        total_count = 0
        ip138check_phone.init(result[2].strip())
        for i in range(1, 10):
            result = json.loads(getUser(i, org_id))
            list_data = result['data']
            count = len(list_data)
            if count == 0:
                total_count = result["_metadata"]["totalCount"]
                break
            # 遍历查询出来的所有手机号 检验手机号
            for j in range(0, count):
                timeStamp = list_data[j]["regTime"]
                timeArray = time.localtime(timeStamp / 1000)
                # fromOrg = list_data[j]["fromOrg"]
                otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                phone = list_data[j]['mobileNo']
                # 获取手机号地区
                ip138_result = ip138check_phone.check(phone)
                p = list_data[j]['mobileNo'] + "  " + otherStyleTime + ip138_result
                print(p)
                file_write.write('%s\n' % p)
                # time.sleep(random.randint(0, 1))
        r = "总量：" + str(total_count) + " 非本地号：" + str(ip138check_phone.get_not_local()) + " 虚拟号：" + str(
            ip138check_phone.get_virtual())
        file_write.write("%s \n" % r)
        file_write.close()


if __name__ == '__main__':
    # getUser(1, "1102213")
    print("开始main方法")
    # get_all_guangchang()
    get_one_guangchang("1100808", "梅州万达广场", "梅州")
