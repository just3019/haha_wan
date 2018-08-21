# -*- coding: UTF-8 -*-

import connect_sql

import requests
import json

import urlparse
from urllib import unquote
import urllib2;

import os
import shutil
import base64

import oss2
from Tkinter import *           # 导入 Tkinter 库

from pyexcel_xls import get_data
from pyexcel_xls import save_data

from win32com.client import Dispatch, constants, gencache

import string
import random
import time
import datetime

from subprocess import Popen, PIPE

from os.path import join, getsize
import ConfigParser

# finance_active_id = base64.decodestring('MjA3OQ==')
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# welian_db_name='welian_117'
# welian_open_db_name='welian_open_117'
welian_db_name = 'online_read'
welian_open_db_name = 'online_plantform'

bp_path = '.\\bp\\%s'
http_str = 'http'
pdf_file = '.pdf'
doc_file = '.doc'
docx_file = '.docx'
ppt_file = '.ppt'
pptx_file = '.pptx'
oss_name_default = 'zanw1493278309203.pdf'
section_name = 'config'

finance_active_id_str = 'finance_active_id'
channel_id_str = 'channel_id'
api_name_financeactive_str = 'api_name_financeactive'
api_name_plantform_str = 'api_name_plantform'
# bp_path_conf_str = 'bp_path'

access_key_id = 'ORamB9ohe2HwN5fY'
access_key_secret = 'foomRoC4lxi6U9ofcrS1qRvURCd29K'
pdf_bucket_name = 'welianresource'
alioss_pdf_endpoint = 'oss-cn-hangzhou.aliyuncs.com'

access_key_id = os.getenv('OSS_TEST_ACCESS_KEY_ID', access_key_id)
access_key_secret = os.getenv('OSS_TEST_ACCESS_KEY_SECRET', access_key_secret)
bucket_name = os.getenv('OSS_TEST_BUCKET', pdf_bucket_name)
endpoint = os.getenv('OSS_TEST_ENDPOINT', alioss_pdf_endpoint)
bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)

def log(s):
    print s
    textView.insert(END,'%s\n'%s)
    # textView.insert(END,'\n')
    textView.update()
    textView.see(END)
    f.write('%s\n'%s)
    # f.write('\n')

def init_conf():
    global conf_dict
    conf_dict = {}
    cf = ConfigParser.ConfigParser()
    cf.read('conf.cfg')
    # sections = cf.sections()
    str_finance = entry1.get() # cf.get(section_name, finance_active_id_str)
    arr = str_finance.split('/')
    aid_aidobj = base64.decodestring(arr[-1])
    if 'aid' in aid_aidobj:
        aidobj = eval(aid_aidobj)
        aid = aidobj['aid']
    else:
        aid = aid_aidobj
    log(aid)
    conf_dict[finance_active_id_str] = aid
    # conf_dict[bp_path_conf_str] = cf.get(section_name, bp_path_conf_str)
    # conn = connect_sql.Conn('online_plantform')
    # conn = connect_sql.Conn('welian_open_72')
    conn = connect_sql.Conn(welian_open_db_name)
    conn.connect()
    sql = "select id from extension_link where link_url='%s'" % entry2.get() #cf.get(section_name, channel_id_str)
    result = conn.select(sql)
    if result:
        conf_dict[channel_id_str] = result[0][0]
    else:
        conf_dict[channel_id_str] = ''
    conn.close()
    assert conf_dict[finance_active_id_str]
    conf_dict[api_name_financeactive_str] = cf.get(section_name, api_name_financeactive_str)
    conf_dict[api_name_plantform_str] = cf.get(section_name, api_name_plantform_str)

    log(conf_dict)


def doc2pdf(infile, output):
    gencache.EnsureModule('{00020905-0000-0000-C000-000000000046}', 0, 8, 4)
    infilepath = os.path.abspath('.\\bp') + '\\' + infile
    outputpath = os.path.abspath('.\\bp') + '\\' + output
    w = Dispatch("Word.Application")
    try:
        doc = w.Documents.Open(infilepath, ReadOnly=1)
        doc.ExportAsFixedFormat(outputpath, constants.wdExportFormatPDF,
                                Item=constants.wdExportDocumentWithMarkup,
                                CreateBookmarks=constants.wdExportCreateHeadingBookmarks)
        return 0
    except BaseException, e:
        log(e.args)
        log(e.message)
        return 1
    finally:
        w.Quit(constants.wdDoNotSaveChanges)


