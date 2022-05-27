import datetime
import time

# 雪球相关配置 (这段本应该放在 config.py，token 是周期性更新，且自用，没必要给自己增加麻烦所以提出来放在这里做全局参数用)
XQ_A_TOKEN = '2ac02e92a4583304b55e106fc6f03919c8f3c883'
TOKEN = 'xq_a_token={};'.format(XQ_A_TOKEN)

def currentTime():
    current = datetime.datetime.now()
    # 打印当前时间
    print("当前时间 :", current)

    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    # 雪球网请求是需要把日往后延一天
    dt = str(year) + '-' + str(month) + '-' + str(day + 1) + ' 17:00:00'
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(timeArray)
    # print(round(timestamp*1000))
    return round(timestamp * 1000)

def zeroTime():
    current = datetime.datetime.now()
    # 打印当前时间
    # print("当前时间 :", current)

    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    # 雪球网请求是需要把日往后延一天
    dt = str(year) + '-' + str(month) + '-' + str(day) + ' 00:00:00'
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(timeArray)
    print(round(timestamp*1000))
    return round(timestamp * 1000)

def customizeTime(offset=9):
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    # 雪球网请求是需要把日往后延一天
    dt = str(year) + '-' + str(month) + '-' + str(day - offset) + ' 00:00:00'
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(timeArray)
    # print(round(timestamp*1000))
    return round(timestamp * 1000)
