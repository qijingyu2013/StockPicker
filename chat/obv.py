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
        obv = calculate_obv(result)
        last_day_obv = obv['obv']
        last_day_obv_ma = obv['obv_ma']
        print(f"最后一天的 OBV 为：{last_day_obv}")
        print(f"最后一天的 OBV_MA 为：{last_day_obv_ma}")
        break


def calculate_obv(datas):
    # 将交易数据转换为DataFrame对象
    df = pd.DataFrame([data.__dict__ for data in datas])

    # 计算 OBV 指标
    # 计算 OBV
    df['obv'] = ((df['close'] - df['close'].shift(1) > 0).astype(int) * df['volume']
                 - (df['close'] - df['close'].shift(1) < 0).astype(int) * df['volume']).cumsum()

    # 计算 OBV_MA
    obv_window = 30  # OBV_MA 窗口大小
    df['obv_ma'] = df['obv'].rolling(obv_window).mean()
    # 输出最后一天的 OBV 数据
    obv = df.iloc[-1]
    return obv


def main():
    fetchDatas()


main()
