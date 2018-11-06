import json

import requests

cookies = {
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22wangli59%22%2C%22%24device_id%22%3A%22164c642c5b7407-048ae012493e02-163b6952-1296000-164c642c5b837%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22164c642c5b7407-048ae012493e02-163b6952-1296000-164c642c5b837%22%7D',
    'JSESSIONID': 'A335AEACCFCF82338D055F725C905E17',
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
    'token': 'MjYxMTAwMDU4ODM1OTQzNDI0',
}

params = (
    ('scope', '1101038'),
    ('orgType', '10003'),
    ('startDate', '2018-11-06'),
    ('endDate', '2018-11-06'),
    ('pageIndex', '1'),
    ('pageSize', '1000'),
    ('timestr', '1540898923917'),
)

response = requests.get(
    'http://wanda.ffan.com/sail/member/report/analyse/expandingAnalyse/expandingSmallProcedureChannel', headers=headers,
    params=params, cookies=cookies)
print(response.text)
r = json.loads(response.text)
print(r)
list = r["data"]
print(list)
for i in range(0, len(list)):
    print(list[i]["mobileNo"])
print(r["_metadata"]["totalCount"])
