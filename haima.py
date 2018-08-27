import json
import time

import requests

import get_code

URL = "http://www.haima668.com:8008/ActionApi/"
USERNAME = "demon3019"
PASSWORD = "123456"


def hm_login():
    url = URL + "loginIn"
    data = [
        ('uid', USERNAME),
        ('pwd', PASSWORD),
    ]
    response = requests.post(url, data).text
    print("登录：" + response)
    return response


def hm_phone(uid, token, hm_type, province):
    url = URL + "getMobilenum?uid=%s&pid=%s&token=%s&type=%s&province=%s" % (uid, "521", token, hm_type, province)
    response = requests.post(url).text
    print("获取手机号：" + response)
    return response


def hm_sms(phone, uid, token, author_uid, pid, timeout):
    url = URL + "getVcodeAndReleaseMobile?mobile=%s&uid=%s&token=%s&author_uid=%s&pid=%s" % (
        phone, uid, token, author_uid, pid)
    start = time.time()
    while True:
        response = requests.post(url).text
        print("获取短信：" + response)
        responses = response.split("|")
        end = time.time()
        if (end - start) > timeout:
            raise RuntimeError("hm_sms获取不到短信")
        if phone in responses:
            return responses[1]
        time.sleep(5)


if __name__ == '__main__':
    login_result = json.loads(hm_login())
    print(str(login_result["Uid"]) + " " + login_result["Token"] + " " + str(login_result["Balance"]) + " " + str(
        login_result["UsedMax"]))
    uid = login_result["Uid"]
    token = login_result["Token"]
    print(token)
    phone_result = hm_phone(uid, token, "", "")
    get_code.get_code(phone_result)
    sms_result = hm_sms(phone_result, uid, token, "demon3019", "521", 60)
