import pysnowball as ball
from Distribution import fetchBottom
from Multiplier import fetchMultiplier
from NineYin import nineDailyData
from ReleaseVolume import fetchReleaseVolume
from StockToDB import upgradeStockList, upgradeStockTrade
from utils import currentTime, TOKEN


def main():
    print('###初始化执行任务')
    print('[1] 保存并且更新股票信息')
    print('[2] 保存并且更新股票行情')
    print('[3] 获取日连阴票')
    print('[4] 获取满足倍量的票')
    print('[5] 获取满足放量的票')
    ball.set_token(TOKEN)
    timestamp = currentTime()
    upgradeStockList(timestamp)
    upgradeStockTrade(timestamp, 'daily')
    nineDailyData()
    fetchMultiplier()
    fetchReleaseVolume()
    fetchBottom()

main()
