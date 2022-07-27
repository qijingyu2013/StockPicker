# 连续十字星的票

from sqlalchemy import and_

import models
from StockToDB import fetchStockListFromDB, StockType


def printUnivList(lists, limit):
    lists_len = len(lists)
    template = "\r{0:>4}\t{1:<}\t{2:>}\t{3:^}"
    if lists_len > 0:
        print(template.format("序号", "股票名称", "股票代码", "连续十字星次数", chr(12288)))
        for i in range(lists_len):
            u = lists[i]
            if u[2] >= limit:
                print(template.format(i + 1, u[0], u[1], u[2], chr(12288)))
    else:
        print("\r今天没有连续十字星的票哦！")


def fetchTradeData(code):
    return models.session.query(
        models.StockTrade
    ).filter(
        and_(
            models.StockTrade.code == code,
        )
    ).order_by(
        models.StockTrade.timestamp.desc()
    ).limit(5).all()


def main():
    lists = fetchStockListFromDB(StockType.HuShenChuang, False)
    length_total = len(lists)
    handle = 0
    container = []
    for item in lists:
        data = fetchTradeData(item)
        count = 0
        for i in range(0, len(data), 1):
            print(data[i].chg)
            if abs(data[i].chg) < 0.05:
                count += 1
            else:
                break
        if count > 1:
            container.append([data[i].name, data[i].code, i])
        handle += 1
        percent = handle / length_total
        surplus = round((length_total - handle) * 0.01, 1)
        print('\r完成度为: {:.2%}, 还剩余: {}秒'.format(percent, surplus), end='', flush=True)
    printUnivList(container, 1)

main()
