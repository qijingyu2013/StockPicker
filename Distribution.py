# 筹码分布
import json

from sqlalchemy import and_

import jfzt
import models
from StockToDB import fetchStockListFromDB, StockType, saveStockMission
from utils import zeroTime, printOptimizedForm


# 查当前价格下
# 最近3天的筹码变化情况
def fetchBottom(price, symbols, symbol_type):
    distribution_data = jfzt.fetchDistrubitionData(symbols, symbol_type)
    length = len(distribution_data)
    today_items = distribution_data[length-1]['items']
    yesterday_items = distribution_data[length-2]['items']
    before_yesterday_items = distribution_data[length-3]['items']
    three_days_ago_items = distribution_data[length-4]['items']
    shapes = distribution_data[length-1]['chipSummary']['shapesQuShi']
    shapes_detail = distribution_data[length-1]['chipSummary']['shapesDetail']
    today_total = 0
    yesterday_total = 0
    before_yesterday_total = 0
    three_days_ago_items_total = 0
    today_ratio = 0
    yesterday_ratio = 0
    before_yesterday_ratio = 0
    for data in today_items:
        if price >= data['price']:
            today_total += data['volume']
    for data in yesterday_items:
        if price >= data['price']:
            yesterday_total += data['volume']
    for data in before_yesterday_items:
        if price >= data['price']:
            before_yesterday_total += data['volume']
    for data in three_days_ago_items:
        if price >= data['price']:
            three_days_ago_items_total += data['volume']

    if yesterday_total > 0:
        today_ratio = (today_total-yesterday_total)/yesterday_total*100
    if before_yesterday_total > 0:
        yesterday_ratio = (yesterday_total-before_yesterday_total)/before_yesterday_total*100
    if three_days_ago_items_total > 0:
        before_yesterday_ratio = (before_yesterday_total-three_days_ago_items_total)/three_days_ago_items_total*100

    print(f'今日低于当前价位:{price}的筹码变化率:{today_ratio == 0 and today_ratio or round(today_ratio, 2)}% 统计数量:{today_total}')
    print(f'昨日低于当前价位:{price}的筹码变化率:{yesterday_ratio == 0 and yesterday_ratio or round(yesterday_ratio, 2)}% 统计数量:{yesterday_total}')
    print(f'前日低于当前价位:{price}的筹码变化率:{before_yesterday_ratio == 0 and before_yesterday_ratio or round(before_yesterday_ratio, 2)}% 统计数量:{before_yesterday_total}')
    print(f'当前趋势:{shapes}--{shapes_detail}')

# 1. 比股价低而且筹码集中的票
# 1.1 抓取股票信息
# 1.2 抓取当日交易信息
# 1.3 筛选出最近五天没有涨停过且5天的幅度都小于3%的票，且当日成交额大于1亿
# 1.4 抓取当日筹码分布信息
# 1.5 统计总筹码数以及比股价低的筹码数
# 1.6 筛选比股价低的筹码数占比总筹码数的10%的股票
# 1.7 筛选比股价低而且筹码集中的票
# 第一天涨停成功,后面4天不破涨停的阳线(不跌破涨停的开盘价)
# 3天涨幅不超过10%，跌幅不超过5%，每天换手率10
def fetchBottomStrategy():
    ulist = []
    zero = zeroTime()
    mission = models.session.query(
        models.StockMission
    ).filter(
        and_(
            models.StockMission.timestamp == zero,
            models.StockMission.type == 6
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
                # 筛选出最近五天没有涨停过 且5天的幅度都小于3%的票 换手率大于5% 且当日成交额大于1亿
                if len(result) == 5:
                    count = 0
                    for i in range(3, -1, -1):
                        if result[i].close == result[i].limit_up:
                            break
                        if result[i].turn_over_rate >= 5:
                            break
                        if abs(result[i].percent) >= 3:
                            break
                        if result[i].amount < 100000000:
                            break
                        count += 1
                    if count == 4:
                        # 抓取当日筹码分布信息
                        distribution = models.session.query(
                            models.StockDistribution
                        ).filter(
                            and_(
                                models.StockDistribution.sid == result[0].sid,
                                models.StockDistribution.timestamp == zero,
                            )
                        ).one_or_none()
                        if distribution is not None:
                            datas = json.loads(distribution.datas)
                            low_total = 0
                            all_total = 0
                            for data in datas:
                                all_total += data['volume'] * data['price'] * 100
                                if data['price'] < result[0].close:
                                    low_total += data['volume'] * data['price'] * 100

                            rate = low_total / all_total
                            if rate < 0.01:
                                ulist.append([result[3].name, result[3].code, round(rate * 100, 2)])
                            # elif rate > 0.99:
                            #     ulist.append([result[3].name, result[3].code, round(rate * 100, 2)])
            except IndexError as e:
                print("this is a IndexError:", e)
                print(result)
            handle += 1
            percent = handle / length_total
            surplus = round((length_total - handle) * 0.005, 1)
            print('\r完成度为: {:.2%}, 还剩余: {}秒'.format(percent, surplus), end='', flush=True)
        saveStockMission(zero, 6, str(ulist))
    else:
        ulist = eval(mission.content)
    printUnivList(ulist)
    return

# 当前价格上下5%浮动范围内筹码总数 占总筹码90%以上


def printUnivList(ulist):
    if len(ulist) > 0:
        tplt = "\r{0:>4}\t{1:<}\t{2:<}\t{3:>}"
        print(tplt.format("序号", "股票名称", "股票代码", "分布占比", chr(12288)))
        for i in range(len(ulist)):
            u = ulist[i]
            print(tplt.format(i, u[0], u[1], u[2], chr(12288)))

        printOptimizedForm(ulist, 0)
        print('\r获取满足倍量的票,已完成！')
    else:
        print("今天没有符合规则的票哦！")
