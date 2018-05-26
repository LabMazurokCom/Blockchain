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
from collections import deque
import exchange
import cex
import exmo
import configs as cf
import requests
import copy

FETCH_TIMEOUT = 5  # number of seconds to wait
MAX_ENTRIES = 200  # maximum allowed number of entries in DB

#cex = cex.CEX(cf.cex_endpoint, cf.cex_api_key, cf.cex_api_secret, cf.cex_id)
#exmo = exmo.EXMO(cf.exmo_endpoint, cf.exmo_api_key, cf.exmo_api_secret)

async def fetch(session, url, name, pair):
    """ GET request via aiohttp, returns JSON """
    try:
        start = time.time()
        with async_timeout.timeout(FETCH_TIMEOUT):
            async with session.get(url) as response:
                response_json = await response.json(content_type=None)
                return name, pair, response_json, time.time() - start
    except asyncio.TimeoutError:
        return name, pair, None, 'timeout'
    except:
        return name, pair, None, 'json'


async def collect_data(pairs):
    """ creates aiohttp session and waits till all requests are done """
    async with aiohttp.ClientSession() as session:
        tasks = []
        for p in pairs.keys():
            for url, name in zip(pairs[p]['urls'], pairs[p]['names']):
                tasks.append(fetch(session, url, name, p))
        return await asyncio.gather(*tasks)


def process_responses(responses, conf, syms, limit):
    order_books = dict()
    #bids = []
    #asks = []
    d = {
        'orders': {'bids': [], 'asks': []}
    }
    time_data = {}

    for sym in syms.keys():
        order_books[sym] = dict()
        order_books[sym] = copy.deepcopy(d)

    for response in responses:
        #response format: exch_name, pair, data, time
        exch = response[0]
        pair = response[1]
        data = response[2]
        timestamp = response[3]
        if data is not None:
            try:
                price_ix = conf[exch]['fields']['price']
                volume_ix = conf[exch]['fields']['volume']
                path = conf[exch]["path"]
                sym = conf[exch]['converter'][pair]
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
                    order_books[pair]['orders']['bids'].append([float(current_bids[i][price_ix]), float(current_bids[i][volume_ix]), exch])
                for i in range(min(limit, len(current_asks))):
                    order_books[pair]['orders']['asks'].append([float(current_asks[i][price_ix]), float(current_asks[i][volume_ix]), exch])
                #tmp = {'ask': current_asks[0][price_ix], 'bid': current_bids[0][price_ix], 'exchange': exch}
                #d['ticker'].append(tmp)
                time_data[exch] = timestamp
            except:  # Some error occurred while parsing json response for current exchange
                #tmp = {'ask': 0, 'bid': 0, 'exchange': exch}
                #d['ticker'].append(tmp)
                time_data[exch] = 'fields'
        else:  # Some error occurred while making HTTP request for current exchange
            #tmp = {'ask': 0, 'bid': 0, 'exchange': exch}
            #d['ticker'].append(tmp)
            time_data[exch] = timestamp
    for pair in order_books.keys():
        if len(order_books[pair]['orders']['bids']) > 0 and len(order_books[pair]['orders']['asks']) > 0:
            order_books[pair]['orders']['bids'].sort(key=lambda triple: triple[0], reverse=True)  # bids sorted in descending order by price
            order_books[pair]['orders']['asks'].sort(key=lambda triple: triple[0])  # asks sorted in ascending order by price
    return order_books, time_data


def make_logging_entry(order_books):
    orders = dict()
    for pair in order_books.keys():
        orders[pair] = dict()
        bx = 0
        ax = 0
        d = order_books[pair]
        bids = order_books[pair]['orders']['bids']
        asks = order_books[pair]['orders']['asks']
        bid_count = len(bids)
        ask_count = len(asks)
        profit = 0
        amount = 0
        '''
        trade_cnt = 0
        profit_points = []
        amount_points = []
        '''
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
            #profit_points.append(profit)
            #amount_points.append(amount)
            bids[bx][1] -= m
            asks[ax][1] -= m
            #trade_cnt += 1

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
        '''
        
        MOVE TO OTHER FUNCTION
        
        **********************
                
        keys_to_delete = []
        for x in bid_orders.keys():
            if bid_orders[x][1] < cur_limits[x][0]:
                keys_to_delete.append(x)
        for x in keys_to_delete:
            del bid_orders[x]
        keys_to_delete = []
        for x in ask_orders.keys():
            if(ask_orders[x][1] < cur_limits[x][0]):
                keys_to_delete.append(x)
        for x in keys_to_delete:
            del ask_orders[x]
        '''

        d['optimal_point'] = dict()

        d['profit'] = profit
        d['amount'] = amount
        #d['trade_cnt'] = trade_cnt
        d['optimal_point']['amount'] = optimal_amount
        d['optimal_point']['profit'] = optimal_profit
        #d['amount_points'] = amount_points
        #d['profit_points'] = profit_points
        d['orders']['bids'] = bid_orders
        d['orders']['asks'] = ask_orders

        orders[pair] = d

    return orders


