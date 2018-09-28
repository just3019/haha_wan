import json
import time

import requests

URL = "http://www.haima668.com:8008/ActionApi/"
USERNAME = "demon3019"
PASSWORD = "123456"
TOKEN = "zPghzzU%2BTqJbhiYruSiTYry5%2B31hVU/yDr9rBgRI9H5vliniFqmmWtEGI/Gj7cdh"
PID = "521"
UID = "29135"
header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}


def hm_login():
    url = URL + "loginIn"
    data = [
        ('uid', USERNAME),
        ('pwd', PASSWORD),
    ]
    response = requests.post(url, data, headers=header_dict).text
    print("登录：" + response)
    return response


def hm_phone(hm_type, province):
    url = URL + "getMobilenum?uid=%s&pid=%s&token=%s&type=%s&province=%s&nonVirtual=true" % (
        UID, PID, TOKEN, hm_type, province)
    response = requests.post(url, headers=header_dict).text
    print("获取手机号：" + response)
    if "余额不足，请充值" == response:
        raise RuntimeError("海码余额不足，请充值")
    if "No_Data" == response:
        raise RuntimeError("没有合适号码")
    return response


def hm_sms(phone, timeout):
    url = URL + "getVcodeAndReleaseMobile?mobile=%s&uid=%s&token=%s&author_uid=%s&pid=%s" % (
        phone, UID, TOKEN, USERNAME, PID)
    start = time.time()
    while True:
        response = requests.post(url, headers=header_dict).text
        print("获取短信：" + response)
        responses = response.split("|")
        end = time.time()
        if (end - start) > timeout:
            hm_black(phone)
            raise RuntimeError("hm_sms获取不到短信")
        if phone in responses:
            hm_black(phone)
            return responses[1]
        time.sleep(5)


def hm_black(phone):
    url = URL + "addIgnoreList?mobiles=%s&token=%s&uid=%s&pid=%s" % (phone, TOKEN, UID, PID)
    response = requests.post(url, headers=header_dict).text
    print("海码拉黑：" + response)


if __name__ == '__main__':
    login_result = json.loads(hm_login())
    print(str(login_result["Uid"]) + " " + login_result["Token"] + " " + str(login_result["Balance"]) + " " + str(
        login_result["UsedMax"]))
    uid = login_result["Uid"]
    token = login_result["Token"]
    print(token)
    phone_result = hm_phone("", "辽宁")
    print(phone_result)
    # # get_code.get_code(phone_result)
    # sms_result = hm_sms(phone_result, 60)
    hm_black(phone_result)
