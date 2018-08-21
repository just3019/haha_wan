import json
import time

import requests

cookies = {
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22adminsm%22%2C%22%24device_id%22%3A%22164a8b7f046bc2-072025535e027a-16386952-1296000-164a8b7f048777%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22164a8b7f046bc2-072025535e027a-16386952-1296000-164a8b7f048777%22%7D',
    'JSESSIONID': '60ED0ACC92B0D3AD019B64433F77F577',
}

headers = {
    'Host': 'wanda.ffan.com',
    'code': '1102566',
    'orgname': '%E4%B8%89%E6%98%8E%E4%B8%87%E8%BE%BE%E5%B9%BF%E5%9C%BA',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'tenantId': '2017092600001',
    'Accept': 'application/json, text/plain, */*',
    'username': '%E4%B8%89%E6%98%8E%E4%B8%87%E8%BE%BE%E5%B9%BF%E5%9C%BA%E7%AE%A1%E7%90%86%E5%91%98',
    'userid': '124914913087848448',
    'orgcode': '1102566',
    'orgTypeCode': '10003',
    'workingOrgCode': '1102566',
    'token': 'MjMwODMwNTA0MTc2MjU0OTc2',
    'orgTypeName': '%E5%B9%BF%E5%9C%BA',
    'Referer': 'http://wanda.ffan.com/',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6',
}


def getUser(index):
    params = (
        ('pageIndex', index),
        ('pageSize', '100'),
        ('scopes[]', '1102566'),
        ('scope', '1102566'),
        ('orgType', '10003'),
        ('date[]', ['2018-07-28T16:00:00.000Z', '2018-07-29T16:00:00.000Z']),
        ('regStartTime', '2018-07-29'),
        ('regEndTime', '2018-07-30'),
        ('wechatBind', '3'),
        ('drainageTypeshow', 'false'),
        ('drainagedateshow', 'false'),
        ('timestr', time.time()),
    )

    response = requests.get('http://wanda.ffan.com/sail/member/list', headers=headers, params=params, cookies=cookies)
    result = response.text
    # print("====>" + result)
    return result


if __name__ == '__main__':
    for i in range(1, 6):
        result = json.loads(getUser(i))
        list_data = result['data']
        count = len(list_data)
        for j in range(0, count):
            print(list_data[j]['mobileNo'])
