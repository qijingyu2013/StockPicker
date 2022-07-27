from sqlalchemy import and_

import models
from myTT import *
from NineYin import fetchNinePeriodData
from StockToDB import fetchStockListFromDB, StockType
from utils import zeroTime

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

else:
    daily_list = eval(mission.content)


CLOSE = df.close.values;
OPEN = df.open.values;
HIGH = df.high.values;
LOW = df.low.values  # 基础数据定义

MA5 = MA(CLOSE, 5)
MA10 = MA(CLOSE, 10)
CROSS_TODAY = RET(CROSS(MA5, MA10))

print(f'BTC5日均线{MA5[-1]}    BTC10日均线 {MA10[-1]}')
print('今天5日线是否上穿10日线', CROSS_TODAY)
print('最近5天收盘价全都大于5日线吗？', EVERY(CLOSE > MA10, 5))

DIF, DEA, MACD = MACD(CLOSE)
print('MACD值', DIF, DEA, MACD)
