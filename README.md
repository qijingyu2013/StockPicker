#自动选股系统

## nineyin
## 9连阴

## LimitUpAfterFourDay
## 添加涨停后4天选股规则

该项目通过pysnowball实现。

使用前先确认 token

`ball.set_token('xq_a_token=727dbbbcb1a3b790f344cdc67f7910d7dfb0e461;')`

token 从访问 url 里的 cookies 中获取

[https://stock.xueqiu.com/v5/stock/realtime/quotec.json?symbol=SH000001,SZ399001,SZ399006&_=1541640828575
](https://stock.xueqiu.com/v5/stock/realtime/quotec.json?symbol=SH000001,SZ399001,SZ399006&_=1541640828575)

版本 1.0.0 现在还欠缺begin时间未完成

版本 1.0.1 自动生成begin

版本 1.0.2 添加涨停后4天选股规则

未来将实现: 定时选股，整合 mariadb