import threading
import time

import requests

# import get_code

headers = {
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6',
}
TOKEN = "7920047BF00ED99E20CCCF859E648FA0"
XMID = "5681"


def yx_login():
    url = "http://47.97.118.96:9180/service.asmx/UserLoginStr?name=demon3019&psw=12345678"
    response = requests.get(url, headers=headers, timeout=10)
    return response.text


def yx_phone():
    url = "http://47.97.118.96:9180/service.asmx/GetHM2Str?token=%s&xmid=%s&sl=1&lx=6&ks=0&rj=demon3018&a1=&a2=&pk=" % (
        TOKEN, XMID)
    response = requests.get(url, headers=headers, timeout=10).text.split("=")
    # print(response)
    if response[0] == '-3':
        yx_release_all()
        raise RuntimeError("需要释放号码")
    if len(response) > 1:
        return response[1]
    print("[" + threading.current_thread().name + "] " + str(response))
    raise RuntimeError("云享获取不到号码")


def yx_sms(phone, timeout):
    url = "http://47.97.118.96:9180/service.asmx/GetYzm2Str?token=%s&xmid=%s&hm=%s&sf=1" % (TOKEN, XMID, phone)
    start = time.time()
    while True:
        response = requests.get(url, headers=headers, timeout=10)
        print("[" + threading.current_thread().name + "] " + response.text)
        if len(response.text) > 4:
            yx_black(phone)
            return response.text
        if response.text == "-1":
            yx_black(phone)
            raise RuntimeError("yx_sms号码已经被释放")
        end = time.time()
        if (end - start) > timeout:
            # 获取不到释放
            yx_black(phone)
            raise RuntimeError("yx_sms获取不到短信")
        time.sleep(5)


def yx_relese(phone):
    url = "http://47.97.118.96:9180/service.asmx/sfHmStr?token=%s&hm=%s" % (TOKEN, phone)
    response = requests.get(url, headers=headers, timeout=10)
    # print("yx释放:" + response.text)


def yx_release_all():
    response = requests.get("http://47.97.118.96:9180/service.asmx/sfAllStr?token=7920047BF00ED99E20CCCF859E648FA0",
                            headers=headers, timeout=10)
    # print("yx释放全部:" + response.text)


def yx_black(phone):
    url = "http://47.97.118.96:9180/service.asmx/Hmd2Str?token=%s&xmid=%s&hm=%s&sf=1" % (TOKEN, XMID, phone)
    response = requests.get(url, headers=headers, timeout=10)
    # print("yx拉黑:" + response.text)


def yx_phone_many(num):
    url = "http://47.97.118.96:9180/service.asmx/GetHM2Str?token=%s&xmid=%s&sl=%s&lx=6&ks=0&rj=demon3018&a1=&a2=&pk=" % (
        TOKEN, XMID, num)
    # print(url)
    response = requests.get(url, headers=headers, timeout=10).text.split("=")
    # print(response)
    if response[0] == '-3':
        yx_release_all()
        raise RuntimeError("需要释放号码")
    if len(response) > 1:
        return response[1]
    raise RuntimeError("云享获取不到号码")


if __name__ == '__main__':
    yx_login()
    # yx_phone_many(100)
    phone = yx_phone()
    print(phone)
    # get_code.get_code(phone)
    # yx_sms(phone, 60)
    # yx_release_all()
    # yx_relese("13894530425")
    # yx_relese("18374111413")
    # yx_relese("18380405428")
