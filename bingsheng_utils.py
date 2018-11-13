import json
import random
import threading
import time
import tkinter
from tkinter import ttk

import requests
from tkinter import *

import yima

WXFFANTOKEN = '0fb65ff60569472082c838fbadc9ff92'
PLAZAID = 1102461
ym_username = "ye907182374"
ym_password = "baobao1515"
TOKEN = yima.ym_login(ym_username, ym_password)
ITEMID = '27894'  # 丙晟科技


def init(plazaId, ):
    global PLAZAID
    PLAZAID = plazaId


def printf(s):
    print('[%s][%s][%s]' % (threading.current_thread().getName(), time.strftime("%X"), s))


def write(path, s):
    f = open(path, "a")
    f.write('[%s][%s]\n' % (time.strftime("%X"), s.strip()))
    f.close()


def get_interval_time():
    interval_time = interval.get()
    slep = random.randint(0, int(interval_time))
    printf("本次停顿：%s秒" + slep)
    if interval_time.isdigit():
        return slep
    return 0


# 发送验证码
def send_v_code(phone):
    headers = {
        'charset': 'utf-8',
        'referer': 'https://servicewechat.com/wx07dfb5d79541eca9/104/page-frame.html',
        'content-type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; MP1503 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/44.0.2403.119 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070339) NetType/WIFI Language/zh_CN Process/appbrand0',
        'Host': 'api.beyonds.com',
    }

    data = 'mobile=%s' % phone
    response = requests.post('https://api.beyonds.com/wdmp/member/v1/sendVerifyCode', headers=headers, data=data)
    printf(response.text)


# 登录
def login(phone, code):
    headers = {
        'charset': 'utf-8',
        'referer': 'https://servicewechat.com/wx07dfb5d79541eca9/104/page-frame.html',
        'content-type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; MP1503 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/44.0.2403.119 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070339) NetType/WIFI Language/zh_CN Process/appbrand0',
        'Host': 'api.beyonds.com',
    }
    data = {
        'mobile': phone,
        'verifyCode': code,
        'wxFfanToken': WXFFANTOKEN,
        'wandaUser': '[object Object]',
        'error': '',
        'downcount': 39,
        'inter': 92,
        'phonefocus': 'true',
        'codefocus': 'false'
    }
    response = requests.post('https://api.beyonds.com/wdmp/member/v1/manualLogin', headers=headers, data=data)
    printf(response.text)


# 领取新人礼
def new_user_coupon(token, memberid, plazaId):
    headers = {
        'charset': 'utf-8',
        'appid': 'wx07dfb5d79541eca9',
        'referer': 'https://servicewechat.com/wx07dfb5d79541eca9/104/page-frame.html',
        'token': token,
        'content-type': 'application/json',
        'memberid': memberid,
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; MP1503 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/44.0.2403.119 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070339) NetType/WIFI Language/zh_CN Process/appbrand0',
        'Host': 'api.beyonds.com',
    }
    data = '{"plazaId":%s}' % plazaId
    response = requests.post('https://api.beyonds.com/wdmp/coupon/v1/newUserCoupon', headers=headers, data=data)
    printf(response.text)


# 获取免费券
def gain_free_coupon(token, memberId, productId):
    headers = {
        'Host': 'api.beyonds.com',
        'appId': 'wx07dfb5d79541eca9',
        'Accept': '*/*',
        'Accept-Language': 'zh-cn',
        'token': token,
        'Content-Type': 'application/json',
        'Referer': 'https://servicewechat.com/wx07dfb5d79541eca9/104/page-frame.html',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16B92 MicroMessenger/6.7.3(0x16070321) NetType/WIFI Language/zh_CN',
        'memberId': memberId,
    }
    data = '{"productId":%s,"channelId":1010}' % productId
    response = requests.post('https://api.beyonds.com/wdmp/coupon/v1/gainFreeCoupon', headers=headers, data=data)
    printf(response.text)


# 获取商品列表
def get_product_list(plazaId):
    headers = {
        'Host': 'api.beyonds.com',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Accept-Language': 'zh-cn',
        'Referer': 'https://servicewechat.com/wx07dfb5d79541eca9/104/page-frame.html',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16B92 MicroMessenger/6.7.3(0x16070321) NetType/WIFI Language/zh_CN',
        'appId': 'wx07dfb5d79541eca9',
    }
    params = (
        ('plazaId', plazaId),
        ('channelId', '1010'),
        ('page', '1'),
        ('limit', '100'),
        ('releaseStatus', '4'),
        ('rushFlag', '0'),
    )
    response = requests.get('https://api.beyonds.com/wdmp/product/v1/getProductList', headers=headers, params=params)
    print(response.text)
    return json.loads(response.text)


def ui():
    root = Tk()  # 创建窗口对象的背景色
    root.title('飞凡刷粉工具')
    root.geometry('320x210')

    fm1 = Frame(root)
    fm1.pack(fill=X)
    value = tkinter.StringVar()  # 窗体自带的文本，新建一个值
    comboxlist = ttk.Combobox(fm1, textvariable=value, width=15)  # 初始化
    list = get_product_list(PLAZAID)
    items = list["data"]["items"]
    tup = ()
    for i in items:
        tmp = ("%s|%s|%s" % (i["price"], i["title"], i["productId"]),)
        tup += tmp
    comboxlist["values"] = tup
    comboxlist["state"] = "readonly"
    comboxlist.current(0)
    comboxlist.pack(side=LEFT)
    label1 = Label(fm1, text='量')
    global entry1
    entry1 = Entry(fm1, width=4)
    label1.pack(side=LEFT)
    entry1.pack(side=LEFT)
    interval_label = Label(fm1, text="间隔")
    global interval
    interval = Entry(fm1, width=5)
    interval_label.pack(side=LEFT)
    interval.pack(side=LEFT)

    global s1
    s1 = Scrollbar(root)
    s1.pack(side=RIGHT, fill=Y)
    global textView
    textView = Text(root, height=10, yscrollcommand=s1.set)
    textView.pack(expand=YES, fill=X)
    s1.config(command=textView.yview)

    fm2 = Frame(root)
    fm2.pack()
    btn4 = Button(fm2, text='快新', command=kuai_xin_submit)
    btn4.pack(side=LEFT)
    btn5 = Button(fm2, text='快普', command=kuai_putong_submit)
    btn5.pack(side=LEFT)

    root.mainloop()


def kuai_putong_submit():
    printf("进行快速普通券")


def kuai_xin_submit():
    printf("进行快速新人券")


if __name__ == '__main__':
    # new_user_coupon("2431933be35f422abb6c1639f1c51075", "15000000275022050", 1102461)
    # get_product_list(1102461)
    ui()
