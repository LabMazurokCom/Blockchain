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
import pymongo
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
                    bids.append([float(current_bids[i][price_ix]), float(current_bids[i][volume_ix]), exch])
                for i in range(min(limit, len(current_asks))):
                    asks.append([float(current_asks[i][price_ix]), float(current_asks[i][volume_ix]), exch])
                tmp = {'ask': current_asks[0][price_ix], 'bid': current_bids[0][price_ix], 'exchange': exch}
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


def collector(conf, urls, names, syms, limit, logfile, techfile):
    loop = asyncio.get_event_loop()
    responses = loop.run_until_complete(collect_data(urls, names))

    timestamp = int(time.time() * 1000)
    bids, asks, d, time_data = process_responses(responses, conf, syms, limit)
    make_logging_entry(bids, asks, d)
    d['timestamp'] = timestamp
    time_data['timestamp'] = timestamp

    # DATABASE
    logfile.insert_one(d)
    techfile.insert_one(time_data)


def run_logger(symbol, limit, config_file, mongo_path, db_name, clear=False):
    try:
        conf = json.load(open(config_file))    # load configuration file
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


        # DATABASE
        client = pymongo.MongoClient(mongo_path)  # defaults to port 27017
        db = client[db_name]
        logfile = db['log_' + symbol]
        techfile = db['tech_' + symbol]
        if clear:
            logfile.drop()
            techfile.drop()


        while True:
            try:
                start_time = time.time()
                collector(conf, urls, names, syms, limit, logfile, techfile)
                time_taken = time.time() - start_time
                if time_taken < MIN_TIME:
                    time.sleep(MIN_TIME - time_taken)
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
