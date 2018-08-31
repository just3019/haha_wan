import json
from urllib import request

import haima
import xunma

list = [{"name": "平阳", "username": "ye907182374", "password": "baobao1515"},
        # {"name": "鸡西", "username": "9879870", "password": "a123123"},
        # {"name": "台州", "username": "demon3019", "password": "123456"},
        {"name": "回民区", "username": "aq123123123", "password": "a123123"},
        # {"name": "湖州", "username": "huzhou", "password": "huzhou"},
        {"name": "金华", "username": "ye907182374", "password": "baobao1515"},
        {"name": "三明", "username": "sanming1", "password": "sanming1"},
        {"name": "辽阳", "username": "chongzhou", "password": "chongzhou"},
        {"name": "崇州", "username": "chongzhou", "password": "chongzhou"},
        {"name": "宁德", "username": "ningde", "password": "ningde"},
        {"name": "西双版纳", "username": "xishuangbanna", "password": "xishuangbanna"},
        # {"name": "重庆北碚", "username": "chongqingbeibei", "password": "chongqingbeibei"},
        {"name": "漳州台商", "username": "zhangzhouts1", "password": "zhangzhouts1"},
        {"name": "观山湖", "username": "guanshanhu", "password": "guanshanhu"},
        {"name": "江门", "username": "jiangmeng", "password": "jiangmeng"},
        {"name": "衢州", "username": "quzhou", "password": "quzhou"},
        # {"name": "北海", "username": "beihai1", "password": "beihai1"},
        {"name": "沈阳铁西", "username": "shenyangtiexi", "password": "shenyangtiexi"},
        {"name": "六盘水", "username": "liupanshui", "password": "liupanshui"},
        {"name": "南宁江南", "username": "nanningjiangnan", "password": "nanningjiangnan"},
        {"name": "乌海", "username": "wuhaiwanda", "password": "wuhaiwanda"},
        {"name": "滨州", "username": "binzhou", "password": "binzhou"}]


#         {"name": "漳州台商", "username": "zhangzhouts", "password": "zhangzhouts"},


def get_user(username, password):
    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
    # 登陆/获取TOKEN
    global TOKEN
    TOKEN = ''
    url = 'http://api.fxhyd.cn/UserInterface.aspx?action=login&username=' + username + '&password=' + password
    TOKEN1 = request.urlopen(request.Request(url=url, headers=header_dict)).read().decode(encoding='utf-8')
    if TOKEN1.split('|')[0] == 'success':
        TOKEN = TOKEN1.split('|')[1]
    else:
        raise RuntimeError("获取不到token")
    # 获取账户信息
    url = 'http://api.fxhyd.cn/UserInterface.aspx?action=getaccountinfo&token=' + TOKEN + '&format=1'
    ACCOUNT1 = request.urlopen(request.Request(url=url, headers=header_dict)).read().decode(encoding='utf-8')
    if ACCOUNT1.split('|')[0] == 'success':
        ACCOUNT = ACCOUNT1.split('|')[1]
        return ACCOUNT
    else:
        print('获取TOKEN错误,错误代码' + ACCOUNT1)
        raise RuntimeError("获取不到用户")


if __name__ == '__main__':
    f = open("账号使用情况.txt", "w")

    for i in list:
        try:
            result = json.loads(get_user(i['username'], i['password']))
            p = i['name'] + " " + i['username'] + " " + i['password'] + " " + str(result['Balance']) + "元 " + TOKEN
            print(p)
            f.write('%s\n' % p)
        except RuntimeError as e:
            print(e)
            pp = i['name'] + " " + i['username'] + " " + i['password'] + "  失效。"
            f.write('%s\n' % pp)
            continue

    f.write("\n")
    r = xunma.xm_login("demon3019", "12345678", "wdVJ21MmabfWT72lAxf3JA==")
    p = "讯码 demon3019 12345678 " + str(r[1]) + " http://www.xunma.net/userManage/index.aspx\n"
    xunma.xm_logout(r[0])
    f.write("%s\n" % p)
    r = json.loads(haima.hm_login())
    p = "海码 demon3019 123456 " + str(r["Balance"])
    f.write("%s" % p)
    f.close()
