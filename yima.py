import json
import time

import requests

YM_USERNAME = "shenyangtiexi"
YM_PASSWORD = "shenyangtiexi"


# 易码登录获取token
def ym_login(username, password):
    url = "http://api.fxhyd.cn/UserInterface.aspx?action=login&username=%s&password=%s" % (username, password)
    response = requests.get(url).text.split("|")
    if response[0] == "success":
        return response[1]
    else:
        raise RuntimeError("ym_login方法获取不到token")


# 易码获取用户信息
# {"UserName":"zhangzhouts","UserLevel":1,"MaxHold":20,"Discount":1.000,"Balance":9.9000,"Status":1,"Frozen":10.0000}
def ym_user(token):
    url = "http://api.fxhyd.cn/UserInterface.aspx?action=getaccountinfo&token=%s&format=1" % token
    response = requests.get(url).text.split("|")
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
    response = requests.get(url, params=param).text.split("|")
    print(response)
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
    while True:
        response = requests.get(url, params=param).content.decode(encoding="utf-8")
        responses = response.split("|")
        print(responses)
        if responses[0] == "success":
            return responses[1]
        end = time.time()
        if (end - start) > timeout:
            # 获取不到释放
            ym_release(token, itemid, mobile)
            raise RuntimeError("ym_sms获取不到短信")
        time.sleep(2)


# 释放号码
def ym_release(token, itemid, mobile):
    url = "http://api.fxhyd.cn/UserInterface.aspx"
    param = {
        ("action", "release"),
        ("token", token),
        ("itemid", itemid),
        ("mobile", mobile),
    }
    response = requests.get(url, param).text.split("|")
    print(response)
    if response[0] != "success":
        print("%s 释放失败" % mobile)


# 拉黑号码
def ym_ignore(token, itemid, mobile):
    url = "http://api.fxhyd.cn/UserInterface.aspx"
    param = {
        ("action", "addignore"),
        ("token", token),
        ("itemid", itemid),
        ("mobile", mobile),
    }
    response = requests.get(url, param).text.split("|")
    print(response)
    if response[0] != "success":
        print("%s 拉黑失败" % mobile)


if __name__ == '__main__':
    itemid = "7982"
    token = ym_login(YM_USERNAME, YM_PASSWORD)
    user = json.loads(ym_user(token))
    print(user)
    phone = ym_phone(token, itemid, "", "", "", "")
    print(phone)
    # sms = ym_sms(token, itemid, phone, 60)
    # print(sms)
    # ym_release(token, itemid, phone)
    # ym_ignore(token, itemid, phone)
