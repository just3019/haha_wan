import json
import time

import requests

cookies = {
    'sajssdk_2015_cross_new_user': '1',
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22lidi%22%2C%22%24device_id%22%3A%22164c642c5b7407-048ae012493e02-163b6952-1296000-164c642c5b837%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22164c642c5b7407-048ae012493e02-163b6952-1296000-164c642c5b837%22%7D',
    'JSESSIONID': 'D2D363A9F90B81D759A3166D770E5B2C',
}

headers = {
        'Host': 'wanda.ffan.com',
        'code': '1104483',
        'orgname': '%E5%9B%9E%E6%B0%91%E5%8C%BA%E4%B8%87%E8%BE%BE%E5%B9%BF%E5%9C%BA',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'tenantId': '2017092600001',
        'Accept': 'application/json, text/plain, */*',
        'username': '%E6%9D%8E%E8%BF%AA',
        'orgcode': '1104483',
        'orgTypeCode': '10003',
        'workingOrgCode': '1104483',
        'token': 'MjMzNTcxMzM4MTg5NTM3Mjgw',
        'orgTypeName': '%E5%B9%BF%E5%9C%BA',
        'Referer': 'http://wanda.ffan.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6',
    }

params = (
    ('pageIndex', '1'),
    ('pageSize', '10'),
    ('scopes[]', 'DQFquanjituan'),
    ('scope', 'DQFquanjituan'),
    ('orgType', '10001'),
    ('mobileNo', '13675822154'),
    ('wechatBind', '3'),
    ('drainageTypeshow', 'false'),
    ('drainagedateshow', 'false'),
    ('timestr', time.time()),
)

response = requests.get('http://wanda.ffan.com/sail/member/list', headers=headers, params=params, cookies=cookies)
result = json.loads(response.text)
print(result)
print(len(result['data']) == 0)

# NB. Original query string below. It seems impossible to parse and
# reproduce query strings 100% accurately so the one below is given
# in case the reproduced version is not "correct".
# response = requests.get('http://wanda.ffan.com/sail/member/list?pageIndex=1&pageSize=10&scopes[]=DQFquanjituan&scope=DQFquanjituan&orgType=10001&mobileNo=13675822155&wechatBind=3&drainageTypeshow=false&drainagedateshow=false&timestr=1532340111603', headers=headers, cookies=cookies)
