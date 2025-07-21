import threading

import pysnowball as ball
# from Distribution import fetchBottom
from Multiplier import fetchMultiplier
from MultiplierHolding import multiplierHolding
from NineYin import nineDailyData
from Amplitude import fetchAmplitude
from StockToDB import upgradeStockList, upgradeStockTrade
from utils import akTime, TOKEN


def main():
    print('###初始化执行任务')
    print('[1] 更新股票行情')
    print('[2] 更新股票信息')
    print('[3] 获取日连阴票')
    print('[4] 获取满足倍量的票')
    # print('[5] 获取满足放量的票')
    # print('[6] 获取底部的票')
    ball.set_token(TOKEN)
    start_dt, end_dt = akTime(0)
    upgradeStockTrade(start_dt, end_dt, 'daily')

    threadUpgradeStockList = threading.Thread(target=upgradeStockList, args=())
    threadNineDailyData = threading.Thread(target=nineDailyData, args=())
    threadMultiplier = threading.Thread(target=fetchMultiplier, args=())
    threadMultiplierHolding = threading.Thread(target=multiplierHolding, args=())
    threadAmplitude = threading.Thread(target=fetchAmplitude, args=())

    threadUpgradeStockList.start()
    threadNineDailyData.start()
    threadMultiplier.start()
    threadMultiplierHolding.start()
    threadAmplitude.start()

    threadUpgradeStockList.join()
    threadNineDailyData.join()
    threadMultiplier.join()
    threadMultiplierHolding.join()
    threadAmplitude.join()

    # upgradeStockList(timestamp)
    # nineDailyData()
    # fetchMultiplier()
    # multiplierHolding()
    # fetchReleaseVolume()
    # fetchBottom()


main()
