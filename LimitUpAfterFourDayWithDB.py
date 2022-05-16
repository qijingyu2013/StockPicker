# 底层逻辑 第一天涨停成功,后面4天不破涨停的阳线(不跌破涨停的开盘价)

# 1. 每天定时自动拉取前一天股票数据
# 1.1 抓取股票信息
# 1.2 抓取指定日期的股票行情
# 2. 第一天涨停成功,后面4天不破涨停的阳线(不跌破涨停的开盘价)
# 2.1 找出4天前涨停成功的票
# 2.2 筛选出4天后不跌破涨停开盘价的票
# 2.3 后面3天涨幅不能超过5%
# 2.4 剔除创业板

from sqlalchemy import and_
import models
from StockToDB import fetchStockListFromDB, StockType, saveStockMission
import pysnowball as ball
from utils import currentTime, zeroTime

# 第一天涨停成功,后面4天不破涨停的阳线(不跌破涨停的开盘价)


def fetchLimitUpAfterFourDay():
    ulist = []
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
            result = models.session.query(
                models.StockTrade
            ).filter(
                and_(
                    models.StockTrade.sid == item[0]
                )
            ).order_by(
                models.StockTrade.timestamp.desc()
            ).limit(5).all()
            try:
                # 筛选出第一天涨停的票
                if len(result) == 5:
                    if result[4].close == result[4].limit_up:
                        count = 0
                        for i in range(3, -1, -1):
                            if result[4].open < result[i].close:
                                count += 1
                            else:
                                break
                            if result[i].turn_over_rate <= 10:
                                break
                        if count == 4:
                            # 第一天的收盘价 和 最后一天的收盘价 幅度不超过5%
                            if (abs(result[0].close - result[4].close)) / result[4].close <= 5:
                                ulist.append([result[4].name, result[4].code])

            except IndexError as e:
                print("this is a IndexError:", e)
                print(result)
            handle += 1
            percent = handle / length_total
            surplus = round((length_total - handle) * 0.005, 1)
            print('\r完成度为: {:.2%}, 还剩余: {}秒'.format(percent, surplus), end='', flush=True)
        saveStockMission(zero, 2, str(ulist))
    else:
        ulist = eval(mission.content)
    printUnivList(ulist)
    return


def printUnivList(ulist):
    if len(ulist) > 0:
        tplt = "\r{0:>4}\t{1:<}\t{2:>}"
        print(tplt.format("序号", "股票名称", "股票代码", chr(12288)))
        for i in range(len(ulist)):
            u = ulist[i]
            print(tplt.format(i, u[0], u[1], chr(12288)))
        print('\r获取满足5天前涨停后4天不破位的票,已完成！')
    else:
        print("今天没有符合规则的票哦！")


# def main():
#     uinfo = []
#     ball.set_token('xq_a_token=9d7c75c59c8b3ef763711f682f3bb26163c4aad7;')
#     # timestamp = currentTime()
#     fetchLimitUpAfterFourDay()
#
#
# main()