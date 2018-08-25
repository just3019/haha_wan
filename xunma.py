import requests

ITEMID = "3410"  # 飞凡网


def xm_login(username, password, developer):
    url = "http://xapi.xunma.net/Login"
    params = {
        ("uName", username),
        ("pWord", password),
        ("Developer", developer),
        ("Code", "UTF8"),
    }
    response = requests.get(url, params=params).text.split("&")
    print(response)
    return response





if __name__ == '__main__':
    login_result = xm_login("demon3019", "12345678", "wdVJ21MmabfWT72lAxf3JA==")
    token = login_result[0]
    print(token)
    xm_project(token)
    # xm_project()
