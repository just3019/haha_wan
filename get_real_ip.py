import requests
from bs4 import BeautifulSoup


def get_host_ip():
    apiurl = "https://www.ipip.net/"
    content = requests.get(apiurl)
    content.encoding = 'utf-8'
    html = BeautifulSoup(content.text, 'lxml')
    i = 0
    result = ''
    for row in html.find('div', class_='yourInfo').find_all('li'):
        i += 1
        value = row.get_text()
        if i > 4:
            break
        result += "|" + value
    return result


if __name__ == '__main__':
    print(get_host_ip())
