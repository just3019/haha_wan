import json
import random
import threading
import tkinter
from tkinter import *
from tkinter import filedialog

import requests
import time

lock = threading.Lock()
place = '大连庄河'

headers = {
    'Host': 'sop.ffan.com',
    'Accept': '*/*',
    'User-Agent': 'com.dianshang.feifanbp/2.0.1 (iPhone; iOS 11.4; Scale/3.00)',
    'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
}


def log(s):
    print(s)
    textView.insert(END, '%s\n' % s)
    textView.update()
    textView.see(END)


def write(s):
    f = open(log_path, "a")
    f.write('[%s] %s\n' % (time.ctime(), s))
    f.close()


def get_random():
    ran = random.randint(100000, 999999)
    return str(ran)


def scan(code):
    params = (
        ('', ''),
        ('storeId', '10421457'),
        ('clientType', 'iOS'),
        ('uid', '464721'),
        ('clientId', 'xapi_01'),
        ('version', '47'),
        ('_uni_source', '2.2'),
        ('merchantId', '10103498'),
        ('loginToken', '9df0b6c31ded941f9bf7e8c6dcf9babc'),
        ('deviceId', '184d19d52857d3628276407b946e367d208c7c5d'),
        ('appType', 'bpMobile'),
        ('username', '15840866817'),
        ('serverVersion', '1'),
        ('clientAgent', 'iPhone9,2/iOS/12.0/1242*2208'),
        ('telephone', '15840866817'),
    )

    data = {
        '_uni_source': '2.2',
        'appType': 'bpMobile',
        'app_time': '26852892206078',
        'app_verification_native': get_random(),
        'certificateno': code,
        'checkDevice': '1',
        'clientAgent': 'iPhone9,2/iOS/12.0/1242*2208',
        'clientId': 'xapi_01',
        'clientType': 'iOS',
        'deviceId': '184d19d52857d3628276407b946e367d208c7c5d',
        'loginToken': '9df0b6c31ded941f9bf7e8c6dcf9babc',
        'merchantId': '10103498',
        'serverVersion': '1',
        'sign': '632265244091937fd2bca4d3d56c4f90',
        'storeId': '10421457',
        'telephone': '15840866817',
        'uid': '464721',
        'username': '15840866817',
        'version': '47'
    }
    response = requests.post('https://sop.ffan.com/goods/coupon/queryUnusedCoupons', headers=headers, params=params,
                             data=data)
    print(response.text)

    params1 = (
        ('storeId', '10421457'),
        ('clientType', 'iOS'),
        ('uid', '464721'),
        ('clientId', 'xapi_01'),
        ('version', '47'),
        ('_uni_source', '2.2'),
        ('merchantId', '10103498'),
        ('loginToken', '9df0b6c31ded941f9bf7e8c6dcf9babc'),
        ('deviceId', '184d19d52857d3628276407b946e367d208c7c5d'),
        ('appType', 'bpMobile'),
        ('username', '15840866817'),
        ('serverVersion', '1'),
        ('clientAgent', 'iPhone9,2/iOS/12.0/1242*2208'),
        ('telephone', '15840866817'),
    )

    data1 = {
        '_uni_source': '2.2',
        'appType': 'bpMobile',
        'app_time': '26852945505160',
        'app_verification_native': get_random(),
        'certificateno': code,
        'clientAgent': 'iPhone9,2/iOS/12.0/1242*2208',
        'clientId': 'xapi_01',
        'clientType': 'iOS',
        'deviceId': '184d19d52857d3628276407b946e367d208c7c5d',
        'loginToken': '9df0b6c31ded941f9bf7e8c6dcf9babc',
        'memberId': '15000000081688778',
        'merchantId': '10103498',
        'serverVersion': '1',
        'sign': 'bc0a91fba5798bcacc74c6da4589669a',
        'storeId': '10421457',
        'telephone': '15840866817',
        'uid': '464721',
        'userId': '464721',
        'username': '15840866817',
        'version': '47'
    }
    response = requests.post('https://sop.ffan.com/goods/coupon/checkCoupon', headers=headers, params=params1,
                             data=data1)
    result = response.text
    if json.loads(result)['status'] != 200:
        raise RuntimeError("已验证过")
    print(result)


def openfile():
    r = filedialog.askopenfilename(title='打开文件', filetypes=[('Python', '*.txt'), ('All Files', '*')])
    log("当前操作的文件是：" + r)
    global file_path
    file_path = r


def ui():
    root = tkinter.Tk()
    root.title(place + '核销工具')
    root.geometry('300x400')
    fm1 = Frame(root)
    fm1.pack()
    global btn_file
    btn_file = Button(fm1, text='选择', command=openfile)
    label1 = Label(fm1, text='最少：')
    global entry1
    entry1 = Entry(fm1, width=5)
    label2 = Label(fm1, text='最大：')
    global entry2
    entry2 = Entry(fm1, width=5)

    btn_file.pack(side=LEFT)
    label1.pack(side=LEFT)
    entry1.pack(side=LEFT)
    label2.pack(side=LEFT)
    entry2.pack(side=LEFT)
    global s1
    s1 = Scrollbar(root)
    s1.pack(side=RIGHT, fill=Y)
    global textView
    textView = Text(root, width=400, height=20, yscrollcommand=s1.set)
    label3 = Label(root, text='日志输出')
    label3.pack()
    textView.pack(expand=YES, fill=X)
    s1.config(command=textView.yview)
    fm2 = Frame(root)
    fm2.pack()
    btn = Button(fm2, text='开始', command=start)
    btn.pack(side=LEFT)
    root.mainloop()


def start():
    global th
    th = threading.Thread(target=deal)
    th.setDaemon(True)  # 守护线程
    th.start()


def deal():
    lock.acquire()
    file = open(file_path, 'r')
    index = 0
    t1 = time.time()
    while True:
        try:
            minTime = entry1.get()
            maxTime = entry2.get()
            if minTime == "" or maxTime == "":
                minTime = 10
                maxTime = 180
            index += 1
            mystr = file.readline()
            if not mystr:
                break
            code = mystr[mystr.find('info=') + 5: mystr.find('info=') + 17]
            log(str(index) + "  " + code)
            scan(code)
            write(mystr.strip())
            log(str(index) + "个核销成功。")
            sleeptime = random.randint(int(minTime), int(maxTime))
            log("本次停顿：" + str(sleeptime))
            time.sleep(sleeptime)
        except RuntimeError as e:
            log(e)
            continue
    t2 = time.time()
    log("总共使用：" + str(t2 - t1))
    file.close()
    lock.release()


if __name__ == '__main__':
    global log_path
    log_path = place + '核销.txt'
    ui()
