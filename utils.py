import datetime
import time

# 雪球相关配置 (这段本应该放在 config.py，token 是周期性更新，且自用，没必要给自己增加麻烦所以提出来放在这里做全局参数用)
try:
    XQ_TOKEN_FILE = open('xueqiu_token.txt', 'r+')
    XQ_A_TOKEN = XQ_TOKEN_FILE.readline().strip()
    U = XQ_TOKEN_FILE.readline().strip()
    TOKEN = 'U={};xq_a_token={};'.format(U, XQ_A_TOKEN)
    XQ_TOKEN_FILE.close()
except FileNotFoundError as e:
    open('xueqiu_token.txt', 'w+')


# 当前时间
def nowTime():
    current = datetime.datetime.now()
    un_time = time.mktime(current.timetuple())
    current = datetime.datetime.now()
    # 打印当前时间
    print("当前时间 :", current)
    return round(un_time)


# （雪球网专用）
def currentTime():
    current = datetime.datetime.now()
    # 打印当前时间
    print("当前时间 :", current)
    today = datetime.date.today()
    # yesterday = today - datetime.timedelta(days=1)
    tomorrow = today + datetime.timedelta(days=1)
    # print("当前时间 :", today)
    # print("昨天 :", yesterday)
    # print("明天 :", tomorrow)
    # year = datetime.datetime.now().year
    # month = datetime.datetime.now().month
    # day = datetime.datetime.now().day
    # 雪球网请求是需要把日往后延一天
    dt = str(tomorrow) + ' 17:00:00'
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(timeArray)
    # print(round(timestamp*1000))
    return round(timestamp * 1000)


def zeroTime():
    current = datetime.datetime.now()
    # 打印当前时间
    print("当前时间 :", current)
    today = datetime.date.today()
    dt = str(today) + ' 00:00:00'
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(timeArray)
    print(round(timestamp * 1000))
    return round(timestamp * 1000)


def customizeTime(offset=9):
    today = datetime.date.today()
    day = today + datetime.timedelta(days=offset)
    dt = str(day) + ' 00:00:00'
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(timeArray)
    # print(round(timestamp*1000))
    return round(timestamp * 1000)


def printOptimizedForm(lists, limit=0):
    lists_len = len(lists)
    single_template = "\r{0:>4}"
    print(single_template.format("股票代码", chr(12288)))
    for i in range(lists_len):
        u = lists[i]
        if limit == 0:
            print(single_template.format("\'" + u[1] + "\',  # " + u[0], chr(12288)))
        else:
            if u[2] >= limit:
                print(single_template.format("\'" + u[1] + "\',  # " + u[0], chr(12288)))
