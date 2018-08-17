from  multiprocessing.dummy import Pool as ThreadPool

import get_html  as gh
import parse_html  as ph

NUM = 5
urls = gh.get_url(NUM)
pool = ThreadPool(4)
htmls = pool.map(gh.get_info,urls[100:150])
pool.close()
pool.join()

names = []
creditors = []
areas = []
moneys = []
dates = []

for html in htmls:
    if ph.judge(html) is "可以正常解析数据!":
        name, creditor, area, money, date=ph.parse_html(html)

        print(name)
        print(creditor)
        print(area)
        print(money)
        print(date)

        names.append(name)
        creditors.append(creditor)
        areas.append(area)
        moneys.append(money)
        dates.append(date)


