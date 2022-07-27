# 导入函数库
from jqdata import *

# 初始化函数，设定基准等等
def initialize(context):
    # 设定沪深300作为基准
    set_benchmark('000300.XSHG')
    # 开启动态复权模式(真实价格)
    set_option('use_real_price', True)
    # 输出内容到日志 log.info()
    log.info('初始函数开始运行且全局只运行一次')
    # 过滤掉order系列API产生的比error级别低的log
    # log.set_level('order', 'error')

    ### 股票相关设定 ###
    # 股票类每笔交易时的手续费是：买入时佣金万分之三，卖出时佣金万分之三加千分之一印花税, 每笔交易佣金最低扣5块钱
    set_order_cost(OrderCost(close_tax=0.001, open_commission=0.0003, close_commission=0.0003, min_commission=5), type='stock')

    # 要操作的股票：平安银行（g.为全局变量）
    g.security = '600309.XSHG'
    g.days = 0
    g.flag = False

    ## 运行函数（reference_security为运行时间的参考标的；传入的标的只做种类区分，因此传入'000300.XSHG'或'510300.XSHG'是一样的）
    # 开盘前运行
    run_daily(before_market_open, time='before_open', reference_security='000300.XSHG')
    # 开盘时运行
    run_daily(market_open, time='open', reference_security='000300.XSHG')
    # 收盘后运行
    run_daily(after_market_close, time='after_close', reference_security='000300.XSHG')

## 开盘前运行函数
def before_market_open(context):
    # 输出运行时间
    log.info('函数运行时间(before_market_open)：'+str(context.current_dt.time()))

    # 给微信发送消息（添加模拟交易，并绑定微信生效）
    # send_message('美好的一天~')

    security = g.security
    all_data = attribute_history(security, 9, '1d', ['open' ,'close'])
    count = 0
    # length = len(all_data)
    for i in range(0, 9, 1):
        if all_data['open'][i] >= all_data['close'][i]:
            count += 1
        else:
            break
    if count >= 9:
        g.flag = True

    if context.portfolio.positions_value > 0:
        g.days += 1
        # g.flag = True
        # log.info(g.flag)
        # log.info(all_data['open'][-1])
        # log.info(all_data['close'][-1])
        # if all_data['open'][-1] >= all_data['close'][-1] and g.days < 3:
        #     g.flag = True


## 开盘时运行函数
def market_open(context):
    log.info('函数运行时间(market_open):'+str(context.current_dt.time()))
    log.info(g.flag)
    log.info(g.days)
    security = g.security
    # 取得上一时间点价格
    # current_price = close_data['close'][-1]
    # 取得当前的现金
    cash = context.portfolio.available_cash

    if g.flag:
        # 记录这次买入
        log.info("买入 %s" % (security))
        # 买入股票
        order_value(security, cash*0.1*(g.days+1))
        g.flag = False

    if context.portfolio.positions_value > 0:
        if 0 < g.days < 3:
            # 记录这次买入
            log.info("买入 %s" % (security))
            # 买入股票
            order_value(security, cash*0.1*(g.days+1))
            g.flag = False
        elif g.days >= 3 or g.days == 0:
            # 记录这次卖出
            log.info("卖出 %s" % (security))
            # 卖出所有股票,使这只股票的最终持有量为0
            order_target(security, 0)
            g.days = 0
            g.flag = False

## 收盘后运行函数
def after_market_close(context):

    log.info(str('函数运行时间(after_market_close):'+str(context.current_dt.time())))
    log.info(g.flag)
    log.info(g.days)
    #得到当天所有成交记录
    trades = get_trades()
    for _trade in trades.values():
        log.info('成交记录：'+str(_trade))
    log.info('一天结束')
    log.info('##############################################################')

def process_initialize(context):
    g.__query = query(valuation)

