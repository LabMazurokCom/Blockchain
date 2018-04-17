import argparse
import json
import requests
from pprint import pprint


"""
        Calling examples:
    python orders_logger.py -h                                      # help
    python orders_logger.py btc_usd                                 # currency pair is the only required argument
    python orders_logger -c "my_new_config.json" btc_usd            # pass configuration file
    python orders_logger -l 10 btc_usd                              # pass number of top orders to be processed
    python orders_logger.py -c "config.json" -l 10 tc_usd           # pass all available arguments       
"""


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
                    help="how many top orders should be processed (default: 50)")
parser.add_argument('symbol',
                    help="currency pair")
args = parser.parse_args(['btc_usd'])

symbol = args.symbol
limit = args.limit

# Access to argumets' values: args.config, args.limit, args.symbol
if (args.limit < 1  or  args.limit > 50):
    print('limit must be an integer between 1 and 50 (inclusively)')
    exit(1)
try:
    with open("log_" + symbol + '.txt', 'a') as log_file, \
            open("last_" + symbol + '.txt', 'w') as last_file:
        conf = json.load(open(args.config))    # load configuration file
        cnt = 0
        for exch in conf.keys():
            try:    # get exchange's symbol for user's symbol
                sym = conf[exch]["converter"][symbol]
                cnt += 1
                url = conf[exch]["url"].format(sym, limit)
                r = requests.get(url).json()
    #            if exch == "cex":
    #                r = {'timestamp': 1523977930, 'bids': [[8086.0, 0.36205], [8085.8, 0.29]], 'asks': [[8083.0, 0.36565009], [8075.6, 0.3]]}
    #            elif exch == "exmo":
    #                r = {'BTC_USD': {'timestamp': 1523977930, 'bid': [[8086.0, 0.36205], [8085.8, 0.29]], 'ask': [[8083.0, 0.36565009], [8075.6, 0.3]]}}
                with open("test_bids.txt", "w") as bids_file, open("test_asks.txt", "w") as asks_file:
                    bids = r
                    for x in conf[exch]["path"]["bids"]:
                        if x == "{}":
                            x = x.format(sym)
                        bids = bids[x]
                    asks = r
                    for x in conf[exch]["path"]["asks"]:
                        if x == "{}":
                            x = x.format(sym)
                        asks = asks[x]
            except KeyError:
                pass
    if (cnt == 0):
        print("\tERROR")
        print("No exchange supports given symbol")
        exit(1)
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
