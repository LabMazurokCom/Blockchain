import initialization as ini
import exchs_data
import matching
import json
import random
from pprint import pprint
import requests


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



botconf = json.load(open('bot_config.json'))
pairs = botconf['symbols']
limit = botconf['limit']
conffile = botconf['config_file']
exchsfile = botconf['exchs_credentials']

exchs, minvolumes = ini.init(pairs, conffile, exchsfile)
currency_list = set()
for pair in pairs:
    for cur in pair.split('_'):
        currency_list.add(cur)


while True:
    balances = ini.get_balances(pairs, conffile)
    total_balance = {cur: 0 for cur in currency_list}
    for cur in currency_list:
        for exch in balances.keys():
            total_balance[cur] += balances[exch][cur]
    order_books = exchs_data.get_order_books(pairs, limit, conffile)
    our_orders = matching.get_arb_opp(order_books, balances)
    best, orders = get_best(our_orders, total_balance)
    break
