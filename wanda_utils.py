# 检测手机有效性
import json
import random
import threading
import time
from tkinter import *

import requests

import haima
import xunma
import yima

# 易码token
TOKEN = '00499849cbf687835af75182698438eb3c2ccdf4'
PLAZAID = ""
PROVINCE = ""
CITY = ""
PLACE = ""
EXCLUDENOS = ["170.171.172"]
TIMEOUT = 30
COUNT = 0
UID = ""
COOKIESTR = ""
PUID = ""
ITEMID = '7982'
WXFFANTOKEN = "74ab910197474826b288edd65d74393c"
xmtoken = ""
LOCK = threading.Lock()
WANDA_LOGIN_500 = 0
XM_LOCAL = ""
HM_PROVINCE = ""

headers = {
    'Host': 'api.ffan.com',
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)'
                  ' Mobile/15F79 MicroMessenger/6.7.1 NetType/4G Language/zh_CN',
    'Referer': 'https://servicewechat.com/wx07dfb5d79541eca9/81/page-frame.html',
    'Accept-Language': 'zh-cn',
}


def init(place, token, province, plazaid, hm_province, xm_local):
    global TOKEN
    if token != "":
        print("易码token：" + token)
        TOKEN = token
    global PLACE
    PLACE = place
    global PROVINCE
    PROVINCE = province
    if hm_province != "":
        global HM_PROVINCE
        HM_PROVINCE = hm_province
    if xm_local != "":
        global XM_LOCAL
        XM_LOCAL = xm_local
    global PLAZAID
    PLAZAID = plazaid
    login_result = xunma.xm_login("demon3019", "12345678", "wdVJ21MmabfWT72lAxf3JA==")
    global xmtoken
    xmtoken = login_result[0]
    print(
        "初始化值：" + TOKEN + " " + PLACE + " " + PROVINCE + " " + PLAZAID + " " + xmtoken + " " + HM_PROVINCE + " " + XM_LOCAL)


def check_phone(phone):
    headers_guanli = {
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
        ('mobileNo', phone),
        ('drainageTypeshow', 'true'),
        ('drainagedateshow', 'true'),
        ('timestr', time.time()),
    )

    response = requests.get('http://wanda.ffan.com/sail/member/list', headers=headers_guanli, params=params)
    print("检测手机号有效性：" + response.text)
    return json.loads(response.text)


def get_sms_code(mobile):
    params = (
        ('sign', 'xcx'),
    )
    data = [
        ('mobile', mobile),
    ]
    requests.post('https://api.ffan.com/wechatxmt/v1/member/verifyCode', headers=headers, params=params, data=data)
    print("发送验证码")


# 处理飞凡短信内容
def get_code(sms):
    if sms is None:
        raise RuntimeError("短信获取不到")
    if "您已经是飞凡会员" in sms:
        raise RuntimeError("该手机号已注册")
    code = sms[sms.find('，') - 8: sms.find('，')]
    pat = "[0-9]+"
    IC = re.search(pat, code)
    if IC:
        code = IC.group()
    log("验证码为：" + code)
    if code is None:
        raise RuntimeError('验证码为空')
    return code


# 飞凡小程序登录
def wanda_login(mobile, code):
    data = [
        ('mobile', mobile),
        ('verifyCode', code),
        ('plazaId', PLAZAID),
        ('source', 'MINA'),
        ('wxFfanToken', WXFFANTOKEN),
    ]
    for i in range(0, 3):
        response = requests.post('https://api.ffan.com/microapp/v1/ffanLogin', headers=headers, data=data)
        result = json.loads(response.text)
        print(result)
        if result["status"] == 200:
            global UID
            global COOKIESTR
            global PUID
            UID = result['data']['uid']
            COOKIESTR = result['data']['cookieStr']
            PUID = result['data']['puid']
            return result
        if result["status"] == 500:
            global WANDA_LOGIN_500
            WANDA_LOGIN_500 += 1
            if WANDA_LOGIN_500 > 50:
                WANDA_LOGIN_500 = 0
                raise RuntimeError("飞凡小程序登录接口有问题，请稍等一会儿再刷")
        if i >= 2:
            raise RuntimeError("登录失败")
        time.sleep(1)


# 获取商品的id,支持到100个商品
def get_product_info():
    params = (
        ('adSpaceId', 'couponList'),
        ('plazaId', PLAZAID),
        ('channelId', '1003'),
        ('type', '1001'),
        ('pageNum', '1'),
        ('pageSize', '10'),
    )
    response = requests.get('https://api.ffan.com/wechatxmt/v5/plaza/coupons', headers=headers, params=params)
    print("获取商品id" + response.text)
    result = json.loads(response.text)
    return result


