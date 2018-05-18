import csv
import json
from pprint import pprint

exchanges = ['binance', 'bitfinex', 'bitstamp', 'bittrex', 'cex', 'cryptopia', 'exmo', 'gdax', 'kraken', 'kucoin', 'poloniex']
conf = json.load(open('orders_config_extended.json'))    # load configuration file
for exch in exchanges:
    with open('symbols/' + exch + '_symbols.txt') as infile:
        reader = csv.reader(infile)
        for row in reader:
            exch_pair = row[0]
            from_sym = row[1]
            to_sym = row[2]
            our_pair = from_sym.lower() + '_' + to_sym.lower()
            conf[exch]['converter'][our_pair] = exch_pair
            our_pair = to_sym.lower() + '_' + from_sym.lower()
            conf[exch]['converter'][our_pair] = exch_pair


with open('orders_config_extended.json', 'w') as outfile:
    json.dump(conf, outfile, indent=4, sort_keys=True)
print('OK')