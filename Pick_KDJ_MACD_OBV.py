from StockToDB import saveStockMission
from indicators import queryStockList, queryTradeList, transferDataFrame, calculate_kdj, calculate_macd, calculate_obv
from utils import zeroTime


def picker():
    lists = queryStockList()
    length_total = len(lists)
    handle = 0
    count_kdj = 0
    count_kdj_macd = 0
    count_kdj_macd_obv = 0
    ulist = []
    zero = zeroTime()
    for item in lists:
        result = queryTradeList(item)
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
                    print(f"OBV for the last day：{last_day_obv:.2f}, OBV_MA：{last_day_obv_ma:.2f}")
                    ulist.append([result[3].name, result[3].code, '二板突破'])
        handle += 1
        percent = handle / length_total
        surplus = round((length_total - handle) * 0.005, 1)
        print('\r完成度为: {:.2%}, 还剩余: {}秒'.format(percent, surplus), end='', flush=True)
    print(f'符合KDJ指标:{count_kdj}')
    print(f'同时符合KDJ和MACD指标:{count_kdj_macd}')
    print(f'同时符合KDJ、MACD和OBV指标:{count_kdj_macd_obv}')
    # saveStockMission(zero, 1, str(ulist))

# def main():
#     picker()
#
#
# main()
