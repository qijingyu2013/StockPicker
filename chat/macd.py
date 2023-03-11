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
        last_macd = calculate_macd(result)
        if last_macd > 0:
            print(f'MACD for the last day: MACD={last_macd:.2f}')
            break


def calculate_macd(datas):
    # 将交易数据转换为DataFrame对象
    df = pd.DataFrame([data.__dict__ for data in datas])

    # 计算12日和26日的指数移动平均线
    ema12 = df['close'].ewm(span=12, adjust=False).mean()
    ema26 = df['close'].ewm(span=26, adjust=False).mean()

    # 计算DIFF
    diff = ema12 - ema26

    # 计算9日的指数移动平均线
    dea = diff.ewm(span=9, adjust=False).mean()

    # 计算MACD指标
    macd = 2 * (diff - dea)

    # 输出最后一天的MACD值
    last_macd = macd.iloc[-1]
    return last_macd


def main():
    fetchDatas()


main()
