
from myTT import *

attribute_history('000001.XSHG', 250, unit='1d',
                  fields=['open', 'close', 'high', 'low', 'volume', 'money'],
                  skip_paused=True, df=False, fq='pre')

h = history(250,'1d','close','000001.XSHG')
CLOSE = h['000001.XSHG'].values


up,mid,lower=BOLL(CLOSE)                                        #获取布林带数据

plt.figure(figsize=(15,8))
plt.plot(CLOSE,label='上证');
plt.plot(up,label='up');        #画图显示
plt.plot(mid,label='mid');
plt.plot(lower,label='lower');