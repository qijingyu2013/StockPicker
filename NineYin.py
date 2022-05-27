# 底层逻辑 输出大于7阴的票

import bs4
import requests
from bs4 import BeautifulSoup
from sqlalchemy import and_

import models
import pysnowball as ball
from StockToDB import fetchStockListFromDB, StockType, saveStockMission
from utils import currentTime, zeroTime


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
    node_xuanguul = soup.find('ul', id='xuanguul')
    timestamp = currentTime()
    for li in node_xuanguul.children:
        # print(li)
        if isinstance(li, bs4.element.Tag):
            span_xh = li('span')[0].string  # 序号 <span class="xh">1</span>
            # print(span_xh)
            span_name_title = li('span')[1].string  # 名称
            # print(span_name_title)
            if li('span')[1].select_one('a[href]'):
                stock_number = li.get('scode')
                stock_number_c = ''
                if int(stock_number) < 680000:  # 过滤掉科创板 68+
                    if int(stock_number) < 600000:
                        stock_number_c = 'SZ' + stock_number
                    else:
                        stock_number_c = 'SH' + stock_number

                    span_name = li('span')[1].select_one(
                        'a[href]').string  # 名称 <span class="sname"><a href="/gupiao/002714.html" target="_blank">牧原股份</a>
                    # print(span_name)
                    stock_url = li('span')[1].select_one('a[href]').get('href')  # 股票 url
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
    for i in range(len(data['item']), -1, -1):
        if i > 0:
            # print(i)
            closing_price_prev = data['item'][i - 2][5]
            # print(closing_price_prev)
            opening_price_current = data['item'][i - 1][2]
            # print(opening_price_current)
            closing_price_current = data['item'][i - 1][5]
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


def printUnivList(lists, limit, period):
    lists_len = len(lists)
    template = "\r{0:>4}\t{1:<}\t{2:>}\t{3:^}"
    if lists_len > 0:
        if period == 'daily':
            print(template.format("序号", "股票名称", "股票代码", "连日阴次数", chr(12288)))
        elif period == 'weekly':
            print(template.format("序号", "股票名称", "股票代码", "连周阴次数", chr(12288)))
        elif period == 'monthly':
            print(template.format("序号", "股票名称", "股票代码", "连月阴次数", chr(12288)))

        for i in range(lists_len):
            u = lists[i]
            if u[2] >= limit:
                print(template.format(i+1, u[0], u[1], u[2], chr(12288)))
    else:
        if period == 'daily':
            print("\r今天没有连日阴" + str(limit) + "的票哦！")
        elif period == 'weekly':
            print("\r今天没有连周阴" + str(limit) + "的票哦！")
        elif period == 'monthly':
            print("\r今天没有连月阴" + str(limit) + "的票哦！")


# 取出9天的行情
# 从最后一天开始累加下跌的次数
# def fetchNineDayData(limit=9):
#     ulist = []
#     zero = zeroTime()
#     mission = models.session.query(
#         models.StockMission
#     ).filter(
#         and_(
#             models.StockMission.timestamp == zero,
#             models.StockMission.type == 1
#         )
#     ).one_or_none()
#
#     if mission is None:
#         lists = fetchStockListFromDB(StockType.HuShen, False)
#         length_total = len(lists)
#         handle = 0
#         for item in lists:
#             result = models.session.query(
#                 models.StockTrade
#             ).filter(
#                 and_(
#                     models.StockTrade.sid == item[0]
#                 )
#             ).order_by(
#                 models.StockTrade.timestamp.desc()
#             ).limit(9).all()
#             # print(result)
#             count = 0
#             for trade in result:
#                 if trade.open > trade.close:
#                     count += 1
#                 else:
#                     break
#             if count >= 4:
#                 ulist.append([trade.name, trade.code, count])
#             handle += 1
#             percent = handle / length_total
#             surplus = round((length_total - handle) * 0.005, 1)
#             print('\r完成度为: {:.2%}, 还剩余: {}秒'.format(percent, surplus), end='', flush=True)
#         saveStockMission(zero, 1, str(ulist))
#     else:
#         ulist = eval(mission.content)
#
#     printUnivList(ulist, limit)
#     return ulist


# 取出9个周期的行情

