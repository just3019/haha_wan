import random
import threading
from tkinter import *
import time
import json
import re
import requests
import yima

TOKEN = '00499849cbf687835af75182698438eb3c2ccdf4'
PLAZAID = '1000769'
ITEMID = '7982'
COUNT = 0
PROVINCE = '330000'
PLACE = '平阳'
EXCLUDENO = ""
CITY = ""
TIMEOUT = 60
CHO = ["74ab910197474826b288edd65d74393c", "6cc7fda5c8674951b446126226ac51ac"]
WXFFANTOKEN = random.choice(CHO)
uid = ""
cookieStr = ""
puid = ""
headers = {
    'Host': 'api.ffan.com',
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)'
                  ' Mobile/15F79 MicroMessenger/6.7.1 NetType/4G Language/zh_CN',
    'Referer': 'https://servicewechat.com/wx07dfb5d79541eca9/81/page-frame.html',
    'Accept-Language': 'zh-cn',
}


def log(s):
    print(s)
    textView.insert(END, '%s\n' % s)
    textView.update()
    textView.see(END)


def write(s):
    log(s)
    f = open(FILE_PATH, "a")
    f.write('%s\n' % s)
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


def deal(num, index):
    user = json.loads(yima.ym_user(TOKEN))
    if user["Balance"] <= 0:
        log("请联系客服，再刷粉！")
        raise RuntimeError("请联系客服，再刷粉！")
    productId = get_product_info()['data']['resource'][index - 1]['couponNo']
    global COUNT
    while COUNT < num:
        try:
            phone = yima.ym_phone(TOKEN, ITEMID, EXCLUDENO, PROVINCE, CITY, "")
            sms = yima.ym_sms(TOKEN, ITEMID, phone, TIMEOUT)
            code = get_code(sms)
            wanda_login(phone, code)
            oid = get_coupon(productId, phone)
            coupon = get_coupon_no(oid)
            write(phone + "  " + "https://api.ffan.com/qrcode/v1/qrcode?type=png&size=200&info=" + coupon)
            print("这里进行业务操作")
            COUNT += 1
        except RuntimeError as e:
            print(e)


# 处理飞凡短信内容
def get_code(sms):
    if '欢迎注册飞凡会员' not in sms:
        raise RuntimeError('该会员已经是注册用户')
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
            global uid
            global cookieStr
            global puid
            uid = result['data']['uid']
            cookieStr = result['data']['cookieStr']
            puid = result['data']['puid']
            return result
        if i >= 3:
            raise RuntimeError("登录失败")


# 获取商品的id,支持到100个商品
def get_product_info():
    params = (
        ('adSpaceId', 'couponList'),
        ('plazaId', PLAZAID),
        ('channelId', '1003'),
        ('type', '1001'),
        ('pageNum', '1'),
        ('pageSize', '100'),
    )
    response = requests.get('https://api.ffan.com/wechatxmt/v5/plaza/coupons', headers=headers, params=params)
    result = json.loads(response.text)
    print("获取商品id" + result)
    return result


# 领券
def get_coupon(productId, mobile):
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
    result = json.loads(response.text)
    print("领券：" + result)
    return result["orderNo"]


# 获取优惠券明细
def get_coupon_no(oid):
    params = (
        ('cookieStr', cookieStr),
        ('oid', oid),
    )
    for i in range(0, 3):
        response = requests.get('https://api.ffan.com/wechatxmt/v1/order', headers=headers, params=params)
        result = json.loads(response.text)
        print("获取明细：" + result)
        if result["status"] == 200 and "couponNo" in result:
            return result['data']['product'][0]['couponNo']
        if i >= 3:
            raise RuntimeError("获取优惠券失败")


if __name__ == '__main__':
    global FILE_PATH
    FILE_PATH = PLACE + "%s.txt" % time.strftime("%Y%m%d")
    ui()