# 领券
def get_coupon(productId, mobile):
    params = (
        ('cookieStr', COOKIESTR),
    )
    productInfos = '[{"productId":"' + productId + '","count":1}]'
    data = [
        ('memberId', UID),
        ('actionType', 'create'),
        ('remark', '{"orderType":"coupon","plazaId":' + PLAZAID + ',"adSpaceId":"couponList"}'),
        ('productInfos', productInfos),
        ('clientInfo', '{"clientVersion":"wx07dfb5d79541eca9","ipAddr":"","clientType":"11"}'),
        ('tradeCode', '7010'),
        ('phoneNo', mobile),
        ('paymentFlag', '0'),
        ('orderSrc', '2010'),
        ('puid', PUID),
        ('totalPrice', '0'),
        ('word_cup_2018', ''),
    ]
    url = "https://api.ffan.com/wechatxmt/v1/order/create/proxy"
    response = requests.post(url, headers=headers, params=params, data=data)
    print("领券：" + response.text)
    result = json.loads(response.text)
    if result["status"] == 5001:
        raise RuntimeError(result["message"])
    if result["status"] == 521:
        print("服务器太火爆")
        time.sleep(5)
        raise RuntimeError(result["message"])
    return result["orderNo"]


# 获取优惠券明细
def get_coupon_no(oid):
    params = (
        ('cookieStr', COOKIESTR),
        ('oid', oid),
    )
    for i in range(0, 3):
        response = requests.get('https://api.ffan.com/wechatxmt/v1/order', headers=headers, params=params)
        print("获取明细：" + response.text)
        result = json.loads(response.text)
        if result["status"] == 200 and "couponNo" in response.text:
            if result['data']['product'][0]['couponNo'] is None:
                log("订单状态：" + result['data']['status'])
                raise RuntimeError("订单未付款或者")
            return result['data']['product'][0]['couponNo']
        if i >= 2:
            raise RuntimeError("获取优惠券失败")


# 易码获取手机号和短信 phone|sms
def ym_result():
    log("从易码获取")
    EXCLUDENO = random.choice(EXCLUDENOS)
    phone = yima.ym_phone(TOKEN, ITEMID, EXCLUDENO, PROVINCE, CITY, "")
    if phone is None:
        log("获取手机号为：" + str(phone))
        raise RuntimeError("手机号获取不到")
    check_result = check_phone(phone)
    if check_result['status'] != '0000' or check_result['_metadata']['totalCount'] != 0:
        yima.ym_release(TOKEN, ITEMID, phone)
        yima.ym_ignore(TOKEN, ITEMID, phone)
        raise RuntimeError("手机号已注册过")
    get_sms_code(phone)
    sms = yima.ym_sms(TOKEN, ITEMID, phone, TIMEOUT)
    return phone + "|" + sms


# 讯码获取手机号和短信 phone|sms
def xm_result(token):
    log("从讯码获取")
    phone = xunma.xm_get_phone(token, XM_LOCAL, random.randint(1, 3))
    if phone == "release" or phone == "timeout":
        xunma.xm_logout(token)
        login_result = xunma.xm_login("demon3019", "12345678", "wdVJ21MmabfWT72lAxf3JA==")
        global xmtoken
        xmtoken = login_result[0]
        raise RuntimeError("讯码重新登录")
    if phone is None:
        log("获取手机号为：" + str(phone))
        raise RuntimeError("手机号获取不到")
    check_result = check_phone(phone)
    phone_list = phone + "-" + ITEMID + ";"
    if check_result['status'] != '0000' or check_result['_metadata']['totalCount'] != 0:
        xunma.xm_relese(token, phone_list)
        raise RuntimeError("手机号已注册过")
    get_sms_code(phone)
    time.sleep(2)
    sms = xunma.xm_sms(token, phone, TIMEOUT)
    return phone + "|" + sms


def hm_result():
    log("从海码获取")
    phone = haima.hm_phone("", HM_PROVINCE)
    if phone is None:
        raise RuntimeError("手机号获取不到")
    check_result = check_phone(phone)
    if check_result['status'] != '0000' or check_result['_metadata']['totalCount'] != 0:
        haima.hm_black(phone)
        raise RuntimeError("手机号已注册过")
    get_sms_code(phone)
    time.sleep(2)
    sms = haima.hm_sms(phone, TIMEOUT)
    return phone + "|" + sms


def phone_sms():
    # 当为1的时候从易码获取，当为其他的时候从讯码获取
    num = random.randint(1, 3)
    if num == 1:
        phone_sms_result = ym_result()
    elif num == 2:
        phone_sms_result = xm_result(xmtoken)
    else:
        phone_sms_result = hm_result()
    return phone_sms_result


def log(s):
    print(s)
    textView.insert(END, '%s\n' % s)
    textView.update()
    textView.see(END)