def collector(conf, pairs, limit, logfile, techfile, db):
    loop = asyncio.get_event_loop()
    responses = loop.run_until_complete(collect_data(pairs))
    timestamp = int(time.time() * 1000)
    order_books, time_data = process_responses(responses, conf, pairs, limit)
    d = make_logging_entry(order_books)
    db.child(logfile).child(timestamp).set(d)
    db.child(techfile).child(timestamp).set(time_data)
    return timestamp, d



def run():
#if __name__ == "__main__":
    # Parsing command line arguments
    '''
    parser = argparse.ArgumentParser(prog="python orders_logger.py",
                                     epilog="See wiki on Github for additional information")
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
    args = parser.parse_args()  # (['-l', '5', '-c', 'orders_config.json', 'eos_btc'])

    '''
    # Access to arguments' values: args.config, args.limit, args.symbol

    botconf = json.load(open('bot_config.json'))

    symbols = botconf['symbols']
    limit = botconf['limit']
    conffile = botconf['config_file']
    pairs = dict()

    badsyms = 0

    try:
        conf = json.load(open(conffile))  # load configuration file
        for symbol in symbols:
            urls = []
            names = []
            syms = dict()
            for exch in conf.keys():
                try:  # get exchange's symbol for user's symbol
                    sym = conf[exch]["converter"][symbol]
                    syms[exch] = sym
                    urls.append(conf[exch]["url"].format(sym, limit))
                    names.append(exch)
                except KeyError:
                    pass
            if len(names) == 0:
                print("\tERROR")
                print("No exchange supports symbol {}".format(symbol))
                badsyms += 1
            else:
                pairs[symbol] = dict()

                pairs[symbol]['urls'] = copy.deepcopy(urls)
                pairs[symbol]['names'] = copy.deepcopy(names)

        if badsyms == len(symbols):
            print("\tERROR")
            print("None of given symbols are supported on any exchanges")
            exit(1)
        '''
        config = {
            "apiKey": "AIzaSyBbUk_Lo0mDuCvAiocniFGCJCsIlwd6Kew",
            "authDomain": "arb-log.firebaseapp.com",
            "databaseURL": "https://arb-log.firebaseio.com",
            "storageBucket": "arb-log.appspot.com",
            "serviceAccount": "firebase_config.json"
        }
        '''
        config = {
            "apiKey": "AIzaSyBqm0oupQb8NFPBCtPv1ZR5exdEsZ9wcyI",
            "authDomain": "test-36f7a.firebaseapp.com",
            "databaseURL": "https://test-36f7a.firebaseio.com",
            "storageBucket": "test-36f7a.appspot.com",
            "serviceAccount": "test_firebase_config.json"
        }

        logfile = 'log_' + 'all' #symbol
        techfile = 'tech_' + 'all' #symbol
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()
        db.child(logfile).remove()
        db.child(techfile).remove()

        last_keys = deque()

        #while True:
        try:
            firebase = pyrebase.initialize_app(config)
            db = firebase.database()
            '''
            best_orders = {
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
            '''
            ts, orders = collector(conf, pairs, limit, logfile, techfile, db)
            pprint(orders)
            last_keys.append(ts)
            #if orders['profit']/orders['amount'] > best_orders['profit']/best_orders['amount']:
            #   best_orders = orders
            if len(last_keys) == MAX_ENTRIES + 1:
                first_key = last_keys.popleft()
                db.child(logfile).child(first_key).remove()
                db.child(techfile).child(first_key).remove()
            #return best_orders
        except Exception as e:
            timestamp = int(time.time())
            #db.child(techfile).child(timestamp).set({'error': str(e)})
            print(timestamp)
            print(e)



    except FileNotFoundError as e:
        print("\t ERROR")
        print("No such file", conffile)
        exit(1)
    except json.JSONDecodeError as e:
        print("\t ERROR")
        print("File {} doesn't seem to be a valid JSON document".format(conffile))
        print("Error occurred on line {}, column {}".format(e.lineno, e.colno))
        print(e.msg)
        exit(1)

run()