def get_file_size(filename):
    if check_bp_exists_in_bp(filename):
        return int(getsize(os.path.abspath('.\\bp') + '\\' + filename) / 1024)
    elif check_bp_exists_in_bp(filename + '.pdf'):
        return int(getsize((os.path.abspath('.\\bp') + '\\' + filename) + '.pdf') / 1024)
    return 0


def gen_oss_name():
    charlist = [random.choice(string.ascii_lowercase) for i in range(4)]
    chars = ''.join(charlist)
    chars = chars + str(int(time.time() * 1000)) + ".pdf"
    return chars


def upload_oss(filename):
    ossname = gen_oss_name()
    # ossname = 'zanw1493278309203.pdf'
    filepath = os.path.abspath('.\\bp')
    bucket.put_object_from_file(ossname, filepath + '\\' + filename)
    assert bucket.object_exists(ossname)
    return ossname


def down_file(url):
    file_name = url.split('/')[-1]
    u = urllib2.urlopen(url)
    f = open(bp_path % file_name, 'wb')  #
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
    f.close()
    return file_name;


len_cols = 9


def check_row(row):
    if len(row) >= len_cols:
        return row
    for i in range(len(row), len_cols):
        row.append('')
    return row


def check_bp_exists_in_bp(filename):
    path = bp_path % filename
    return os.path.exists(path)


# 姓名	手机号	公司	职位	项目名称	一句话介绍	项目阶段	bp网址或文件名	城市名称	一级领域	二级领域	融资阶段	融资金额	融资金额单位	出让股份(%)
col_name = 0
col_mobile = 1
col_company = 2
col_position = 3
col_pname = 4
col_intro = 5
col_bp = 6
col_bp_ossname = 7

# api_name_financeactive = "http://sevnew.welian.com/web/financeactive/guestrecord"
# api_name_financeactive = "http://192.168.1.253:8090/web/financeactive/guestrecord"
# api_name_financeactive = "http://localhost:8080/web/financeactive/guestrecord"
# api_name_financeactive = "http://welian.online:8084/web/financeactive/guestrecord"
# api_name_financeactive = "http://sev.welian.com/web/financeactive/guestrecord"

headers = {'content-type': 'application/json'}


def modify_mobile(mobile):
    return mobile.replace('-', '').replace(' ', '') + "_手机号"


def getNotNullStr(s):
    if s:
        return s
    else:
        ''


def get_limit_str(intro, lim):
    if not intro:
        return '无'
    return intro[0:lim]


def getWuStr(s):
    if not s:
        return '无'
    return s


def request_plantform(mobile):
    data = {}
    data['extensionLinkId'] = conf_dict[channel_id_str]
    data['isOpenFinancingService'] = 0  # 不开启融资服务
    data['type'] = 1  # 来自pc
    # 用户
    user = {}
    # conn_welian = connect_sql.Conn('online_read')
    # conn_welian = connect_sql.Conn('welian_72')
    conn_welian = connect_sql.Conn(welian_db_name)
    conn_welian.connect()
    sql_get_uid = 'select id from account where username = "%s"' % mobile
    get_uid = conn_welian.select(sql_get_uid)
    if get_uid:
        user['uid'] = get_uid[0][0]
    data['user'] = user
    # 项目
    project = {}
    if 'uid' in user and user['uid']:
        sql_get_project = 'select id,name,intro,logo from project where uid = %s and deleted=0 order by id desc limit 0,1' % \
                          user['uid']
        get_project = conn_welian.select(sql_get_project)
        if get_project:
            project['pid'] = get_project[0][0]
            project['name'] = get_project[0][1]
            project['logo'] = get_project[0][3]
            project['intro'] = get_limit_str(get_project[0][2], 100)
            project['cityId'] = 1
            project['cityName'] = '中国'
            project['projectStage'] = 3
            project['industryFirstId'] = 34
            project['industryFirstName'] = '工具'
            project['industrySecondId'] = 349
            project['industrySecondName'] = '其他'
    data['project'] = project
    # 融资信息
    financingInfo = {}
    financingInfo['stage'] = 0
    financingInfo['amount'] = 100
    financingInfo['amountUnit'] = 3  # 亿人民币
    financingInfo['share'] = 1

    data['financingInfo'] = financingInfo

    # bp信息
    bp = {}
    if 'pid' in project and project['pid']:
        sql_get_bp = 'select id,title,size,url from project_plan where pid=%s order by id desc limit 0,1' % project[
            'pid']
        get_bp = conn_welian.select(sql_get_bp)
        if get_bp:
            bp['bpId'] = get_bp[0][0]
            bp['bpName'] = get_bp[0][1]
            bp['bpSize'] = get_bp[0][2]
            bp['bpUrl'] = get_bp[0][3]

    data['bp'] = bp

    conn_welian.close()

    log(json.dumps(data))
    r = requests.post(conf_dict[api_name_plantform_str], data=json.dumps(data), headers=headers)
    log(r.text)
    # st = str(r.text)
    # print unquote(st)


