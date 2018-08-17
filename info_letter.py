#-*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import string
import itertools
import pandas as pd
#获取网址
def get_url(num):
    letters=list(string.ascii_uppercase)
    combinations=[''.join(x) for x in itertools.product(*[letters] *num)]
    urls=[]
    for combt in combinations:
        urls.append('http://www.cuitx.cn/'+combt)
    return urls
# 给定网址，请求数据
def get_info(url):
    headers = {'User-Agent': 'Mozilla/5.0(Windows NT 6.1; Win64;x64;rv:59.0) Gecko/20100101 Firefox/59.0'}
    html= requests.get(url=url, headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')
    return soup
#解析数据之前，需要判断数据是否存在
#判断网页请求结果
def judge(soup):
    title=soup.find('title').get_text()
    if "404" in title:
        return "找不到文件或目录!"
    elif  "500" in title :
        return "内部服务器错误!"
    else:
        form=soup.find('form',{'id':'form1'}).get('action')
        if form=="./Error.aspx":
            return "程序暂时无法处理访问请求!"
        else:
            script=str(list(soup.find_all('script'))[-1])
            if "该数据不存在或已删除！" in script:
                return "该数据不存在或已删除!"
            elif "债权暂时无法查看！" in script:
                return "债权暂时无法查看!"
            else:
                return "可以正常解析数据!"
#解析数据
def parse_info(soup):
    data= soup.find_all('span')
    name=re.findall(r'<span id="alternate_field13" .*?>(.*?)</span>',str(data))[0]
    creditor=re.findall(r'<span id="alternate_field12" .*?>(.*?)</span>',str(data))[1]
    area=re.findall(r'<span id="alternate_field14" .*?>(.*?)</span>',str(data))[0]+"小区"
    money=re.findall(r'<span id="alternate_field14" .*?>(.*?)</span>',str(data))[1]+"元"
    year=re.findall(r'<span id="year" .*?>(.*?)</span>',str(data))[0]
    month=re.findall(r'<span id="month" .*?>(.*?)</span>',str(data))[0]
    day=re.findall(r'<span id="day" .*?>(.*?)</span>',str(data))[0]
    date=str(year)+"年"+str(month)+"月"+str(day)+"日"
    return name,creditor,area,money,date
#保存信息
def save_info(names,creditors,areas,moneys,dates):
    result = pd.DataFrame()
    result['names'] = names
    result['creditors'] = creditors
    result['areas'] = areas
    result['moneys'] = moneys
    result['dates'] = dates
    result.to_csv('result.csv', index=None)
#运行程序
urls=get_url(5)
names=[];creditors=[];areas=[];moneys=[];dates=[]
for url in urls:
    soup=get_info(url)
    if judge(soup)=="可以正常解析数据!":
        name, creditor, area, money, date=parse_info(soup)
        names.append(name)
        creditors.append(creditor)
        areas.append(area)
        moneys.append(money)
        dates.append(date)
save_info(names,creditors,areas,moneys,dates)



