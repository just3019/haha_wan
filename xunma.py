import random
import time

import requests

ITEMID = "3410"  # 飞凡网


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
        response = requests.get(url, params=params).text.split("&")
        print("讯码登录：" + str(response))
        return response
    except RuntimeError as e:
        print(e)


def xm_get_phone(token):
    url = "http://xapi.xunma.net/getPhone"
    params = {
        ("ItemId", ITEMID),
        ("token", token),
        ("PhoneType", random.randint(0, 3)),
        ("Code", "UTF8"),
    }
    response = requests.get(url, params=params).text.split(";")
    print("讯码获取手机号：" + str(response))
    if "False" in response[0]:
        raise RuntimeError("获取号码失败")
    return response[0]


def xm_sms(token, phone, timeout):
    try:
        url = "http://xapi.xunma.net/getMessage"
        params = {
            ("token", token),
            ("itemId", ITEMID),
            ("phone", phone),
            ("Code", "UTF8"),
        }
        start = time.time()
        while True:
            response = requests.get(url, params=params).text.split("&")
            print(response)
            end = time.time()
            if (end - start) > timeout:
                raise RuntimeError("xm_sms获取不到短信")
            if "MSG" in response:
                return response[3]
            time.sleep(5)
    except RuntimeError as e:
        print(e)


def xm_relese(token, phoneList):
    url = "http://xapi.xunma.net/releasePhone"
    params = {
        ("token", token),
        ("phoneList", phoneList),
        ("Code", "UTF8"),
    }
    response = requests.get(url, params=params).text
    print("释放号码：" + response)


def xm_black(token, phoneList):
    url = "http://xapi.xunma.net/addBlack"
    params = {
        ("token", token),
        ("phoneList", phoneList),
        ("Code", "UTF8"),
    }
    response = requests.get(url, params=params).text
    print("拉黑号码：" + response)


def xm_logout(token):
    try:
        url = "http://xapi.xunma.net/Exit"
        params = {
            ("token", token),
            ("Code", "UTF8"),
        }
        response = requests.get(url, params=params).text
        print("登出：" + response)
    except RuntimeError as e:
        print(e)


if __name__ == '__main__':
    login_result = xm_login("demon3019", "12345678", "wdVJ21MmabfWT72lAxf3JA==")
    token = login_result[0]
    print(token)
    phone = xm_get_phone(token)
    print(phone)
    # get_code.get_code(phone)
    time.sleep(2)
    sms = xm_sms(token, phone, 60)
    print(sms)
    phone_list = phone + "-" + ITEMID + ";"
    xm_relese(token, phone_list)
    xm_black(token, phone_list)
    xm_logout(token)