def nineDailyData(limit=9):
    daily_list = []
    zero = zeroTime()
    mission = models.session.query(
        models.StockMission
    ).filter(
        and_(
            models.StockMission.timestamp == zero,
            models.StockMission.type == 2
        )
    ).one_or_none()

    if mission is None:
        lists = fetchStockListFromDB(StockType.HuShen, False)
        length_total = len(lists)
        handle = 0
        for item in lists:
            result_daily = fetchNinePeriodData(item[0], 'daily')
            count = 0
            for trade in result_daily:
                if trade.open > trade.close:
                    count += 1
                else:
                    break
            if count >= 5:
                daily_list.append([trade.name, trade.code, count])

            handle += 1
            percent = handle / length_total
            surplus = round((length_total - handle) * 0.005, 1)
            print('\r完成度为: {:.2%}, 还剩余: {}秒'.format(percent, surplus), end='', flush=True)

        saveStockMission(zero, 2, str(daily_list))
    else:
        daily_list = eval(mission.content)

    printUnivList(daily_list, limit, 'daily')
    return daily_list


def nineWeeklyData(limit=10):
    weekly_list = []
    zero = zeroTime()
    mission = models.session.query(
        models.StockMission
    ).filter(
        and_(
            models.StockMission.timestamp == zero,
            models.StockMission.type == 3
        )
    ).one_or_none()

    if mission is None:
        lists = fetchStockListFromDB(StockType.HuShen, False)
        length_total = len(lists)
        handle = 0
        for item in lists:
            result_weekly = fetchNinePeriodData(item[0], 'weekly')
            if len(result_weekly) == 10:
                count = 0
                for trade in result_weekly:
                    if trade.open > trade.close:
                        count += 1
                    else:
                        break
                if count >= 6:
                    if result_weekly[0].turn_over_rate > 20:
                        weekly_list.append([result_weekly[0].name, result_weekly[0].code, count])
                    # else:
                    #     print(result_weekly[0].name, result_weekly[0].code, count, result_weekly[0].turn_over_rate)

            handle += 1
            percent = handle / length_total
            surplus = round((length_total - handle) * 0.005, 1)
            print('\r完成度为: {:.2%}, 还剩余: {}秒'.format(percent, surplus), end='', flush=True)

        saveStockMission(zero, 3, str(weekly_list))
    else:
        weekly_list = eval(mission.content)

    printUnivList(weekly_list, limit, 'weeklyly')
    return weekly_list


def nineMonthlyData(limit=11):
    monthly_list = []
    zero = zeroTime()
    mission = models.session.query(
        models.StockMission
    ).filter(
        and_(
            models.StockMission.timestamp == zero,
            models.StockMission.type == 4
        )
    ).one_or_none()

    if mission is None:
        lists = fetchStockListFromDB(StockType.HuShen, False)
        length_total = len(lists)
        handle = 0
        for item in lists:
            result_monthly = fetchNinePeriodData(item[0], 'monthly')
            if len(result_monthly) == 11:
                count = 0
                for trade in result_monthly:
                    if trade.open > trade.close:
                        count += 1
                    else:
                        break
                if count >= 7:
                    if result_monthly[0].turn_over_rate > 20:
                        monthly_list.append([result_monthly[0].name, result_monthly[0].code, count])
                    # else:
                    #     print(result_monthly[0].name, result_monthly[0].code, count, result_monthly[0].turn_over_rate)

            handle += 1
            percent = handle / length_total
            surplus = round((length_total - handle) * 0.005, 1)
            print('\r完成度为: {:.2%}, 还剩余: {}秒'.format(percent, surplus), end='', flush=True)

        saveStockMission(zero, 4, str(monthly_list))
    else:
        monthly_list = eval(mission.content)

    printUnivList(monthly_list, limit, 'monthly')
    return monthly_list


def fetchNinePeriodData(sid, period):
    if period == 'daily':
        return models.session.query(
            models.StockTrade
        ).filter(
            and_(
                models.StockTrade.sid == sid
            )
        ).order_by(
            models.StockTrade.timestamp.desc()
        ).limit(9).all()
    elif period == 'weekly':
        return models.session.query(
            models.StockTradeWeekly
        ).filter(
            and_(
                models.StockTradeWeekly.sid == sid
            )
        ).order_by(
            models.StockTradeWeekly.timestamp.desc()
        ).limit(10).all()
    elif period == 'monthly':
        return models.session.query(
            models.StockTradeMonthly
        ).filter(
            and_(
                models.StockTradeMonthly.sid == sid
            )
        ).order_by(
            models.StockTradeMonthly.timestamp.desc()
        ).limit(11).all()

# def main():
#     uinfo = []
#     url = 'http://www.tetegu.com/4lianyin/?src=indexgezi'
#     ball.set_token(TOKEN)
#     html = getHTMLText(url)
#     fillFourYinList(uinfo, html)
#     printUnivList(uinfo)
#     # fetchNineDayData()
#
# main()
