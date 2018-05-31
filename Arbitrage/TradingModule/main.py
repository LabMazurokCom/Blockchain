import initialization as ini
import exchs_data
import matching
import json
import random
from pprint import pprint
import requests

def get_best(our_orders):

    profit = 0
    best_pair = ''
    for pair in our_orders.keys():
        if(our_orders[pair]['profit'] > profit):
            profit = our_orders[pair]['profit']
            best_pair = pair

    return best_pair, our_orders[best_pair]


botconf = json.load(open('bot_config.json'))

pairs = botconf['symbols']
limit = botconf['limit']
conffile = botconf['config_file']
exchsfile = botconf['exchs_credentials']

exchs, minvolumes = ini.init(pairs, conffile, exchsfile)

while True:

    balances = ini.get_balances(pairs, conffile)
    order_books = exchs_data.get_order_books(pairs, limit, conffile)
    our_orders = matching.get_arb_opp(order_books, balances)
    pprint(our_orders)
    best, orders = get_best(our_orders)
    pprint(best)
    pprint(orders)
    break