def getUid(mobile):
    result = 0
    sql = 'select id from account where username = "%s"' % mobile
    conn_welian = connect_sql.Conn(welian_db_name)
    conn_welian.connect()
    data = conn_welian.select(sql)
    if data:
        result = data[0][0]
    conn_welian.close()
    return result


def getPid(uid, pname):
    result = 0
    if 0 == uid:
        return result
    sql = 'select id from project where uid="%s" and name="%s" and deleted=0 and type!=1' % (uid, pname)
    conn_welian = connect_sql.Conn(welian_db_name)
    conn_welian.connect()
    data = conn_welian.select(sql)
    if data:
        result = data[0][0]
    conn_welian.close()
    return result


def read_xls_file():

    init_conf()

    # print os.getcwd()
    # print os.path.abspath('.')
    log(u'开始导入')
    path = os.path.abspath('.') + "\\bp.xlsx"
    log(path)
    xls_data = get_data(path)
    # xls_data = get_data(os.path.abspath('.')+"\\bp_1.xlsx")
    failed_result = {}

    active_id = conf_dict[finance_active_id_str]  # base64.decodestring(conf_dict[finance_active_id_str])
    for sheet_n in xls_data.keys():
        # print sheet_n, ":", xls_data[sheet_n]
        # print (type(xls_data[sheet_n]))
        l = xls_data[sheet_n][1:]
        len_of_l = len(l)
        for row in l:
            index = l.index(row) + 1
            jindu = float(index) / len_of_l * 100
            log('\n')
            log(datetime.datetime.now().strftime('%b-%d-%y %H:%M:%S'))
            log(u'正在报名融资活动第%s条数据,进度%s%%' % (index, jindu))
            # print row[col_bp]
            # print len(row)
            row = check_row(row)
            if '' == row[col_bp] or '无' == row[col_bp]:
                row[col_bp] = oss_name_default
                row[col_bp_ossname] = oss_name_default
            else:
                if oss_name_default == row[col_bp]:
                    row[col_bp_ossname] = oss_name_default
                else:
                    if row[col_bp].startswith(http_str):
                        row[col_bp] = down_file(row[col_bp])
                        log(row[col_bp])
                        # if not row[col_bp].endswith(pdf_file): # 有些文件没有后缀名,不能直接这么转换
                        #     # 转换非pdf文件
                        if row[col_bp].endswith(doc_file) or row[col_bp].endswith(docx_file):  # 如果后缀名是doc或者docx，转换
                            output = (os.path.splitext(row[col_bp]))[0] + '.pdf'
                            if 0 == doc2pdf(row[col_bp], output):
                                row[col_bp] = output
                                # print 'word'
                                #     if row[col_bp].endswith(ppt_file) or row[col_bp].endswith(pptx_file):
                                #         print 'ppt'

            # 通过oss api上传 得到文件名
            if not row[col_bp_ossname]:
                # 上传之前判断文件是否存在,如果不存在,放弃这条数据(第一批给到的数据中,文件名都没有.pdf的后缀,判断文件是否存在,不存在时,加上.pdf再判断一次,还不存在就放弃)
                local_file_name = row[col_bp]
                local_file_name2 = row[col_bp] + ".pdf"
                if check_bp_exists_in_bp(local_file_name):
                    log(local_file_name)
                    oss_name = upload_oss(local_file_name)
                    row[col_bp_ossname] = oss_name
                else:
                    if check_bp_exists_in_bp(local_file_name2):
                        log(local_file_name2)
                        oss_name = upload_oss(local_file_name2)
                        row[col_bp_ossname] = oss_name

            log('row[col_bp_ossname]:%s' % row[col_bp_ossname])
            if not row[col_bp_ossname]:
                row[col_bp_ossname] = oss_name_default
                failed_result[index] = row

            if row[col_bp_ossname]:
                # 组装数据报名融资活动
                s = {}
                user = {}

                user["name"] = get_limit_str(row[col_name], 20)
                user["mobile"] = modify_mobile(str(row[col_mobile]))  # row[col_mobile] #
                user["uid"] = getUid(user["mobile"])
                user["position"] = getWuStr(row[col_position])
                user["company"] = getWuStr(row[col_company])
                s["user"] = user
                project = {}
                project["pid"] = getPid(user["uid"], row[col_pname])
                project["name"] = getWuStr(row[col_pname])
                project["intro"] = get_limit_str(row[col_intro], 500)
                bp = {}
                bp["bpid"] = 0
                bp["size"] = get_file_size(row[col_bp])
                bp["title"] = row[col_bp]
                bp["url"] = row[col_bp_ossname]
                project["bp"] = bp
                s["project"] = project
                s["activeid"] = active_id
                s["emailnotice"] = -1
                s["source"] = 5
                s["resource"] = 'leadin'

                log(json.dumps(s))
                r = requests.post(conf_dict[api_name_financeactive_str], data=json.dumps(s), headers=headers)
                # print r.text
                st = str(r.text)
                # print st
                log(unquote(st).decode('utf-8'))

                # # 组装数据报名开放平台
                # if conf_dict[channel_id_str] and conf_dict[api_name_plantform_str] and "mobile" in user:
                #     request_plantform(user["mobile"])

        log('\n融资活动报名结束\n\n')
        for row in l:
            index = l.index(row) + 1
            jindu = float(index) / len_of_l * 100
            log('\n')
            log(datetime.datetime.now().strftime('%b-%d-%y %H:%M:%S'))
            log(u'正在报名开放平台的第%s条数据,进度%s%%' % (index, jindu))
            # 组装数据报名开放平台
            if conf_dict[channel_id_str] and conf_dict[api_name_plantform_str]:
                request_plantform(modify_mobile(str(row[col_mobile])))
        log('\n开发平台报名结束\n\n')
        if failed_result:
            log('\n\n')
            log(u"使用默认bp文件的部分:\n")
            log(json.dumps(failed_result))
        log('\n\n')
        log(u'导入完成')

