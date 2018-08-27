import requests

# admin.ffan.com 后台查询会员

cookies = {
    'CITY_ID': '110100',
    'SESSIONID': '375b2bed82fb38cc784f8df94d06318f',
    'U_UID': '6004c205-8291-457b-800d-bdb0a6a3c1a7',
    'PHPSESSID': 'amv9kogdtr0hog2pqf8ktei137',
    'UM_distinctid': '1657b50c98f79-06b6d9a76f451b-34677908-13c680-1657b50c990f6',
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22lidi%22%2C%22%24device_id%22%3A%22164a8b7f046bc2-072025535e027a-16386952-1296000-164a8b7f048777%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22164a8b7f046bc2-072025535e027a-16386952-1296000-164a8b7f048777%22%7D',
}

headers = {
    'Origin': 'https://admin.ffan.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'https://admin.ffan.com/member/member/index',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}

data = [
  ('key', 'value'),
  ('query_type', '1'),
  ('mobile', '13675822154'),
  ('uid', ''),
  ('cardNo', ''),
  ('memberRealName', ''),
  ('carNo', ''),
  ('cardStatus', '-1'),
  ('cardGrade', '-1'),
  ('memberGrade', '-1'),
  ('realName', ''),
  ('idCardType', '1'),
  ('idCardNo', ''),
  ('createTimeStart', ''),
  ('createTimeEnd', ''),
  ('plazaCity', '-1'),
  ('plaza_id', '-1'),
  ('merchantName', ''),
  ('merchant_id', ''),
  ('storeName', ''),
  ('store_id', ''),
  ('version', ''),
  ('activityId', ''),
  ('p', '1'),
  ('limit', '10'),
]

response = requests.post('https://admin.ffan.com/member/member/query', headers=headers, cookies=cookies, data=data)
print(response.text)