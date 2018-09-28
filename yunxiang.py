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


def yx_phone():
    params = (
        ('token', TOKEN),
        ('xmid', XMID),
        ('sl', '1'),
        ('lx', '6'),
        ('a1', ''),
        ('a2', ''),
        ('pk', ''),
        ('ks', '0'),
        ('rj', 'demon3018'),
    )
    response = requests.get('http://47.97.118.96:9180/service.asmx/GetHM2Str', headers=headers,
                            params=params).text.split("=")
    print(response)
    if response[0] == '-3':
        raise RuntimeError("需要释放号码")
    if len(response) > 1:
        return response[1]
    raise RuntimeError("云享获取不到号码")


def yx_sms(phone, timeout):
    params = (
        ('token', TOKEN),
        ('xmid', XMID),
        ('hm', phone),
        ('sf', '1'),
    )
    start = time.time()
    while True:
        response = requests.get('http://47.97.118.96:9180/service.asmx/GetYzm2Str', headers=headers, params=params)
        print(response.text)
        if len(response.text) > 4:
            return response.text
        if response.text == "-1":
            yx_relese(phone)
            raise RuntimeError("yx_sms号码已经被释放")
        end = time.time()
        if (end - start) > timeout:
            # 获取不到释放
            yx_relese(phone)
            raise RuntimeError("yx_sms获取不到短信")
        time.sleep(5)


def yx_relese(phone):
    params = (
        ('token', TOKEN),
        ('hm', phone),
    )
    response = requests.get('http://47.97.118.96:9180/service.asmx/sfHmStr', headers=headers, params=params)
    print(response.text)


def yx_release_all():
    params = (
        ('token', TOKEN),
    )
    requests.get("http://47.97.118.96:9180/service.asmx/sfAllStr", headers=headers, params=params)


def yx_black(phone):
    params = (
        ('token', TOKEN),
        ('xmid', XMID),
        ('hm', phone),
        ('sf', '1'),
    )
    response = requests.get('http://47.97.118.96:9180/service.asmx/Hmd2Str', headers=headers, params=params)
    print(response.text)


if __name__ == '__main__':
    phone = yx_phone()
    # get_code.get_code(phone)
    yx_sms(phone, 60)
