import json

import requests
import time

cookies = {
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22wangli59%22%2C%22%24device_id%22%3A%22164c642c5b7407-048ae012493e02-163b6952-1296000-164c642c5b837%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22164c642c5b7407-048ae012493e02-163b6952-1296000-164c642c5b837%22%7D',
    'JSESSIONID': '47E235019DEE6C164723C328CBF340B0',
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
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'tenantId': '2017092600001',
    'Accept': 'application/json, text/plain, */*',
    'username': '%E7%8E%8B%E5%8A%9B',
    'Referer': 'http://wanda.ffan.com/',
    'token': 'MjY2NjQ2MjA5NTA1MDAxNDcy',
}

file = "朝阳普通20181110"
file_write = "/Users/demon/Desktop/1/" + file + "校验号码.txt"
file_read = "/Users/demon/Desktop/1/" + file + ".txt"
file_write_success = "/Users/demon/Desktop/1/" + file + "succ.txt"
name = "朝阳万达广场"
# 非该广场名
notequal = ""
# 非该广场数
notequal_num = 0
# 查询不到数
no_num = 0


def write(s):
    f = open(file_write, "a")
    f.write('%s\n' % s.strip())
    f.close()


def write_success(s):
    f = open(file_write_success, "a")
    f.write('%s\n' % s.strip())
    f.close()


def check(phone):
    params = (
        ('scope', '1101038'),
        ('orgType', '10003'),
        ('startDate', '2018-11-10'),
        ('endDate', '2018-11-10'),
        ("mobileNo", phone),
        ('pageIndex', '1'),
        ('pageSize', '10'),
        ('timestr', '1541503034013'),
    )

    response = requests.get(
        'http://wanda.ffan.com/sail/member/report/analyse/expandingAnalyse/expandingSmallProcedureChannel',
        headers=headers, params=params, cookies=cookies)
    print(response.text)
    result = json.loads(response.text)
    if result["status"] != "0000" or len(result["data"]) == 0:
        raise RuntimeError("查询不到")


if __name__ == '__main__':
    # print(check("18281017495"))
    file = open(file_read, 'r')
    index = 0
    t1 = time.time()
    while True:
        try:
            index += 1
            mystr = file.readline()
            if not mystr:
                break
            phone = mystr[0: 11]
            print(str(index) + " " + phone)
            result = check(phone)
            write_success(mystr.strip())
            write(phone)
        except RuntimeError as e:
            no_num += 1
            print(e)
            write(phone + " 查询不到")
            continue
    p = "总共：" + str(index - 1) + " 非该广场数：" + str(notequal_num) + " 查询不到广场数：" + str(no_num) + "\n非该广场名：" + str(notequal)
    write(p)
    t2 = time.time()
    print("总共使用：" + str(t2 - t1))
    file.close()
