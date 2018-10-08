import json
import time

import requests

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
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
    'tenantId': '2017092600001',
    'Accept': 'application/json, text/plain, */*',
    'username': '%E6%98%86%E6%98%8E%E8%A5%BF%E5%B1%B1%E4%B8%87%E8%BE%BE%E5%B9%BF%E5%9C%BA%E7%AE%A1%E7%90%86%E5%91%98',
    'Referer': 'http://wanda.ffan.com/',
    'token': 'MjUxNzcwNDk1MTQ0Mjk2NDQ4',
}
file = "丹东新人礼20181008"
file_write = "/Users/demon/Desktop/1/" + file + "校验号码.txt"
file_read = "/Users/demon/Desktop/1/" + file + ".txt"
name = "丹东万达广场"
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


def check(phone):
    params = (
        ('pageIndex', '1'),
        ('pageSize', '10'),
        ('scopes/[/]', 'DQFquanjituan'),
        ('scope', 'DQFquanjituan'),
        ('orgType', '10001'),
        ('mobileNo', phone),
        ('wechatBind', '3'),
        ('drainageTypeshow', 'false'),
        ('drainagedateshow', 'false'),
        ('timestr', time.time()),
    )
    response = requests.get('http://wanda.ffan.com/sail/member/list', headers=headers, params=params)
    print(response.text)
    result = json.loads(response.text)
    if result["status"] == "0000" and len(result["data"]) > 0:
        return result["data"][0]
    else:
        raise RuntimeError("查询不到")


if __name__ == '__main__':
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
            print(index)
            result = check(phone)
            address = result["fromOrg"]
            if address != name:
                if address not in notequal:
                    notequal += " " + address
                notequal_num += 1
            write(phone + " " + result["fromOrg"])
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
