import json
import random
import threading
import tkinter
from tkinter import *
from tkinter import filedialog

import requests
import time

lock = threading.Lock()
place = '大连甘井子'

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
        ('storeId', '10373776'),
        ('clientType', 'iOS'),
        ('uid', '467440'),
        ('clientId', 'xapi_01'),
        ('version', '47'),
        ('_uni_source', '2.2'),
        ('merchantId', '10093267'),
        ('loginToken', 'b622d06cf4c48a025e24458d1aac2ffb'),
        ('deviceId', '184d19d52857d3628276407b946e367d208c7c5d'),
        ('appType', 'bpMobile'),
        ('username', '\u5218\u6625\u6653'),
        ('serverVersion', '1'),
        ('clientAgent', 'iPhone9,2/iOS/11.4.1/1242*2208'),
        ('telephone', '15046589521'),
    )

    data = [
        ('_uni_source', '2.2'),
        ('appType', 'bpMobile'),
        ('app_time', '6041370945198'),
        ('app_verification_native', get_random()),
        ('certificateno', code),
        ('checkDevice', '1'),
        ('clientAgent', 'iPhone9,2/iOS/11.4.1/1242*2208'),
        ('clientId', 'xapi_01'),
        ('clientType', 'iOS'),
        ('deviceId', '184d19d52857d3628276407b946e367d208c7c5d'),
        ('loginToken', 'b622d06cf4c48a025e24458d1aac2ffb'),
        ('merchantId', '10093267'),
        ('serverVersion', '1'),
        ('sign', 'b51322396a47e55edf6439d6ccdfe1e8'),
        ('storeId', '10373776'),
        ('telephone', '15046589521'),
        ('uid', '467440'),
        ('username', '%E5%88%98%E6%98%A5%E6%99%93'),
        ('version', '47'),
    ]

    response = requests.post('https://sop.ffan.com/goods/coupon/queryUnusedCoupons', headers=headers, params=params,
                             data=data)
    print(response.text)

    params1 = (
        ('storeId', '10373776'),
        ('clientType', 'iOS'),
        ('uid', '467440'),
        ('clientId', 'xapi_01'),
        ('version', '47'),
        ('_uni_source', '2.2'),
        ('merchantId', '10093267'),
        ('loginToken', 'b622d06cf4c48a025e24458d1aac2ffb'),
        ('deviceId', '184d19d52857d3628276407b946e367d208c7c5d'),
        ('appType', 'bpMobile'),
        ('username', '\u5218\u6625\u6653'),
        ('serverVersion', '1'),
        ('clientAgent', 'iPhone9,2/iOS/11.4.1/1242*2208'),
        ('telephone', '15046589521'),
    )

    data1 = [
        ('_uni_source', '2.2'),
        ('appType', 'bpMobile'),
        ('app_time', '6045306484518'),
        ('app_verification_native', get_random()),
        ('certificateno', code),
        ('clientAgent', 'iPhone9,2/iOS/11.4.1/1242*2208'),
        ('clientId', 'xapi_01'),
        ('clientType', 'iOS'),
        ('deviceId', '184d19d52857d3628276407b946e367d208c7c5d'),
        ('loginToken', 'b622d06cf4c48a025e24458d1aac2ffb'),
        ('memberId', '15000000112912135'),
        ('merchantId', '10093267'),
        ('serverVersion', '1'),
        ('sign', 'b1eff1276e4895873b02b8a83e0b0b33'),
        ('storeId', '10373776'),
        ('telephone', '15046589521'),
        ('uid', '467440'),
        ('userId', '467440'),
        ('username', '%E5%88%98%E6%98%A5%E6%99%93'),
        ('version', '47'),
    ]

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
