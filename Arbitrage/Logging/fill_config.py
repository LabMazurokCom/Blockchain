import csv
import json
from pprint import pprint

exchanges = ['binance', 'bitstamp', 'cex', 'exmo', 'gdax', 'kucoin']
conf = json.load(open('orders_config.json'))    # load configuration file
for exch in exchanges:
    with open(exch + '_symbols.txt') as infile:
        reader = csv.reader(infile)
        for row in reader:
            exch_pair = row[0]
            from_sym = row[1]
            to_sym = row[2]
            our_pair = from_sym.lower() + '_' + to_sym.lower()
            conf[exch]['converter'][our_pair] = exch_pair

with open('orders_config.json', 'w') as outfile:
    json.dump(conf, outfile, indent=4, sort_keys=True)
print('OK')