# 主文件

import pysnowball as ball
from Distribution import fetchBottom
from Multiplier import fetchMultiplier
from NineYin import nineDailyData
# from Pick_KDJ_MACD_OBV import picker
from ReleaseVolume import fetchReleaseVolume
from StockToDB import upgradeStockList, upgradeStockTrade
from Predictor import tradeT
from utils import currentTime, TOKEN

def main():
    # 提前处理日常任务
    print('-----九阴票-----')
    nineDailyData(9)
    print('-----九阴票-----')
    print('-----倍量票-----')
    fetchMultiplier()
    print('-----倍量票-----')
    # print('-----放量票-----')
    # fetchReleaseVolume()
    # print('-----放量票-----')
    # print('-----底部票-----')
    # fetchBottom()
    # print('-----底部票-----')

    print('###初始化执行任务')
    print('[1] 保存并且更新股票信息')
    print('[2] 保存并且更新股票行情')
    print('[3] 全量更新')
    print('[4] 获取连日阴票(9)')
    print('[5] 获取底部票')
    print('[6] 获取满足技术指标的票')
    # print('[6] 获取连月阴票(11)')
    print('[7] 获取倍量票')
    print('[8] 获取放量票')
    print('[9] 预测第二天交易信息')
    print('根据编号选择任务:')
    s = int(input())
    ball.set_token(TOKEN)
    timestamp = currentTime()

    if s == 1:
        upgradeStockList(timestamp)
        print('\r保存并且更新股票信息,已完成！')
    elif s == 2:
        upgradeStockTrade(timestamp, 'daily')
        print('\r保存并且更新股票行情,已完成！')
    elif s == 3:
        upgradeStockList(timestamp)
        upgradeStockTrade(timestamp)
        print('\r全量更新,已完成！')
    elif s == 4:
        print('输入连阴次数:')
        count = int(input())
        if count <= 5:
            nineDailyData(5)
        elif count >= 9:
            nineDailyData(9)
        else:
            nineDailyData(count)
    elif s == 5:
        fetchBottom()
    # elif s == 6:
        # picker()

    # elif s == 5:
    #     print('输入连阴次数:')
    #     count = int(input())
    #     if count <= 6:
    #         nineWeeklyData(6)
    #     elif count >= 10:
    #         nineWeeklyData(10)
    #     else:
    #         nineWeeklyData(count)
    # elif s == 6:
    #     print('输入连阴次数:')
    #     count = int(input())
    #     if count <= 7:
    #         nineMonthlyData(7)
    #     elif count >= 11:
    #         nineMonthlyData(11)
    #     else:
    #         nineMonthlyData(count)
    elif s == 7:
        fetchMultiplier()
    elif s == 8:
        fetchReleaseVolume()
    # elif s == 8:
    #     print('[1] 前十股东信息:')
    #     print('[2] 全部股东信息:')
    #     print('根据编号选择任务:')
    #     t = int(input())
    #     print('请输入股票编码(带上大写SZ或者SH):')
    #     code = str(input())
    #     if t == 1:
    #         topTenHolders(code)
    #     elif t == 2:
    #         allHolders(code)
    #     else:
    #         topTenHolders(code)
    elif s == 9:
        # 固定位
        steady_list = [
            '300581',
            '300077',
            '002373',
            '600486',
        ];
        # 持仓区
        trade_list = [
            '300769',  # 德方纳米
            '002812',  # 恩捷股份
            '603217',  # 元利科技
        ];
        # 观察区
        observe_list = [
            '600072',  # 中船科技
            '601728',  # 中国电信
            '600050',  # 中国联通

        ];
        # list = ['000554']
        print('固定位 ============')
        tradeT(steady_list)
        print('固定位 ============')
        print('持仓区 ========')
        tradeT(trade_list)
        print('持仓区 ========')
        print('观察区 ========')
        tradeT(observe_list)
        print('观察区 ========')
    else:
        print('输入错误。。。')


main()
