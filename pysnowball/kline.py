from pysnowball import api_ref
from pysnowball import utls


def daily(symbol, begin=1652024902313, count=-10):
    return period(symbol, begin, count, 'day')


def weekly(symbol, begin=1652024902313, count=-10):
    return period(symbol, begin, count, 'week')


def monthly(symbol, begin=1652024902313, count=-10):
    return period(symbol, begin, count, 'month')


def period(symbol, begin=1652024902313, count=-10, date_period='day'):
    url = api_ref.kline_list_url + symbol

    url = url + '&period=' + date_period
    url = url + '&type=before'
    url = url + '&indicator=kline'
    url = url + '&begin=' + str(begin)
    url = url + '&count=' + str(count)
    # print(url)

    return utls.fetch(url)
