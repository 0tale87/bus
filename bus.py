#!/usr/bin/python3/env
# -*- Coding: utf-8 -*-
import requests, bs4,re
import datetime,urllib.parse

now = datetime.datetime.now()
print("現在時刻は"'{0:%Y}'"年"'{0:%m}'"月"'{0:%d}'"日"'{0:%H}'"時"'{0:%M}'"分です".format(now))

now = now + datetime.timedelta(minutes=15)

url='https://www.navitime.co.jp/bustransit/search?orvStationName=%E7%A5%9E%E5%A7%AB%E3%83%90%E3%82%B9%E4%B8%89%E3%83%8E%E5%AE%AE%E3%83%90%E3%82%B9%E3%82%BF%E3%83%BC%E3%83%9F%E3%83%8A%E3%83%AB&dnvStationName=%E3%82%86%E3%82%8A%E3%81%AE%E3%81%8D%E5%8F%B0%EF%BC%93%E4%B8%81%E7%9B%AE&month=2018%2F7&day=12&hour=9&minute=22&orvStationCode=00081556&dnvStationCode=&basis=1&ctl=020010&atr=2&detailset=1&init=#detail_route_0'


qs = urllib.parse.urlparse(url).query

qs_d = urllib.parse.parse_qs(qs)


def update_query(url, key, org_val, new_val):
    pr = urllib.parse.urlparse(url)
    d = urllib.parse.parse_qs(pr.query)
    l = d.get(key)
    if l:
        d[key] = [new_val if v == org_val else v for v in l]
    else:
        d[key] = new_val
    return urllib.parse.urlunparse(pr._replace(query=urllib.parse.urlencode(d, doseq=True)))

url = update_query(url, 'month', '2018', '{:0%Y}'.format(now))
url = update_query(url, 'month', '7', '{:0%m}'.format(now))
url = update_query(url, 'day', '12', '{:0%d}'.format(now))
url = update_query(url, 'hour', '9', '{:0%H}'.format(now))
url = update_query(url, 'minute', '22', '{:0%M}'.format(now))

res = requests.get(url)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, "html.parser")
elems = soup.select('dt.left')
for elem in elems:
    if '所要時間' in elem:
        break  # 一致したので、breakで抜ける
    print(elem.getText())
