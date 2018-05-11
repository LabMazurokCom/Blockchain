#!/usr/bin/python3
import requests
import argparse
from pprint import pprint
from time import sleep

def get_ticker(sym_pair, init=False):
    url = 'https://arbitrage-logger.firebaseio.com/log_{}.json?orderBy="$key"&limitToLast=1'.format(sym_pair)
    while True:
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            for t, val in data.items():
                ticker = data[t]['ticker']
                for x in ticker:
                    exch = x['exchange']
                    bid = x['bid']
                    ask = x['ask']
                    if bid != 0.0 and ask != 0.0:
                        if init == True:
                            with open(exch + '_' + sym_pair + '.csv', 'w') as f:
                                print('time,bid,ask', file=f)
                                print('{},{},{}'.format(t, bid, ask), file=f)
                        else:
                            with open(exch + '_' + sym_pair + '.csv', 'a') as f:
                                print('{},{},{}'.format(t, bid, ask), file=f)
                init = False
            sleep(3)

if __name__ == "__main__":
    # Parsing command line arguments
    parser = argparse.ArgumentParser(prog="python get_ticker.py")
    parser.add_argument('-i', '--init',
                        type=bool,
                        default=False,
                        required=False,
                        help="if True, creates new files with given pair of symbols for every exchange")
    parser.add_argument('symbol',
                        help="currency pair")
    args = parser.parse_args(['-i', 'True', 'btc_usd'])
    get_ticker(args.symbol, init=args.init)