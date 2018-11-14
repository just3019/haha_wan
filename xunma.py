import random
import threading
import time

import requests

ITEMID = "3410"  # 飞凡网
# ITEMID = "29188"  # 丙晟科技

header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}


# 地区：吉林 四川 江苏 湖南 北京 辽宁 浙江 云南 黑龙江 陕西 广东

def xm_login(username, password, developer):
    try:
        url = "http://xapi.xunma.net/Login"
        params = {
            ("uName", username),
            ("pWord", password),
            ("Developer", developer),
            ("Code", "UTF8"),
        }
        response = requests.get(url, params=params, headers=header_dict, timeout=10).text.split("&")
        # print("讯码登录：" + str(response))
        return response
    except RuntimeError as e:
        print(e)


def xm_get_phone(token, area, PhoneType, itemid=ITEMID):
    try:
        url = "http://xapi.xunma.net/getPhone"
        # ("PhoneType", random.randint(0, 3)),
        params = {
            ("ItemId", itemid),
            ("token", token),
            ("Code", "UTF8"),
            ("PhoneType", PhoneType),
            ("Area", area),
        }
        s = requests.session()
        s.keep_alive = False
        response = s.get(url, params=params, headers=header_dict, timeout=10).text.split(";")
        time.sleep(1)
        # print("讯码获取手机号：" + str(response))
        if "False:暂时没有此项目号码，请等会试试..." == response[0]:
            raise RuntimeError("获取号码失败")
        if "False:单个用户获取数量不足" == response[0]:
            return "release"
        if "False" in response[0]:
            return "timeout"
        if "False:余额不足，请先释放号码" == response[0]:
            raise ("False:余额不足，请先释放号码")
        return response[0]
    except RuntimeError as e:
        print("[" + threading.current_thread().name + "] " + "讯码平台问题phone")
        raise RuntimeError(e)


def xm_sms(token, phone, timeout, itemid=ITEMID):
    try:
        url = "http://xapi.xunma.net/getMessage"
        params = {
            ("token", token),
            ("itemId", itemid),
            ("phone", phone),
            ("Code", "UTF8"),
        }
        start = time.time()
        s = requests.session()
        s.keep_alive = False
        while True:
            response = s.get(url, params=params, headers=header_dict, timeout=10).text
            if "飞凡" in response:
                return response
            print("[" + threading.current_thread().name + "] " + response)
            response = response.split("&")
            end = time.time()
            if "False:Session 过期" in response:
                raise RuntimeError("xm的token已经过期")
            if (end - start) > timeout:
                phone_list = phone + "-" + ITEMID + ";"
                xm_relese(token, phone_list)
                raise RuntimeError("xm_sms获取不到短信")
            if "MSG" in response:
                black_phone_list = ITEMID + "-" + phone + ";"
                xm_black(token, black_phone_list)
                return response[3]
            time.sleep(5)
    except RuntimeError as e:
        print("[" + threading.current_thread().name + "] " + "讯码平台问题sms")
        raise RuntimeError(e)


def xm_relese(token, phoneList):
    try:
        url = "http://xapi.xunma.net/releasePhone?token=%s&phoneList=%s&Code=UFT8" % (token, phoneList)
        s = requests.session()
        s.keep_alive = False
        response = s.get(url, headers=header_dict, timeout=10).text
        # print("释放号码：" + response)
    except RuntimeError as e:
        raise RuntimeError("释放失败")


def xm_black(token, phoneList):
    url = "http://xapi.xunma.net/addBlack?token=%s&phoneList=%s&Code=UTF8" % (token, phoneList)
    s = requests.session()
    s.keep_alive = False
    response = s.get(url, headers=header_dict, timeout=10).text
    # print("拉黑号码：" + response)


def xm_logout(token):
    try:
        url = "http://xapi.xunma.net/Exit"
        params = {
            ("token", token),
            ("Code", "UTF8"),
        }
        response = requests.get(url, params=params, headers=header_dict, timeout=10).text
        print("[" + threading.current_thread().name + "] " + "登出：" + response)
    except RuntimeError as e:
        print(e)


if __name__ == '__main__':
    login_result = xm_login("demon3019", "12345678", "wdVJ21MmabfWT72lAxf3JA==")
    token = login_result[0]
    print("[" + threading.current_thread().name + "] " + token)
    phone = xm_get_phone(token, "辽宁", random.randint(0, 4), "29188")
    print("[" + threading.current_thread().name + "] " + phone)
    # get_code.get_code(phone)
    time.sleep(15)
    sms = xm_sms(token, phone, 120, "29188")
    print(sms)
    # phone_list = phone + "-" + ITEMID + ";"
    # xm_relese(token, phone_list)
    # xm_black(token, phone_list)
    # xm_logout(token)
