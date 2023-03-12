import pandas as pd
import talib
from sqlalchemy import and_

import models
from StockToDB import fetchStockListFromDB, StockType


def fetchDatas():
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
        ).limit(900).all()
        k, d, j, is_golden_cross = calculate_kdj(result)
        if d <= 20 and is_golden_cross:
            print(f'KDJ for the last day: 股票名称={item[3]}, 股票代码={item[2]}')
            print(f'KDJ for the last day: K={k:.2f}, D={d:.2f}, J={j:.2f}')
            break


def calculate_kdj(datas):
    # 将数据集转换为pandas DataFrame对象
    df = pd.DataFrame.from_records([data.__dict__ for data in datas])

    # 将timestamp列转换为日期格式
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.date

    # 按日期排序
    df = df.sort_values(by='date')

    # 计算KDJ指标
    df['slowk'], df['slowd'] = talib.STOCH(df['high'], df['low'], df['close'], fastk_period=9, slowk_period=5, slowk_matype=1, slowd_period=5, slowd_matype=1)
    last_k = df.iloc[-1]['slowk']
    last_d = df.iloc[-1]['slowd']
    last_j = 3 * last_k - 2 * last_d


    # 判断是否出现金叉
    prev_k = df.iloc[-2]['slowk']
    prev_d = df.iloc[-2]['slowd']
    # prev_j = 3 * prev_k - 2 * prev_d
    is_golden_cross = prev_k < prev_d and last_k > last_d

    # 返回最后一天的KDJ值
    return last_k, last_d, last_j, is_golden_cross


def main():
    fetchDatas()


main()