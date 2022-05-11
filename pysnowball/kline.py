from pysnowball import api_ref
from pysnowball import utls

def daily(symbol, begin=1652024902313, count=-10):

    url = api_ref.kline_list_url+symbol

    url = url + '&period=day'
    url = url + '&type=before'
    url = url + '&indicator=kline'
    url = url + '&begin='+str(begin)
    url = url + '&count='+str(count)
    # print(url)

    return utls.fetch(url)