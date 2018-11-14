import json
import random
import threading
import time
from tkinter import *
from tkinter import filedialog

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


def openfile():
    r = filedialog.askopenfilename(title='打开文件', filetypes=[('Python', '*.txt'), ('All Files', '*')])
    log("当前操作的文件是：" + r)
    global file_path
    file_path = r


def ui():
    root = Tk()
    root.title('核销工具')
    root.geometry('320x280')

    fm1 = Frame(root)
    fm1.pack(fill=X)
    Label(fm1, text='账号').pack(side=LEFT)
    global entryPhone
    entryPhone = Entry(fm1, width=11)
    entryPhone.pack(side=LEFT)
    Button(fm1, text="发送验证码", command=send_v_code).pack(side=LEFT)

    fm2 = Frame(root)
    fm2.pack(fill=X)
    Label(fm2, text="验证码").pack(side=LEFT)
    global entryCode
    entryCode = Entry(fm2, width=8)
    entryCode.pack(side=LEFT)
    Button(fm2, text="登录", command=login).pack(side=LEFT)

    fm3 = Frame(root)
    fm3.pack(fill=X)
    global btn_file
    btn_file = Button(fm3, text='选择券文件', command=openfile).pack(side=LEFT)
    Label(fm3, text="间隔").pack(side=LEFT)
    global interval
    ie = StringVar()
    interval = Entry(fm3, width=4, textvariable=ie)
    ie.set(30)
    interval.pack(side=LEFT)

    global s1
    s1 = Scrollbar(root)
    s1.pack(side=RIGHT, fill=Y)
    global textView
    textView = Text(root, height=10, yscrollcommand=s1.set)
    textView.pack(expand=YES, fill=X)
    s1.config(command=textView.yview)

    fm4 = Frame(root)
    fm4.pack()
    Button(fm4, text="核销").pack(side=LEFT)

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
    result = json.loads(response.text)
    if result["status"] == 200:
        log("验证码发送成功")
    else:
        log("发送失败：%s" % result["message"])


def login():
    printf("登录")


if __name__ == '__main__':
    ui()
