from myTT import *

h = history(250,'1d','close','000001.XSHG')
HIGH = h['000001.XSHG'].values
LOW = h['000001.XSHG'].values

up ,mid ,dow n =TAQ(HIGH ,LOW ,20)  # 获取唐安奇交易通道数据，大道至简，能穿越牛熊
plt.figure(figsize=(15 ,8))
plt.plot(CLOSE ,label='沪深300指数')
plt.plot(up ,label='唐安奇-上轨');     plt.plot(mid ,label='唐安奇-中轨');      plt.plot(down ,label='唐安奇-下轨')