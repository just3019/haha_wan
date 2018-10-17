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
import yunxiang

# 平台标识：1，易码 2，讯码 3，海码 4，云享
ym_username = "ye907182374"
ym_password = "baobao1515"
TOKEN = yima.ym_login(ym_username, ym_password)
# TOKEN = "00499849c00c557b7598dda4ebaeed5b1e30f8d5e701"
PLAZAID = ""
PROVINCE = ""
CITY = ""
PLACE = ""
EXCLUDENOS = ["170.171.172"]
TIMEOUT = 60
COUNT = 0
SUCCESS_COUNT = 0
ITEMID = '7982'
XM_ITEMID = "3410"
WXFFANTOKEN = "ddde88c336cb4030b9b81ad2f44febf5"
xmtoken = ""
LOCK = threading.Lock()
WANDA_LOGIN_500 = 0
XM_LOCAL = ""
HM_PROVINCE = ""
not_eq = 0
QRCODE_URL = "https://api.ffan.com/qrcode/v1/qrcode?type=png&size=200&info="
yunxiang.yx_login()

headers = {
    'Host': 'api.ffan.com',
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A366 MicroMessenger/6.7.3(0x16070321) NetType/WIFI Language/zh_CN',
    'Referer': 'https://servicewechat.com/wx07dfb5d79541eca9/92/page-frame.html',
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
    # print("检测手机号有效性：" + response.text)
    return json.loads(response.text)


def get_sms_code(mobile):
    params = (
        ('sign', 'xcx'),
    )
    data = {
        'mobile': mobile
    }
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
    print("验证码为：" + code)
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
        data = result["data"]
        if result["status"] == 200 and "uid" in data and "cookieStr" in data and "puid" in data:
            return data
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
def get_coupon(productId, mobile, cookieStr, uid, puid):
    params = (
        ('cookieStr', cookieStr),
    )
    productInfos = '[{"productId":"' + productId + '","count":1}]'
    data = [
        ('memberId', uid),
        ('actionType', 'create'),
        ('remark', '{"orderType":"coupon","plazaId":' + PLAZAID + ',"adSpaceId":"couponList"}'),
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
def get_coupon_no(oid, cookieStr):
    params = (
        ('cookieStr', cookieStr),
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
    # log("从易码获取")
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
    # log("从讯码获取")
    phone = xunma.xm_get_phone(token, XM_LOCAL, 0)
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
    black_phone_list = ITEMID + "-" + phone + ";"
    if check_result['status'] != '0000' or check_result['_metadata']['totalCount'] != 0:
        xunma.xm_relese(token, phone_list)
        xunma.xm_black(token, black_phone_list)
        raise RuntimeError("手机号已注册过")
    get_sms_code(phone)
    time.sleep(2)
    sms = xunma.xm_sms(token, phone, TIMEOUT)
    return phone + "|" + sms


def hm_result():
    # log("从海码获取")
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


def yx_result():
    phone = yunxiang.yx_phone()
    if phone is None:
        raise RuntimeError("手机号码获取不到")
    check_result = check_phone(phone)
    if check_result['status'] != '0000' or check_result['_metadata']['totalCount'] != 0:
        yunxiang.yx_relese(phone)
        yunxiang.yx_black(phone)
        raise RuntimeError("手机号已注册过")
    get_sms_code(phone)
    time.sleep(2)
    sms = yunxiang.yx_sms(phone, TIMEOUT)
    return phone + "|" + sms


def phone_sms():
    # 当为1的时候从易码获取，当为其他的时候从讯码获取
    global not_eq
    num = random.randint(1, 4)
    if num == 1 and num != not_eq:
        phone_sms_result = ym_result()
        print("本次易码获取号码")
        not_eq = 1
    elif num == 2 and num != not_eq:
        phone_sms_result = xm_result(xmtoken)
        print("本次讯码获取号码")
        not_eq = 2
    elif num == 3 and num != not_eq:
        phone_sms_result = hm_result()
        print("本次海码获取号码")
        not_eq = 3
    elif num == 4 and num != not_eq:
        phone_sms_result = yx_result()
        print("本次云享获取号码")
        not_eq = 4
    else:
        raise RuntimeError("重新选平台")
    return phone_sms_result


def log(s):
    print(s)
    textView.insert(END, '[%s] [%s] %s\n' % (threading.current_thread().name, time.ctime(), s))
    textView.update()
    textView.see(END)


def write(s):
    f = open(FILE_PATH, "a")
    f.write('%s\n' % s.strip())
    f.close()


# 客户端规划
def ui():
    root = Tk()  # 创建窗口对象的背景色
    # 创建两个列表
    root.title('飞凡刷粉工具-' + PLACE + '万达版')
    root.geometry('600x600')
    fm1 = Frame(root)
    fm1.pack(fill=X)

    label1 = Label(fm1, text='生成数量：')
    global entry1
    entry1 = Entry(fm1, width=10)

    label2 = Label(fm1, text='第几个商品：')
    global entry2
    entry2 = Entry(fm1, width=10)
    label1.pack(side=LEFT)
    entry1.pack(side=LEFT)
    label2.pack(side=LEFT)
    entry2.pack(side=LEFT)

    interval_label = Label(fm1, text="间隔时间")
    global interval
    interval = Entry(fm1, width=10)
    interval_label.pack(side=LEFT)
    interval.pack(side=LEFT)

    global s1
    s1 = Scrollbar(root)
    s1.pack(side=RIGHT, fill=Y)
    global textView
    textView = Text(root, height=34, yscrollcommand=s1.set)

    label3 = Label(root, text='日志输出：')  # '
    label3.pack()
    textView.pack(expand=YES, fill=X)
    s1.config(command=textView.yview)

    fm2 = Frame(root)
    fm2.pack()
    btn = Button(fm2, text='开始', command=submit)
    btn.pack(side=LEFT)
    btn1 = Button(fm2, text='新人礼开始', command=xinren_submit)
    btn1.pack(side=LEFT)
    btn2 = Button(fm2, text="只注册用户", command=user_submit)
    btn2.pack(side=LEFT)
    btn3 = Button(fm2, text='大连特定二维码', command=dalian_submit)
    btn3.pack(side=LEFT)
    btn4 = Button(fm2, text='快速新人礼刷粉', command=kuai_xinren_submit)
    btn4.pack(side=LEFT)

    root.mainloop()  # 进入消息循环


def dalian_submit():
    LOCK.acquire()
    global FILE_PATH
    FILE_PATH = PLACE + "%s.txt" % time.strftime("%Y%m%d")
    fans = entry1.get()
    if fans == '':
        log('参数不能为空')
        raise RuntimeError('参数不能为空')
    try:
        num = int(entry1.get())
        if num == '' and num < 0:
            num = 0
        th = threading.Thread(target=dalian_deal, args=(num,))
        th.setDaemon(True)  # 守护线程
        th.start()
    except RuntimeError as e:
        print(e)
        log('获取失败，请确保输入参数都是整数')
    LOCK.release()


def dalian_deal(num):
    productId = "20180906094543"
    global COUNT
    while COUNT < num:
        try:
            log("执行到第" + str(COUNT + 1) + "条。")
            phone_sms_result = phone_sms()
            phone_smss = phone_sms_result.split("|")
            phone = phone_smss[0]
            sms = phone_smss[1]
            code = get_code(sms)
            login_result = wanda_login(phone, code)
            oid = get_coupon(productId, phone, login_result["cookieStr"], login_result["uid"], login_result["puid"])
            time.sleep(1)
            coupon = get_coupon_no(oid, login_result["cookieStr"])
            log("第" + str(COUNT + 1) + "条成功。")
            write(phone + "  " + "https://api.ffan.com/qrcode/v1/qrcode?type=png&size=200&info=" + str(coupon))
            COUNT += 1
            time.sleep(get_interval_time())
        except RuntimeError as e:
            print(e)
    xunma.xm_logout(xmtoken)


def user_submit():
    LOCK.acquire()
    global FILE_PATH
    FILE_PATH = PLACE + "%s.txt" % time.strftime("%Y%m%d")
    fans = entry1.get()
    if fans == '':
        log('参数不能为空')
        raise RuntimeError('参数不能为空')
    try:
        num = int(entry1.get())
        if num == '' and num < 0:
            num = 0
        th = threading.Thread(target=user_deal, args=(num,))
        th.setDaemon(True)  # 守护线程
        th.start()
    except RuntimeError as e:
        print(e)
        log('获取失败，请确保输入参数都是整数')
    LOCK.release()


def user_deal(num):
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
            log("第" + str(COUNT + 1) + "条成功。")
            write(phone + "  ")
            COUNT += 1
            time.sleep(get_interval_time())
        except RuntimeError as e:
            print(e)
            continue
    xunma.xm_logout(xmtoken)


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
            login_result = wanda_login(phone, code)
            oid = get_coupon(productId, phone, login_result["cookieStr"], login_result["uid"], login_result["puid"])
            time.sleep(1)
            coupon = get_coupon_no(oid, login_result["cookieStr"])
            log("第" + str(COUNT + 1) + "条成功。")
            write(phone + "  " + "https://api.ffan.com/qrcode/v1/qrcode?type=png&size=200&info=" + str(coupon))
            COUNT += 1
            time.sleep(get_interval_time())
        except RuntimeError as e:
            print(e)
    xunma.xm_logout(xmtoken)


def get_interval_time():
    interval_time = interval.get()
    slep = random.randint(0, int(interval_time))
    print("本次停顿：" + str(slep))
    if interval_time.isdigit():
        return slep
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
        th = threading.Thread(target=xinren_deal, args=(num, index))
        th.setDaemon(True)  # 守护线程
        th.start()
    except RuntimeError as e:
        print(e)
        log('获取失败，请确保输入参数都是整数')
    LOCK.release()


# 循环新人礼
def xinren_deal(num, index):
    global COUNT
    while COUNT < num:
        try:
            log("执行到第" + str(COUNT + 1) + "条。")
            phone_sms_result = phone_sms()
            t = threading.Thread(target=xinren, args=(phone_sms_result, COUNT, index))
            t.setDaemon(True)
            t.start()
            COUNT += 1
            time.sleep(get_interval_time())
        except RuntimeError as e:
            print(e)
            continue
    t.join()
    xunma.xm_logout(xmtoken)


# 新人礼操作流程
def xinren(phone_sms_result, num, index):
    login_result = get_phone_login(phone_sms_result)
    time.sleep(1)
    oid = get_new_order_no(int(index), login_result["cookieStr"])
    time.sleep(1)
    coupon = get_coupon_no(oid, login_result["cookieStr"])
    log("第" + str(num + 1) + "条成功。")
    write(login_result["member"]["mobile"] + "  " + QRCODE_URL + coupon)


# 获取新用户优惠券
def get_new_order_no(index, cookieStr):
    params = (
        ('cookieStr', cookieStr),
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
    if len(result["data"]) == 0:
        log("新人券已经领完，请上券")
    return result['data'][index]['order']['orderNo']


def get_phone_login(phone_sms_result):
    phone_smss = phone_sms_result.split("|")
    phone = phone_smss[0]
    sms = phone_smss[1]
    code = get_code(sms)
    return wanda_login(phone, code)


###################################新方法###########################


# 易码获取号码
def new_ym_phone():
    EXCLUDENO = random.choice(EXCLUDENOS)
    phone = yima.ym_phone(TOKEN, ITEMID, EXCLUDENO, PROVINCE, CITY, "")
    if phone is None:
        raise RuntimeError("手机号获取不到")
    print("易码获取手机号为：" + str(phone))
    return phone


# 讯码获取号码
def new_xm_phone(token):
    phone = xunma.xm_get_phone(token, XM_LOCAL, 0)
    if phone == "release" or phone == "timeout":
        xunma.xm_logout(token)
        login_result = xunma.xm_login("demon3019", "12345678", "wdVJ21MmabfWT72lAxf3JA==")
        global xmtoken
        xmtoken = login_result[0]
        raise RuntimeError("讯码重新登录")
    if phone is None:
        raise RuntimeError("手机号获取不到")
    print("讯码获取手机号为：" + str(phone))
    return phone


# 海码获取号码
def new_hm_phone():
    phone = haima.hm_phone("", HM_PROVINCE)
    if phone is None:
        raise RuntimeError("手机号获取不到")
    # print("海码获取手机号：" + str(phone))
    return phone


# 云享获取号码
def new_yx_phone():
    phone = yunxiang.yx_phone()
    if phone is None:
        raise RuntimeError("手机号码获取不到")
    print("云享获取手机号：" + str(phone))
    return phone


# 返回手机号
def new_get_phone(platform, token):
    count = 0
    while True:
        phone = ""
        if platform == 1:
            phone = new_ym_phone()
        elif platform == 2:
            phone = new_xm_phone(token)
        elif platform == 3:
            phone = new_hm_phone()
        elif platform == 4:
            phone = new_yx_phone()
        check_result = check_phone(phone)
        if check_result['status'] != '0000' or check_result['_metadata']['totalCount'] != 0:
            if platform == 1:
                yima.ym_release(TOKEN, ITEMID, phone)
                yima.ym_ignore(TOKEN, ITEMID, phone)
            elif platform == 2:
                phone_list = phone + "-" + XM_ITEMID + ";"
                black_phone_list = XM_ITEMID + "-" + phone + ";"
                xunma.xm_relese(token, phone_list)
                xunma.xm_black(token, black_phone_list)
            elif platform == 3:
                haima.hm_black(phone)
            elif platform == 4:
                yunxiang.yx_relese(phone)
                yunxiang.yx_black(phone)
            count += 1
            if (count >= 10):
                raise RuntimeError("本次%s通道10次没有成功获取号码。" % str(platform))
            continue
        return phone


# 新版获取短信
def new_get_sms(platform, phone, xm_token):
    get_sms_code(phone)
    time.sleep(2)
    if platform == 1:
        return yima.ym_sms(TOKEN, ITEMID, phone, TIMEOUT)
    elif platform == 2:
        return xunma.xm_sms(xm_token, phone, TIMEOUT)
    elif platform == 3:
        return haima.hm_sms(phone, TIMEOUT)
    elif platform == 4:
        return yunxiang.yx_sms(phone, TIMEOUT)


# 快速刷粉提交
def kuai_xinren_submit():
    LOCK.acquire()
    try:
        global FILE_PATH
        FILE_PATH = PLACE + "新人礼%s.txt" % time.strftime("%Y%m%d")
        fans = entry1.get()  # 多少粉丝
        index = entry2.get()  # 第几个商品
        if fans == '' or index == '':
            log('参数不能为空')
            raise RuntimeError('参数不能为空')
        num = int(fans)
        if num == '' and num < 0:
            num = 0
        t = threading.Thread(target=kuai_xinren_thread, args=(num, index))
        t.setDaemon(True)
        t.start()
    except RuntimeError as e:
        print(e)
        log("入参请正确输入")
    LOCK.release()


# 快速新人线程
def kuai_xinren_thread(num, index):
    global COUNT
    threads = []
    while COUNT < num:
        try:
            th = threading.Thread(target=kuai_xinren_deal, args=(index, COUNT))
            threads.append(th)
            th.setDaemon(True)  # 守护线程
            th.start()
            COUNT += 1
            time.sleep(get_interval_time())
        except RuntimeError as e:
            print(e)
            continue

    for t in threads:
        t.join()

    time.sleep(5)
    COUNT = SUCCESS_COUNT
    log("本次任务完成,成功%s,已修改成%s,如果缺失，请再点击开始。" % (str(SUCCESS_COUNT), str(COUNT)))
    xunma.xm_logout(xmtoken)


# 快速新人礼处理
def kuai_xinren_deal(index, num):
    log("执行到第" + str(COUNT + 1) + "条。")
    platform = random.randint(1, 4)
    xm_token = xmtoken
    phone = new_get_phone(platform, xm_token)
    # 获取验证码，进行领券
    sms = new_get_sms(platform, phone, xm_token)
    code = get_code(sms)
    login_result = wanda_login(phone, code)
    time.sleep(1)
    oid = get_new_order_no(int(index), login_result["cookieStr"])
    time.sleep(1)
    coupon = get_coupon_no(oid, login_result["cookieStr"])
    global SUCCESS_COUNT
    SUCCESS_COUNT += 1
    log("第" + str(num + 1) + "条成功。")
    write(login_result["member"]["mobile"] + "  " + QRCODE_URL + coupon)
