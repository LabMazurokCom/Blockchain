import pymongo
from logger import run_logger
from multiprocessing import Process
import datetime


if __name__ == '__main__':
    print('multi_logger.py started at', datetime.datetime.utcnow())

    client = pymongo.MongoClient("mongodb://admin:415096396771@23.100.25.146/admin")  # defaults to port 27017

    print('multi_logger.py connected to MongoDB at', datetime.datetime.utcnow())

    db = client['test_db']

    trading_symbols = ['bch_btc', 'bch_usd', 'dash_btc', 'eth_btc', 'btc_usd', 'xrp_btc', 'dash_usd', 'eth_usd', 'xrp_usd']
    limit = 50
    config_file = 'orders_config.json'

    print('multi_logger.py started running subprocesses at', datetime.datetime.utcnow())

    for symbol in trading_symbols:
        p = Process(target=run_logger, args=(symbol, limit, config_file, db))
        p.start()

    print('multi_logger.py finished running subprocesses at', datetime.datetime.utcnow())
