import requests
import sys
import time


def get_binance_ticker(symbol='BTCUSDT'):
    """
    doc:
        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#symbol-order-book-ticker
    limit: 1200 / min (?)
    """
    main_path = 'https://api.binance.com'
    info_path = '/api/v3/ticker/bookTicker?symbol={0}'.format(symbol)
    r = requests.get(main_path + info_path)
    data_json = r.json()
    return data_json['bidPrice'], data_json['askPrice']


def get_bitstamp_ticker(symbol='btcusd'):
    """
    doc:
        https://www.bitstamp.net/api/
    limit: 600 / 10 min
    """
    main_path = 'https://www.bitstamp.net'
    info_path = '/api/v2/ticker/{0}/'.format(symbol)
    r = requests.get(main_path + info_path)
    data_json = r.json()
    return data_json['bid'], data_json['ask']


def get_cex_ticker(symbol='BTC/USD'):
    """
    doc:
        https://cex.io/rest-api#ticker
    limit: 600 / 10 min
    """
    main_path = 'https://cex.io/api'
    info_path = '/ticker/' + symbol
    r = requests.get(main_path + info_path)
    data_json = r.json()
    return data_json['bid'], data_json['ask']


def get_exmo_ticker(symbol='BTC_USDT'):
    """
    doc:
        https://exmo.com/en/api#/public_api
    limit: 180 / min
    """
    main_path = 'https://api.exmo.com'
    info_path = '/v1/ticker/'
    r = requests.get(main_path + info_path)
    data_json = r.json()
    return data_json[symbol]['buy_price'], data_json[symbol]['sell_price']


def get_hitbtc_ticker(symbol='BTCUSD'):
    """
    doc:
        https://api.hitbtc.com/#tickers
    limit: UNKNOWN
    """
    main_path = 'https://api.hitbtc.com'
    info_path = '/api/2/public/ticker/{0}'.format(symbol)
    r = requests.get(main_path + info_path)
    data_json = r.json()
    return data_json['bid'], data_json['ask']


def get_kucoin_ticker(symbol='BTC-USDT'):
    """
    doc:
        https://kucoinapidocs.docs.apiary.io/#reference/0/market/tick(open)
    limit: UNKNOWN
    """
    main_path = 'https://api.kucoin.com'
    info_path = '/v1/open/tick?symbol={0}'.format(symbol)
    r = requests.get(main_path + info_path)
    data_json = r.json()
    return data_json['data']['buy'], data_json['data']['sell']


exchanges = ['binance', 'bitstamp', 'cex', 'exmo', 'hitbtc', 'kucoin']
funcs = {'binance': get_binance_ticker, 'bitstamp': get_bitstamp_ticker, 'cex': get_cex_ticker,
     'exmo': get_exmo_ticker, 'hitbtc': get_hitbtc_ticker, 'kucoin': get_kucoin_ticker}


def get_best_price(exchange, symbol=None):
    fun = funcs[exchange]
    if symbol:
        tmp = fun(symbol)
    else:
        tmp = fun()
    if tmp:
        return float(tmp[0]), float(tmp[1])


#for ex in exchanges:
#    start = time.time()
#    fun = funcs[ex]
#    ans = get_best_price(ex)
#    print(ex, '   ', ans, '   ', time.time() - start)
