# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
import json
import time

import requests
from bs4 import BeautifulSoup
import bs4
import pysnowball as ball

def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def getHTMLJson(req, url, params):
    try:
        # headers = {'Content-Type': 'application/json'}
        r = req.get(url, params=params, timeout=30)
        # r.raise_for_status()
        # r.encoding = r.apparent_encoding
        # print(r.json())
        return r.text
    except:
        return ""

def fillFourYinList(ulist, html):
    soup = BeautifulSoup(html, "html.parser")
    node_xuanguul = soup.find('ul',id='xuanguul')
    timestamp = currentTime()
    for li in node_xuanguul.children:
        # print(li)
        if isinstance(li, bs4.element.Tag):
            span_xh = li('span')[0].string #序号 <span class="xh">1</span>
            # print(span_xh)
            span_name_title = li('span')[1].string #名称
            # print(span_name_title)
            if li('span')[1].select_one('a[href]'):
                stock_number = li.get('scode')
                stock_number_c = ''
                if int(stock_number) < 680000: # 过滤掉科创板 68+
                    if int(stock_number) < 600000:
                        stock_number_c = 'SZ' + stock_number
                    else:
                        stock_number_c = 'SH' + stock_number

                    span_name = li('span')[1].select_one('a[href]').string #名称 <span class="sname"><a href="/gupiao/002714.html" target="_blank">牧原股份</a>
                    # print(span_name)
                    stock_url = li('span')[1].select_one('a[href]').get('href') # 股票 url
                    # print(stock_url)
                    greenTimes = totalNineYinList(stock_number_c, timestamp)
                    ulist.append([span_xh, span_name, stock_number_c, greenTimes])


        # print(li.get_text())
    #     node_span_text = li.find('span',scode_='span').get_text()
    #     print(node_span_text)
    # for tr in soup.find('tbody').children: #遍历表签树
    #     if isinstance(tr, bs4.element.Tag):
    #         tds = tr('td') #简写，等价于下一行代码
    #         #tds = tr.find_all('td')
    #         ulist.append([tds[0].string, tds[1].string, tds[2].string,tds[3].string])

def totalNineYinList(stock_number_c, begin):
    data = ball.daily(stock_number_c, begin)['data']
    # print(data['item'])
    greenTimes = 0
    ## 按照当前交易日的开盘价-收盘价 进行计算
    # for item in reversed(data['item']):
    #     print(item[5])
    #     print(item[2])
    #     print(item[5] < item[2])
    #     if item[5] < item[2]:
    #         greenTimes += 1
    #     else:
    #         return greenTimes

    ## 以下算法是根据 上一个交易日的收盘价 && 当前开盘价 && 当前收盘价 进行计数
    for i in range( len(data['item']), -1, -1):
        if i > 0:
            # print(i)
            closing_price_prev = data['item'][i-2][5]
            # print(closing_price_prev)
            opening_price_current = data['item'][i-1][2]
            # print(opening_price_current)
            closing_price_current = data['item'][i-1][5]
            # print(closing_price_current)

            if closing_price_current < opening_price_current:
                greenTimes += 1
            elif closing_price_current == opening_price_current:
                if closing_price_current < closing_price_prev:
                    greenTimes += 1
                else:
                    return greenTimes
            else:
                return greenTimes
    return greenTimes

def printUnivList(ulist):
    tplt = "{0:^4}\t{1:^8}\t{2:6}\t{3:^4}"
    print(tplt.format("序号","股票名称","股票代码","连阴次数", chr(12288)))
    for i in range(len(ulist)):
        u = ulist[i]
        if u[3] > 6 :
            print(tplt.format(u[0],u[1],u[2],u[3],chr(12288)))

def currentTime():
    current = datetime.datetime.now()
    #打印当前时间
    print("当前时间 :", current)

    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    # 雪球网请求是需要把日往后延一天
    dt = str(year) + '-' + str(month) + '-' + str(day+1) + ' 17:00:00'
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(timeArray)
    # print(round(timestamp*1000))
    return round(timestamp*1000)

def main():
    uinfo = []
    url = 'http://www.tetegu.com/4lianyin/?src=indexgezi'
    ball.set_token('xq_a_token=727dbbbcb1a3b790f344cdc67f7910d7dfb0e461;')
    html = getHTMLText(url)
    fillFourYinList(uinfo, html)
    printUnivList(uinfo)

main()
