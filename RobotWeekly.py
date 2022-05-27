import pysnowball as ball
from NineYin import nineWeeklyData
from StockToDB import upgradeStockTrade
from utils import currentTime, TOKEN


def main():
    print('###初始化执行任务')
    print('[1] 保存并且更新股票行情')
    print('[2] 获取连周阴票')
    ball.set_token(TOKEN)
    timestamp = currentTime()
    upgradeStockTrade(timestamp, 'weekly')
    nineWeeklyData()


main()
