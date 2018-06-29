import json
import pymongo
from pprint import pprint


def arbitrage_analysis(config_file='arbitrage_analysis_config.json'):
    try:
        print('\t# Reading configuration file')
        config = json.load(open(config_file))
        auth_string = config['auth_string']
        db_name = config['db_name']
        inf = config['inf']
        number_of_entries = config['number_of_entries']
        pairs = config['pairs']
        exchanges = config['exchanges']

        print('\t# Imitating balances')
        balances = dict()
        for exch in exchanges:
            exch_name = exch['name']
            exch_balance = exch['balance']
            if len(exch_balance) > 0:
                balances[exch_name] = dict()
                for currency, cur_balance in exch_balance.items():
                    if cur_balance == -1:
                        balances[exch_name][currency] = inf
                    else:
                        balances[exch_name][currency] = cur_balance
    except Exception as e:
        print('\tERROR while processing config file')
        print(e)
        exit(1)
    else:
        try:
            print('\t# Connecting to Mongo')
            client = pymongo.MongoClient(auth_string)  # defaults to port 27017
            db = client[db_name]
            #db = client['arbitrage_logs']
            print(db.collection_names())

            # print('\t# Getting data from Mongo')
            # data = dict()
            # for pair in pairs:
            #     data[pair] = dict()
            #     col = db['ob_' + pair]
            #     for entry in col.find(limit=number_of_entries, sort=[("_id", pymongo.DESCENDING)]):
            #         print(type(entry))
            #         break
        except Exception as e:
            print('\tERROR while connecting to MongoDB and getting data')
            print(e)
            exit(1)



arbitrage_analysis()
