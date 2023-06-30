# 获取6天的 最高价 最低价 开盘价 收盘价
# 计算5日均线
# 计算 5天的最高幅度 （去除一个最大数，一个最小数）
# 计算 5天的最低幅度  （去除一个最大数，一个最小数）

# 卖出价格 前一日的收盘价 * （100 +（高于均线+0.5+2）/100 或者低于均线时取均线价格
# 买入价格 前一日的收盘价 * （100 -（低于均线+0.5+2））/100 或者高于均线时取均线价格
# 通过机器学习来预测上涨和下跌的概率
# 先定义股票列表
from sqlalchemy import and_

import models
from Distribution import fetchBottom


def fetchTradeData(code, num=30):
    return models.session.query(
        models.StockTrade
    ).filter(
        and_(
            models.StockTrade.code == code,
            models.StockTrade.delete == 0
        )
    ).order_by(
        models.StockTrade.timestamp.desc()
    ).limit(num + 1).all()


def fetchTradeDataAll(code):
    return models.session.query(
        models.StockTrade
    ).filter(
        and_(
            models.StockTrade.code == code,
            models.StockTrade.delete == 0
        )
    ).order_by(
        models.StockTrade.timestamp.desc()
    ).all()


def ma5(data):
    price = 0
    percents = 0
    conversion = 0
    for i in range(0, 5, 1):
        price += data[i].close
        percents += abs(data[i].percent)
        conversion += data[i].turn_over_rate
    return [price / 5, percents / 5, conversion / 5]


def ma(data, num=30):
    price = 0
    percents = 0
    conversion = 0
    for i in range(0, num, 1):
        price += data[i].close
        percents += abs(data[i].percent)
        conversion += data[i].turn_over_rate
    return [price / num, percents / num, conversion / num]


def highMargin(data, num=21):
    margin = []
    for i in range(0, num, 1):
        # 最高 - 前一天收盘价
        # margin.append((data[i].high - data[i].close) / data[i].close)
        # 最高 - 开盘价
        margin.append((data[i].high - data[i].open) / data[i].open)
        # 最高 - 前一天收盘价
        # margin.append((data[i].high - data[i + 1].close) / data[i + 1].close)
        # 所有涨的幅度
        if data[i].percent > 0:
            margin.append(data[i].percent / 100)
    return average(margin)


def lowMargin(data, num=21):
    margin = []
    for i in range(0, num, 1):
        # 开盘价 - 最低
        # margin.append((data[i].open - data[i].low) / data[i].open)
        # 收盘价 - 最低
        margin.append((data[i].close - data[i].low) / data[i].close)
        # 前一天收盘价 - 最低
        # margin.append((data[i + 1].close - data[i].low) / data[i + 1].close)
        # 所有跌的幅度
        if data[i].percent < 0:
            margin.append(abs(data[i].percent) / 100)
    return average(margin)


# 此处是求平均， 但其实可以引入 cost function
def average(margin):
    # print(margin)
    margin.sort()
    margin.pop()
    margin.pop()
    margin.reverse()
    margin.pop()
    margin.pop()
    # print(margin)
    return sum(margin) / len(margin)


# 剔除成功率低于50%的计算
def history(item):
    datas = fetchTradeDataAll(item)
    length = len(datas) - 6

    s_arr = []
    b_arr = []

    for ratio in range(5000, 1, -1):
        s_c = 0
        b_c = 0
        for i in range(1, length, 1):
            # print(i)
            data = datas[i:i + 6]
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
    # 此处应该引入回归函数
    for i in range(0, 4999, 1):
        if s_arr[i] > 80:
            # print('当前系数', i, '成功率', s_arr[i])
            s_coefficient = 10000 - (i + 5000)
            break
    for i in range(0, 4999, 1):
        if b_arr[i] > 80:
            # print('当前系数', i, '成功率', b_arr[i])
            b_coefficient = 10000 - (i + 5000)
            break

    # print("卖的最高系数", s_coefficient)
    # print("卖的最高系数成功率", s_arr[s_coefficient-5000])
    # print("买的最高系数", b_coefficient)
    # print("买的最高系数成功率", b_arr[b_coefficient-5000])
    return [s_coefficient, b_coefficient]


def tradeT(lists):
    for item in lists:
        data = fetchTradeData(item)
        # ma5s = ma(data, 5)
        # # 5日均价
        # avg = ma5s[0]
        # # 5日平均涨幅
        # percent = ma5s[1]
        # # 5日平均换手率
        # conversion = ma5s[2]
        high = highMargin(data)
        low = lowMargin(data)
        print(">>>>>>>>>>>>>>>>>>>")
        print("股票代号:", item)
        print("股票名称:", data[0].name)
        print("平均上涨幅度:", round(high * 100, 2), "%")
        print("平均下跌幅度:", round(low * 100, 2), "%")
        # print(low)
        # 获取历史高于80%成功率的交易系数
        # coefficient = history(item)
        # 买卖还要在均线上下还要加一点成功率
        # 买卖点越接近均线 成功率越高
        # 买点低于均线时 成功率低 买点高于均线时 成功率高
        # 低于均线卖 成功率高 * (1 + percent / 100)  + percent / 2 * conversion / 100
        # print(coefficient)
        # sell = data[0].close * (1 + high) * (1 + coefficient[0] / 10000)
        # buy = data[0].close * (1 - low) * (1 - coefficient[1] / 10000)

        # 卖出价
        sell = data[0].close * (1 + high)
        # 卖出价 下方筹码比重
        # 买入价
        buy = data[0].close * (1 - low)
        # 买入价 上方筹码比重

        # print("当天收盘价:", data[0].close)
        # print("当天均价:", round(avg, 2))

        print("今日收盘:", data[0].close)
        print("明日卖点:", round(sell, 2))
        print("明日买点:", round(buy, 2))
        fetchBottom(data[0].close, item, int(item) >= 600000 and "sh" or "sz")
        print("<<<<<<<<<<<<<<<<<<<")
        if item == '002184':
            print("<<<<<<<<<<<<<<<<<<<")
            fetchBottom(15.19, item, int(item) >= 600000 and "sh" or "sz")
            print("<<<<<<<<<<<<<<<<<<<")
        if item == '600330':
            print("<<<<<<<<<<<<<<<<<<<")
            fetchBottom(12, item, int(item) >= 600000 and "sh" or "sz")
            print("<<<<<<<<<<<<<<<<<<<")
        if item == '002694':
            print("<<<<<<<<<<<<<<<<<<<")
            fetchBottom(6.07, item, int(item) >= 600000 and "sh" or "sz")
            print("<<<<<<<<<<<<<<<<<<<")
        if item == '300769':
            print("<<<<<<<<<<<<<<<<<<<")
            fetchBottom(110.23, item, int(item) >= 600000 and "sh" or "sz")
            print("<<<<<<<<<<<<<<<<<<<")
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