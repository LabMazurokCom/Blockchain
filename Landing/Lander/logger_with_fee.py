#!/usr/bin/python3
"""
    N.B. Timestamps are given in ms !!!
"""
"""
        Calling examples:
    python orders_logger.py -h                                      # help
    python orders_logger.py btc_usd                                 # currency pair is the only required argument
    python orders_logger -c "my_new_config.json" btc_usd            # pass configuration file
    python orders_logger -l 10 btc_usd                              # pass number of top orders to be processed
    python orders_logger.py -c "config.json" -l 10 btc_usd          # pass all available arguments
"""


import aiohttp
import asyncio
import async_timeout
import json
import sys
import os
# import pymongo
import time
from pprint import pprint


FETCH_TIMEOUT = 5   # number of seconds to wait
MIN_TIME = 15       # minimum time between consequent queries


async def fetch(session, url, name):
    """ GET request via aiohttp, returns JSON """
    try:
        start = time.time()
        with async_timeout.timeout(FETCH_TIMEOUT):
            async with session.get(url) as response:
                response_json = await response.json(content_type=None)
                return name, response_json, time.time() - start
    except asyncio.TimeoutError:
        return name, None, 'timeout'
    except:
        return name, None, 'json'


async def collect_data(urls, names):
    """ creates aiohttp session and waits till all requests are done """
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url, name) for url, name in zip(urls, names)]
        return await asyncio.gather(*tasks)


def process_responses(responses, conf, syms, limit):
    bids = []
    asks = []
    d = {
        'amount': 0,
        'amount_points': [],
        'optimal_point': {
            'amount': 0,
            'profit': 0
        },
        'profit': 0,
        'profit_points': [],
        'ticker': [],
        'orders': {'bids': {}, 'asks': {}},
        'trade_cnt': 0
    }
    time_data = {}

    for response in responses:
        exch = response[0]
        data = response[1]
        timestamp = response[2]
        if data is not None:
            try:
                #try:
                price_ix = conf[exch]['fields']['price']
                volume_ix = conf[exch]['fields']['volume']
                path = conf[exch]["path"]
                sym = syms[exch]
                # extract orders for current exchange
                current_bids = data
                for x in path["bids"]:
                    if x == "{}":
                        x = x.format(sym)
                    current_bids = current_bids[x]
                current_asks = data
                for x in path["asks"]:
                    if x == "{}":
                        x = x.format(sym)
                    current_asks = current_asks[x]

                # add current orders to bids and asks arrays
                for i in range(min(limit, len(current_bids))):
                    bids.append([float(current_bids[i][price_ix]), float(current_bids[i][volume_ix]), exch, float(current_bids[i][price_ix])])

                for i in range(min(limit, len(current_asks))):
                    asks.append([float(current_asks[i][price_ix]), float(current_asks[i][volume_ix]), exch, float(current_asks[i][price_ix])])

                tmp = {'ask': float(current_asks[0][price_ix]), 'bid': float(current_bids[0][price_ix]), 'exchange': exch}
                d['ticker'].append(tmp)
                time_data[exch] = timestamp
            except Exception as e: # Some error occurred while parsing json response for current exchange
                # print(exch, type(e), int(time.time()))
                # pprint(data)
                # print()
                tmp = {'ask': 0, 'bid': 0, 'exchange': exch}
                d['ticker'].append(tmp)
                time_data[exch] = 'fields'
        else:  # Some error occurred while making HTTP request for current exchange
            # print(exch, "didn't respond", int(time.time()))
            # print()
            tmp = {'ask': 0, 'bid': 0, 'exchange': exch}
            d['ticker'].append(tmp)
            time_data[exch] = timestamp
    for bid in bids:
        if 'fee' in conf[bid[2]].keys():
            alpha = conf[bid[2]]['fee']
        else:
            alpha = 0.0
        bid[0] *= (1 - alpha)
    for ask in asks:
        if 'fee' in conf[ask[2]].keys():
            alpha = conf[ask[2]]['fee']
        else:
            alpha = 0.0
        ask[0] *= (1 + alpha)
    if  len(bids) > 0  and  len(asks) > 0:
        bids.sort(key = lambda quadriple: quadriple[0], reverse = True)   # bids sorted in descending order by price
        asks.sort(key = lambda quadriple: quadriple[0])                   # asks sorted in ascending order by price

    for x in d['ticker']:
        if 'fee' in conf[x['exchange']].keys():
            alpha = conf[x['exchange']]['fee']
        else:
            alpha = 0.0
        x['bid'] = float(x['bid']) * (1 - alpha)
        x['ask'] = float(x['ask']) * (1 + alpha)

    return bids, asks, d, time_data


