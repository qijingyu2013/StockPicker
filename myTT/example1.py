#数字货币行情获取和指标计算演示
from  hb_hq_api import *
from  myTT import *

df=get_price('btc.usdt',count=120,frequency='1d');
CLOSE=df.close.values;  OPEN=df.open.values;   HIGH=df.high.values;   LOW=df.low.values   #基础数据定义

up,mid,down=TAQ(HIGH,LOW,20)                                    #获取唐安奇交易通道数据，大道至简，能穿越牛熊
plt.figure(figsize=(15,8))
plt.plot(CLOSE,label='沪深300指数')
plt.plot(up,label='唐安奇-上轨');     plt.plot(mid,label='唐安奇-中轨');      plt.plot(down,label='唐安奇-下轨')


#
# df=get_price('btc.usdt',count=120,frequency='1d');      #日线数据获取  1d:1天  4h:4小时   60m: 60分钟    15m:15分钟
# CLOSE=df.close.values;  OPEN=df.open.values;   HIGH=df.high.values;   LOW=df.low.values   #基础数据定义
#
# MA5=MA(CLOSE,5)
# MA10=MA(CLOSE,10)
# CROSS_TODAY=RET(CROSS(MA5,MA10))
#
# print(f'BTC5日均线{ MA5[-1]}    BTC10日均线 {MA10[-1]}' )
# print('今天5日线是否上穿10日线',CROSS_TODAY)
# print('最近5天收盘价全都大于5日线吗？',EVERY(CLOSE>MA10,5) )
#
# DIF,DEA,MACD=MACD(CLOSE)
# print('MACD值',DIF,DEA,MACD)