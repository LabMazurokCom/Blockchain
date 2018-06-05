import initialization as ini
import exchs_data
import matching
import json
from pprint import pprint
import requests
import trading
import time


def get_best(our_orders, total_balance):
    best_coeff = 0.0
    best_pair = ''
    for pair in our_orders.keys():
        quote_cur = pair.split('_')[1]
        q = our_orders[pair]['profit'] / total_balance[quote_cur]
        if q > best_coeff:
            best_coeff = q
            best_pair = pair
    return best_pair, our_orders[best_pair]


def get_json_from_file(file_path):
    try:
        return json.load(open(file_path))
    except FileNotFoundError:
        print("File {} not found".format(file_path))
    except json.JSONDecodeError as e:
        print("File {} is not a valid JSON file")
        print(e)
    except Exception as e:
        print("Some error occurred while parsing {}".format(file_path))
        print(type(e))
        print(e)


botconf = get_json_from_file('bot_config.json')
if botconf is None:
    exit(1)
try:
    pairs = botconf['symbols']
    limit = botconf['limit']
    conffile = get_json_from_file(botconf['config_file'])
    exchsfile = get_json_from_file(botconf['exchs_credentials'])
except KeyError:
    print("Some of bot_config.json's required keys are not set")
    exit(1)
exchs, minvolumes = ini.init(pairs, conffile, exchsfile)


currency_list = set()
for pair in pairs:
    for cur in pair.split('_'):
        currency_list.add(cur)


counter = 0


with open('responses.txt', 'a') as respfile:
    while True:
        counter += 1
        if counter == 100:
            exchs, minvolumes = ini.init(pairs, conffile, exchsfile)
            counter = 0
            if len(exchs) <= 1:
                time.sleep(60)
                continue
        try:
            balances = ini.get_balances(pairs, conffile)
            #balances = {'binance': {'bch': 0.0, 'eth': 0.0, 'usd': 0.0, 'dash': 0.0, 'xrp': 0.0, 'btc': 0.0, 'usdt': 0.0}, 'bitfinex': {'bch': 0.0, 'eth': 0.0, 'usd': 0.0, 'dash': 0.0, 'xrp': 0.0, 'btc': 0.0, 'usdt': 0.0}, 'bitstamp': {'bch': 0.0, 'eth': 0.0, 'usd': 0.0, 'dash': 0.0, 'xrp': 0.0, 'btc': 0.0, 'usdt': 0.0}, 'bittrex': {'bch': 0.0, 'eth': 0.0, 'usd': 0.0, 'dash': 0.0, 'xrp': 0.0, 'btc': 0.0, 'usdt': 0.0}, 'cex': {'bch': 0.0, 'eth': 0.0, 'usd': 0.0, 'dash': 0.0, 'xrp': 0.0, 'btc': 0.002, 'usdt': 0.0}, 'cryptopia': {'bch': 0.0, 'eth': 0.0, 'usd': 0.0, 'dash': 0.0, 'xrp': 0.0, 'btc': 0.0, 'usdt': 0.0}, 'exmo': {'bch': 0.0, 'eth': 0.0, 'usd': 73.39, 'dash': 0.0, 'xrp': 0.0, 'btc': 0.0, 'usdt': 0.0}, 'gdax': {'bch': 0.0, 'eth': 0.0, 'usd': 0.0, 'dash': 0.0, 'xrp': 0.0, 'btc': 0.0, 'usdt': 0.0}, 'kraken': {'bch': 8.39e-06, 'eth': 3.06e-06, 'usd': 0.0, 'dash': 0.0, 'xrp': 3.86e-06, 'btc': 6.922e-06, 'usdt': 150.0}, 'kucoin': {'bch': 0.0, 'eth': 0.0, 'usd': 0.0, 'dash': 0.0, 'xrp': 0.0, 'btc': 0.0, 'usdt': 0.0}, 'poloniex': {'bch': 0.0, 'eth': 0.0, 'usd': 0.0, 'dash': 0.0, 'xrp': 0.0, 'btc': 0.0, 'usdt': 0.0}}

            #pprint(balances)
            total_balance = {cur: 0 for cur in currency_list}
            for cur in currency_list:
                for exch in balances.keys():
                    total_balance[cur] += balances[exch][cur]

            order_books = exchs_data.get_order_books(pairs, limit, conffile)
            #pprint(order_books)

            our_orders = matching.get_arb_opp(order_books, balances)
            pprint(our_orders['btc_usd'])
            best, orders = get_best(our_orders, total_balance)
            if(orders['profit'] < 0.0001):
                continue
            # print(best, orders)
            #best = 'btc_usd'
            #orders = {'required_base_amount': 0.01788522, 'required_quote_amount': 132.7579803399024, 'profit': 1.051173937182616, 'buy': {'exmo': [7409, 0.002]}, 'sell': {'cex': [7489, 0.002]}}
            req, res = trading.make_all_orders(best, orders, exchs, conffile)
            print(best) #, file=respfile)
            print(req) #, file=respfile)
            print(res) #, end='\n\n', file=respfile)
            # pprint(req)
            # print()
            # pprint(res)
            time.sleep(30)
        except Exception as e:
            print(type(e))
            print(e)
