import json
import time

import requests

headers = {
    'tenantId': '2017092600001',
    'Accept': 'application/json, text/plain, */*',
    'orgcode': '1104483',
    'orgTypeCode': '10003',
    'token': 'MjM1MDY0MDgxMjgxNzEyMTI4',
}


def write(s):
    f = open("校验号码.txt", "a")
    f.write('%s\n' % s)
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
    if result["status"] == "0000":
        return result["data"][0]


if __name__ == '__main__':
    file = open("/Users/demon/PycharmProjects/wanda/v3/台州20180828.txt", 'r')
    index = 0
    t1 = time.time()
    while True:
        try:
            index += 1
            mystr = file.readline()
            if not mystr:
                break
            phone = mystr[0: 11]
            print(phone)
            result = check(phone)
            write(phone + " " + result["fromOrg"])
        except RuntimeError as e:
            print(e)
            continue
    t2 = time.time()
    print("总共使用：" + str(t2 - t1))
    file.close()
