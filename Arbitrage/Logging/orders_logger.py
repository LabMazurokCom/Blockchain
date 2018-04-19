import argparse
import aiohttp
import asyncio
import async_timeout
import json
import os
import requests
import time
from pprint import pprint


FETCH_TIMEOUT = 0.5   # number of seconds to wait


async def fetch(session, url, name):
    """ GET request via aiohttp, returns JSON """
    start = time.time()
    try:
        with async_timeout.timeout(FETCH_TIMEOUT):
            if (name == 'binance'):
                await asyncio.sleep(1)
            async with session.get(url) as response:
                response_json = await response.json(content_type=None)
                #print(name, '{:.4f}'.format(time.time() - start))
                return name, response_json
    except:
        return name, None


async def collect_data(urls, names):
    """ creates aiohttp session and waits till all requests are done """
    start = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url, name) for url, name in zip(urls, names)]
        ans = await asyncio.gather(*tasks)
        #print('COLLECTING RESPONSES: {:.4f}'.format(time.time() - start))
        return ans


def collector(conf, urls, names, syms, limit):
    start = time.time()
    loop = asyncio.get_event_loop()
    responses = loop.run_until_complete(collect_data(urls, names))
    bids = []
    asks = []
    d = {
        'amount_points': [],
        'optimal_point': {
            'amount': 0,
            'profit': 0
        },
        'profit': 0,
        'profit_points': [],
        'ticker': [],
        'orders': [],
        'trade_cnt': 0,
        'usd_amount': 0
    }
    with open("log.txt", "w") as log_file, open("last.txt", "w") as last_file, open('test.txt', 'w') as f:
        for response in responses:
            exch = response[0]
            data = response[1]
            print(exch, end='\n', file=f)
            if data is not None:
                try:
                    path = conf[exch]["path"]
                    sym = syms[exch]
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

                    bids = []
                    asks = []
                    for i in range(min(limit, len(current_bids))):
                        bids.append((float(current_bids[i][0]), float(current_bids[i][1]), exch))
                    for i in range(min(limit, len(current_asks))):
                        asks.append((float(current_asks[i][0]), float(current_asks[i][1]), exch))
                    tmp = {'ask': current_asks[0], 'bid': current_bids[0], 'exchange': exch}
                    d['ticker'].append(tmp)
                    print('ASKS: ', asks, end='\n', file=f)
                    print('BIDS: ', bids, end='\n', file=f)
                    print(file=f)
                except:
                    tmp = {'ask': 0, 'bid': 0, 'exchange': exch}
                    d['ticker'].append(tmp)
                    print('ASKS: []', end='\n', file=f)
                    print('BIDS: []', end='\n', file=f)
                    print(file=f)
            else:  # Some error occurred while getting data for current exchange
                tmp = {'ask': 0, 'bid': 0, 'exchange': exch}
                d['ticker'].append(tmp)
                print('ASKS: []', end='\n', file=f)
                print('BIDS: []', end='\n', file=f)
                print(file=f)

        bids.sort(key = lambda triple: triple[0], reverse = True)   # bids sorted in descending order by price
        asks.sort(key = lambda triple: triple[0])                   # asks sorted in ascending order by price
        json.dump(d, last_file, indent=4, sort_keys=True)
        # print('TOTAL: {:.4f}'.format(time.time() - start))


"""
        Calling examples:
    python orders_logger.py -h                                      # help
    python orders_logger.py btc_usd                                 # currency pair is the only required argument
    python orders_logger -c "my_new_config.json" btc_usd            # pass configuration file
    python orders_logger -l 10 btc_usd                              # pass number of top orders to be processed
    python orders_logger.py -c "config.json" -l 10 tc_usd           # pass all available arguments       
"""


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
    args = parser.parse_args(['-l', '5', '-c', 'test_config.json', 'btc_usd'])


    # Access to argumets' values: args.config, args.limit, args.symbol
    symbol = args.symbol
    limit = args.limit


    try:
        with open("log_" + symbol + '.txt', 'a') as log_file, \
                open("last_" + symbol + '.txt', 'w') as last_file:
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
            i = 0
            T = 0
            while i < 1:
                i += 1
                if i % 10 == 0:
                    print('{} / 50'.format(i))
                start = time.time()
                collector(conf, urls, names, syms, limit)
                T += time.time() - start
                #print('{:.4f}'.format(time.time() - start))
            print('{:.4f}'.format(T / 100))
    except FileNotFoundError as e:
        print("\t ERROR")
        print("No such file", args.config)
        exit(1)
    except json.JSONDecodeError as e:
        print("\tERROR")
        print("File {} doesn't seem to be a valid JSON document".format(args.config))
        print("Error occurred on line {}, column {}".format(e.lineno, e.colno))
        print(e.msg)
        exit(1)
    except Exception as e:
        print("\t ERROR")
        print(type(e))
        exit(1)
