# -*- coding: utf-8 -*-
# python3.6
import threading
from tkinter import *
from urllib import request
import time
import json
import re
import requests

headers = {
    'Host': 'api.ffan.com',
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15F79 MicroMessenger/6.7.1 NetType/4G Language/zh_CN',
    'Referer': 'https://servicewechat.com/wx07dfb5d79541eca9/81/page-frame.html',
    'Accept-Language': 'zh-cn',
}
header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
TOKEN = '007711720862de70a346fc1788db353c18c5d478'
plazaId = '1000266'
ITEMID = '7982'
count = 0
province = '210000'
place = '沈阳铁西'
lock = threading.Lock()


def log(s):
    print(s)
    textView.insert(END, '%s\n' % s)
    textView.update()
    textView.see(END)


def write(s):
    f = open(file_path, "a")
    f.write('%s\n' % s)
    f.close()


def log_err(s):
    textView.insert(END, '%s\n' % s)
    textView.update()
    textView.see(END)


def get_phone():
    EXCLUDENO = '170.171.172'  # 排除号段170_171
    url = 'http://api.fxhyd.cn/UserInterface.aspx?action=getmobile&token=' + TOKEN + '&itemid=' + ITEMID + '&excludeno=' + EXCLUDENO
    MOBILE = request.urlopen(request.Request(url=url, headers=header_dict)).read().decode(encoding='utf-8')
    print(MOBILE)
    if MOBILE.split('|')[0] == 'success':
        MOBILE = MOBILE.split('|')[1]
        log('获取手机号：' + MOBILE)
        result = json.loads(check_phone(MOBILE))
        if result['status'] == '0000' and result['_metadata']['totalCount'] == 0:
            return MOBILE
        else:
            # # 释放号码
            url = 'http://api.fxhyd.cn/UserInterface.aspx?action=release&token=' + TOKEN + '&itemid=' + ITEMID + '&mobile=' + MOBILE
            RELEASE = request.urlopen(request.Request(url=url, headers=header_dict)).read().decode(encoding='utf-8')
            if RELEASE == 'success':
                log('号码成功释放')
            # # 拉黑号码
            url = 'http://api.fxhyd.cn/UserInterface.aspx?action=addignore&token=' + TOKEN + '&itemid=' + ITEMID + '&mobile=' + MOBILE
            BLACK = request.urlopen(request.Request(url=url, headers=header_dict)).read().decode(encoding='utf-8')
            if BLACK == 'success':
                log('号码拉黑成功')
            return get_phone()
    else:
        log('获取不到手机号')
        return ''


def check_phone(mobile):
    cookies = {
        'sajssdk_2015_cross_new_user': '1',
        'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22lidi%22%2C%22%24device_id%22%3A%22164c642c5b7407-048ae012493e02-163b6952-1296000-164c642c5b837%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22164c642c5b7407-048ae012493e02-163b6952-1296000-164c642c5b837%22%7D',
        'JSESSIONID': 'D2D363A9F90B81D759A3166D770E5B2C',
    }

    headers = {
        'Host': 'wanda.ffan.com',
        'code': '1104483',
        'orgname': '%E5%9B%9E%E6%B0%91%E5%8C%BA%E4%B8%87%E8%BE%BE%E5%B9%BF%E5%9C%BA',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'tenantId': '2017092600001',
        'Accept': 'application/json, text/plain, */*',
        'username': '%E6%9D%8E%E8%BF%AA',
        'orgcode': '1104483',
        'orgTypeCode': '10003',
        'workingOrgCode': '1104483',
        'token': 'MjMzNTcxMzM4MTg5NTM3Mjgw',
        'orgTypeName': '%E5%B9%BF%E5%9C%BA',
        'Referer': 'http://wanda.ffan.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6',
    }

    params = (
        ('pageIndex', '1'),
        ('pageSize', '10'),
        ('scopes[]', 'DQFquanjituan'),
        ('scope', 'DQFquanjituan'),
        ('orgType', '10001'),
        ('mobileNo', mobile),
        ('wechatBind', '3'),
        ('drainageTypeshow', 'false'),
        ('drainagedateshow', 'false'),
        ('timestr', time.time()),
    )

    response = requests.get('http://wanda.ffan.com/sail/member/list', headers=headers, params=params, cookies=cookies)
    result = response.text
    print("验证手机号是否可用" + result)
    return result


# 获取验证码
def get_code(mobile):
    params = (
        ('sign', 'xcx'),
    )

    data = [
        ('mobile', mobile),
    ]

    requests.post('https://api.ffan.com/wechatxmt/v1/member/verifyCode', headers=headers, params=params, data=data)


