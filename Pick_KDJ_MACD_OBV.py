import numpy as np
import talib
from sqlalchemy import and_
import models
from StockToDB import fetchStockListFromDB, StockType, saveStockMission
import pysnowball as ball
from utils import currentTime, zeroTime, printOptimizedForm
import pandas as pd

from StockToDB import fetchStockListFromDB, StockType


def filterData():
    lists = fetchStockListFromDB(StockType.HuShenChuang, False)
    length_total = len(lists)
    handle = 0
    count_kdj = 0
    count_kdj_macd = 0
    count_kdj_macd_obv = 0
    for item in lists:
        result = models.session.query(
            models.StockTrade
        ).filter(
            and_(
                models.StockTrade.sid == item[0]
            )
        ).order_by(
            models.StockTrade.timestamp.desc()
        ).limit(365).all()
        df = transferDataFrame(result)
        k, d, j, gold = calculate_kdj(df)

        if d < 20 and gold:
            count_kdj += 1
            # print(f'符合指标: 股票名称={item[3]}, 股票代码={item[2]}')
            # print(f'KDJ for the last day: K={k:.2f}, D={d:.2f}, J={j:.2f}')
            dif, dea, macd = calculate_macd(df)
            if macd > dif: #  and macd > 0
                count_kdj_macd += 1
                # print(f'MACD for the last day: MACD={macd:.2f}')
                last_day_obv, last_day_obv_ma, tend = calculate_obv(df)
                if tend == 1:
                    count_kdj_macd_obv += 1
                    print(f'符合指标: 股票名称={item[3]}, 股票代码={item[2]}')
                    print(f'KDJ for the last day: K={k:.2f}, D={d:.2f}, J={j:.2f}')
                    print(f'MACD for the last day: MACD={macd:.2f}')
                    print(f"最后一天的 OBV 为：{last_day_obv}, 最后一天的 OBV_MA 为：{last_day_obv_ma}")
    print(f'符合KDJ指标:{count_kdj}')
    print(f'同时符合KDJ和MACD指标:{count_kdj_macd}')
    print(f'同时符合KDJ、MACD和OBV指标:{count_kdj_macd_obv}')


def transferDataFrame(datas):
    # 将数据集转换为pandas DataFrame对象
    df = pd.DataFrame.from_records([data.__dict__ for data in datas])

    # 将timestamp列转换为日期格式
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.date

    # 按日期排序
    df = df.sort_values(by='date')
    return df


def calculate_kdj(df):
    # 计算KDJ指标
    df['slowk'], df['slowd'] = talib.STOCH(df['high'], df['low'], df['close']
                                           , fastk_period=9, slowk_period=5, slowk_matype=1
                                           , slowd_period=5, slowd_matype=1)
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


def calculate_macd(df):
    # 计算 MACD
    macd, macd_signal, macd_histogram = talib.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)

    # 获取最后一天的 MACD 数据
    last_dif = macd.iloc[-1]
    last_dea = macd_signal.iloc[-1]
    last_macd = (last_dif-last_dea)*2
    # last_macd = macd_histogram.iloc[-1]
    return last_dif, last_dea, last_macd


def calculate_obv(df):
    # 计算 obv 指标
    df['obv'] = talib.OBV(df['close'], df['volume'])

    # 计算 obv_ma 指标
    df['obv_ma'] = talib.MA(df['obv'], timeperiod=30)

    # 整理出日期、当日 obv 和当日 obv_ma 数据，并保存在一个新的数组 obvs 中
    obvs = df[['timestamp', 'obv', 'obv_ma']].values.tolist()

    last_day_obv, last_day_obv_ma = obvs[-1][1], obvs[-1][2]
    # print("最后一天的 OBV 指标为：", last_day_obv)
    # print("最后一天的 OBV_MA 指标为：", last_day_obv_ma)

    # 取最近 30 天的 obv_ma 数据，并计算均值
    obv_ma_30 = np.mean(df['obv_ma'].rolling(window=30).mean().tail(30))

    # 取最近 14 天的 obv_ma 数据，并计算均值
    obv_ma_14 = np.mean(df['obv_ma'].rolling(window=14).mean().tail(14))

    # 取最近 7 天的 obv_ma 数据，并计算均值
    obv_ma_7 = np.mean(df['obv_ma'].rolling(window=7).mean().tail(7))
    tend = 0
    # 判断趋势
    if obv_ma_7 > obv_ma_14 > obv_ma_30:
        tend = 1
        # print("趋势为上涨")
    elif obv_ma_7 < obv_ma_14 < obv_ma_30:
        tend = -1
        # print("趋势为下跌")
    else:
        tend = 0
        # print("趋势为震荡")
    return last_day_obv, last_day_obv_ma, tend


def main():
    filterData()


main()
