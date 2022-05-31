# 获取6天的 最高价 最低价 开盘价 收盘价
# 计算5日均线
# 计算 5天的最高幅度 （去除一个最大数，一个最小数）
# 计算 5天的最低幅度  （去除一个最大数，一个最小数）

# 卖出价格 前一日的收盘价 * （100 +（高于均线+0.5+2）/100 或者低于均线时取均线价格
# 买入价格 前一日的收盘价 * （100 -（低于均线+0.5+2））/100 或者高于均线时取均线价格

# 先定义股票列表
from sqlalchemy import and_

import models


def fetchTradeData(code):
    return models.session.query(
        models.StockTrade
    ).filter(
        and_(models.StockTrade.code == code)
    ).order_by(
        models.StockTrade.timestamp.desc()
    ).limit(6).all()


def fetchTradeDataAll(code):
    return models.session.query(
        models.StockTrade
    ).filter(
        and_(models.StockTrade.code == code)
    ).order_by(
        models.StockTrade.timestamp.desc()
    ).all()


def ma5(data):
    total = 0
    for i in range(0, 5, 1):
        total += data[i].close
        # print(data[i].close)
    avg = total / 5
    # print(avg)
    return avg


def highMargin(data):
    margin = []
    for i in range(0, 5, 1):
        margin.append((data[i].high - data[i].open) / data[i].open)
        margin.append((data[i].high - data[i].close) / data[i + 1].close)
        margin.append((data[i].high - data[i].open) / data[i + 1].close)
        margin.append((data[i].high - data[i + 1].close) / data[i + 1].close)
    return average(margin)


def lowMargin(data):
    margin = []
    for i in range(0, 5, 1):
        margin.append((data[i].open - data[i].low) / data[i].open)
        margin.append((data[i].close - data[i].low) / data[i + 1].close)
        margin.append((data[i].open - data[i].low) / data[i + 1].close)
        margin.append((data[i + 1].close - data[i].low) / data[i + 1].close)
    return average(margin)


def average(margin):
    margin.sort()
    margin.pop()
    margin.reverse()
    margin.pop()
    return sum(margin) / len(margin)


def history():
    lists = ['300581']
    datas = fetchTradeDataAll(lists)
    length = len(datas) - 6

    s_arr = []
    b_arr = []

    for ratio in range(10000, 0, -1):
        s_c = 0
        b_c = 0
        for i in range(1, length, 1):
            # print(i)
            data = datas[i:i + 6]
            avg = ma5(data)
            high = highMargin(data)
            low = lowMargin(data)
            # print("股票:", data[0].name)
            # print("当天收盘价:", data[0].close)

            # print("当天均价:", round(avg, 2))

            sell = data[0].close * (1 + high * ratio / 10000)
            # print("当天卖点:", round(sell, 2), "当天最高价：", datas[i - 1].high)
            if sell < datas[i - 1].high:
                s_c += 1

            # 买入价格 前一日的收盘价 * （100 -（低于均线+0.5+2））/100 或者高于均线时取均线价格
            buy = data[0].close * (1 - low * ratio / 10000)
            # print("当天买点:", round(buy, 2), "当天最低价：", datas[i - 1].low)
            if buy > datas[i - 1].low:
                b_c += 1

        # print(ratio)
        # print("一共计算", length, '次')
        # print("卖成功", s_c, '次', '成功率:', str(round(s_c / length * 100, 2)) + '%')
        # print("买成功", b_c, '次', '成功率:', str(round(b_c / length * 100, 2)) + '%')
        s_arr.append(round(s_c / length * 100, 2))
        b_arr.append(round(b_c / length * 100, 2))

    # s_arr.reverse()
    # b_arr.reverse()
    # print("卖成功率", len(s_arr), s_arr)
    # print("买成功率", len(b_arr), b_arr)
    s_coefficient = 0
    b_coefficient = 0

    for i in range(0, 9999, 1):
        if s_arr[i] >= 80:
            s_coefficient = i + 1
            break
    for i in range(0, 9999, 1):
        if b_arr[i] >= 80:
            b_coefficient = i + 1
            break

    # print("卖的最高系数", s_coefficient)
    # print("买的最高系数", b_coefficient)
    return [s_coefficient, b_coefficient]


def tradeT():
    lists = ['300581', '000930', '300077', '600893', '000017', '002620']
    for item in lists:
        data = fetchTradeData(item)
        avg = ma5(data)
        high = highMargin(data)
        low = lowMargin(data)
        print("股票:", data[0].name)
        coefficient = history()

        sell = data[0].close * (1 + high * coefficient[0]/10000)
        buy = data[0].close * (1 - low * coefficient[1]/10000)
        # print("当天收盘价:", data[0].close)
        # print("当天均价:", round(avg, 2))
        # 卖出价格 前一日的收盘价 * （100 +（高于均线+0.5+2）/100 或者低于均线时取均线价格
        # if item == '300581':
        #     # 晨曦航空用
        #     sell = data[0].close * (1 + high*0.47)
        #     buy = data[0].close * (1 - low*0.35)
        # elif item == '000930':
        #     # 中粮科技用
        #     sell = data[0].close * (1 + high*0.29)
        #     buy = data[0].close * (1 - low*0.28)
        # elif item == '300077':
        #     # 国民技术用
        #     sell = data[0].close * (1 + high*0.18)
        #     buy = data[0].close * (1 - low*0.31)
        # elif item == '600893':
        #     sell = data[0].close * (1 + high*0.21)
        #     buy = data[0].close * (1 - low*0.37)

        print("明日卖点:", round(sell, 2))
        print("明日买点:", round(buy, 2))
        # sell = data[0].close * (1 + high*0.33)
        # if sell < avg:
        #     print("明日卖点:", round(avg, 2))
        # else:
        #     print("明日卖点:", round(sell, 2))
        # # 买入价格 前一日的收盘价 * （100 -（低于均线+0.5+2））/100 或者高于均线时取均线价格
        # buy = data[0].close * (1 - low*0.33)
        # if buy > avg:
        #     print("明日买点:", round(avg, 2))
        # else:
        #     print("明日买点:", round(buy, 2))


# history()
