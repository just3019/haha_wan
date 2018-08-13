import json

import requests


def login(username, password):
    url = "http://api.fxhyd.cn/UserInterface.aspx?action=login&username=%s&password=%s" % (username, password)
    print(url)


if __name__ == '__main__':
    login("zhangzhouts", "zhangzhouts")
