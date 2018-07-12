import json
import pymongo
import sys
import time
from bot_utils import get_data, get_pairs, save_to_mongo
from multiprocessing import Process


MIN_TIME = 30
old_stdout = sys.stdout


def mini_logger(symbol, conf, limit, auth_string, db_name, exchanges):
    print("I've started: {}".format(symbol))

    client = pymongo.MongoClient(auth_string)  # defaults to port 27017
    db = client[db_name]

    pairs = get_pairs([symbol], conf, limit, exchanges)

    while True:
        start_time = time.time()

        data = get_data(pairs, conf, limit)
        save_to_mongo(data, db)

        time_taken = time.time() - start_time
        if time_taken < MIN_TIME:
            time.sleep(MIN_TIME - time_taken)


print('\t#Reading configuration file')
mongo_config = json.load(open('logger_config.json'))

conf = json.load(open(mongo_config['orders_config']))
limit = mongo_config['limit']
symbols = mongo_config['symbols']
exchanges = mongo_config['exchanges']
auth_string = mongo_config['auth_string']
db_name = mongo_config['database']

# print('\t#Connecting to Mongo')
# client = pymongo.MongoClient(auth_string)  # defaults to port 27017
# client.drop_database(db_name)

print('\t#Starting processes')
for sym in symbols:
    p = Process(target=mini_logger, args=(sym, conf, limit, auth_string, db_name, exchanges))
    p.start()
    time.sleep(0.3)
exit(0)