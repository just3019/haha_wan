import requests

headers = {
    'charset': 'utf-8',
    'referer': 'https://servicewechat.com/wx57ebde74de5e6267/6/page-frame.html',
    'workingorgcode': '100004997',
    'tenantid': '2018092600001',
    'token': 'MjY5NDcwMzQzNjY3OTAwNDE2',
    'userid': '266207569143951360',
    'content-type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; MP1503 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/44.0.2403.119 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070339) NetType/WIFI Language/zh_CN Process/appbrand0',
    'Host': 'api.beyonds.com',
}

params = (
    ('couponCode', '073504770792'),
)

response = requests.get('https://api.beyonds.com/wpxe/v1/coupon/getCodeDetail', headers=headers, params=params)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://api.beyonds.com/wpxe/v1/coupon/getCodeDetail?couponCode=073504770792', headers=headers)
