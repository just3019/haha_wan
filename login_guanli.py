# import requests
#
# cookies = {
#     'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22chentinghuang%22%2C%22%24device_id%22%3A%22164a8b7f046bc2-072025535e027a-16386952-1296000-164a8b7f048777%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22164a8b7f046bc2-072025535e027a-16386952-1296000-164a8b7f048777%22%7D',
#     'JSESSIONID': '5D9C3E09FCC6DA2176B6F9C146C40D4B',
# }
#
# headers = {
#     'Host': 'wanda.ffan.com',
#     'code': '1000769',
#     'orgname': '%E6%B8%A9%E5%B7%9E%E5%B9%B3%E9%98%B3%E4%B8%87%E8%BE%BE%E5%B9%BF%E5%9C%BA',
#     'Origin': 'http://wanda.ffan.com',
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
#     'tenantId': '2017092600001',
#     'Content-Type': 'application/json;chartset=utf-8',
#     'Accept': 'application/json, text/plain, */*',
#     'username': '%E9%99%88%E5%BB%B7%E7%9A%87',
#     'userid': '131737550254505984',
#     'orgcode': '1000769',
#     'orgTypeCode': '10003',
#     'workingOrgCode': '1000769',
#     'token': 'MjM0NDQ4NDY1NzM4ODU4NDk2',
#     'orgTypeName': '%E5%B9%BF%E5%9C%BA',
#     'Referer': 'http://wanda.ffan.com/',
#     'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6',
# }
#
# data = '{"username":"chentinghuang","password":"a66abb5684c45962d887564f08346e8d"}'
#
# response = requests.post('http://wanda.ffan.com/sail/merchant/users/login', headers=headers, cookies=cookies, data=data)
# print(response.text)


import requests

# cookies = {
#     'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%2216527e5ea2274f-03992cb526bf068-49183707-1296000-16527e5ea238a0%22%2C%22%24device_id%22%3A%2216527e5ea2274f-03992cb526bf068-49183707-1296000-16527e5ea238a0%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D',
#     'sajssdk_2015_cross_new_user': '1',
# }

headers = {
    'Content-Type': 'application/json;chartset=utf-8',
}

data = '{"username":"chentinghuang","password":"a66abb5684c45962d887564f08346e8d"}'

response = requests.post('http://wanda.ffan.com/sail/merchant/users/login', headers=headers, data=data)
print(response.text)
