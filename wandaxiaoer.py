import random
import threading
import time
from tkinter import *

import requests


def printf(s):
    print('[%s][%s]%s' % (threading.current_thread().getName(), time.strftime("%X"), s))


def log(s):
    printf(s)
    textView.insert(END, '[%s][%s]%s\n' % (threading.current_thread().name, time.strftime("%X"), s))
    textView.update()
    textView.see(END)


def write(s):
    f = open("核销数据.txt", "a")
    f.write('[%s]%s\n' % (time.strftime("%X"), s.strip()))
    f.close()


def get_interval_time():
    interval_time = interval.get()
    slep = random.randint(0, int(interval_time))
    printf("本次停顿：%s秒" % slep)
    if interval_time.isdigit():
        return slep
    return 0


def ui():
    root = Tk()
    root.title('核销工具')
    root.geometry('320x210')

    fm1 = Frame(root)
    fm1.pack(fill=X)
    Label(fm1, text='账号').pack(side=LEFT)
    global entryPhone
    entryPhone = Entry(fm1, width=11)
    entryPhone.pack(side=LEFT)
    Button(fm1, text="发送验证码", command=send_v_code)
    Label(fm1, text="间隔").pack(side=LEFT)
    global interval
    ie = StringVar()
    interval = Entry(fm1, width=4, textvariable=ie)
    ie.set(30)
    interval.pack(side=LEFT)

    global s1
    s1 = Scrollbar(root)
    s1.pack(side=RIGHT, fill=Y)
    global textView
    textView = Text(root, height=10, yscrollcommand=s1.set)
    textView.pack(expand=YES, fill=X)
    s1.config(command=textView.yview)

    root.mainloop()


def send_v_code():
    phone = entryPhone.get()
    headers = {
        'charset': 'utf-8',
        'referer': 'https://servicewechat.com/wx57ebde74de5e6267/6/page-frame.html',
        'content-type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; MP1503 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/44.0.2403.119 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070339) NetType/WIFI Language/zh_CN Process/appbrand2',
        'Host': 'api.beyonds.com',
    }
    data = 'mobile=%s' % phone
    response = requests.post('https://api.beyonds.com/wpxe/v1/user/sendVerifyCode', headers=headers, data=data)
    printf(response.text)


if __name__ == '__main__':
    ui()
