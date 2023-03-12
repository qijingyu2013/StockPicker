import pandas as pd
from sqlalchemy import and_

import models
from StockToDB import fetchStockListFromDB, StockType


def queryStockList():
    return fetchStockListFromDB(StockType.HuShenChuang, False)


def queryTradeList(item):
    return models.session.query(
        models.StockTrade
    ).filter(
        and_(
            models.StockTrade.sid == item[0]
        )
    ).order_by(
        models.StockTrade.timestamp.desc()
    ).limit(365).all()


def transferDataFrame(result):
    # 将数据集转换为pandas DataFrame对象
    df = pd.DataFrame.from_records([data.__dict__ for data in result])

    # 将timestamp列转换为日期格式
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.date

    # 按日期排序
    df = df.sort_values(by='date')
    return df