def write(s):
    log(s)
    f = open(FILE_PATH, "a")
    f.write('%s\n' % s.strip())
    f.close()


# 客户端规划
def ui():
    root = Tk()  # 创建窗口对象的背景色
    # 创建两个列表
    root.title('飞凡刷粉工具-' + PLACE + '万达版')
    root.geometry('600x600')
    label1 = Label(root, text='生成粉丝数量：')
    global entry1
    entry1 = Entry(root, width=100)
    label2 = Label(root, text='第一页第几个商品：')
    global entry2
    entry2 = Entry(root, width=100)
    interval_label = Label(root, text="间隔时间")
    global interval
    interval = Entry(root, width=100)
    label1.pack(expand=YES, fill=X)
    entry1.pack()
    label2.pack(expand=YES, fill=X)
    entry2.pack()
    interval_label.pack(expand=YES, fill=X)
    interval.pack()
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
    btn1 = Button(root, text='新人礼开始', command=xinren_submit)
    btn1.pack(expand=YES, fill=X)
    root.mainloop()  # 进入消息循环


def submit():
    LOCK.acquire()
    global FILE_PATH
    FILE_PATH = PLACE + "%s.txt" % time.strftime("%Y%m%d")
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
    except RuntimeError as e:
        print(e)
        log('获取失败，请确保输入参数都是整数')
    LOCK.release()


def deal(num, index):
    user = json.loads(yima.ym_user(TOKEN))
    if user["Balance"] <= 0:
        log("请联系客服，再刷粉！")
        raise RuntimeError("请联系客服，再刷粉！")
    productId = get_product_info()['data']['resource'][index - 1]['couponNo']
    global COUNT
    while COUNT < num:
        try:
            log("执行到第" + str(COUNT + 1) + "条。")
            phone_sms_result = phone_sms()
            phone_smss = phone_sms_result.split("|")
            phone = phone_smss[0]
            sms = phone_smss[1]
            code = get_code(sms)
            wanda_login(phone, code)
            oid = get_coupon(productId, phone)
            time.sleep(1)
            coupon = get_coupon_no(oid)
            write(phone + "  " + "https://api.ffan.com/qrcode/v1/qrcode?type=png&size=200&info=" + str(coupon))
            COUNT += 1
            time.sleep(get_interval_time())
        except RuntimeError as e:
            print(e)
    xunma.xm_logout(xmtoken)


def get_interval_time():
    interval_time = interval.get()
    print(interval_time)
    if interval_time.isdigit():
        return random.randint(0, int(interval_time))
    return 0


def xinren_submit():
    LOCK.acquire()
    global FILE_PATH
    FILE_PATH = PLACE + "新人礼%s.txt" % time.strftime("%Y%m%d")
    fans = entry1.get()
    index = entry2.get()
    if fans == '' or index == '':
        log('参数不能为空')
        raise RuntimeError('参数不能为空')
    try:
        num = int(entry1.get())
        if num == '' and num < 0:
            num = 0
        th = threading.Thread(target=xinren_deal, args=(num,))
        th.setDaemon(True)  # 守护线程
        th.start()
    except RuntimeError as e:
        print(e)
        log('获取失败，请确保输入参数都是整数')
    LOCK.release()


def xinren_deal(num):
    user = json.loads(yima.ym_user(TOKEN))
    if user["Balance"] <= 0:
        log("请联系客服，再刷粉！")
        raise RuntimeError("请联系客服，再刷粉！")
    global COUNT
    while COUNT < num:
        try:
            log("执行到第" + str(COUNT + 1) + "条。")
            phone_sms_result = phone_sms()
            phone_smss = phone_sms_result.split("|")
            phone = phone_smss[0]
            sms = phone_smss[1]
            code = get_code(sms)
            wanda_login(phone, code)
            time.sleep(1)
            oid = get_new_order_no(2)
            time.sleep(1)
            coupon = get_coupon_no(oid)
            write(phone + "  " + "https://api.ffan.com/qrcode/v1/qrcode?type=png&size=200&info=" + coupon)
            COUNT += 1
            time.sleep(get_interval_time())
        except RuntimeError as e:
            print(e)
            continue
    xunma.xm_logout(xmtoken)


# 获取新用户优惠券
def get_new_order_no(index):
    params = (
        ('cookieStr', COOKIESTR),
    )
    data = [
        ('plazaId', PLAZAID),
    ]
    response = requests.post('https://api.ffan.com/wechatxmt/v1/coupons-package/', headers=headers, params=params,
                             data=data)
    print("领取新用户优惠券：" + response.text)
    if ":5001" in response.text:
        raise RuntimeError("该用户已领取过")
    if "CURLE_OPERATION_TIMEDOUT" in response.text:
        raise RuntimeError("领券超时")
    result = json.loads(response.text)
    return result['data'][index]['order']['orderNo']
