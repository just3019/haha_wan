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

params = (
    ('pageIndex', '1'),
    ('pageSize', '10'),
    ('scopes[]', 'DQFquanjituan'),
    ('scope', 'DQFquanjituan'),
    ('orgType', '10001'),
    ('mobileNo', '17075106431'),
    ('drainageTypeshow', 'true'),
    ('drainagedateshow', 'true'),
    ('timestr', time.time()),
)

response = requests.get('http://wanda.ffan.com/sail/member/list', headers=headers, params=params)
print(response.text)
result = json.loads(response.text)
print(result)
print(len(result['data']) == 0)
