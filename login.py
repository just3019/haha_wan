import random

import requests

# c57f13fb3b2e4b038b316bf4f0cd1e79
# 74ab910197474826b288edd65d74393c
wxFfanToken = "c57f13fb3b2e4b038b316bf4f0cd1e79"
cho = ["74ab910197474826b288edd65d74393c", "74ab910197474826b288edd65d74393c"]
wxFfanToken = random.choice(cho)
print(wxFfanToken)


def wanda_login(mobile, code):
    data = [
        ('mobile', mobile),
        ('verifyCode', code),
        ('plazaId', '1000770'),
        ('source', 'MINA'),
        ('wxFfanToken', "74ab910197474826b288edd65d74393c"),
    ]
    response = requests.post('https://api.ffan.com/microapp/v1/ffanLogin', data=data)
    result = response.text
    print('登录后的信息：\n' + result)
    return result


if __name__ == '__main__':
    wanda_login('18294437809', '146492')

#
# import requests
#
# headers = {
#     'Host': 'api.ffan.com',
#     'Accept': '*/*',
#     'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15G77 MicroMessenger/6.7.1 NetType/WIFI Language/zh_CN',
#     'Referer': 'https://servicewechat.com/wx07dfb5d79541eca9/83/page-frame.html',
#     'Accept-Language': 'zh-cn',
# }
#
# data = [
#   ('mobile', '15143214532'),
#   ('verifyCode', '739028'),
#   ('plazaId', '1000770'),
#   ('source', 'MINA'),
#   ('wxFfanToken', '4b3fa83eb4ec4c518d58f03ab176c98d'),
#   ('wandaUser', '[object Object]'),
#   ('error', ''),
#   ('downcount', '32'),
#   ('inter', '588'),
#   ('phonefocus', 'false'),
#   ('codefocus', 'false'),
# ]
#
# response = requests.post('https://api.ffan.com/microapp/v1/ffanLogin', headers=headers, data=data)
# print(response.text)
