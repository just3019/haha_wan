import json
import random
import threading
import time
import tkinter
from tkinter import ttk

import requests
from tkinter import *

import haima
import yima
import yunxiang
from thread_pool import ThreadPool

PLAZAID = '1102461'
PLACE = "滨州"

LOCK = threading.Lock()
WXFFANTOKEN = '0fb65ff60569472082c838fbadc9ff92'
ym_username = "binzhou"
ym_password = "binzhou"
YM_TOKEN = yima.ym_login(ym_username, ym_password)
YM_ITEMID = '27894'  # 丙晟科技
HM_PID = "11147"
YX_ID = "171348"
COUNT = 1
SUCCESS_COUNT = 0
TIMEOUT = 80


def init(plazaId, place):
    global PLAZAID
    PLAZAID = plazaId
    global PLACE
    PLACE = place
    global FILE_PATH_PHONE
    FILE_PATH_PHONE = "%s%sphone.txt" % (place, time.strftime("%Y%m%d"))
    global FILE_PATH
    FILE_PATH = "%s%s.txt" % (place, time.strftime("%Y%m%d"))


def printf(s):
    print('[%s][%s]%s' % (threading.current_thread().getName(), time.strftime("%X"), s))


def log(s):
    printf(s)
    textView.insert(END, '[%s][%s]%s\n' % (threading.current_thread().name, time.strftime("%X"), s))
    textView.update()
    textView.see(END)


def write(s):
    f = open(FILE_PATH, "a")
    f.write('[%s]%s\n' % (time.strftime("%X"), s.strip()))
    f.close()


def write_phone(s):
    f = open(FILE_PATH_PHONE, "a")
    f.write('[%s]%s\n' % (time.strftime("%X"), s.strip()))
    f.close()


def get_interval_time():
    interval_time = interval.get()
    slep = random.randint(0, int(interval_time))
    printf("本次停顿：%s秒" % slep)
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
    for i in range(0, 3):
        response = requests.post('https://api.beyonds.com/wdmp/member/v1/manualLogin', headers=headers, data=data)
        printf(response.text)
        result = json.loads(response.text)
        if result["status"] == 200:
            write_phone(phone)
            return result["data"]
        if i >= 2:
            raise RuntimeError("登录失败")


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
    return json.loads(response.text)


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
    return json.loads(response.text)


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
    printf(response.text)
    return json.loads(response.text)


# 验证号码是否可用
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
    printf("检测手机号有效性：%s" % response.text)
    return json.loads(response.text)


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
    print("[" + threading.current_thread().name + "] " + "验证码为：" + code)
    if code is None:
        raise RuntimeError('验证码为空')
    return code


######################号码处理###################

# 易码获取号码
def new_ym_phone():
    phone = yima.ym_phone(YM_TOKEN, YM_ITEMID, "170.171.172", "", "", "")
    if phone is None:
        raise RuntimeError("手机号获取不到")
    printf("易码获取手机号为：%s" % phone)
    return phone


# 海码获取号码
def new_hm_phone():
    phone = haima.hm_phone("", "", HM_PID)
    if phone is None:
        raise RuntimeError("手机号获取不到")
    printf("海码获取手机号：%s" % phone)
    return phone


# 云享获取号码
def new_yx_phone():
    phone = yunxiang.yx_phone(YX_ID)
    if phone is None:
        raise RuntimeError("手机号码获取不到")
    printf("云享获取手机号：%s" % phone)
    return phone


# 返回手机号
def new_get_phone(platform):
    count = 0
    while True:
        phone = ""
        if platform == 1:
            phone = new_ym_phone()
        check_result = check_phone(phone)
        if check_result['status'] != '0000' or check_result['_metadata']['totalCount'] != 0:
            if platform == 1:
                yima.ym_release(YM_TOKEN, YM_ITEMID, phone)
                yima.ym_ignore(YM_TOKEN, YM_ITEMID, phone)
            count += 1
            if count >= 10:
                raise RuntimeError("本次%s通道10次没有成功获取号码。" % platform)
            continue
        return phone


# 新版获取短信
def new_get_sms(platform, phone):
    send_v_code(phone)
    time.sleep(5)
    if platform == 1:
        return yima.ym_sms(YM_TOKEN, YM_ITEMID, phone, TIMEOUT)


