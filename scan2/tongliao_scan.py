import random
import threading
import time
from tkinter import *
from tkinter import filedialog

import requests

from thread_pool import ThreadPool

lock = threading.Lock()

place = "通辽"

storeId = "100006884"
userid = "269038101515313152"
token = "MjcwNjQ4NzMzMDExMzgyMjcy"


def printf(s):
    print('[%s][%s]%s' % (threading.current_thread().getName(), time.strftime("%X"), s))


def log(s):
    printf(s)
    textView.insert(END, '[%s][%s]%s\n' % (threading.current_thread().name, time.strftime("%X"), s))
    textView.update()
    textView.see(END)


def write(s):
    f = open("%s核销数据%s.txt" % (place, time.strftime("%Y%m%d")), "a")
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
    root.title('%s核销工具' % place)
    root.geometry('320x220')

    # fm1 = Frame(root)
    # fm1.pack(fill=X)
    # Label(fm1, text='账号').pack(side=LEFT)
    # global entryPhone
    # entryPhone = Entry(fm1, width=11)
    # entryPhone.pack(side=LEFT)
    # Button(fm1, text="发送验证码", command=send_v_code).pack(side=LEFT)
    #
    # fm2 = Frame(root)
    # fm2.pack(fill=X)
    # Label(fm2, text="验证码").pack(side=LEFT)
    # global entryCode
    # entryCode = Entry(fm2, width=8)
    # entryCode.pack(side=LEFT)
    # Button(fm2, text="登录", command=login).pack(side=LEFT)

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
    Button(fm4, text="核销", command=verification).pack(side=LEFT)

    root.mainloop()


def verification():
    th = threading.Thread(target=deal)
    th.setDaemon(True)
    th.start()


def deal():
    lock.acquire()
    file = open(file_path, 'r')
    index = 0
    t1 = time.time()
    TP = ThreadPool(30)
    while True:
        try:
            index += 1
            mystr = file.readline()
            if not mystr:
                break
            code = mystr.split("|")[1].strip()
            TP.add_task(scan, code, index)
            time.sleep(get_interval_time())
        except RuntimeError as e:
            log(e)
            continue
    TP.wait_completion()
    log("总共使用：%s" % (time.time() - t1))
    file.close()
    lock.release()


def scan(code, index):
    try:
        log("第%s个核销开始" % index)
        verify(code)
        write(code)
        log("核销第%s个券%s成功" % (index, code))
    except RuntimeError as e:
        log("%s核销有问题" % code)


def verify(code):
    headers = {
        'charset': 'utf-8',
        'referer': 'https://servicewechat.com/wx57ebde74de5e6267/6/page-frame.html',
        'workingorgcode': storeId,
        'tenantid': "2018092600001",
        'token': token,
        'userid': userid,
        'content-type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; MP1503 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/44.0.2403.119 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070339) NetType/WIFI Language/zh_CN Process/appbrand2',
        'Host': 'api.beyonds.com',
    }
    data = 'couponCode=%s&storeId=%s' % (code, storeId)
    response = requests.post('https://api.beyonds.com/wpxe/v1/coupon/verify', headers=headers, data=data)
    printf(response.text)


if __name__ == '__main__':
    ui()
