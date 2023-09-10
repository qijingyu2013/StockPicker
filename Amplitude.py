# 底层逻辑 最近1周以及1月内的振幅倒序


from sqlalchemy import and_
import models
from StockToDB import fetchStockListFromDB, StockType, saveStockMission
import pysnowball as ball
from utils import currentTime, zeroTime, printOptimizedForm


# 1. 创建周榜数组、双周榜数组和月榜数组
# 2. 找出7日、14日、28日交易数据
# 3. 计算平均值，把最高放入对应数组，只保留前三
# 4. 振幅=（最高-最低）/开盘
def fetchAmplitude():
    ulist = []
    week_chart = []
    two_week_chart = []
    month_chart = []
    zero = zeroTime()
    mission = models.session.query(
        models.StockMission
    ).filter(
        and_(
            models.StockMission.timestamp == zero,
            models.StockMission.type == 8
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
                    models.StockTrade.sid == item[0],
                    # models.StockTrade.close != models.StockTrade.limit_up,
                    # models.StockTrade.close != models.StockTrade.limit_down,
                    models.StockTrade.open != models.StockTrade.limit_up,
                    models.StockTrade.open != models.StockTrade.limit_down,
                )
            ).order_by(
                models.StockTrade.timestamp.desc()
            ).limit(29).all()
            try:
                if len(result) == 29:
                    week_amplitude = 0
                    two_week_amplitude = 0
                    month_amplitude = 0
                    for i in range(28):
                        amplitude = (result[i].high - result[i].low) / result[i + 1].close
                        if i < 7:
                            week_amplitude += amplitude
                        if i < 14:
                            two_week_amplitude += amplitude
                        month_amplitude += amplitude
                    week_chart.append([result[0].name, result[0].code, week_amplitude/7])
                    two_week_chart.append([result[0].name, result[0].code, two_week_amplitude/14])
                    month_chart.append([result[0].name, result[0].code, month_amplitude/28])

            except IndexError as e:
                print("this is a IndexError:", e)
                print(result)
            handle += 1
            percent = handle / (length_total+10)
            surplus = round((length_total + 10 - handle) * 0.005, 1)
            print('\r完成度为: {:.2%}, 还剩余: {}秒'.format(percent, surplus), end='', flush=True)

        week_chart.sort(key=lambda x: x[2], reverse=True)
        print('\r完成度为: {:.2%}, 还剩余: {}秒'.format(handle / (length_total+7), round((length_total + 7 - handle) * 0.005, 1)), end='', flush=True)
        two_week_chart.sort(key=lambda x: x[2], reverse=True)
        print('\r完成度为: {:.2%}, 还剩余: {}秒'.format(handle / (length_total+4), round((length_total + 4 - handle) * 0.005, 1)), end='', flush=True)
        month_chart.sort(key=lambda x: x[2], reverse=True)
        print('\r完成度为: {:.2%}, 还剩余: {}秒'.format(handle / length_total, round((length_total + 1 - handle) * 0.005, 1)), end='', flush=True)
        # for i in range(3):
        #     ulist.append([week_chart[i][0], week_chart[i][1], week_chart[i][2], '7天内'])
        # for i in range(3):
        #     ulist.append([two_week_chart[i][0], two_week_chart[i][1], two_week_chart[i][2], '14天内'])
        for i in range(5):
            ulist.append([month_chart[i][0], month_chart[i][1], month_chart[i][2], '28天内'])
        print('\r完成度为: {:.2%}, 还剩余: {}秒'.format(handle / length_total, round((length_total - handle) * 0.005, 1)), end='', flush=True)
        saveStockMission(zero, 8, str(ulist))
    else:
        ulist = eval(mission.content)
    printUnivList(ulist)
    return


def printUnivList(ulist):
    if len(ulist) > 0:
        tplt = "\r{0:>5}\t{1:<}\t{2:<}\t{3:>}\t{4:>}"
        print(tplt.format("序号", "股票名称", "股票代码", "振幅", "类型", chr(12288)))
        for i in range(len(ulist)):
            u = ulist[i]
            print(tplt.format(i+1, u[0], u[1], round(u[2] * 100, 2), u[3], chr(12288)))

        printOptimizedForm(ulist, 0)
        print('\r获取振幅排行榜,已完成！')
    else:
        print("今天没有符合规则的票哦！")


# def main():
#     #     uinfo = []
#     #     ball.set_token(TOKEN)
#     #     # timestamp = currentTime()
#     fetchAmplitude()
#
#
# #
# #
# main()
