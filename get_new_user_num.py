import requests

cookies = {
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22adminkmxs%22%2C%22%24device_id%22%3A%22164c642c5b7407-048ae012493e02-163b6952-1296000-164c642c5b837%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22164c642c5b7407-048ae012493e02-163b6952-1296000-164c642c5b837%22%7D',
    'JSESSIONID': '8731C48BFE9B4B40F0E870DE4A93F56D',
}

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
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'tenantId': '2017092600001',
    'Accept': 'application/json, text/plain, */*',
    'username': '%E6%98%86%E6%98%8E%E8%A5%BF%E5%B1%B1%E4%B8%87%E8%BE%BE%E5%B9%BF%E5%9C%BA%E7%AE%A1%E7%90%86%E5%91%98',
    'Referer': 'http://wanda.ffan.com/',
    'token': 'MjUyNzEwODQ0NjI0Nzk3Njk2',
}

params = (
    ('date/[/]', ['2018-09-28', '2018-09-28']),
    ('orgCode', '1000625'),
    ('channel', '01'),
    ('startDate', '2018-09-30'),
    ('endDate', '2018-09-30'),
    ('timeType', 'day'),
    ('pageSize', '10'),
    ('pageIndex', '1'),
    ('orgType', '10003'),
    ('timeOrder', 'descending'),
    ('selectOrg/[/]', '1000625'),
    ('timestr', '1538186155447'),
)

response = requests.get('http://wanda.ffan.com/sail/member/report/analyse/memberNumByPlaza', headers=headers, params=params, cookies=cookies)
print(response.text)