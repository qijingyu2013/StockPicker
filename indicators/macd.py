import talib
from indicators.basic import queryStockList, queryTradeList, transferDataFrame


# 通过以下步骤计算MACD指标：
#
# 创建一个DataFrame来保存原始数据。可以使用Pandas的read_sql函数从数据库中读取数据，或者使用Pandas的read_csv函数从CSV文件中读取数据。
# 计算12天和26天的EMA。可以使用Pandas的ewm函数来计算指数加权移动平均线（EMA）。
# 计算DIF线。DIF线等于12天EMA减去26天EMA。
# 计算9天的EMA作为MACD的信号线。
# 计算MACD柱。MACD柱等于DIF线减去信号线。


def fetchDatas():
    lists = queryStockList()
    for item in lists:
        trades = queryTradeList(item)
        df = transferDataFrame(trades)
        dif, dea, macd = calculate_macd(df)

        if macd > dif:
            print(f'MACD for the last day: 股票名称={item[3]}, 股票代码={item[2]}')
            print(f"最后一天的 MACD 数据：dif={dif}, dea={dea}, macd={macd}")
            break


def calculate_macd(df):
    # 计算 MACD
    macd, macd_signal, macd_histogram = talib.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)

    # 获取最后一天的 MACD 数据
    last_dif = macd.iloc[-1]
    last_dea = macd_signal.iloc[-1]
    last_macd = (last_dif - last_dea) * 2
    # last_macd = macd_histogram.iloc[-1]
    return last_dif, last_dea, last_macd

# def main():
#     fetchDatas()
#
#
# main()
