import pysnowball as ball
from LimitUpAfterThreeDayWithDB import fetchLimitUpAfterThreeDay
from NineYin import nineMonthlyData
from StockToDB import upgradeStockList, upgradeStockTrade
from utils import currentTime


def main():
    print('###初始化执行任务')
    print('[1] 保存并且更新股票行情')
    print('[2] 获取连月阴票')
    ball.set_token('xq_a_token=9d7c75c59c8b3ef763711f682f3bb26163c4aad7;')
    timestamp = currentTime()
    upgradeStockTrade(timestamp, 'monthly')
    nineMonthlyData()


main()
