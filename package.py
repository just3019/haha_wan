# -*- coding: utf-8 -*-
# python3.6

from tkinter import *
from urllib import request
import time
import json
import re
import requests

header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
TOKEN = '00499849cbf687835af75182698438eb3c2ccdf4'
ITEMID = '7982'


def log(s):
    print(s)
    textView.insert(END, '%s\n' % s)
    textView.update()
    textView.see(END)
    f = open(file_path, "a")
    f.write('%s\n' % s)
    f.close()


def log_err(s):
    textView.insert(END, '%s\n' % s)
    textView.update()
    textView.see(END)


# num生成多少个粉丝，index下表
def submit():
    fans = entry1.get()
    index = entry2.get()
    if fans == '' or index == '':
        log('参数不能为空')
        raise RuntimeError('参数不能为空')
    try:
        num = int(entry1.get())
        if num == '' and num < 0:
            num = 0
        index = int(entry2.get())
        if index == '' and index < 0:
            index = 0
        deal(num, index)
    except:
        log('获取失败，请确保输入参数都是整数')


def get_phone():
    EXCLUDENO = ''  # 排除号段170_171
    url = 'http://api.fxhyd.cn/UserInterface.aspx?action=getmobile&token=' + TOKEN + '&itemid=' + ITEMID + '&excludeno=' + EXCLUDENO
    MOBILE = request.urlopen(request.Request(url=url, headers=header_dict)).read().decode(encoding='utf-8')
    if MOBILE.split('|')[0] == 'success':
        MOBILE = MOBILE.split('|')[1]
        print('获取手机号：' + MOBILE)
        return MOBILE
    else:
        print('获取不到手机号')
        return ''


# 获取验证码
def get_code(mobile):
    headers = {
        'Host': 'api.ffan.com',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15F79 MicroMessenger/6.7.1 NetType/WIFI Language/zh_CN',
        'Referer': 'https://servicewechat.com/wx07dfb5d79541eca9/81/page-frame.html',
        'Accept-Language': 'zh-cn',
    }

    params = (
        ('sign', 'xcx'),
    )

    data = [
        ('mobile', mobile),
    ]

    requests.post('https://api.ffan.com/wechatxmt/v1/member/verifyCode', headers=headers, params=params, data=data)


# 飞凡登录
def wanda_login(mobile, code):
    import requests

    headers = {
        'Host': 'api.ffan.com',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15F79 MicroMessenger/6.7.1 NetType/WIFI Language/zh_CN',
        'Referer': 'https://servicewechat.com/wx07dfb5d79541eca9/81/page-frame.html',
        'Accept-Language': 'zh-cn',
    }

    data = [
        ('mobile', mobile),
        ('verifyCode', code),
        ('plazaId', '1000770'),
        ('source', 'MINA'),
        ('wxFfanToken', '6cc7fda5c8674951b446126226ac51ac'),
        ('wandaUser', '[object Object]'),
        ('error', ''),
        ('downcount', '60'),
        ('inter', 'null'),
        ('phonefocus', 'false'),
        ('codefocus', 'false'),
    ]

    response = requests.post('https://api.ffan.com/microapp/v1/ffanLogin', headers=headers, data=data)
    result = response.text
    print(result)
    status = json.loads(result)['status']
    if status != 200:
        for i in range(0, 3):
            response = requests.post('https://api.ffan.com/microapp/v1/ffanLogin', headers=headers, data=data)
            result = response.text
            print(result)
            status = json.loads(result)['status']
            if status == 200:
                break
    return result


def get_coupon(memberId, productId, mobile, cookieStr, puid):
    productInfos = '[{"productId":"' + productId + '","count":1}]'
    headers = {
        'Host': 'api.ffan.com',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15F79 MicroMessenger/6.7.1 NetType/4G Language/zh_CN',
        'Referer': 'https://servicewechat.com/wx07dfb5d79541eca9/81/page-frame.html',
        'Accept-Language': 'zh-cn',
    }

    params = (
        ('cookieStr', cookieStr),
    )

    data = [
        ('memberId', memberId),
        ('actionType', 'create'),
        ('remark', '{"orderType":"coupon","plazaId":1000769,"adSpaceId":"couponList"}'),
        ('productInfos', productInfos),
        ('clientInfo', '{"clientVersion":"wx07dfb5d79541eca9","ipAddr":"","clientType":"11"}'),
        ('tradeCode', '7010'),
        ('phoneNo', mobile),
        ('paymentFlag', '0'),
        ('orderSrc', '2010'),
        ('puid', puid),
        ('totalPrice', '0'),
        ('word_cup_2018', ''),
    ]

    response = requests.post('https://api.ffan.com/wechatxmt/v1/order/create/proxy', headers=headers, params=params,
                             data=data)
    result = response.text
    print("领券：" + result)
    return result


