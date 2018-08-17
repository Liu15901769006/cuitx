from pymongo import MongoClient
import time

import get_html as gh
import parse_html as ph

user = 'crawl'
pwd = 'crawl123'
server = '10.138.61.39'
port = "27017"
db_name = 'crawl'

uri = 'mongodb://' + user + ':' + pwd + '@' + server + ':' + port +'/'+ db_name
client = MongoClient(uri)
db = client["crawl"]
col = db.a

urls = gh.get_url(5)
total = 0
start = time.time()
url = urls[0]
html = gh.get_info(url)
state = ph.judge(html)
col.insert_one({'url': url, 'state': state, 'html': html})

total += 1
print("已插入%d条数据" % total)

time.sleep(20)
end = time.time()
print(end-start)
