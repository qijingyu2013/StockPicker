from pysnowball import api_ref, utls
from utils import nowTime


def fetchDistrubitionData(symbols, symbol_type):
    today = nowTime()
    url = api_ref.distrubition_url.format(symbols, symbol_type.lower(), today)
    data = utls.fetch_9fzt_distribution(url)
    # length = len(data)
    return data


# def main():
    # data = fetchDistrubitionData('600010', 'SH')
    # items = data['items']
    # saveStockDistributionDaily(7, data)

# main()
