# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup

import get_html as gh


# Judge the contents of html
def judge(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        if html is not None:
            title = soup.find('title').get_text()

            if "404" in title:
                return "找不到文件或目录!"
            elif "500" in title:
                return "内部服务器错误!"
            else:
                form = soup.find('form', {'id': 'form1'}).get('action')
                if form == "./Error.aspx":
                    return "程序暂时无法处理访问请求!"
                else:
                    script = str(list(soup.find_all('script'))[-1])
                    if "该数据不存在或已删除！" in script:
                        return "该数据不存在或已删除!"
                    elif "债权暂时无法查看！" in script:
                        return "债权暂时无法查看!"
                    else:
                        return "可以正常解析数据!"
    except:
        return "未知页面状态"


# Parse the html
def parse_html(html):
    soup = BeautifulSoup(html, 'lxml')
    # info = soup.find('div', {'class': 'personal'})
    # info = info.find_all('li')
    # sex = re.findall(r'别：([男女])', info)
    # idnum1 = re.findall(r'证：(\d{6})', info)
    # idnum2 = info[3].find_all('span')[2].get_text()
    # idnum = idnum1 + '??' + idnum2
    # phonenum = re.findall(r'手机号码：(\d{9})', info)
    data = soup.find_all('span')
    name = re.findall(r'<span id="alternate_field13" .*?>(.*?)</span>',str(data))[0]
    creditor = re.findall(r'<span id="alternate_field12" .*?>(.*?)</span>',str(data))[1]
    area = re.findall(r'<span id="alternate_field14" .*?>(.*?)</span>',str(data))[0]+"小区"
    money = re.findall(r'<span id="alternate_field14" .*?>(.*?)</span>',str(data))[1]+"元"
    year = re.findall(r'<span id="year" .*?>(.*?)</span>',str(data))[0]
    month = re.findall(r'<span id="month" .*?>(.*?)</span>',str(data))[0]
    day = re.findall(r'<span id="day" .*?>(.*?)</span>',str(data))[0]
    date = str(year)+"年"+str(month)+"月"+str(day)+"日"
    return name, creditor, area, money, date

if __name__ == '__main__':
    urls = ['http://www.cuitx.cn/AGNEGC', 'http://www.cuitx.cn/AGNEGB', 'http://www.cuitx.cn/AGNEGA']
    for url in urls:
        html = gh.get_info(url)
        state = judge(html)
        if state is "可以正常解析数据!":
            name, creditor, area, money, date = parse_html(html)
            print(name)
            print(creditor)
            print(area)
            print(money)
            print(date)