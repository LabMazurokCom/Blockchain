import json
import pymongo
from bot_utils import join_and_sort, get_arb_opp
from pprint import pprint

EPS = 1e-4


def arbitrage_analysis(config_file='arbitrage_analysis_config.json'):
    try:
        print('# Reading configuration file')
        config = json.load(open(config_file))
        auth_string = config['auth_string']
        db_name = config['db_name']
        inf = config['inf']
        number_of_entries = config['number_of_entries']
        pair = config['pair']
        exchanges = config['exchanges']

        print('# Forming list of currencies')
        current_balance = dict()
        currencies = set()
        for exch in exchanges:
            for key in exch['balance']:
                currencies.add(key)

        print('# Imitating balances')
        for exch in exchanges:
            exch_name = exch['name']
            exch_balance = exch['balance']
            if len(exch_balance) == 0:
                continue
            current_balance[exch_name] = dict()
            for currency in currencies:
                try:
                    cur_balance = exch_balance[currency]
                    if cur_balance == -1:
                        current_balance[exch_name][currency] = inf
                    else:
                        current_balance[exch_name][currency] = cur_balance
                except:
                    current_balance[exch_name][currency] = 0.0
    except Exception as e:
        print('\tERROR while processing config file')
        print(e)
    else:
        try:
            pass
            # print('# Connecting to Mongo')
            # client = pymongo.MongoClient(auth_string)  # defaults to port 27017
            # db = client[db_name]
            # print('\t', db.collection_names())
        except Exception as e:
            print('\t', e)
        else:
            print('# Entering the main loop')
            cur = pair.split('_')
            cur_base = cur[0]
            cur_quote = cur[1]
            with open(pair + '_arb.csv', 'w') as f:
                print('{},{},{},{},{},{}'.format('timestamp', 'buy_exchange', 'sell_exchange',
                                                 'profit_' + cur_quote, 'volume_' + cur_quote, 'volume_' + cur_base),
                      file=f)
                # col = db['ob_' + pair]
                it = 0
                # x = []
                # for entry in col.find(): #limit=number_of_entries, sort=[("_id", pymongo.DESCENDING)]):
                #     x.append(entry['timestamp'])
                # print(len(set(x)))
                # for entry in col.find(limit=number_of_entries, sort=[("_id", pymongo.DESCENDING)]):
                # iterator = col.find()
                # x = set()
                # for entry in iterator: #sort=[("_id", pymongo.ASCENDING)]):
                with open('ob_btc_usd.json') as collection:
                    for row in collection:
                        entry = json.loads(row)
                        it += 1
                        #print('\t# Getting list of exchanges for iteration', it)
                        exchs = [key for key in entry['data'].keys() if len(entry['data'][key]['asks']) > 0]
                        n_exchs = len(exchs)
                        #print(n_exchs)
                        timestamp = entry['timestamp']
                        print(timestamp)
                        # print(exchs)
                        if timestamp == 1530620346.2809477:
                            print(current_balance)
                            print()
                            for key in entry['data']:
                                print('\t', key)
                                print('\t\tasks:', entry['data'][key]['asks'])
                                print('\t\tbids:', entry['data'][key]['bids'])


                        #print('\t# Computing pairwise arbitrage for iteration', it)
                        for i in range(n_exchs):
                            exch_i = exchs[i]
                            ob_i = entry['data'][exch_i]
                            for k in range(i+1, n_exchs):
                                if i == k:
                                    continue
                                try:
                                    exch_k = exchs[k]
                                    ob_k = entry['data'][exch_k]
                                    # print('\t', i, k, exch_i, exch_k)

                                    data = {pair: {exch_i: ob_i, exch_k: ob_k}}

                                    if timestamp == 1530620346.2809477:
                                        for key in data[pair]:
                                            print('\t', key)
                                            print('\t\tasks:', data[pair][key]['asks'])
                                            print('\t\tbids:', data[pair][key]['bids'])
                                    d = get_arb_opp(join_and_sort(data), current_balance, copy_balance=True, copy_order_books=True)
                                    profit = d[pair]['profit']  # quote currency
                                    if timestamp == 1530620346.2809477:
                                        pprint(d)
                                        print(profit)
                                        print()
                                    if profit < EPS:
                                        continue
                                    volume_quote = d[pair]['required_quote_amount']
                                    volume_base = d[pair]['required_base_amount']
                                    buy_orders = d[pair]['buy']

                                    if exch_i in buy_orders:
                                        buy_exchange = exch_i
                                        sell_exchange = exch_k
                                    else:
                                        buy_exchange = exch_k
                                        sell_exchange = exch_i
                                    print('{},{},{},{},{},{}'.format(timestamp, buy_exchange, sell_exchange,
                                                                     profit, volume_quote, volume_base), file=f)
                                except Exception as e:
                                    print('\t', e)


arbitrage_analysis()
