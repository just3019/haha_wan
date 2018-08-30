import requests

headers = {
    'Host': 'api.ffan.com',
    'Accept': '*/*',
    'User-Agent': 'com.dianshang.feifanbp/2.0.1 (iPhone; iOS 11.4.1; Scale/3.00)',
    'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
}

params = (
    ('deviceId', '184d19d52857d3628276407b946e367d208c7c5c'),
    ('clientAgent', 'iPhone9,2/iOS/11.4.1/1242*2208'),
    ('clientType', 'iOS'),
    ('clientId', 'xapi_01'),
    ('version', '47'),
    ('_uni_source', '2.2'),
    ('appType', 'bpMobile'),
    ('serverVersion', '1'),
)

data = [
    ('_uni_source', '2.2'),
    ('appType', 'bpMobile'),
    ('authRangeType', 'store,merchant'),
    ('clientAgent', 'iPhone9,2/iOS/11.4.1/1242*2208'),
    ('clientId', 'xapi_01'),
    ('clientType', 'iOS'),
    ('deviceId', '184d19d52857d3628276407b946e367d208c7c5c'),
    ('password', 'Abc123456'),
    ('serverVersion', '1'),
    ('userName', '15973700520'),
    ('version', '47'),
]

response = requests.post('https://api.ffan.com/mapp/v1/login', headers=headers, params=params, data=data)
print(response.text)


# {
# 	"data": {
# 		"authRangeType": "store",
# 		"bwid": "",
# 		"expire": 1535716579,
# 		"identity": "商户店员角色",
# 		"loginToken": "a091049e43765fa2bd1b65d9caa5022e",
# 		"login_origin": 1,
# 		"merchantId": "10078556",
# 		"merchantName": "皇茶新世纪（益阳万达店）_10269075",
# 		"name": "周思玲",
# 		"organizationId": "627535",
# 		"organization_type_id": "5",
# 		"phone": "15973700520",
# 		"storeId": "10269075",
# 		"storeName": "皇茶新世纪（益阳万达店）",
# 		"top_organization_id": "615362",
# 		"uid": "466514",
# 		"userId": "",
# 		"userStatus": "99",
# 		"userType": "3"
# 	},
# 	"message": "登陆成功!",
# 	"msg": "",
# 	"status": 200
# }
