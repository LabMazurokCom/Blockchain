import bot_utils
import datetime
import exchs_data
import initialization as ini
import json
import matching
import os
import pymongo
import sys
from pprint import pprint
import trading
import time


File = os.path.basename(__file__)


verbose = True
logfile = open('log.txt', 'a')
old_stdout = sys.stdout
# logfile = sys.stdout
sys.stdout = logfile


def get_best(our_orders, total_balance):
    """
    chooses pair to be traded
    :param our_orders: list of dictionaries with orders for all pairs in form our_orders[pair] = {
                                                                                     'asks': [],
                                                                                     'bids': [],
                                                                                     'required_base_amount': float,
                                                                                     'required_quote_amount': float,
                                                                                     'profit': float
                                                                                 }
    :param total_balance: dictionary with total balance (sum of balances from all exchanges) for each currency
    :return: name of best pair, and dictionary with orders for it
    """
    best_coeff = 0.0
    best_pair = ''
    for pair in our_orders.keys():
        quote_cur = pair.split('_')[1]
        q = our_orders[pair]['profit'] / total_balance[quote_cur]
        if q > best_coeff:
            best_coeff = q
            best_pair = pair
    if best_pair == '':
        return None, None
    else:
        return best_pair, our_orders[best_pair]


def print2console(message, last=False):
    if verbose:
        sys.stdout = old_stdout
        print('\t\t{}, {}'.format(message, datetime.datetime.utcnow()))
        if last:
            print()
        sys.stdout = logfile


def get_json_from_file(file_path):
    """
    extracts JSON from given file
    :param file_path: path to file
    :return: content of file in json format
    """
    try:
        return json.load(open(file_path))
    except FileNotFoundError as e:
        Time = datetime.datetime.utcnow()
        EventType = "Error"
        Function = "get_json_from_file"
        Explanation = "File {} not found".format(file_path)
        EventText = e
        ExceptionType = type(e)
        print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                            ExceptionType))
    except json.JSONDecodeError as e:
        Time = datetime.datetime.utcnow()
        EventType = "JSONDecodeError"
        Function = "get_json_from_file"
        Explanation = "File {} is not a valid JSON file"
        EventText = e
        ExceptionType = type(e)
        print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                            ExceptionType))
    except Exception as e:
        Time = datetime.datetime.utcnow()
        EventType = "Error"
        Function = "get_json_from_file"
        Explanation = "Some error occurred while parsing {}".format(file_path)
        EventText = e
        ExceptionType = type(e)
        print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                            ExceptionType))


print2console('Parsing config file')
botconf = get_json_from_file('bot_config.json')
if botconf is None:
    exit(1)

try:
    pairs = botconf['symbols']
    limit = botconf['limit']
    conffile = get_json_from_file(botconf['config_file'])
    exchsfile = get_json_from_file(botconf['exchs_credentials'])
    exchanges_names = botconf['exchanges']
    auth_string = botconf['auth_string']
    db_name = botconf['database']
except KeyError as e:
    Time = datetime.datetime.utcnow()
    EventType = "KeyError"
    Function = "main"
    Explanation = "Some of bot_config.json's required keys are not set"
    EventText = e
    ExceptionType = type(e)
    print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                        ExceptionType))
    exit(1)
else:
    print2console('Parsing successful', last=True)

print2console('Initialization')
exchs, minvolumes = ini.init(pairs, conffile, exchsfile, exchanges_names)
requests = ini.get_urls(pairs, conffile, limit)

while len(exchs) <= 1:
    time.sleep(60)
    exchs, minvolumes = ini.init(pairs, conffile, exchsfile, exchanges_names)
    continue

currency_list = set()
for pair in pairs:
    for cur in pair.split('_'):
        currency_list.add(cur)
print2console('Initialization successful', last=True)

print2console('Connecting to Mongo')
ok_mongo = False
try:
    client = pymongo.MongoClient(auth_string)
    db = client[db_name]
    ok_mongo = True
except Exception as e:
    ok_mongo = False
    Time = datetime.datetime.utcnow()
    EventType = "Error"
    Function = None
    Explanation = 'Some error occurred while connecting to Mongo before main loop'
    EventText = e
    ExceptionType = type(e)
    print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText, ExceptionType))
else:
    print2console('Connected successfully', last=True)

print2console('Entering the main loop', last=True)
counter = 0
iter = 0
session = (int)(time.time())

while True:
    iter += 1
    print2console('Iteration #{}'.format(iter))
    counter += 1

    if counter == 100:
        print2console('Reinitialization')
        exchs, minvolumes = ini.init(pairs, conffile, exchsfile, exchanges_names)
        requests = ini.get_urls(pairs, conffile, limit)
        try:
            client = pymongo.MongoClient(auth_string)
            db = client[db_name]
            ok_mongo = True
        except Exception as e:
            ok_mongo = False
            Time = datetime.datetime.utcnow()
            EventType = "Error"
            Function = None
            Explanation = 'Some error occurred while connecting to Mongo in main loop'
            EventText = e
            ExceptionType = type(e)
            print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText, ExceptionType))
        if len(exchs) <= 1:
            time.sleep(60)
            print2console('')
            counter = 99
            continue
        counter = 0
        print2console('Reinitialization successful')

    try:
        print2console('Cancelling open orders')
        trading.cancel_all_open_orders(exchs)

        print2console('Getting balances')
        balances, balances_for_db = ini.get_balances(pairs, conffile)
        Time = datetime.datetime.utcnow()
        EventType = "Balances"
        Function = None
        Explanation = '{}#{}#Balances'.format(session, iter)
        EventText = balances_for_db
        ExceptionType = None
        print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText, ExceptionType))
        total_balance = {cur: 0 for cur in currency_list}
        for cur in currency_list:
            for exch in balances.keys():
                total_balance[cur] += balances[exch][cur]

        print2console('Getting order books')
        data = exchs_data.get_order_books(requests, limit, conffile)
        if ok_mongo:
            bot_utils.save_to_mongo(data, db, iter, session, counter)
        order_books = matching.join_and_sort(data)

        print2console('Generating arbitrage orders')
        our_orders = matching.get_arb_opp(order_books, balances)

        print2console('Choosing best orders')
        best, orders = get_best(our_orders, total_balance)
        if best is not None:
            orders = trading.filter_orders(best, orders, minvolumes)
        if best is None or orders['profit'] < 0.0001 or orders["buy"] == {} or orders["sell"] == {}:
            print2console('No good orders. Going to sleep for 30 seconds', last=True)
            time.sleep(30)
            continue

        print2console('Making orders: {}'.format(best))
        req, res = trading.make_all_orders(best, orders, exchs, conffile)
        Time = datetime.datetime.utcnow()
        EventType = "RequestsForPlacingOrders"
        Function = "main while true"
        Explanation = '{}#{}#{}'.format(session, iter, "Orders generated")
        EventText = req
        ExceptionType = None
        print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText, ExceptionType))
        Time = datetime.datetime.utcnow()
        EventType = "ResponsesAfterPlacingOrders"
        Function = "main while true"
        Explanation = '{}#{}#{}'.format(session, iter, "Exchanges respond to orders placed")
        EventText = res
        ExceptionType = None
        print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText, ExceptionType))
        print2console('Iteration ended. Going to sleep for 30 seconds', last=True)
        time.sleep(30)
    except Exception as e:
        Time = datetime.datetime.utcnow()
        EventType = "Error"
        Function = "main while true"
        Explanation = "Something strange happens"
        EventText = e
        ExceptionType = type(e)
        print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                            ExceptionType))
        print2console('Going to sleep for 30 seconds', last=True)
        time.sleep(30)