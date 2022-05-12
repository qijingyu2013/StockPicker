# 底层逻辑 第一天涨停成功,后面4天不破涨停的阳线(不跌破涨停的开盘价)

# 1. 每天定时自动拉取前一天股票数据
# 1.1 抓取股票信息
# 1.2 抓取指定日期的股票行情
# 2. 第一天涨停成功,后面4天不破涨停的阳线(不跌破涨停的开盘价)
# 2.1 找出4天前涨停成功的票
# 2.2 筛选出4天后不跌破涨停开盘价的票

import datetime
import time
import requests
from bs4 import BeautifulSoup
import bs4
import pysnowball as ball

# 该版本属于远程拉取版

# 抓取股票列表
def fetchStockList(timestamp):
    list = ball.list(5000)
    # print(list)
    return list

# 抓取股票信息
def fetchStockInfo(ulist, data, timestamp):
    print("Loading", end="")
    lists = data['data']['list']
    length_total = len(lists)
    handle = 0
    for item in lists:
        # 沪深标识位
        item['symbol'][0:2]
        # 股票代码
        item['symbol'][-6:]
        # 股票名称
        item['name']
        # 当天价格
        item['current']
        try:
            # 5天行情
            data_five = ball.daily(item['symbol'], timestamp, -5)['data']
            # 数据长度
            length = len(data_five['item'])
            # 第一天开盘价
            opening_price_first = data_five['item'][0][2]
            # 第一天收盘价
            closing_price_first = data_five['item'][0][5]

            # 第一天涨停价
            if item['symbol'][0:3] == 'SZ3':
                limit_up_price_first = round(data_five['item'][0][2] * 1.2, 2)
            else:
                limit_up_price_first = round(data_five['item'][0][2] * 1.1, 2)
            # print(opening_price_first, closing_price_first, limit_up_price_first)

            # 第一天涨停价 = 第一天收盘价
            if closing_price_first == limit_up_price_first:
                times_flag = 0
                for i in range(length, -1, -1):
                    # 当前开盘价
                    opening_price_current = data_five['item'][i - 1][2]
                    # 当前收盘价
                    closing_price_current = data_five['item'][i - 1][5]
                    # 找出当天收盘价高于第一天开盘价
                    if closing_price_current > opening_price_first:
                        times_flag += 1
                if times_flag == 5:
                    ulist.append([item['name'], item['symbol']])
        #当需要分开捕获多个异常可以使用多条except语句，try与except之间语句触发任意一个异常捕获后就跳到对应except执行其下面的语句，其余except不在继续执行
        except IndexError as e:
            print("this is a IndexError:",e)
        except KeyError as e:
            print("this is a KeyError:",e)

        time.sleep(0.1)
        handle += 1
        percent = handle / length_total
        surplus = round((length_total - handle)*0.15, 1)
        print('\r完成度为: {:.2%}, 还剩余: {}秒'.format(percent, surplus), end='', flush=True)
        # print("\r 完成度为%f%, 还剩余%f秒。" %percent %surplus, end='', flush=True)
    return ulist

def printUnivList(ulist):
    tplt = "\r{0:^4}\t{1:^8}\t{2:8}"
    print(tplt.format("序号", "股票名称", "股票代码", chr(12288)))
    for i in range(len(ulist)):
        u = ulist[i]
        print(tplt.format(i, u[0], u[1], chr(12288)))

def currentTime():
    current = datetime.datetime.now()
    # 打印当前时间
    print("当前时间 :", current)

    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    # 雪球网请求是需要把日往后延一天
    dt = str(year) + '-' + str(month) + '-' + str(day + 1) + ' 17:00:00'
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(timeArray)
    # print(round(timestamp*1000))
    return round(timestamp * 1000)

def main():
    uinfo = []
    ball.set_token('xq_a_token=9d7c75c59c8b3ef763711f682f3bb26163c4aad7;')
    timestamp = currentTime()
    lists = fetchStockList(timestamp)
    fetchStockInfo(uinfo, lists, timestamp)
    printUnivList(uinfo)


main()