def ui():
    root = Tk()  # 创建窗口对象的背景色
    root.title('飞凡刷粉工具-%s' % PLACE)
    root.geometry('320x210')

    fm1 = Frame(root)
    fm1.pack(fill=X)
    value = tkinter.StringVar()  # 窗体自带的文本，新建一个值
    global comboxlist
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
    ee = StringVar()
    entry1 = Entry(fm1, width=4, textvariable=ee)
    ee.set(0)
    label1.pack(side=LEFT)
    entry1.pack(side=LEFT)
    interval_label = Label(fm1, text="间隔")
    global interval
    ie = StringVar()
    interval = Entry(fm1, width=4, textvariable=ie)
    ie.set(30)
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
    Button(fm2, text='快新', command=kuai_xin_submit).pack(side=LEFT)
    Button(fm2, text='快普', command=kuai_putong_submit).pack(side=LEFT)

    root.mainloop()


def kuai_putong_submit():
    num = entry1.get()
    if not num.isdigit() or int(num) <= 0:
        log("输入需要刷的量")
        raise RuntimeError("输入需要刷的量")
    t = threading.Thread(target=kuai_putong_thread)
    t.setDaemon(True)
    t.start()


def kuai_putong_thread():
    global COUNT
    product = str(comboxlist.get()).split("|")
    log(product)
    productId = product[2]
    TP = ThreadPool(30)
    while True:
        # 如果当前大于等于要刷的数量则跳出循环
        if COUNT >= int(entry1.get()):
            break
        TP.add_task(kuai_putong_deal, COUNT, productId)
        COUNT += 1
        time.sleep(get_interval_time())

    TP.wait_completion()
    time.sleep(1)
    COUNT = SUCCESS_COUNT
    log("本次任务完成,成功%s,已修改成%s,如果缺失，请再点击开始。" % (SUCCESS_COUNT, COUNT))


def kuai_putong_deal(num, productId):
    try:
        log("进行第%s个任务" % num)
        platform = random.randint(1, 1)
        phone = new_get_phone(platform)
        sms = new_get_sms(platform, phone)
        code = get_code(sms)
        login_result = login(phone, code)
        memberId = login_result["memberId"]
        token = login_result["token"]
        time.sleep(get_interval_time())
        free_coupon = gain_free_coupon(token, memberId, productId)
        coupon = free_coupon["data"]["code"]
        s = "%s|%s" % (phone, coupon)
        write(s)
        global SUCCESS_COUNT
        SUCCESS_COUNT += 1
        log("第%s个任务完成" % num)
    except RuntimeError as e:
        printf(e)


def kuai_xin_submit():
    num = entry1.get()
    if not num.isdigit() or int(num) <= 0:
        log("输入需要刷的量")
        raise RuntimeError("输入需要刷的量")
    t = threading.Thread(target=kuai_xin_thread)
    t.setDaemon(True)
    t.start()


def kuai_xin_thread():
    global COUNT
    TP = ThreadPool(30)
    while True:
        # 如果当前大于等于要刷的数量则跳出循环
        if COUNT > int(entry1.get()):
            break
        TP.add_task(kuai_xin_deal, COUNT)
        COUNT += 1
        time.sleep(get_interval_time())

    TP.wait_completion()
    time.sleep(1)
    COUNT = SUCCESS_COUNT
    log("本次任务完成,成功%s,已修改成%s,如果缺失，请再点击开始。" % (SUCCESS_COUNT, COUNT))


def kuai_xin_deal(num):
    try:
        log("进行第%s个任务" % num)
        platform = random.randint(1, 1)
        phone = new_get_phone(platform)
        sms = new_get_sms(platform, phone)
        code = get_code(sms)
        login_result = login(phone, code)
        memberId = login_result["memberId"]
        token = login_result["token"]
        time.sleep(get_interval_time())
        xin_coupon = new_user_coupon(token, memberId, PLAZAID)
        coupon = xin_coupon["data"]
        rr = ""
        for i in coupon:
            rr += "%s|" % i["code"]
        s = "%s|%s" % (phone, rr)
        write(s)
        global SUCCESS_COUNT
        SUCCESS_COUNT += 1
        log("第%s个任务完成" % num)
    except RuntimeError as e:
        printf(e)


if __name__ == '__main__':
    ui()
