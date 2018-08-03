import json
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
        ('storeId', '10157953'),
        ('uid', '349235'),
        ('merchantId', '10069936'),
        ('loginToken', 'f00eac6e6d964ae09f2c7e9da7b77ec4'),
        ('deviceId', '184d19d52857d3628276407b946e367d208c7c5d'),
        ('username', '17681697772'),
        ('telephone', '17681697772'),
        ('clientType', 'iOS'),
        ('clientId', 'xapi_01'),
        ('version', '47'),
        ('_uni_source', '2.2'),
        ('appType', 'bpMobile'),
        ('serverVersion', '1'),
        ('clientAgent', 'iPhone9,2/iOS/11.4/1242*2208'),
    )

    data = [
        ('_uni_source', '2.2'),
        ('appType', 'bpMobile'),
        ('app_time', '225678871954'),
        ('app_verification_native', get_random()),
        ('certificateno', code),
        ('checkDevice', '1'),
        ('clientAgent', 'iPhone9,2/iOS/11.4/1242*2208'),
        ('clientId', 'xapi_01'),
        ('clientType', 'iOS'),
        ('deviceId', '184d19d52857d3628276407b946e367d208c7c5d'),
        ('loginToken', 'f00eac6e6d964ae09f2c7e9da7b77ec4'),
        ('merchantId', '10069936'),
        ('serverVersion', '1'),
        ('sign', 'd93ed5cce015bc859fadcf0856329194'),
        ('storeId', '10157953'),
        ('telephone', '17681697772'),
        ('uid', '349235'),
        ('username', '17681697772'),
        ('version', '47'),
    ]

    response = requests.post('https://sop.ffan.com/goods/coupon/queryUnusedCoupons', headers=headers, params=params,
                             data=data)
    print(response.text)

    cookies1 = {
        'PHPSESSID': 'hq7illp5s8u0m3nk89m2f57v67',
    }

    params1 = (
        ('storeId', '10157953'),
        ('clientType', 'iOS'),
        ('uid', '349235'),
        ('clientId', 'xapi_01'),
        ('version', '47'),
        ('_uni_source', '2.2'),
        ('merchantId', '10069936'),
        ('loginToken', 'f00eac6e6d964ae09f2c7e9da7b77ec4'),
        ('deviceId', '184d19d52857d3628276407b946e367d208c7c5d'),
        ('appType', 'bpMobile'),
        ('username', '17681697772'),
        ('serverVersion', '1'),
        ('clientAgent', 'iPhone9,2/iOS/11.4.1/1242*2208'),
        ('telephone', '17681697772'),
    )

    data1 = [
        ('_uni_source', '2.2'),
        ('appType', 'bpMobile'),
        ('app_time', '239664188372'),
        ('app_verification_native', get_random()),
        ('certificateno', code),
        ('clientAgent', 'iPhone9,2/iOS/11.4.1/1242*2208'),
        ('clientId', 'xapi_01'),
        ('clientType', 'iOS'),
        ('deviceId', '184d19d52857d3628276407b946e367d208c7c5d'),
        ('loginToken', 'f00eac6e6d964ae09f2c7e9da7b77ec4'),
        ('memberId', '15000000371991724'),
        ('merchantId', '10069936'),
        ('serverVersion', '1'),
        ('sign', '2f3c58a64f979908830fd91fa989f77e'),
        ('storeId', '10157953'),
        ('telephone', '17681697772'),
        ('uid', '349235'),
        ('userId', '349235'),
        ('username', '17681697772'),
        ('version', '47'),
    ]

    response = requests.post('https://sop.ffan.com/goods/coupon/checkCoupon', headers=headers, params=params1,
                             cookies=cookies1, data=data1)
    result = response.text
    if json.loads(result)['status'] != 200:
        raise RuntimeError("已验证过")
    print(result)


if __name__ == '__main__':
    # scan('088003966832')
    file = open("/Users/demon/Desktop/fan/huzhou/2.txt", 'r')
    index = 0
    t1 = time.time()
    while True:
        try:
            index += 1
            mystr = file.readline()
            if not mystr:
                break
            print(str(index) + "  " + mystr, end='')
            code = mystr[mystr.find('info=') + 5: mystr.find('info=') + 17]
            print(code)
            scan(code)
            sleeptime = random.randint(10, 60)
            print("本次停顿：" + str(sleeptime))
            time.sleep(sleeptime)
            print(str(index) + "次耗时" + str(time.time() - t1))
        except RuntimeError as e:
            print(e)
            continue

    t2 = time.time()
    print("总共使用：" + str(t2 - t1))
