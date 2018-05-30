import initialization as ini
import exchs_data
import matching
import json
import random
from pprint import pprint

botconf = json.load(open('bot_config.json'))

pairs = botconf['symbols']
limit = botconf['limit']
conffile = botconf['config_file']
exchsfile = botconf['exchs_credentials']

exchs, minvolumes = ini.init(pairs, conffile, exchsfile)

while True:

    balances = ini.get_balances(pairs, conffile)
    order_books = exchs_data.get_order_books(pairs, limit, conffile)
    for key in balances.keys():
        for kkey in balances[key].keys():
            balances[key][kkey] = random.randint(0, 10000)
    pprint(balances)
    our_orders = matching.get_arb_opp(order_books, balances)
    pprint(our_orders)

    break





