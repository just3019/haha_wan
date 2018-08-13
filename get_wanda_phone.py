import json
import time

import requests


def get_wanda_phone(pageIndex, pageSize, start, end):
    headers = {
        'userid': '131737550254505984',
        'orgcode': '1000769',
        'orgTypeCode': '10003',
        'tenantId': '2017092600001',
        'token': 'MjM0NDQ4NDY1NzM4ODU4NDk2',
    }

    params = (
        ('pageIndex', pageIndex),
        ('pageSize', pageSize),
        ('scopes/[/]', '1000769'),
        ('scope', '1000769'),
        ('orgType', '10003'),
        ('regStartTime', start),
        ('regEndTime', end),
        ('wechatBind', '3'),
        ('timestr', time.time()),
    )

    response = requests.get('http://wanda.ffan.com/sail/member/list', headers=headers, params=params)
    return response.text


if __name__ == '__main__':
    pageIndex = 1
    pageSize = 100
    start = '2018-08-01'
    end = '2018-09-01'
    f = open("平阳" + start + end + ".txt", "w")
    while True:
        result = json.loads(get_wanda_phone(pageIndex, pageSize, start, end))
        pageIndex += 1
        print(result)
        count = len(result['data'])
        if count > 0:
            for row in result['data']:
                f.write('%s\n' % row['mobileNo'])
            if count < pageSize:
                break
