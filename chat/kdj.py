from sqlalchemy import and_
import models
from StockToDB import fetchStockListFromDB, StockType, saveStockMission
import pysnowball as ball
from utils import currentTime, zeroTime, printOptimizedForm
import pandas as pd

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
        k, d, j = calculate_kdj(result)
        if k <= 20 and d <= 20 and j <= 20:
            print(f'KDJ for the last day: K={k:.2f}, D={d:.2f}, J={j:.2f}')
            break


def calculate_kdj(datas):
    # 构造DataFrame
    df = pd.DataFrame([data.__dict__ for data in datas])
    df.set_index('timestamp', inplace=True)
    # 计算RSV
    df['low_n'] = df['low'].rolling(window=9, min_periods=1).min()
    df['high_n'] = df['high'].rolling(window=9, min_periods=1).max()
    df['rsv'] = (df['close'] - df['low_n']) / (df['high_n'] - df['low_n']) * 100
    # 计算KDJ
    df['k'] = df['rsv'].ewm(com=2).mean()
    df['d'] = df['k'].ewm(com=2).mean()
    df['j'] = 3 * df['k'] - 2 * df['d']
    # 返回最后一天的KDJ值
    return df.iloc[-1]['k'], df.iloc[-1]['d'], df.iloc[-1]['j']


def main():
    fetchDatas()


main()

# # 计算KDJ指标
# def calc_kdj(highs, lows, closes, n=9, m1=3, m2=3):
#     """
#     :param highs: 最高价序列
#     :param lows: 最低价序列
#     :param closes: 收盘价序列
#     :param n: KDJ指标中的N值，默认为9
#     :param m1: KDJ指标中的M1值，默认为3
#     :param m2: KDJ指标中的M2值，默认为3
#     :return: K值序列、D值序列、J值序列
#     """
#     # 计算RSV值
#     low_list = pd.Series(lows).rolling(window=n, min_periods=n).min()
#     high_list = pd.Series(highs).rolling(window=n, min_periods=n).max()
#     rsv = (closes - low_list) / (high_list - low_list) * 100
#     # 计算K值、D值、J值
#     k = rsv.ewm(com=m1).mean()
#     d = k.ewm(com=m2).mean()
#     j = 3 * k - 2 * d
#     return k, d, j
#
# # 从数据中取出需要的字段
# df = pd.DataFrame(datas, columns=["name", "timestamp", "high", "low", "close"])
#
# # 取出最近一天的数据
# latest_data = df.iloc[-1]
#
# # 取出最近9天的数据
# last_n_days = df.iloc[-9:]
#
# # 计算KDJ指标
# k, d, j = calc_kdj(last_n_days["high"], last_n_days["low"], last_n_days["close"])
#
# # 输出最近一天的KDJ指标
# print(f"最近一天的KDJ指标为：K={k.iloc[-1]}, D={d.iloc[-1]}, J={j.iloc[-1]}")
