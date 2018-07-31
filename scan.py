import random

import requests
import time

headers = {
    'Host': 'sop.ffan.com',
    'Accept': '*/*',
    'User-Agent': 'com.dianshang.feifanbp/2.0.1 (iPhone; iOS 11.4; Scale/3.00)',
    'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
}


def get_random():
    ran = random.randint(100000, 999999)
    print(str(ran))
    return str(ran)


def scan(code):
    params = (
        ('', ''),
        ('storeId', '10249638'),
        ('clientType', 'iOS'),
        ('uid', '403504'),
        ('clientId', 'xapi_01'),
        ('version', '47'),
        ('_uni_source', '2.2'),
        ('merchantId', '10077248'),
        ('loginToken', '25b415356f00fed9057f580a2e0888c4'),
        ('deviceId', '184d19d52857d3628276407b946e367d208c7c5d'),
        ('appType', 'bpMobile'),
        ('username', '\u738B\u8D85'),
        ('serverVersion', '1'),
        ('clientAgent', 'iPhone9,2/iOS/11.4/1242*2208'),
        ('telephone', '18888888888'),
    )

    data = [
        ('_uni_source', '2.2'),
        ('appType', 'bpMobile'),
        ('app_time', '692546985281'),
        ('app_verification_native', get_random()),
        ('certificateno', code),
        ('checkDevice', '1'),
        ('clientAgent', 'iPhone9,2/iOS/11.4/1242*2208'),
        ('clientId', 'xapi_01'),
        ('clientType', 'iOS'),
        ('deviceId', '184d19d52857d3628276407b946e367d208c7c5d'),
        ('loginToken', '25b415356f00fed9057f580a2e0888c4'),
        ('merchantId', '10077248'),
        ('serverVersion', '1'),
        ('sign', '2b82ce122332d91136603ed35187118a'),
        ('storeId', '10249638'),
        ('telephone', '18888888888'),
        ('uid', '403504'),
        ('username', '%E7%8E%8B%E8%B6%85'),
        ('version', '47'),
    ]

    response = requests.post('https://sop.ffan.com/goods/coupon/queryUnusedCoupons', headers=headers, params=params,
                             data=data)
    print(response.text)

    cookies1 = {
        'PHPSESSID': 'hq7illp5s8u0m3nk89m2f57v67',
    }

    params1 = (
        ('storeId', '10249638'),
        ('clientType', 'iOS'),
        ('uid', '403504'),
        ('clientId', 'xapi_01'),
        ('version', '47'),
        ('_uni_source', '2.2'),
        ('merchantId', '10077248'),
        ('loginToken', '25b415356f00fed9057f580a2e0888c4'),
        ('deviceId', '184d19d52857d3628276407b946e367d208c7c5d'),
        ('appType', 'bpMobile'),
        ('username', '\u738B\u8D85'),
        ('serverVersion', '1'),
        ('clientAgent', 'iPhone9,2/iOS/11.4/1242*2208'),
        ('telephone', '18888888888'),
    )

    data1 = [
        ('_uni_source', '2.2'),
        ('appType', 'bpMobile'),
        ('app_time', '694629071718'),
        ('app_verification_native', get_random()),
        ('certificateno', code),
        ('clientAgent', 'iPhone9,2/iOS/11.4/1242*2208'),
        ('clientId', 'xapi_01'),
        ('clientType', 'iOS'),
        ('deviceId', '184d19d52857d3628276407b946e367d208c7c5d'),
        ('loginToken', '25b415356f00fed9057f580a2e0888c4'),
        ('memberId', '15000000371471409'),
        ('merchantId', '10077248'),
        ('serverVersion', '1'),
        ('sign', '84e7f693485c7add1cf6eeb33f80d41c'),
        ('storeId', '10249638'),
        ('telephone', '18888888888'),
        ('uid', '403504'),
        ('userId', '403504'),
        ('username', '%E7%8E%8B%E8%B6%85'),
        ('version', '47'),
    ]

    response = requests.post('https://sop.ffan.com/goods/coupon/checkCoupon', headers=headers, params=params1,
                             cookies=cookies1, data=data1)
    print(response.text)


if __name__ == '__main__':
    # scan('088003966832')
    file = open("/Users/demon/Desktop/fan/jixi/3.txt", 'r')
    index = 0
    while True:
        index += 1
        mystr = file.readline()
        if not mystr:
            break
        print(str(index) + "  " + mystr, end='')
        code = mystr[mystr.find('info=') + 5: mystr.find('info=') + 17]
        print(code)
        scan(code)
        time.sleep(random.randint(2, 5))
