# -*- coding: utf-8 -*-

import requests
import string
import itertools



# Get url
def get_url(num):
    letters = list(string.ascii_uppercase)
    combinations = [''.join(x) for x in itertools.product(*[letters] * num)]
    urls = []

    for combt in combinations:
        urls.append('http://www.cuitx.cn/A'+combt)
    return urls


# Request url
def get_info(url):
    headers = {'User-Agent': 'Mozilla/5.0(Windows NT 6.1; Win64;x64;rv:59.0) Gecko/20100101 Firefox/59.0'}
    html = requests.get(url=url, headers=headers)
    return html.text


if __name__ == "__main__":
    num = 5
    urls = get_url(num)
    for url in urls:
        html = get_info(url)
        print(html)


