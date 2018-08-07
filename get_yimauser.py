import json
from urllib import request

list = [{"name": "平阳", "username": "ye907182374", "password": "baobao1515"},
        {"name": "鸡西", "username": "9879870", "password": "a123123"},
        {"name": "台州", "username": "demon3019", "password": "123456"},
        {"name": "回民区", "username": "aq123123123", "password": "a123123"},
        {"name": "湖州", "username": "huzhou", "password": "huzhou"},
        {"name": "金华", "username": "ye907182374", "password": "baobao1515"},
        {"name": "三明", "username": "sanming1", "password": "sanming1"},
        {"name": "辽阳", "username": "chongzhou", "password": "chongzhou"},
        {"name": "崇州", "username": "chongzhou", "password": "chongzhou"},
        {"name": "宁德", "username": "ningde", "password": "ningde"},
        {"name": "西双版纳", "username": "xishuangbanna", "password": "xishuangbanna"},
        {"name": "重庆北碚", "username": "chongqingbeibei", "password": "chongqingbeibei"},
        {"name": "漳州台商", "username": "zhangzhouts1", "password": "zhangzhouts1"},
        {"name": "观山湖", "username": "guanshanhu", "password": "guanshanhu"},
        {"name": "江门", "username": "jiangmeng", "password": "jiangmeng"}]


#         {"name": "漳州台商", "username": "zhangzhouts", "password": "zhangzhouts"},


def get_user(username, password):
    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}

    # 登陆/获取TOKEN
    TOKEN = ''
    url = 'http://api.fxhyd.cn/UserInterface.aspx?action=login&username=' + username + '&password=' + password
    TOKEN1 = request.urlopen(request.Request(url=url, headers=header_dict)).read().decode(encoding='utf-8')
    if TOKEN1.split('|')[0] == 'success':
        TOKEN = TOKEN1.split('|')[1]
    else:
        print(
            '获取TOKEN错误,错误代码' + TOKEN1 + '。代码释义：1001:参数token不能为空;1002:参数action不能为空;1003:参数action错误;1004:token失效;1005'
                                        ':用户名或密码错误;1006:用户名不能为空;1007:密码不能为空;1008:账户余额不足;1009:账户被禁用;1010:参数错误;1011'
                                        ':账户待审核;1012:登录数达到上限')

    # 获取账户信息
    url = 'http://api.fxhyd.cn/UserInterface.aspx?action=getaccountinfo&token=' + TOKEN + '&format=1'
    ACCOUNT1 = request.urlopen(request.Request(url=url, headers=header_dict)).read().decode(encoding='utf-8')
    if ACCOUNT1.split('|')[0] == 'success':
        ACCOUNT = ACCOUNT1.split('|')[1]
        return ACCOUNT
    else:
        print('获取TOKEN错误,错误代码' + ACCOUNT1)


if __name__ == '__main__':
    f = open("账号使用情况.txt", "w")

    for i in list:
        result = json.loads(get_user(i['username'], i['password']))
        p = i['name'] + " " + i['username'] + " " + i['password'] + " " + str(result['Balance']) + "元"
        print(p)
        f.write('%s\n' % p)

    f.close()
