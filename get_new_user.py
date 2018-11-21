import json
import random
import re
import time

import requests

import ip138check_phone

cookies = {
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22wangli59%22%2C%22%24device_id%22%3A%2216690649dac257-0f43bc7d76bf74-346c780e-1296000-16690649dad980%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%2216690649dac257-0f43bc7d76bf74-346c780e-1296000-16690649dad980%22%7D',
    'JSESSIONID': '470149D51C40277AFDDAD80074493F76',
}

headers = {
    'orgname': '%E6%B2%88%E9%98%B3%E5%8C%BA%E5%9F%9F',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6',
    'orgTypeName': '%E5%8C%BA%E5%9F%9F',
    'userid': '231161357641187328',
    'orgcode': 'syqy',
    'orgTypeCode': '10002',
    'Connection': 'keep-alive',
    'workingOrgCode': 'syqy',
    'code': 'syqy',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
    'tenantId': '2017092600001',
    'Accept': 'application/json, text/plain, */*',
    'username': '%E7%8E%8B%E5%8A%9B',
    'Referer': 'http://wanda.ffan.com/',
    'token': 'MjcyMTI3MzIxMTYxMzM0Nzg0',
}
params = (
    ('pageIndex', '1'),
    ('pageSize', '10'),
    ('scopes/[/]', 'syqy'),
    ('scope', 'syqy'),
    ('orgType', '10002'),
    ('wechatBind', '3'),
    ('drainageTypeshow', 'false'),
    ('drainagedateshow', 'false'),
    ('timestr', '1542809894421'),
)


def getUser(index, scope, start, end):
    params = (
        ('regStartTime', start),
        ('regEndTime', end),
        ('pageIndex', index),
        ('pageSize', '10'),
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


def init():
    global not_local
    not_local = 0
    global virtual
    virtual = 0
    print(" " + str(not_local) + " " + str(virtual))


def check_phone(phone):
    pat = "^1[7]\d{9}$"
    IC = re.search(pat, phone)
    if IC:
        print(IC.group())
        global virtual
        virtual += 1
        return " 虚拟 "
    return " "


def get_one_guangchang(id, guangchangname, localname, start, end):
    place_name = "1102/" + guangchangname + ".txt"
    file_write = open(place_name, "a")
    total_count = 0
    ip138check_phone.init(localname)
    init()
    for i in range(1, 100):
        result = json.loads(getUser(i, id, start, end))
        list_data = result['data']
        count = len(list_data)
        if count == 0:
            total_count = result["_metadata"]["totalCount"]
            break
        # 遍历查询出来的所有手机号 检验手机号
        for j in range(0, count):
            try:
                timeStamp = list_data[j]["regTime"]
                timeArray = time.localtime(timeStamp / 1000)
                # fromOrg = list_data[j]["fromOrg"]
                otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                phone = list_data[j]['mobileNo']
                # 获取手机号地区
                ip138_result = ip138check_phone.check(phone)
                p = time.ctime() + " " + list_data[j]['mobileNo'] + "  " + otherStyleTime + ip138_result
                # p = list_data[j]['mobileNo'] + "  " + otherStyleTime + check_phone(phone)
                print(p)
                file_write.write('%s\n' % p)
                # time.sleep(random.randint(0, 1))
            except RuntimeError as e:
                print(e)
                continue
    r = "总量：" + str(total_count) + " 非本地号：" + str(ip138check_phone.get_not_local()) + " 虚拟号：" + str(
        ip138check_phone.get_virtual())
    file_write.write("%s \n" % r)
    file_write.close()


def get_all_guangchang(start, end):
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
        place_name = "1003/" + result[1] + ".txt"
        file_write = open(place_name, "a")
        total_count = 0
        init()
        for i in range(1, 9):
            result = json.loads(getUser(i, org_id, start, end))
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
                # ip138_result = ip138check_phone.check(phone)
                p = list_data[j]['mobileNo'] + "  " + otherStyleTime + check_phone(phone)
                print(p)
                file_write.write('%s\n' % p)
                # time.sleep(random.randint(0, 1))
        r = "总量：" + str(total_count) + " 虚拟号：" + str(virtual)
        file_write.write("%s \n" % r)
        file_write.close()


def get_and_check_local_phone(local_file, write_file):
    file_read = open(local_file, "r")
    index = 0
    write = open(write_file, "a")
    while True:
        index += 1
        mystr = file_read.readline()
        if not mystr:
            break
        result = mystr.split(" ")
        phone = result[0]
        ip138_result = ip138check_phone.check(phone)
        p = phone + " " + ip138_result
        print(p)
        write.write('%s\n' % p)
        time.sleep(random.randint(0, 1))
    write.close()


def get_no_done_user_count(start1, end1, start2, end2):
    file_read = open("广场信息.txt", "r")
    index = 0
    while True:
        try:
            index += 1
            mystr = file_read.readline()
            if not mystr:
                break
            result = mystr.split(" ")
            print(result)
            org_id = result[0]
            total_count1 = json.loads(getUser(1, org_id, start1, end1))["_metadata"]["totalCount"]
            if total_count1 == 0:
                raise RuntimeError("1为0")
            total_count2 = json.loads(getUser(1, org_id, start2, end2))["_metadata"]["totalCount"]
            if total_count2 == 0:
                raise RuntimeError("2为0")
            p = result[1] + " " + str(total_count1) + " " + str(total_count2) + " 完成：" + str(
                total_count2 / total_count1)
            write(p)
        except RuntimeError as e:
            print(e)


def write(s):
    f = open("广场完成情况3.txt", "a")
    f.write('%s\n' % s.strip())
    f.close()


if __name__ == '__main__':
    start1 = '2018-11-16'
    end1 = '2018-11-21'
    orgId = "1000907"
    # getUser(1, orgId, start1, end1)

    start2 = '2018-11-01'
    end2 = '2018-11-30'
    # getUser(1, orgId, start2, end2)

    print("开始main方法")

    get_no_done_user_count("2018-10-01", "2018-10-31", start1, end1)
    # get_all_guangchang(start1, end1)
    # get_one_guangchang("1104581", "锦州万达广场", "锦州", start1, end1)
    # local_file = "/Users/demon/PycharmProjects/wanda/v3song/丹东新人礼20180911-check.txt"
    # write_file = "/Users/demon/PycharmProjects/wanda/v3song/丹东新人礼20180911-check-result.txt"
    # get_and_check_local_phone(local_file, write_file)
