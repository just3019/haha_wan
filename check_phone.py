import json
import time

import requests

headers = {
    'tenantId': '2017092600001',
    'Accept': 'application/json, text/plain, */*',
    'orgcode': '1105208',
    'orgTypeCode': '10003',
    'token': 'MjQxNDc1MzIxMzI3NTE3Njk2',
}
file = "六盘水新人礼20180827"
file_write = "/Users/demon/Desktop/1/" + file + "校验号码.txt"
file_read = "/Users/demon/Desktop/1/" + file + ".txt"
name = "六盘水万达广场"
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
        ('scopes[]', 'DQFquanjituan'),
        ('scope', 'DQFquanjituan'),
        ('orgType', '10001'),
        ('mobileNo', phone),
        ('drainageTypeshow', 'true'),
        ('drainagedateshow', 'true'),
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