# 飞凡登录
def wanda_login(mobile, code):
    data = [
        ('mobile', mobile),
        ('verifyCode', code),
        ('plazaId', plazaId),
        ('source', 'MINA'),
        ('wxFfanToken', '74ab910197474826b288edd65d74393c'),
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
            else:
                raise RuntimeError("登录失败")
    return result


# 获取新用户优惠券
def get_order_no(cookieStr):
    params = (
        ('cookieStr', cookieStr),
    )

    data = [
        ('plazaId', plazaId),
    ]

    response = requests.post('https://api.ffan.com/wechatxmt/v1/coupons-package/', headers=headers, params=params,
                             data=data)
    print("获取订单号：" + response.text)
    return response.text


# 获取指定优惠券
def get_coupon(memberId, productId, mobile, cookieStr, puid):
    params = (
        ('cookieStr', cookieStr),
    )
    productInfos = '[{"productId":"' + productId + '","count":1}]'

    data = [
        ('memberId', memberId),
        ('actionType', 'create'),
        ('remark', '{"orderType":"coupon","plazaId":' + plazaId + ',"adSpaceId":"couponList"}'),
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
    params = (
        ('adSpaceId', 'couponList'),
        ('plazaId', plazaId),
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
    WAIT = 30  # 接受短信时长60s
    url = 'http://api.fxhyd.cn/UserInterface.aspx?action=getsms&token=' + TOKEN + '&itemid=' + ITEMID + '&mobile=' + MOBILE + '&release=1'
    text1 = request.urlopen(request.Request(url=url, headers=header_dict)).read().decode(encoding='utf-8')
    TIME1 = time.time()
    TIME2 = time.time()
    ROUND = 1
    while (TIME2 - TIME1) < WAIT and not text1.split('|')[0] == "success":
        time.sleep(2)
        print(text1)
        text1 = request.urlopen(request.Request(url=url, headers=header_dict)).read().decode(encoding='utf-8')
        TIME2 = time.time()
        ROUND = ROUND + 1

    ROUND = str(ROUND)
    text = ''
    if text1.split('|')[0] == "success":
        text = text1.split('|')[1]
        TIME = str(round(TIME2 - TIME1, 1))
        log('短信内容是' + text + '\n耗费时长' + TIME + 's,循环数是' + ROUND)
    else:
        log('获取短信超时，错误代码是' + text1 + ',循环数是' + ROUND)

    # # 释放号码
    url = 'http://api.fxhyd.cn/UserInterface.aspx?action=release&token=' + TOKEN + '&itemid=' + ITEMID + '&mobile=' + MOBILE
    RELEASE = request.urlopen(request.Request(url=url, headers=header_dict)).read().decode(encoding='utf-8')
    if RELEASE == 'success':
        log('号码成功释放')

    # # 拉黑号码
    url = 'http://api.fxhyd.cn/UserInterface.aspx?action=addignore&token=' + TOKEN + '&itemid=' + ITEMID + '&mobile=' + MOBILE
    BLACK = request.urlopen(request.Request(url=url, headers=header_dict)).read().decode(encoding='utf-8')
    if BLACK == 'success':
        log('号码拉黑成功')

    # if '欢迎注册飞凡会员' not in text:
    #     raise RuntimeError('该会员已经是注册用户')
    code = text[text.find('，') - 8: text.find('，')]
    pat = "[0-9]+"
    IC = re.search(pat, code)
    if IC:
        code = IC.group()

    log("验证码为：" + code)
    if code is None:
        raise RuntimeError('验证码为空')

    # 模拟飞凡小程序登录
    result = json.loads(wanda_login(MOBILE, code))
    uid = result['data']['uid']
    cookieStr = result['data']['cookieStr']
    puid = result['data']['puid']
    # 获取第一页的第几个商品id
    productId = json.loads(get_product_info())['data']['resource'][index - 1]['couponNo']
    # 领取商品id的优惠券，生成订单号
    # couponResult = json.loads(get_order_no(cookieStr))
    # oid = couponResult['data'][0]['order']['orderNo']
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
    if couponNo is None:
        couponInfoResult = json.loads(get_couponNo(cookieStr, oid))
        couponNo = couponInfoResult['data']['product'][0]['couponNo']
        if couponNo is None:
            raise RuntimeError("优惠券为null")

    log(MOBILE + "  " + "https://api.ffan.com/qrcode/v1/qrcode?type=png&size=200&info=" + couponNo)
    write(MOBILE + "  " + "https://api.ffan.com/qrcode/v1/qrcode?type=png&size=200&info=" + couponNo)


def deal(num, index):
    global count
    lock.acquire()
    while count < num:
        try:
            log("执行到第" + str(count + 1) + "条。")
            mobile = get_phone()
            if mobile == '':
                continue
            get_code_login(mobile, index)
            count += 1
        except RuntimeError as e:
            print(e)
    lock.release()


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

        th = threading.Thread(target=deal, args=(num, index,))
        th.setDaemon(True)  # 守护线程
        th.start()
        # deal(num, index)
    except RuntimeError as e:
        print(e)
        log('获取失败，请确保输入参数都是整数')


def ui():
    root = Tk()  # 创建窗口对象的背景色
    # 创建两个列表
    root.title('飞凡刷粉工具-' + place + '万达版')
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
    file_path = place + '%s.txt' % time.strftime("%Y%m%d")
    print(file_path)
    ui()
    # get_phone()