def make_logging_entry(bids, asks, d):
    bx = 0
    ax = 0
    bid_count = len(bids)
    ask_count = len(asks)
    profit = 0
    amount = 0
    trade_cnt = 0
    profit_points = []
    amount_points = []
    alpha = 0.1
    prev_profit = 0
    prev_amount = 0
    optimal_amount = 0
    optimal_profit = 0
    num = 0
    bid_orders = {}
    ask_orders = {}

    ok = True

    while bx < bid_count and ax < ask_count and bids[bx][0] > asks[ax][0]:
        ask_price = asks[ax][0]
        bid_price = bids[bx][0]
        bid_vol = bids[bx][1]
        ask_vol = asks[ax][1]
        ask_exch = asks[ax][2]  # BID: base -> quote
        bid_exch = bids[bx][2]  # ASK: quote -> base
        ask_price_real = asks[ax][3]
        bid_price_real = bids[bx][3]

        if bid_vol == 0:
            bx += 1
            continue
        if ask_vol == 0:
            ax += 1
            continue

        if ask_price == 0:
            ax += 1
            continue
        if bid_price == 0:
            bx += 1
            continue


        m = min(ask_vol, bid_vol)  # current micro-trade volume
        current_profit = (bid_price - ask_price) * m  # current micro-trade profit
        profit = prev_profit + current_profit
        amount = prev_amount + ask_price * m
        profit_points.append(profit)
        amount_points.append(amount)
        bids[bx][1] -= m
        asks[ax][1] -= m
        trade_cnt += 1

        num += 1
        if num == 1:
            prev_amount = amount
            prev_profit = profit
        elif num == 2:
            first_k = (profit - prev_profit) / (amount - prev_amount)
            prev_amount = amount
            prev_profit = profit
        else:
            k = (profit - prev_profit) / (amount - prev_amount)
            if k >= alpha * first_k:
                optimal_amount = amount
                optimal_profit = profit
            else:
                ok = False
            if ok:
                if bid_exch in bid_orders:
                    bid_orders[bid_exch][0] = min(bid_orders[bid_exch][0], bid_price_real)
                    bid_orders[bid_exch][1] += m
                else:
                    bid_orders[bid_exch] = [bid_price_real, m]

                if ask_exch in ask_orders:
                    ask_orders[ask_exch][0] = max(ask_orders[ask_exch][0], ask_price_real)
                    ask_orders[ask_exch][1] += m
                else:
                    ask_orders[ask_exch] = [ask_price_real, m]
            prev_amount = amount
            prev_profit = profit
    d['profit'] = profit
    d['amount'] = amount
    d['trade_cnt'] = trade_cnt
    d['optimal_point']['amount'] = optimal_amount
    d['optimal_point']['profit'] = optimal_profit
    d['amount_points'] = amount_points
    d['profit_points'] = profit_points
    d['orders']['bids'] = bid_orders
    d['orders']['asks'] = ask_orders


def collector(conf, urls, names, syms, limit, symbol):
    loop = asyncio.get_event_loop()
    responses = loop.run_until_complete(collect_data(urls, names))

    timestamp = int(time.time() * 1000)
    bids, asks, d, time_data = process_responses(responses, conf, syms, limit)
    make_logging_entry(bids, asks, d)
    d['timestamp'] = timestamp
    time_data['timestamp'] = timestamp

    # DATABASE

    file = symbol + '.json'
    records = {}
    records[symbol] = d

    file_write = open(file, 'w')
    json.dump(records, file_write)
    file_write.close()



def run_logger(symbol, limit, config_file, clear=False):
#    print("\t I've started!")
    try:
        conf = json.load(open(config_file))    # load configuration file
        urls = []
        names = []
        syms = dict()
        for exch in conf.keys():
            if exch != 'livecoin' and exch != 'lakebtc' and exch != 'coinsbank':
                try:    # get exchange's symbol for user's symbol
                    sym = conf[exch]["converter"][symbol]
                    syms[exch] = sym
                    urls.append(conf[exch]["url"].format(sym, limit))
                    names.append(exch)
                except KeyError:
                    pass
        if len(names) == 0:
            print("\tERROR")
            print("No exchange supports given symbol")
            exit(1)


        # # DATABASE
        # client = pymongo.MongoClient(mongo_path)  # defaults to port 27017
        # db = client[db_name]
        # logfile = db['log_' + symbol]
        # techfile = db['tech_' + symbol]
        # if clear:
        #     logfile.drop()
        #     techfile.drop()

        try:
            start_time = time.time()
            collector(conf, urls, names, syms, limit, symbol)
            time_taken = time.time() - start_time
        except Exception as e:
            print(e)


    except FileNotFoundError:
        print("\t ERROR")
        print("No such file", config_file)
        exit(1)
    except json.JSONDecodeError as e:
        print("\t ERROR")
        print("File {} doesn't seem to be a valid JSON document".format(config_file))
        print("Error occurred on line {}, column {}".format(e.lineno, e.colno))
        print(e.msg)
        exit(1)

args = sys.argv;
print(args, args[1], args[2])
config_file = 'orders_config.json'
logfile = args[1] + '.json'
run_logger(args[1], int(args[2]), config_file)
