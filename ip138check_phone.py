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
    'User-Agent': 'Mozilla/4.9 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
header_dict3 = {
    'User-Agent': 'Mozilla/4.8 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
header_dict4 = {
    'User-Agent': 'Mozilla/4.7 (Macintosh; Intel Mac OS X 10_10_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
header_dict5 = {
    'User-Agent': 'Mozilla/4.6 (Macintosh; Intel Mac OS X 10_9_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

pro = ["118.190.95.35:9001",
       "171.39.78.4:8123",
       "221.220.67.246:8118",
       "114.115.170.247:80",
       "117.21.191.151:61007",
       "111.155.124.84:8123",
       "180.118.240.207:808",
       "114.225.168.235:53128",
       "221.226.68.194:30442",
       "222.133.178.146:48239",
       "163.125.250.228:8118",
       "112.85.72.147:53128",
       "182.88.135.33:8123",
       "60.24.142.126:8118",
       "49.76.162.95:8123",
       "219.157.147.115:8118",
       "118.213.182.194:47944",
       "42.56.120.2:55258",
       "114.95.213.123:8118",
       "115.219.110.68:8010"]


def validate_ip(ip, protocol):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

    url = "http://www.baidu.com"
    try:
        proxy_host = {protocol: protocol + "://" + ip}
        print(proxy_host)
        html = requests.get(url, proxies=proxy_host, timeout=5, headers=headers)
        print(html.status_code)
        if html.status_code == 200:
            return True
        else:
            return False
    except RuntimeError as e:
        return e


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

        # server = random.choice(pro)
        # while True:
        #     if validate_ip(server, "http"):
        #         proxy = {"http": server}
        #         break
        #     else:
        #         server = random.choice(pro)

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
        time.sleep(1)
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
