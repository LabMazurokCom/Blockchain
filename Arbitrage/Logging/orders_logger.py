import argparse
import aiohttp
import asyncio
import async_timeout
import json
import os
import requests
import time
from pprint import pprint


FETCH_TIMEOUT = 5   # number of seconds to wait


async def fetch(session, url, name):
    """ GET request via aiohttp, returns JSON """
    with async_timeout.timeout(FETCH_TIMEOUT):
        async with session.get(url) as response:
            start = time.time()
            response_json = await response.json(content_type=None)
            # print(name, '{:.8f}'.format(time.time() - start))
            return name, response_json


async def collect_data(loop, urls, names):
    """ creates aiohttp session and waits till all requests are done """
    async with aiohttp.ClientSession(loop=loop) as session:
        tasks = [fetch(session, url, name) for url, name in zip(urls, names)]
        return await asyncio.gather(*tasks)


def collector(conf, urls, names, syms, limit):
    loop = asyncio.get_event_loop()
    responses = loop.run_until_complete(collect_data(loop, urls, names))
    bids = []
    asks = []
    for response in responses:
        exch = response[0]
        data = response[1]
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

        for i in range(min(limit, len(current_bids))):
            bids.append((float(current_bids[i][0]), float(current_bids[i][1]), exch))
        for i in range(min(limit, len(current_asks))):
            asks.append((float(current_asks[i][0]), float(current_asks[i][1]), exch))
    bids.sort(key = lambda triple: triple[0], reverse = True)   # bids sorted in descending order by price
    asks.sort(key = lambda triple: triple[0])                   # asks sorted in ascending order by price
    '''
        if exch == "cex":
            r = {'timestamp': 1523977930, 'bids': [[8086.0, 0.36205], [8085.8, 0.29]], 'asks': [[8083.0, 0.36565009], [8075.6, 0.3]]}
        elif exch == "binance":
            r = {'lastUpdateID': 1027024, 'bids': ["4.00000000", "431.00000000", []], 'asks': ["4.00000200", "12.00000000", []]}
        elif exch == "exmo":
            r = {'BTC_USD': {'timestamp': 1523977930, 'bid': [[8086.0, 0.36205], [8085.8, 0.29]], 'ask': [[8083.0, 0.36565009], [8075.6, 0.3]]}}
    '''
    '''
        with open("test_bids.txt", "w") as bids_file, open("test_asks.txt", "w") as asks_file:
    '''


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
    args = parser.parse_args(['-l', '50', 'btc_usd'])


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
            while i > -1:
                i += 1
                start = time.time()
                collector(conf, urls, names, syms, limit)
                print('{:.4f}'.format(time.time() - start))
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
        print(e)
        exit(1)
