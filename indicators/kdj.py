import talib

from indicators.basic import transferDataFrame, queryTradeList, queryStockList


def fetchDatas():
    lists = queryStockList()
    for item in lists:
        trades = queryTradeList(item)
        df = transferDataFrame(trades)
        k, d, j, is_golden_cross = calculate_kdj(df)
        if d <= 20 and is_golden_cross:
            print(f'KDJ for the last day: 股票名称={item[3]}, 股票代码={item[2]}')
            print(f'KDJ for the last day: K={k:.2f}, D={d:.2f}, J={j:.2f}')
            break


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

# def main():
#     fetchDatas()
#
#
# main()
