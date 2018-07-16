# -*- coding: utf-8 -*-
# python3.6
from urllib import request
import time
import login
import get_code
import get_coupon
import get_coupon_info
import json
import re

header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
TOKEN = '00499849cbf687835af75182698438eb3c2ccdf4'
ITEMID = '7982'
uid = ''
cookieStr = ''
puid = ''


def get_phone():
    EXCLUDENO = ''  # 排除号段170_171
    url = 'http://api.fxhyd.cn/UserInterface.aspx?action=getmobile&token=' + TOKEN + '&itemid=' + ITEMID + '&excludeno=' + EXCLUDENO
    MOBILE = request.urlopen(request.Request(url=url, headers=header_dict)).read().decode(encoding='utf-8')
    if MOBILE.split('|')[0] == 'success':
        MOBILE = MOBILE.split('|')[1]
        print('获取号码是:\n' + MOBILE)
        return MOBILE
    else:
        print('获取TOKEN错误,错误代码' + MOBILE)
        return ''


def get_code_login(MOBILE, productId):
    get_code.get_code(MOBILE)
    WAIT = 100  # 接受短信时长60s
    url = 'http://api.fxhyd.cn/UserInterface.aspx?action=getsms&token=' + TOKEN + '&itemid=' + ITEMID + '&mobile=' + MOBILE + '&release=1'
    text1 = request.urlopen(request.Request(url=url, headers=header_dict)).read().decode(encoding='utf-8')
    TIME1 = time.time()
    TIME2 = time.time()
    ROUND = 1
    while (TIME2 - TIME1) < WAIT and not text1.split('|')[0] == "success":
        time.sleep(5)
        text1 = request.urlopen(request.Request(url=url, headers=header_dict)).read().decode(encoding='utf-8')
        TIME2 = time.time()
        ROUND = ROUND + 1

    ROUND = str(ROUND)
    text = ''
    if text1.split('|')[0] == "success":
        text = text1.split('|')[1]
        TIME = str(round(TIME2 - TIME1, 1))
        print('短信内容是' + text + '\n耗费时长' + TIME + 's,循环数是' + ROUND)
    else:
        print('获取短信超时，错误代码是' + text1 + ',循环数是' + ROUND)

    # 释放号码
    url = 'http://api.fxhyd.cn/UserInterface.aspx?action=release&token=' + TOKEN + '&itemid=' + ITEMID + '&mobile=' + MOBILE
    RELEASE = request.urlopen(request.Request(url=url, headers=header_dict)).read().decode(encoding='utf-8')
    if RELEASE == 'success':
        print('号码没有成功释放')

    # 拉黑号码
    url = 'http://api.fxhyd.cn/UserInterface.aspx?action=addignore&token=' + TOKEN + '&itemid=' + ITEMID + '&mobile=' + MOBILE
    BLACK = request.urlopen(request.Request(url=url, headers=header_dict)).read().decode(encoding='utf-8')
    if BLACK == 'success':
        print('号码没有拉黑成功')

    code = text[text.find('，') - 8: text.find('，')]
    pat = "[0-9]+"
    IC = 0
    IC = re.search(pat, code)
    if IC:
        code = IC.group()
        print("验证码是:\n" + code)
    else:
        print("请重新设置表达式")
    print("验证码为：" + code)
    result = json.loads(login.wanda_login(MOBILE, code))
    uid = result['data']['uid']
    cookieStr = result['data']['cookieStr']
    puid = result['data']['puid']
    couponResult = json.loads(get_coupon.get_coupon(uid, productId, MOBILE, cookieStr, puid))
    oid = couponResult['orderNo']
    couponInfoResult = json.loads(get_coupon_info.get_couponNo(cookieStr, oid))
    couponNo = couponInfoResult['data']['product'][0]['couponNo']
    print(MOBILE + "  " + "https://api.ffan.com/qrcode/v1/qrcode?type=png&size=200&info=" + couponNo)


if __name__ == '__main__':
    # print('开始')
    for i in range(0, 10):
        mobile = ''
        try:
            mobile = get_phone()
            get_code_login(mobile, '20180713184317')
        except:
            print(mobile)
            continue
