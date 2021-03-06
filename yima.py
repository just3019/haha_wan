import threading
import time

import requests

YM_USERNAME = "ye907182374"
YM_PASSWORD = "baobao1515"
header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}


# 易码登录获取token
def ym_login(username, password):
    url = "http://api.fxhyd.cn/UserInterface.aspx?action=login&username=%s&password=%s" % (username, password)
    response = requests.get(url, headers=header_dict, timeout=10).text.split("|")
    if response[0] == "success":
        return response[1]
    else:
        raise RuntimeError("ym_login方法获取不到token")


# 易码获取用户信息
# {"UserName":"zhangzhouts","UserLevel":1,"MaxHold":20,"Discount":1.000,"Balance":9.9000,"Status":1,"Frozen":10.0000}
def ym_user(token):
    url = "http://api.fxhyd.cn/UserInterface.aspx?action=getaccountinfo&token=%s&format=1" % token
    response = requests.get(url, headers=header_dict, timeout=10).text.split("|")
    if response[0] == "success":
        return response[1]
    else:
        raise RuntimeError("ym_user方法获取不到用户信息")


# 易码获取手机号
def ym_phone(token, itemid, excludeno, province, city, mobile):
    url = "http://api.fxhyd.cn/UserInterface.aspx"
    param = {
        ("action", "getmobile"),
        ("token", token),
        ("itemid", itemid),
        ("excludeno", excludeno),
        ("isp", ""),
        ("province", province),
        ("city", city),
        ("mobile", mobile),
    }
    s = requests.session()
    s.keep_alive = False
    response = s.get(url, params=param, headers=header_dict, timeout=10).text.split("|")
    # print(response)
    if response[0] == "success":
        return response[1]
    else:
        raise RuntimeError("ym_phone方法没有获取到手机号")


# 获取该手机号的短信
def ym_sms(token, itemid, mobile, timeout):
    url = "http://api.fxhyd.cn/UserInterface.aspx"
    param = {
        ("action", "getsms"),
        ("token", token),
        ("itemid", itemid),
        ("mobile", mobile),
        ("release", "1"),
    }
    start = time.time()
    s = requests.session()
    s.keep_alive = False
    while True:
        response = s.get(url, params=param, headers=header_dict, timeout=10).content.decode(encoding="utf-8")
        print("[" + threading.current_thread().name + "] " + response)
        responses = response.split("|")
        if responses[0] == "2008":
            raise RuntimeError("号码已离线")
        if responses[0] == "success":
            ym_ignore(token, itemid, mobile)
            return responses[1]
        end = time.time()
        if (end - start) > timeout:
            # 获取不到释放
            ym_release(token, itemid, mobile)
            raise RuntimeError("ym_sms获取不到短信")
        time.sleep(5)


# 释放号码
def ym_release(token, itemid, mobile):
    url = "http://api.fxhyd.cn/UserInterface.aspx"
    param = {
        ("action", "release"),
        ("token", token),
        ("itemid", itemid),
        ("mobile", mobile),
    }
    response = requests.get(url, param, headers=header_dict, timeout=10).text.split("|")
    # print(response)
    if response[0] != "success":
        print("[" + threading.current_thread().name + "] " + "%s 释放失败" % mobile)


# 拉黑号码
def ym_ignore(token, itemid, mobile):
    url = "http://api.fxhyd.cn/UserInterface.aspx"
    param = {
        ("action", "addignore"),
        ("token", token),
        ("itemid", itemid),
        ("mobile", mobile),
    }
    response = requests.get(url, param, headers=header_dict, timeout=10).text.split("|")
    # print(response)
    if response[0] != "success":
        print("[" + threading.current_thread().name + "] " + "%s 拉黑失败" % mobile)


if __name__ == '__main__':
    itemid = "7982"
    token = ym_login(YM_USERNAME, YM_PASSWORD)
    print(token)

    # user = json.loads(ym_user(token))
    # print(user)
    # phone = ym_phone(token, itemid, "", "", "", "")
    # print(phone)
    # sms = ym_sms(token, itemid, phone, 60)
    # print(sms)
    # ym_release(token, itemid, phone)
    # ym_ignore(token, itemid, phone)