# 获取优惠券明细
def get_couponNo(cookieStr, oid):
    headers = {
        'Host': 'api.ffan.com',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15F79 MicroMessenger/6.7.1 NetType/WIFI Language/zh_CN',
        'Referer': 'https://servicewechat.com/wx07dfb5d79541eca9/81/page-frame.html',
        'Accept-Language': 'zh-cn',
    }

    params = (
        ('cookieStr', cookieStr),
        ('oid', oid),
    )

    response = requests.get('https://api.ffan.com/wechatxmt/v1/order', headers=headers, params=params)
    result = response.text
    print("获取明细：" + result)
    return result


# 获取商品的id
def get_product_info():
    headers = {
        'Host': 'api.ffan.com',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15F79 MicroMessenger/6.7.1 NetType/WIFI Language/zh_CN',
        'Referer': 'https://servicewechat.com/wx07dfb5d79541eca9/83/page-frame.html',
        'Accept-Language': 'zh-cn',
    }

    params = (
        ('adSpaceId', 'couponList'),
        ('plazaId', '1000769'),
        ('channelId', '1003'),
        ('type', '1001'),
        ('pageNum', '1'),
        ('pageSize', '10'),
    )

    response = requests.get('https://api.ffan.com/wechatxmt/v5/plaza/coupons', headers=headers, params=params)

    result = response.text
    print("获取商品id" + result)
    return result


def get_code_login(MOBILE, index):
    get_code(MOBILE)
    WAIT = 60  # 接受短信时长60s
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
    if text1.split('|')[0] == "success":
        text = text1.split('|')[1]
        TIME = str(round(TIME2 - TIME1, 1))
        print('短信内容是' + text + '\n耗费时长' + TIME + 's,循环数是' + ROUND)
    else:
        print('获取短信超时，错误代码是' + text1 + ',循环数是' + ROUND)

    # # 释放号码
    url = 'http://api.fxhyd.cn/UserInterface.aspx?action=release&token=' + TOKEN + '&itemid=' + ITEMID + '&mobile=' + MOBILE
    RELEASE = request.urlopen(request.Request(url=url, headers=header_dict)).read().decode(encoding='utf-8')
    if RELEASE == 'success':
        print('号码成功释放')

    # # 拉黑号码
    url = 'http://api.fxhyd.cn/UserInterface.aspx?action=addignore&token=' + TOKEN + '&itemid=' + ITEMID + '&mobile=' + MOBILE
    BLACK = request.urlopen(request.Request(url=url, headers=header_dict)).read().decode(encoding='utf-8')
    if BLACK == 'success':
        print('号码拉黑成功')

    code = text[text.find('，') - 8: text.find('，')]
    pat = "[0-9]+"
    IC = re.search(pat, code)
    if IC:
        code = IC.group()

    print("验证码为：" + code)

    # 模拟飞凡小程序登录
    result = json.loads(wanda_login(MOBILE, code))
    uid = result['data']['uid']
    cookieStr = result['data']['cookieStr']
    puid = result['data']['puid']
    # 获取第一页的第几个商品id
    productId = json.loads(get_product_info())['data']['resource'][index - 1]['couponNo']
    # 领取商品id的优惠券，生成订单号
    couponResult = json.loads(get_coupon(uid, productId, MOBILE, cookieStr, puid))
    oid = couponResult['orderNo']
    # 获取订单号下对应的优惠券信息
    couponInfoResult = json.loads(get_couponNo(cookieStr, oid))
    # 处理没有成功拿到优惠券操作
    if couponInfoResult['status'] != 200:
        json.loads(wanda_login(MOBILE, code))
        cookieStr = result['data']['cookieStr']
        couponInfoResult = json.loads(get_couponNo(cookieStr, oid))
    couponNo = couponInfoResult['data']['product'][0]['couponNo']
    log(MOBILE + "  " + "https://api.ffan.com/qrcode/v1/qrcode?type=png&size=200&info=" + couponNo)


def deal(num, index):
    for i in range(0, num):
        mobile = ''
        try:
            mobile = get_phone()
            if mobile == '':
                continue
            get_code_login(mobile, index)
        except:
            print(mobile)
            continue


def ui():
    root = Tk()  # 创建窗口对象的背景色
    # 创建两个列表
    root.title('飞凡刷粉工具-平阳万达版')
    root.geometry('600x600')
    label1 = Label(root, text='生成粉丝数量：')
    global entry1
    entry1 = Entry(root, width=100)
    label2 = Label(root, text='第一页第几个商品：')
    global entry2
    entry2 = Entry(root, width=100)
    label1.pack(expand=YES, fill=X)
    entry1.pack()
    label2.pack(expand=YES, fill=X)
    entry2.pack()
    global s1
    s1 = Scrollbar(root)
    s1.pack(side=RIGHT, fill=Y)
    global textView
    textView = Text(root, width=400, height=20, yscrollcommand=s1.set)

    label3 = Label(root, text='日志输出：')  # '
    label3.pack()
    textView.pack(expand=YES, fill=X)
    s1.config(command=textView.yview)
    btn = Button(root, text='开始', command=submit)
    btn.pack(expand=YES, fill=X)
    root.mainloop()  # 进入消息循环


if __name__ == '__main__':
    global file_path
    file_path = '%s.txt' % time.strftime("%Y%m%d%H%M")
    ui()
