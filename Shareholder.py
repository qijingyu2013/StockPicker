import pysnowball as ball


def topTenHolders(symbol):
    ulist = ball.top_holders(symbol)
    print(ulist)
    return


def allHolders(symbol):
    ulist = ball.holders(symbol)
    print(ulist)
    return
