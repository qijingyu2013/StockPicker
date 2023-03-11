from sqlalchemy import and_
import models
import pandas as pd
from StockToDB import fetchStockListFromDB, StockType
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np


def fetchDatas():
    lists = fetchStockListFromDB(StockType.HuShen, False)
    length_total = len(lists)
    handle = 0
    for item in lists:
        result = models.session.query(
            models.StockTrade
        ).filter(
            and_(
                models.StockTrade.sid == item[0]
            )
        ).order_by(
            models.StockTrade.timestamp.desc()
        ).limit(900).all()
        obvs = calculate_obv(result)

        break


def calculate_obv(datas):
    # 将交易数据转换为DataFrame对象
    df = pd.DataFrame.from_records([s.__dict__ for s in datas])
    df = df.sort_values(by='timestamp')
    #
    # 接下来可以计算 OBV 和 OBV_MA。OBV 是一个累加指标，根据成交量的涨跌情况计算出来，公式如下：
    #
    # 如果当日收盘价大于昨日收盘价，则 OBV 累加当日成交量；
    # 如果当日收盘价小于昨日收盘价，则 OBV 减去当日成交量；
    # 如果当日收盘价等于昨日收盘价，则 OBV 不变。
    # OBV_MA 是 OBV 的移动平均值，可以通过 pandas 的 rolling 函数实现。
    # 计算 OBV
    df['obv'] = 0
    df.loc[df['close'] > df['close'].shift(), 'obv'] = df['volume']
    df.loc[df['close'] < df['close'].shift(), 'obv'] = -df['volume']
    df['obv'] = df['obv'].cumsum()

    # 计算 OBV_MA
    df['obv_ma'] = df['obv'].rolling(window=10).mean()
    # 接下来将日期、当日的 OBV 和 OBV_MA 整理出来并存入一个新的数组 obvs：
    obvs = df[['timestamp', 'obv', 'obv_ma']].values.tolist()

    return obvs


# 定义LSTM+CNN模型
class LSTM_CNN_Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(input_size=1, hidden_size=32, num_layers=1, batch_first=True)
        self.conv = nn.Sequential(
            nn.Conv1d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2)
        )
        self.fc = nn.Linear(64, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        out, _ = self.lstm(x.unsqueeze(-1))
        out = out.permute(0, 2, 1)
        out = self.conv(out)
        out = out.view(-1, 64)
        out = self.fc(out)
        out = self.sigmoid(out)
        return out.squeeze()


# 训练模型
def train(model, X, y, num_epochs=100, lr=0.001):
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = nn.BCELoss()
    for epoch in range(num_epochs):
        optimizer.zero_grad()
        y_pred = model(X)
        loss = criterion(y_pred, y)
        loss.backward()
        optimizer.step()
        if epoch % 10 == 0:
            print(f"Epoch {epoch}, Loss: {loss.item()}")


def main():
    lists = fetchStockListFromDB(StockType.HuShen, False)
    for item in lists:
        result = models.session.query(
            models.StockTrade
        ).filter(
            and_(
                models.StockTrade.sid == item[0]
            )
        ).order_by(
            models.StockTrade.timestamp.desc()
        ).limit(900).all()
        obvs = calculate_obv(result)

        # 将obvs数组转换为张量
        obvs_tensor = torch.from_numpy(np.array(obvs))
        # 将数据拆分为训练集和测试集
        train_size = len(obvs) - 100
        train_data = obvs_tensor[:train_size]
        test_data = obvs_tensor[train_size:]

        # 构造训练集和测试集的输入和输出
        X_train = train_data[:-1].float()
        y_train = (train_data[1:] > train_data[:-1]).float()
        X_test = test_data[:-1].float()
        y_test = (test_data[1:] > test_data[:-1]).float()

        # 训练模型
        model = LSTM_CNN_Model()
        train(model, X_train, y_train)

        # 在测试集上进行预测并输出结果
        with torch.no_grad():
            y_pred = model(X_test)
            test_loss = nn.BCELoss()(y_pred, y_test)
            y_pred = y_pred.numpy() > 0.5
            print(f"Test Loss: {test_loss.item()}, Accuracy: {(y_pred == y_test.numpy()).mean()}")
            print(f"Predictions: {y_pred}")
        break


main()
