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


import argparse
import aiohttp
import asyncio
import async_timeout
import json
import pyrebase
import time
from pprint import pprint


FETCH_TIMEOUT = 5   # number of seconds to wait


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
                if exch == 'bitfinex':
                    for i in range(min(limit, len(current_bids))):
                        bids.append([float(current_bids[i]['price']), float(current_bids[i]['amount']), exch])
                    for i in range(min(limit, len(current_asks))):
                        asks.append([float(current_asks[i]['price']), float(current_asks[i]['amount']), exch])
                elif exch == 'bittrex':
                    for i in range(min(limit, len(current_bids))):
                        bids.append([float(current_bids[i]['Rate']), float(current_bids[i]['Quantity']), exch])
                    for i in range(min(limit, len(current_asks))):
                        asks.append([float(current_asks[i]['Rate']), float(current_asks['Quantity'][1]), exch])
                else:
                    for i in range(min(limit, len(current_bids))):
                        bids.append([float(current_bids[i][0]), float(current_bids[i][1]), exch])
                    for i in range(min(limit, len(current_asks))):
                        asks.append([float(current_asks[i][0]), float(current_asks[i][1]), exch])
                # add top bid and ask price to the ticker
                tmp = {'ask': float(current_asks[0][0]), 'bid': float(current_bids[0][0]), 'exchange': exch}
                d['ticker'].append(tmp)
                time_data[exch] = timestamp
            except:  # Some error occurred while parsing json response for current exchange
                tmp = {'ask': 0, 'bid': 0, 'exchange': exch}
                d['ticker'].append(tmp)
                time_data[exch] = 'fields'
        else:  # Some error occurred while making HTTP request for current exchange
            tmp = {'ask': 0, 'bid': 0, 'exchange': exch}
            d['ticker'].append(tmp)
            time_data[exch] = timestamp
    if  len(bids) > 0  and  len(asks) > 0:
        bids.sort(key = lambda triple: triple[0], reverse = True)   # bids sorted in descending order by price
        asks.sort(key = lambda triple: triple[0])                   # asks sorted in ascending order by price
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
    optimal_amount = 0
    optimal_profit = 0
    num = 0
    bid_orders = {}
    ask_orders = {}
    ok = True

    while bx < bid_count and ax < ask_count and bids[bx][0] > asks[ax][0]:
        bid_vol = bids[bx][1]
        ask_vol = asks[ax][1]
        if bid_vol == 0:
            bx += 1
            continue
        if ask_vol == 0:
            ax += 1
            continue

        m = min(bid_vol, ask_vol)
        current_profit = (bids[bx][0] - asks[ax][0]) * m
        profit += current_profit
        amount += asks[ax][0] * m
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
            if k / first_k >= alpha:
                optimal_amount = amount
                optimal_profit = profit
            else:
                ok = False
            if ok:
                bid_exch = bids[bx][2]
                if bid_exch in bid_orders:
                    bid_orders[bid_exch][0] = min(bid_orders[bid_exch][0], bids[bx][0])
                    bid_orders[bid_exch][1] += m
                else:
                    bid_orders[bid_exch] = [bids[bx][0], m]
                ask_exch = asks[ax][2]
                if ask_exch in ask_orders:
                    ask_orders[ask_exch][0] = max(ask_orders[ask_exch][0], asks[ax][0])
                    ask_orders[ask_exch][1] += m
                else:
                    ask_orders[ask_exch] = [asks[ax][0], m]
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


def collector(conf, urls, names, syms, limit, logfile, lastfile, techfile, db):
    loop = asyncio.get_event_loop()
    responses = loop.run_until_complete(collect_data(urls, names))
    timestamp = int(time.time() * 1000)
    bids, asks, d, time_data = process_responses(responses, conf, syms, limit)
    # make_logging_entry(bids, asks, d)
    # db.child(logfile).child(timestamp).set(d)
    # db.child(lastfile).child(timestamp).set(d)
    # db.child(techfile).child(timestamp).set(time_data)


if __name__ == "__main__":
    # Parsing command line arguments
    parser = argparse.ArgumentParser(prog="python orders_logger.py", epilog="See wiki on Github for additional information")
    parser.add_argument('-c', '--config',
                        default='orders_config.json',
                        required=False,
                        help="json configuration file (default: orders_config.json)")
    parser.add_argument('-l', '--limit',
                        type=int,
                        default=50,
                        required=False,
                        choices=[5, 10, 20, 50],
                        help="how many top orders should be processed (default: 50)")
    parser.add_argument('symbol',
                        help="currency pair")
    args = parser.parse_args() #(['-l', '5', '-c', 'orders_config.json', 'btc_usd'])


    # Access to arguments' values: args.config, args.limit, args.symbol
    symbol = args.symbol
    limit = args.limit


    try:
        conf = json.load(open(args.config))    # load configuration file
        urls = []
        names = []
        syms = dict()
        for exch in conf.keys():
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

        config = {
            "apiKey": "AIzaSyBwWAi7siuckIiYrcVz7kN5e17NcIlkhG0",
            "authDomain": "arbitrage-logger.firebaseapp.com",
            "databaseURL": "https://arbitrage-logger.firebaseio.com",
            "storageBucket": "arbitrage-logger.appspot.com",
            "serviceAccount": "firebase_config.json"
        }
        logfile = 'log_' + symbol
        lastfile = 'last_' + symbol
        techfile = 'tech_' + symbol
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()
        # db.child(logfile).remove()
        # db.child(lastfile).remove()
        # db.child(techfile).remove()

        # while True:
        for i in range(1):
            try:
                firebase = pyrebase.initialize_app(config)
                db = firebase.database()
                collector(conf, urls, names, syms, limit, logfile, lastfile, techfile, db)
            except Exception as e:
                timestamp = int(time.time())
                db.child(techfile).child(timestamp).set({'error': str(e)})
                print(e)

    except FileNotFoundError as e:
        print("\t ERROR")
        print("No such file", args.config)
        exit(1)
    except json.JSONDecodeError as e:
        print("\t ERROR")
        print("File {} doesn't seem to be a valid JSON document".format(args.config))
        print("Error occurred on line {}, column {}".format(e.lineno, e.colno))
        print(e.msg)
        exit(1)