#自动选股系统

### NineYin
### 9连阴

### LimitUpAfterFourDay
### 涨停后4天选股规则

该项目通过pysnowball实现。

使用前先确认 token

`ball.set_token('xq_a_token=727dbbbcb1a3b790f344cdc67f7910d7dfb0e461;')`

token 从访问 url 里的 cookies 中获取

[https://stock.xueqiu.com/v5/stock/realtime/quotec.json?symbol=SH000001,SZ399001,SZ399006&_=1541640828575
](https://stock.xueqiu.com/v5/stock/realtime/quotec.json?symbol=SH000001,SZ399001,SZ399006&_=1541640828575)

操作流程

###初始化执行任务
[1] 保存并且更新股票信息

[2] 保存并且更新股票行情

[3] 全量更新

[4] 获取连日阴票(9)

[5] 获取连周阴票(10)

[6] 获取连月阴票(11)

[7] 获取满足4天前涨停后3天不破位的票

[8] 获取股票股东信息

根据编号选择任务:





版本 1.0.0 现在还欠缺begin时间未完成

版本 1.0.1 自动生成begin

版本 1.0.2 添加涨停后4天选股规则

版本 1.0.3 整合mariadb，整合操作流程

未来将实现: 定时选股，定时更新行情