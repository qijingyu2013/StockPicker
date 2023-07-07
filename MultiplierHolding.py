#  底层逻辑 第一天涨停后面一直没有破位

# 1. 每天定时自动拉取前一天股票数据
# 1.1 抓取股票信息
# 1.2 抓取指定日期的股票行情
# 2. 涨停日开始，获取所有股
# 2.1 找出最近一次涨停的数据
# 2.2 根据涨停日开盘价过滤
# 2.3 要求第二天的量比涨停日高1.7
# 2.4 剔除创业板

from sqlalchemy import and_
import models
from StockToDB import fetchStockListFromDB, StockType, saveStockMission
from utils import zeroTime, printOptimizedForm


def multiplierHolding():
    ulist = []
    zero = zeroTime()
    mission = fetchMission(zero)
    if mission is None:
        lists = fetchStockListFromDB(StockType.HuShen, False)
        length_total = len(lists)
        handle = 0
        for item in lists:
            ceilingDataSet = fetchCeilingDatas(item[0])
            try:
                if len(ceilingDataSet) > 0:
                    ceilingData = ceilingDataSet[0]
                    ceilingAfterData = fetchCeilingAfterData(ceilingData)
                    total = len(ceilingAfterData)
                    # 过滤数据太少和不是倍量的情况
                    if total > 3 and ceilingAfterData[0].volume > ceilingData.volume * 1.7:
                        # 过滤破位的情况
                        target = True
                        for trade in ceilingAfterData:
                            if ceilingData.open > trade.low:
                                target = False
                                break
                        if target:
                            # 逼近破位价
                            if ceilingData.open * 1.1 > ceilingAfterData[total - 1].close:
                                # 最后一天放量
                                if ceilingAfterData[total - 1].volume > ceilingAfterData[total - 2].volume * 1.5:
                                    ulist.append([ceilingData.name, ceilingData.code, '倍量横盘'])
            except IndexError as e:
                print("this is a IndexError:", e)
                print(ceilingData)
            handle += 1
            percent = handle / length_total
            surplus = round((length_total - handle) * 0.05, 1)
            print('\r完成度为: {:.2%}, 还剩余: {}秒'.format(percent, surplus), end='', flush=True)
        saveStockMission(zero, 7, str(ulist))
    else:
        ulist = eval(mission.content)
    printUnivList(ulist)
    return


def fetchMission(zero):
    return models.session.query(
        models.StockMission
    ).filter(
        and_(
            models.StockMission.timestamp == zero,
            models.StockMission.type == 7
        )
    ).one_or_none()


def fetchCeilingDatas(sid):
    return models.session.query(
        models.StockTrade
    ).filter(
        and_(
            models.StockTrade.sid == sid,
            models.StockTrade.close == models.StockTrade.limit_up,
        )
    ).order_by(
        models.StockTrade.timestamp.desc()
    ).all()


def fetchCeilingAfterData(ceiling):
    return models.session.query(
        models.StockTrade
    ).filter(
        and_(
            models.StockTrade.sid == ceiling.sid,
            models.StockTrade.timestamp > ceiling.timestamp,
        )
    ).order_by(
        models.StockTrade.timestamp.asc()
    ).all()


def printUnivList(ulist):
    if len(ulist) > 0:
        tplt = "\r{0:>4}\t{1:<}\t{2:<}\t{3:>}"
        print(tplt.format("序号", "股票名称", "股票代码", "类型", chr(12288)))
        for i in range(len(ulist)):
            u = ulist[i]
            print(tplt.format(i, u[0], u[1], u[2], chr(12288)))

        printOptimizedForm(ulist, 0)
        print('\r获取满足倍量的票,已完成！')
    else:
        print("今天没有符合规则的票哦！")

# def main():
#     #     uinfo = []
#     #     ball.set_token(TOKEN)
#     #     # timestamp = currentTime()
#     multiplierHolding()
#
#
# #
# #
# main()
