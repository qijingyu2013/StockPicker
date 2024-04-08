# 底层逻辑 CCI指标的计算公式：
#
# TP=(最高价+最低价+收盘价)÷3
#
# MA=最近N日收盘价的累计之和÷N
#
# MD=最近N日(MA-收盘价)的累计之和÷N，0.015为计算系数，N为计算周期
# TYP赋值：(最高价+最低价+收盘价)/3
# CCI：(TYP-TYP的N日简单移动平均)/(0.015*TYP的N日平均绝对方差)
import math

from sqlalchemy import and_
import models
from utils import currentTime, zeroTime, printOptimizedForm


def tp(high, low, close):
    return (high + low + close) / 3


def cci(sid, timestamp, high, low, close):
    cciValue = 0.00
    trades = models.session.query(
        models.StockTrade
    ).filter(
        and_(
            models.StockTrade.sid == sid,
            models.StockTrade.timestamp < timestamp,
        )
    ).order_by(
        models.StockTrade.timestamp.desc()
    ).limit(13).all()

    if len(trades) == 13:
        tpFirst = tp(high, low, close)
        tps = 0
        tps += tpFirst

        for trade in trades:
            tps += tp(trade.high, trade.low, trade.close)
        ma = tps/14

        mds = math.fabs(tpFirst - ma)
        for trade in trades:
            mds += math.fabs(tp(trade.high, trade.low, trade.close) - ma)
            #  typs += typ(trade.high, trade.low, trade.close)
        md = mds/14
        cciValue = (tpFirst - ma)/(md*0.015)
        # for trade in trades:
        #     tps - ma
        # (TP[i] - MA[i])/(MD[i]*0.015)
        # td = math.fabs(typs - ma)
        print(ma)
        print(md)
        print()
    return cciValue


# 1. 创建周榜数组、双周榜数组和月榜数组
# 2. 找出7日、14日、28日交易数据
# 3. 计算平均值，把最高放入对应数组，只保留前三
# 4. 振幅=（最高-最低）/开盘
# def fetchCCI():
#     ulist = []
#     week_chart = []
#     two_week_chart = []
#     month_chart = []
#     zero = zeroTime()
#     mission = models.session.query(
#         models.StockMission
#     ).filter(
#         and_(
#             models.StockMission.timestamp == zero,
#             models.StockMission.type == 8
#         )
#     ).one_or_none()
#     if mission is None:
#         lists = fetchStockListFromDB(StockType.HuShen, False)
#         length_total = len(lists)
#         handle = 0
#         for item in lists:
#             result = models.session.query(
#                 models.StockTrade
#             ).filter(
#                 and_(
#                     models.StockTrade.sid == item[0],
#                     # models.StockTrade.close != models.StockTrade.limit_up,
#                     # models.StockTrade.close != models.StockTrade.limit_down,
#                     # models.StockTrade.open != models.StockTrade.limit_up,
#                     # models.StockTrade.open != models.StockTrade.limit_down,
#                 )
#             ).order_by(
#                 models.StockTrade.timestamp.desc()
#             ).limit(14).all()
#             try:
#                 if len(result) == 14:
#                     high = []
#                     low = []
#                     close = []
#                     for i in range(14):
#                         high.append(result[i].high)
#                         low.append(result[i].low)
#                         close.append(result[i].close)
#                     cci = talib.CCI(high, low, close, timeperiod=14)
#                     print(cci[-5:])
#
#             except IndexError as e:
#                 print("this is a IndexError:", e)
#                 print(result)
#             handle += 1
#             percent = handle / (length_total+10)
#             surplus = round((length_total + 10 - handle) * 0.005, 1)
#             print('\r完成度为: {:.2%}, 还剩余: {}秒'.format(percent, surplus), end='', flush=True)
#
#         # week_chart.sort(key=lambda x: x[2], reverse=True)
#         # print('\r完成度为: {:.2%}, 还剩余: {}秒'.format(handle / (length_total+7), round((length_total + 7 - handle) * 0.005, 1)), end='', flush=True)
#         # two_week_chart.sort(key=lambda x: x[2], reverse=True)
#         # print('\r完成度为: {:.2%}, 还剩余: {}秒'.format(handle / (length_total+4), round((length_total + 4 - handle) * 0.005, 1)), end='', flush=True)
#         # month_chart.sort(key=lambda x: x[2], reverse=True)
#         # print('\r完成度为: {:.2%}, 还剩余: {}秒'.format(handle / length_total, round((length_total + 1 - handle) * 0.005, 1)), end='', flush=True)
#         # for i in range(5):
#         #     ulist.append([week_chart[i][0], week_chart[i][1], week_chart[i][2], '7天内'])
#         # for i in range(5):
#         #     ulist.append([two_week_chart[i][0], two_week_chart[i][1], two_week_chart[i][2], '14天内'])
#         # for i in range(10):
#         #     ulist.append([month_chart[i][0], month_chart[i][1], month_chart[i][2], '28天内'])
#         # print('\r完成度为: {:.2%}, 还剩余: {}秒'.format(handle / length_total, round((length_total - handle) * 0.005, 1)), end='', flush=True)
#         # saveStockMission(zero, 8, str(ulist))
#     else:
#         ulist = eval(mission.content)
#     printUnivList(ulist)
#     return


def printUnivList(ulist):
    if len(ulist) > 0:
        tplt = "\r{0:>5}\t{1:<}\t{2:<}\t{3:>}\t{4:>}"
        print(tplt.format("序号", "股票名称", "股票代码", "振幅", "类型", chr(12288)))
        for i in range(len(ulist)):
            u = ulist[i]
            print(tplt.format(i + 1, u[0], u[1], round(u[2] * 100, 2), u[3], chr(12288)))

        printOptimizedForm(ulist, 0)
        print('\r获取振幅排行榜,已完成！')
    else:
        print("今天没有符合规则的票哦！")


def main():
    #     uinfo = []
    #     ball.set_token(TOKEN)
    #     # timestamp = currentTime()
    cci(2142, 1712073600000, 10.55, 10.42, 10.46)


#
#
main()
