import requests
import time


def get_binance_order_book(bidfile, askfile, symbol='BTCUSDT', limit=50):
    """
    doc:
        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#symbol-order-book-ticker
    max requests: 1200 / min (?)
    limit = 0  -->  full order book
    """
    main_path = 'https://api.binance.com'
    info_path = '/api/v1/depth?symbol={0}&limit={1}'.format(symbol, limit)
    r = requests.get(main_path + info_path)
    data_json = r.json()
    print(list(data_json.keys()))
    print()
    print(data_json)
    bidfile.write('\t\t\tBinance\n')
    for x in data_json['bids']:
        bidfile.write('{},{}\n'.format(x[0], x[1]))
    askfile.write('\t\t\tBinance\n')
    for x in data_json['asks']:
        askfile.write('{},{}\n'.format(x[0], x[1]))


def get_bitstamp_order_book(bidfile, askfile, symbol='btcusd', limit=50):
    """
    doc:
        https://www.bitstamp.net/api/
    max requests: 600 / 10 min
    DATA IS ACCUMULATED WITHIN AN HOUR (whatever it means)
    """
    main_path = 'https://www.bitstamp.net'
    info_path = '/api/v2/order_book/{0}/'.format(symbol)
    r = requests.get(main_path + info_path)
    data_json = r.json()
    #print(list(data_json.keys()))
    #print()
    #print(data_json)
    bidfile.write('\t\t\tBitstamp\n')
    bids = data_json['bids']
    for i in range(limit):
        bidfile.write('{},{}\n'.format(bids[i][0], bids[i][1]))
    askfile.write('\t\t\tBitstamp\n')
    asks = data_json['asks']
    for i in range(limit):
        askfile.write('{},{}\n'.format(asks[i][0], asks[i][1]))


def get_cex_order_book(bidfile, askfile, symbol='BTC/USD', limit=1):
    """
    doc:
        https://cex.io/rest-api#orderbook
    max requests: 180 / min
    """
    main_path = 'https://cex.io/api'
    info_path = '/order_book/{}/?depth={}'.format(symbol, limit)
    r = requests.get(main_path + info_path)
    data_json = r.json()
    #print(list(data_json.keys()))
    #print()
    #print(data_json)
    bidfile.write('\t\t\tCEX\n')
    bids = data_json['bids']
    for i in range(limit):
        bidfile.write('{},{}\n'.format(bids[i][0], bids[i][1]))
    askfile.write('\t\t\tCEX\n')
    asks = data_json['asks']
    for i in range(limit):
        askfile.write('{},{}\n'.format(asks[i][0], asks[i][1]))


def get_exmo_order_book(bidfile, askfile, symbol='BTC_USDT', limit=50):
    """
    doc:
        https://exmo.com/en/api#/public_api
    max requests: 180 / min
    limit <= 1000
    """
    main_path = 'https://api.exmo.com'
    info_path = '/v1/order_book/?pair={}&limit={}'.format(symbol, limit)
    r = requests.get(main_path + info_path)
    data_json = r.json()[symbol]
    #print(list(data_json.keys()))
    #print()
    #print(data_json)
    bidfile.write('\t\t\tExmo (USDT)\n')
    for x in data_json['bid']:
        bidfile.write('{},{}\n'.format(x[0], x[1]))
    askfile.write('\t\t\tExmo (USDT)\n')
    for x in data_json['ask']:
        askfile.write('{},{}\n'.format(x[0], x[1]))


def get_exmo_usd_order_book(bidfile, askfile, symbol='BTC_USD', limit=50):
    """
    doc:
        https://exmo.com/en/api#/public_api
    max requests: 180 / min
    limit <= 1000
    """
    main_path = 'https://api.exmo.com'
    info_path = '/v1/order_book/?pair={}&limit={}'.format(symbol, limit)
    r = requests.get(main_path + info_path)
    data_json = r.json()[symbol]
    #print(list(data_json.keys()))
    #print()
    #print(data_json)
    bidfile.write('\t\t\tExmo (USD)\n')
    for x in data_json['bid']:
        bidfile.write('{},{}\n'.format(x[0], x[1]))
    askfile.write('\t\t\tExmo (USD)\n')
    for x in data_json['ask']:
        askfile.write('{},{}\n'.format(x[0], x[1]))


def get_gdax_order_book(bidfile, askfile, symbol='BTC-USD', limit=2):
    """
    doc:
        https://docs.gdax.com/#get-product-order-book
    max requests: 3 / sec
    limit=2  -->  top 50 prices (aggregated)
    """
    main_path = 'https://api.gdax.com'
    info_path = '/products/{}/book?level={}'.format(symbol, limit)
    r = requests.get(main_path + info_path)
    data_json = r.json()
#    print(list(data_json.keys()))
#    print()
#    print(data_json)
    bidfile.write('\t\t\tGDAX\n')
    for x in data_json['bids']:
        bidfile.write('{},{}\n'.format(x[0], x[1]))
    askfile.write('\t\t\tGDAX\n')
    for x in data_json['asks']:
        askfile.write('{},{}\n'.format(x[0], x[1]))


def get_kucoin_order_book(bidfile, askfile, symbol='BTC-USDT', limit=50):
    """
    doc:
        https://kucoinapidocs.docs.apiary.io/#reference/0/market/order-books(open)
    max requests: UNKNOWN
    """
    main_path = 'https://api.kucoin.com'
    info_path = '/v1/open/orders?symbol={}&limit={}'.format(symbol, limit)
    r = requests.get(main_path + info_path)
    data_json = r.json()['data']
    #print(list(data_json.keys()))
    #print()
    #print(data_json)
    bidfile.write('\t\t\tKuCoin\n')
    for x in data_json['BUY']:
        bidfile.write('{},{}\n'.format(x[0], x[1]))
    askfile.write('\t\t\tKuCoin\n')
    for x in data_json['SELL']:
        askfile.write('{},{}\n'.format(x[0], x[1]))


exchanges = ['binance', 'bitstamp', 'cex', 'exmo', 'exmo_usd', 'gdax', 'kucoin']
funcs = {'binance': get_binance_order_book, 'bitstamp': get_bitstamp_order_book, 'cex': get_cex_order_book,
     'exmo': get_exmo_order_book, 'exmo_usd': get_exmo_usd_order_book,
    'gdax': get_gdax_order_book, 'kucoin': get_kucoin_order_book}


def get_order_book(bidfile, askfile, exchange, symbol=None, limit=None):
    fun = funcs[exchange]
    if symbol:
        if limit:
            fun(bidfile, askfile, symbol=symbol, limit=limit)
        else:
            fun(bidfile, askfile, symbol=symbol)
    else:
        if limit:
            fun(bidfile, askfile, limit=limit)
        else:
            fun(bidfile, askfile)


with open('bid.csv', 'w') as bid_csv:
    with open('ask.csv', 'w') as ask_csv:
        A = get_binance_order_book(bid_csv, ask_csv)
        #print('\t\tExmo')
        #get_exmo_order_book(bid_csv, ask_csv)
        #print('\n\n\t\tExmo (USD)')
        #get_exmo_usd_order_book(bid_csv, ask_csv)
        '''
        global_start = time.time()
        time_sum = 0.0
        for ex in exchanges:
            fun = funcs[ex]
            start_time = time.time()
            try:
                get_order_book(bid_csv, ask_csv, ex)
                print(ex, time.time() - start_time)
            except:
                pass
        print(time.time() - global_start)
        '''