import time
from urllib import request

import requests

TOKEN = '007373010e787df886c6a246f5877fec161a9316'
ITEMID = '7982'


def get_old_phone(oldphone):
    url = 'http://api.fxhyd.cn/UserInterface.aspx?action=getmobile&token=' + TOKEN + '&itemid=' + ITEMID + '&mobile=' + oldphone
    MOBILE = request.urlopen(request.Request(url=url)).read().decode(encoding='utf-8')
    print(MOBILE)
    if MOBILE.split('|')[0] == 'success':
        MOBILE = MOBILE.split('|')[1]
        print('获取手机号：' + MOBILE)
        return MOBILE
    else:
        print('获取不到手机号')
        return ''


def checkout_coupon(phone):
    headers = {
        'tenantId': '2017092600001',
        'Accept': 'application/json, text/plain, */*',
        'userid': '131737550254505984',
        'orgcode': '1000769',
        'token': 'MjM1MDU5MjY1Nzg0NTEyNTEy',
    }

    params = (
        ('orgId', '1000769'),
        ('tenantId', '2017092600001'),
        ('pageNum', '1'),
        ('pageSize', '10'),
        ('mobile', phone),
        ('status', '1'),
        ('buyBeginTime', '1533962271000'),
        ('buyEndTime', '1534048671000'),
        ('timestr', time.time()),
    )

    response = requests.get('http://wanda.ffan.com/sail/marketing/coupons/records', headers=headers, params=params)
    print(response.text)


if __name__ == '__main__':
    # checkout_coupon("18815150996")
    f = open("平阳2018-08-012018-09-01.txt", "r")
    index = 0
    while True:
        index += 1
        mystr = f.readline()
        if not mystr:
            break
        print(str(index) + "  " + mystr)
        result = get_old_phone("13666997306")
        if result != '':
            break