def showUI():
    root = Tk()  # 创建窗口对象的背景色
    # 创建两个列表
    root.title('外部项目导入')
    root.geometry('400x400')
    label1 = Label(root, text='融资活动地址：')  # '融资活动地址：'
    global entry1
    entry1 = Entry(root, width=200) #root,textvariable=Labelvar, anchor='w'
    label2 = Label(root, text='开放平台地址：')  # '开放平台地址'
    global entry2
    entry2 = Entry(root, width=200)
    label1.pack(expand=YES, fill=X)
    entry1.pack()
    label2.pack(expand=YES, fill=X)
    entry2.pack()
    global s1
    s1 = Scrollbar(root)
    s1.pack(side=RIGHT, fill=Y)
    global textView
    textView = Text(root, width=400, height=20, yscrollcommand=s1.set)

    label3 = Label(root, text='日志输出：')  # '
    label3.pack()
    textView.pack(expand=YES, fill=X)
    s1.config(command=textView.yview)
    btn = Button(root, text='开始', command=read_xls_file)
    btn.pack(expand=YES, fill=X)
    root.mainloop()  # 进入消息循环

if __name__ == '__main__':
    global f
    f = open('.\\logs\\%s.txt' % time.time(), 'w+')
    showUI()

    # read_xls_file()
    f.close()
    pass
