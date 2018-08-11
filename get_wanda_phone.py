import requests

import requests

cookies = {
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22chentinghuang%22%2C%22%24device_id%22%3A%22164a8b7f046bc2-072025535e027a-16386952-1296000-164a8b7f048777%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22164a8b7f046bc2-072025535e027a-16386952-1296000-164a8b7f048777%22%7D',
    'JSESSIONID': '5F2FA7E04B6489A8DA897D15AB8D3463',
}

headers = {
    'orgname': '%E6%B8%A9%E5%B7%9E%E5%B9%B3%E9%98%B3%E4%B8%87%E8%BE%BE%E5%B9%BF%E5%9C%BA',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6',
    'orgTypeName': '%E5%B9%BF%E5%9C%BA',
    'userid': '131737550254505984',
    'orgcode': '1000769',
    'orgTypeCode': '10003',
    'Connection': 'keep-alive',
    'workingOrgCode': '1000769',
    'code': '1000769',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
    'tenantId': '2017092600001',
    'Accept': 'application/json, text/plain, */*',
    'username': '%E9%99%88%E5%BB%B7%E7%9A%87',
    'Referer': 'http://wanda.ffan.com/',
    'token': 'MjM0NDQ4NDY1NzM4ODU4NDk2',
}

params = (
    ('pageIndex', '1000'),
    ('pageSize', '10'),
    ('scopes/[/]', '1000769'),
    ('scope', '1000769'),
    ('orgType', '10003'),
    ('regStartTime', '2018-07-01'),
    ('regEndTime', '2018-09-01'),
    ('wechatBind', '3'),
    ('drainageTypeshow', 'false'),
    ('drainagedateshow', 'false'),
    ('timestr', '1533827453578'),
)

response = requests.get('http://wanda.ffan.com/sail/member/list', headers=headers, params=params, cookies=cookies)

print(response.text)
