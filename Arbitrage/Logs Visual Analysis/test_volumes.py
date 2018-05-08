#!/usr/bin/python3

import aiohttp
import asyncio
import async_timeout
import argparse
import json
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


def process_responses(responses, conf, syms, limit, bid_orders, ask_orders, timestamp):
    bids = []
    asks = []

    for response in responses:
        exch = response[0]
        data = response[1]
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


                # test volumes
                if exch in bid_orders:
                    bid_price = bid_orders[exch][0]
                    bid_volume = bid_orders[exch][1]
                if exch in ask_orders:
                    ask_price = ask_orders[exch][0]
                    ask_volume = ask_orders[exch][1]


                # add current orders to bids and asks arrays
                for i in range(min(limit, len(current_bids))):
                    if exch == 'bitfinex':
                        cur_bid_price = float(current_bids[i]['price'])
                        cur_bid_volume = float(current_bids[i]['amount'])
                    elif exch == 'bittrex':
                        cur_bid_price = float(current_bids[i]['Rate'])
                        cur_bid_volume = float(current_bids[i]['Quantity'])
                    else:
                        cur_bid_price = float(current_bids[i][0])
                        cur_bid_volume = float(current_bids[i][1])
                    bids.append([cur_bid_price, cur_bid_volume, exch])
                    if exch in bid_orders:
                        if cur_bid_price >= bid_price:
                            bid_volume -= cur_bid_volume

                for i in range(min(limit, len(current_asks))):
                    if exch == 'bitfinex':
                        cur_ask_price = float(current_asks[i]['price'])
                        cur_ask_volume = float(current_asks[i]['amount'])
                    elif exch == 'bittrex':
                        cur_ask_price = float(current_asks[i]['Rate'])
                        cur_ask_volume = float(current_asks[i]['Quantity'])
                    else:
                        cur_ask_price = float(current_asks[i][0])
                        cur_ask_volume = float(current_asks[i][1])
                    asks.append([cur_ask_price, cur_ask_volume, exch])
                    if exch in ask_orders:
                        if cur_ask_price <= ask_price:
                            ask_volume -= cur_ask_volume

                if exch in bid_orders:
                    print(exch, 'bid')
                    with open(exch + '_bid_vol.csv', 'a') as f:
                        print('{},{}'.format(timestamp, max(0, bid_volume) / bid_volume)) #, file=f)
                if exch in ask_orders:
                    print(exch, 'ask')
                    with open(exch + '_ask_vol.csv', 'a') as f:
                        print('{},{}'.format(timestamp, max(0, ask_volume) / ask_volume), file=f)
            except:  # Some error occurred while parsing json response for current exchange
                pass
    if  len(bids) > 0  and  len(asks) > 0:
        bids.sort(key = lambda triple: triple[0], reverse = True)   # bids sorted in descending order by price
        asks.sort(key = lambda triple: triple[0])                   # asks sorted in ascending order by price
    return bids, asks


def generate_orders(bids, asks):
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
            if k / first_k < alpha:
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

    return bid_orders, ask_orders


def collector(conf, urls, names, syms, limit, bid_orders, ask_orders):
    loop = asyncio.get_event_loop()
    responses = loop.run_until_complete(collect_data(urls, names))
    timestamp = int(time.time() * 1000)
    bids, asks = process_responses(responses, conf, syms, limit, bid_orders, ask_orders, timestamp)
    return generate_orders(bids, asks)


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
    args = parser.parse_args(['-l', '50', '-c', 'orders_config.json', 'btc_usd'])


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

        bid_orders = []
        ask_orders = []
        i = 0
        while True:
            try:
                bid_orders, ask_orders = collector(conf, urls, names, syms, limit, bid_orders, ask_orders)
            except Exception as e:
                print(e)
            time.sleep(3)
            i += 1
            if i == 3:
                break

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