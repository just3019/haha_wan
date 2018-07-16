import requests


def wanda_login(mobile, code):
    import requests

    headers = {
        'Host': 'api.ffan.com',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15F79 MicroMessenger/6.7.1 NetType/WIFI Language/zh_CN',
        'Referer': 'https://servicewechat.com/wx07dfb5d79541eca9/81/page-frame.html',
        'Accept-Language': 'zh-cn',
    }

    data = [
        ('mobile', mobile),
        ('verifyCode', code),
        ('plazaId', '1000770'),
        ('source', 'MINA'),
        ('wxFfanToken', '6cc7fda5c8674951b446126226ac51ac'),
        ('wandaUser', '[object Object]'),
        ('error', ''),
        ('downcount', '60'),
        ('inter', 'null'),
        ('phonefocus', 'false'),
        ('codefocus', 'false'),
    ]

    response = requests.post('https://api.ffan.com/microapp/v1/ffanLogin', headers=headers, data=data)
    result = response.text
    print('登录后的信息：\n' + result)
    return result


if __name__ == '__main__':
    wanda_login('18815150996', '545929')
