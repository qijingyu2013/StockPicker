from pysnowball import api_ref
from pysnowball import utls


# 获取沪深所有股票代码
def stock_list(size=5000, begin=1652024902313):
    url = api_ref.stock_list_url
    url = url + '&page=1'
    url = url + '&size=' + str(size)
    url = url + '&_=' + str(begin)
    # print(url)

    return utls.fetch(url, 'xueqiu.com')

# 废弃（旧版）
# def stock_list():
#     url = api_ref.stock_list_url
#     return utls.fetch(url, 'xueqiu.com')


# 获取沪深所有股票代码
def debenture_list(size=5000, begin=1652024902313):
    url = api_ref.debenture_list_url
    url = url + '&page=1'
    url = url + '&size=' + str(size)
    url = url + '&_=' + str(begin)
    # print(url)

    return utls.fetch(url, 'xueqiu.com')
