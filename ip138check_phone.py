import random
import time

import requests
from bs4 import BeautifulSoup

local_name = "大同"
name = ""
file_read = "815/" + name
file_write = "ip138check/" + name
# 不是当地的号码
global not_local
not_local = 0
global virtual
virtual = 0
header_dict1 = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
header_dict2 = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
header_dict3 = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
header_dict4 = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
header_dict5 = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}


def check_ip(ip):
    try:
        requests.get('http://wenshu.court.gov.cn/', proxies={"http": "http://183.234.38.213:6300"})
    except:
        print('connect failed')
    else:
        print('success')


def check(phone):
    try:
        url = "http://www.ip138.com:8080/search.asp?action=mobile&mobile=%s" % phone
        i = random.randint(0, 5)
        if i == 0:
            headers = header_dict1
        elif i == 1:
            headers = header_dict2
        elif i == 2:
            headers = header_dict3
        elif i == 3:
            headers = header_dict4
        else:
            headers = header_dict5
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'gb2312'
        html = BeautifulSoup(response.text, 'lxml')
        # for row in html.find_all("table")[1].find_all("td"):
        #     print(row.text)
        local = html.find_all("table")[1].find_all("td")[4].text
        type = html.find_all("table")[1].find_all("td")[6].text
        # print(local)
        # print(type)
        # result = phone
        result = " "
        if local_name not in local:
            # print(local)
            global not_local
            not_local += 1
            result += (" " + local)
        if "虚拟" in type:
            # print(type)
            global virtual
            virtual += 1
            result += (" " + type)
        # else:
        #     result += (" 非虚拟号 " + type)
        return result
    except RuntimeError as e:
        time.sleep(1)
        print("被拦截")
        raise RuntimeError("请求失败")


def init(name):
    global local_name
    local_name = name
    global not_local
    not_local = 0
    global virtual
    virtual = 0
    print(local_name + " " + str(not_local) + " " + str(virtual))


def get_not_local():
    return not_local


def get_virtual():
    return virtual


def write(s):
    print(s)
    f = open(file_write, "a")
    f.write('%s\n' % s.strip())
    f.close()


def taobaocheck(phone):
    url = "http://tcc.taobao.com/cc/json/mobile_tel_segment.htm?tel=%s" % phone
    response = requests.get(url, headers=header_dict1).text
    print(response)


if __name__ == '__main__':
    # check("17099827723")
    # taobaocheck("15713753916")

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
            result = check(phone)
            write(result)
        except RuntimeError as e:
            print(e)
    p = "总量：" + str(index) + " 非本地号码量：" + str(not_local) + " 虚拟号码量：" + str(virtual)
    write("\n %s" % p)
