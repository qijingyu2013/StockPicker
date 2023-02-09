# 底层逻辑 3天内的成交量之和2倍于前3天的成交量之和

# 1. 每天定时自动拉取前一天股票数据
# 1.1 抓取股票信息
# 1.2 抓取指定日期的股票行情
# 2. 3天内的成交量之和2倍于前3天的成交量之和
# 2.1 3天内的成交量之和2倍于前3天的成交量之和
# 2.2 6天内涨幅不超过5%

from sqlalchemy import and_
import models
from StockToDB import fetchStockListFromDB, StockType, saveStockMission
import pysnowball as ball
from utils import currentTime, zeroTime, printOptimizedForm


# 3天内的成交量之和2倍于前3天的成交量之和
def fetchReleaseVolume():
    ulist = []
    zero = zeroTime()
    mission = models.session.query(
        models.StockMission
    ).filter(
        and_(
            models.StockMission.timestamp == zero,
            models.StockMission.type == 5
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
            ).limit(7).all()
            try:
                # 筛选出3天内的成交量之和2倍于前3天的成交量之和
                if len(result) == 7:
                    lastThreeDays = result[0].volume+result[1].volume+result[2].volume
                    threeDaysAgo = result[3].volume+result[4].volume+result[5].volume
                    # print(lastThreeDays)
                    # print(threeDaysAgo)
                    if lastThreeDays > 3*threeDaysAgo:
                        # 6天内涨幅不超过5%
                        flag_1=0
                        for i in range(5, -1, -1):
                            if (result[i].high-result[i+1].close)/result[i+1].close > 0.05:
                                flag_1=1
                                break
                        if flag_1 == 0:
                            ulist.append([result[0].name, result[0].code])
            except IndexError as e:
                print("this is a IndexError:", e)
                print(result)
            handle += 1
            percent = handle / length_total
            surplus = round((length_total - handle) * 0.005, 1)
            print('\r完成度为: {:.2%}, 还剩余: {}秒'.format(percent, surplus), end='', flush=True)
        saveStockMission(zero, 5, str(ulist))
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

        printOptimizedForm(ulist, 0)
        print('\r获取满足放量的票,已完成！')
    else:
        print("今天没有符合规则的票哦！")

# def main():
#     uinfo = []
#     ball.set_token(TOKEN)
#     # timestamp = currentTime()
#     fetchMultiplier()
#
#
# main()