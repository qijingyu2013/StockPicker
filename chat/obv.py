import numpy as np
import talib
from sqlalchemy import and_
import models
import pandas as pd
from StockToDB import fetchStockListFromDB, StockType


# 通过以下步骤计算MACD指标：
#
# 创建一个DataFrame来保存原始数据。可以使用Pandas的read_sql函数从数据库中读取数据，或者使用Pandas的read_csv函数从CSV文件中读取数据。
# 计算12天和26天的EMA。可以使用Pandas的ewm函数来计算指数加权移动平均线（EMA）。
# 计算DIF线。DIF线等于12天EMA减去26天EMA。
# 计算9天的EMA作为MACD的信号线。
# 计算MACD柱。MACD柱等于DIF线减去信号线。


def fetchDatas():
    lists = fetchStockListFromDB(StockType.HuShenChuang, False)
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
        ).limit(365).all()
        last_day_obv, last_day_obv_ma, tend = calculate_obv(result)
        if tend == 1:
            print(f'MACD for the last day: 股票名称={item[3]}, 股票代码={item[2]}')
            print(f"最后一天的 OBV 为：{last_day_obv}, 最后一天的 OBV_MA 为：{last_day_obv_ma}")
            break


def calculate_obv(datas):
    # 将数据集转换为pandas DataFrame对象
    df = pd.DataFrame.from_records([data.__dict__ for data in datas])

    # 将timestamp列转换为日期格式
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.date

    # 按日期排序
    df = df.sort_values(by='date')

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
    fetchDatas()


main()
