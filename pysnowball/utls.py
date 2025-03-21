import requests
import json
from datetime import datetime

import pysnowball.token as token


def fetch(url, host="stock.xueqiu.com"):
    HEADERS = {'Host': host,
               'Accept': 'application/json',
               'Cookie': token.get_token(),
               'User-Agent': 'Xueqiu iPhone 11.8',
               'Accept-Language': 'zh-Hans-CN;q=1, ja-JP;q=0.9',
               'Accept-Encoding': 'br, gzip, deflate',
               'Connection': 'keep-alive'}

    response = requests.get(url, headers=HEADERS)

    # print(url)
    # print(HEADERS)
    # print(response)
    # print(response.content)

    if response.status_code != 200:
        raise Exception(response.content)

    return json.loads(response.content)


def fetch_without_token(url, host="stock.xueqiu.com"):
    HEADERS = {'Host': host,
               'Accept': 'application/json',
               'User-Agent': 'Xueqiu iPhone 11.8',
               'Accept-Language': 'zh-Hans-CN;q=1, ja-JP;q=0.9',
               'Accept-Encoding': 'br, gzip, deflate',
               'Connection': 'keep-alive'}

    response = requests.get(url, headers=HEADERS)

    # print(url)
    # print(HEADERS)
    # print(response)
    # print(response.content)

    if response.status_code != 200:
        raise Exception(response.content)

    return json.loads(response.content)


def fetch_xiuqiu_kline(url):
    session = requests.Session()
    session.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    session.get('https://xueqiu.com/?md5__1038=QqGxcDnDyiitnD05o4%2Br%3D8%3DeD5mEf40I3dx')
    r = session.get(url)
    # print(r.text)
    content = json.loads(r.text)
    # print(content)
    if content['error_code'] != 0:
        raise Exception(content['error_code']['error_description'])

    return content['data']


def fetch_eastmoney(url):
    HEADERS = {"Host": "datacenter-web.eastmoney.com",
               "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
               "Accept-Encoding": "gzip, deflate, br",
               "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,cy;q=0.6"}
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        raise Exception(response.content.decode('utf-8'))

    return json.loads(response.content)


def fetch_csindex(url):
    HEADERS = {"Host": "www.csindex.com.cn",
               "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
               "Accept": "application/json, text/plain, */*",
               "Accept-Encoding": "gzip, deflate, br",
               "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,cy;q=0.6"}
    response = requests.get(url, headers=HEADERS)

    # print(url)
    # print(HEADERS)
    # print(response)
    # print(response.content)

    if response.status_code != 200:
        raise Exception(response.content)

    return json.loads(response.content)


def fetch_hkc(url, txt_date=None):
    today = datetime.today()
    if txt_date is None:
        txt_date = today.strftime('%Y/%m/%d')
    today_str = today.strftime('%Y%m%d')
    payload = {
        '__VIEWSTATE': '/wEPDwUJNjIxMTYzMDAwZGSFj8kdzCLeVLiJkFRvN5rjsPotqw==',
        '__VIEWSTATEGENERATOR': '3C67932C',
        '__EVENTVALIDATION': '/wEdAAdbi0fj+ZSDYaSP61MAVoEdVobCVrNyCM2j+bEk3ygqmn1KZjrCXCJtWs9HrcHg6Q64ro36uTSn/Z2SUlkm9HsG7WOv0RDD9teZWjlyl84iRMtpPncyBi1FXkZsaSW6dwqO1N1XNFmfsMXJasjxX85ju3P1WAPUeweM/r0/uwwyYLgN1B8=',
        'today': today_str,
        'sortBy': 'stockcode',
        'sortDirection': 'asc',
        'alertMsg': '',
        'txtShareholdingDate': txt_date,
        'btnSearch': 'Search'
    }
    # payload = parse.urlencode(payload)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    requests.packages.urllib3.disable_warnings()
    response = requests.post(url, headers=headers, data=payload, verify=False)

    # print(url)
    # print(response)
    # print(response.content)

    if response.status_code != 200:
        raise Exception(response.content)
    return response.content


def fetch_9fzt_distribution(url):
    header = {'content-type': 'application/json; charset=utf-8',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    response = requests.get(url, headers=header)

    if response.status_code != 200:
        raise Exception(response.content)

    json_data = response.json()

    if json_data['code'] != 1:
        print(json_data['message'])
        raise Exception(response.content)

    return json_data['data']
