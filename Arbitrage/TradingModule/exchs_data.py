import aiohttp
import asyncio
import async_timeout
import json
import time
import copy

FETCH_TIMEOUT = 5  # number of seconds to wait
MAX_ENTRIES = 200  # maximum allowed number of entries in DB

async def fetch(session, url, name, pair):
    """ GET request via aiohttp, returns JSON """
    try:
        start = time.time()
        with async_timeout.timeout(FETCH_TIMEOUT):
            async with session.get(url) as response:
                response_json = await response.json(content_type=None)
                return name, pair, response_json, time.time() - start
    except asyncio.TimeoutError:
        return name, pair, None, 'timeout'
    except:
        return name, pair, None, 'json'


async def collect_data(pairs):
    """ creates aiohttp session and waits till all requests are done """
    async with aiohttp.ClientSession() as session:
        tasks = []
        for p in pairs.keys():
            for url, name in zip(pairs[p]['urls'], pairs[p]['names']):
                tasks.append(fetch(session, url, name, p))
        return await asyncio.gather(*tasks)


def process_responses(responses, conf, syms, limit):
    order_books = dict()
    d = {
        'orders': {'bids': [], 'asks': []}
    }
    time_data = {}

    for sym in syms.keys():
        order_books[sym] = dict()
        order_books[sym] = copy.deepcopy(d)

    for response in responses:
        # response format: exch_name, pair, data, time
        exch = response[0]
        pair = response[1]
        data = response[2]
        timestamp = response[3]
        if data is not None:
            try:
                price_ix = conf[exch]['fields']['price']
                volume_ix = conf[exch]['fields']['volume']
                path = conf[exch]["path"]
                sym = conf[exch]['converter'][pair]
                # extract orders for current exchange
                current_bids = data
                for x in path["bids"]:
                    if x == "{}":
                        x = x.format(sym)
                    current_bids = current_bids[x]
                current_asks = data
                for x in path["asks"]:
                    if x == "{}":
                        x = x.format(sym)
                    current_asks = current_asks[x]
                # add current orders to bids and asks arrays
                for i in range(min(limit, len(current_bids))):
                    order_books[pair]['orders']['bids'].append(
                        [float(current_bids[i][price_ix]), float(current_bids[i][volume_ix]), exch])
                for i in range(min(limit, len(current_asks))):
                    order_books[pair]['orders']['asks'].append(
                        [float(current_asks[i][price_ix]), float(current_asks[i][volume_ix]), exch])
                time_data[exch] = timestamp
            except:  # Some error occurred while parsing json response for current exchange
                time_data[exch] = 'fields'
        else:  # Some error occurred while making HTTP request for current exchange
            time_data[exch] = timestamp
    for pair in order_books.keys():
        for bid in order_books[pair]['orders']['bids']:
            if 'fee' in conf[bid[2]].keys():
                alpha = conf[bid[2]]['fee']
            else:
                alpha = 0
            bid[0] *= (1 - alpha)
        for ask in order_books[pair]['orders']['asks']:
            if 'fee' in conf[ask[2]].keys():
                alpha = conf[ask[2]]['fee']
            else:
                alpha = 0
            ask[0] *= (1 + alpha)

    for pair in order_books.keys():
        if len(order_books[pair]['orders']['bids']) > 0 and len(order_books[pair]['orders']['asks']) > 0:
            order_books[pair]['orders']['bids'].sort(key=lambda triple: triple[0],
                                                     reverse=True)  # bids sorted in descending order by price
            order_books[pair]['orders']['asks'].sort(
                key=lambda triple: triple[0])  # asks sorted in ascending order by price
    return order_books, time_data


def collector(conf, pairs, limit, logfile='', techfile='', db=None):
    loop = asyncio.get_event_loop()
    responses = loop.run_until_complete(collect_data(pairs))
    timestamp = int(time.time() * 1000)
    order_books, time_data = process_responses(responses, conf, pairs, limit)
    # d = make_logging_entry(order_books)
    # db.child(logfile).child(timestamp).set(d)
    # db.child(techfile).child(timestamp).set(time_data)
    return timestamp, order_books


def get_order_books(symbols, limit, conffile):
    # if __name__ == "__main__":
    # Parsing command line arguments
    '''
    parser = argparse.ArgumentParser(prog="python orders_logger.py",
                                     epilog="See wiki on Github for additional information")
    parser.add_argument('-c', '--config',
                        default='orders_config.json',
                        required=False,
                        help="json configuration file (default: orders_config.json)")
    parser.add_argument('-l', '--limit',
                        type=int,
                        default=50,
                        required=False,
                        choices=[5, 10, 20, 50],
                        help="how many top orders should be processed (default: 50)")
    parser.add_argument('symbol',
                        help="currency pair")
    args = parser.parse_args()  # (['-l', '5', '-c', 'orders_config.json', 'eos_btc'])

    '''
    # Access to arguments' values: args.config, args.limit, args.symbol

    pairs = dict()

    badsyms = 0

    try:
        conf = json.load(open(conffile))  # load configuration file
        for symbol in symbols:
            urls = []
            names = []
            syms = dict()
            for exch in conf.keys():
                try:  # get exchange's symbol for user's symbol
                    sym = conf[exch]["converter"][symbol]
                    syms[exch] = sym
                    urls.append(conf[exch]["url"].format(sym, limit))
                    names.append(exch)
                except KeyError:
                    pass
            if len(names) == 0:
                print("\tERROR")
                print("No exchange supports symbol {}".format(symbol))
                badsyms += 1
            else:
                pairs[symbol] = dict()

                pairs[symbol]['urls'] = copy.deepcopy(urls)
                pairs[symbol]['names'] = copy.deepcopy(names)

        if badsyms == len(symbols):
            print("\tERROR")
            print("None of given symbols are supported on any exchanges")
            exit(1)
        '''
        config = {
            "apiKey": "AIzaSyBbUk_Lo0mDuCvAiocniFGCJCsIlwd6Kew",
            "authDomain": "arb-log.firebaseapp.com",
            "databaseURL": "https://arb-log.firebaseio.com",
            "storageBucket": "arb-log.appspot.com",
            "serviceAccount": "firebase_config.json"
        }
        
        config = {
            "apiKey": "AIzaSyBqm0oupQb8NFPBCtPv1ZR5exdEsZ9wcyI",
            "authDomain": "test-36f7a.firebaseapp.com",
            "databaseURL": "https://test-36f7a.firebaseio.com",
            "storageBucket": "test-36f7a.appspot.com",
            "serviceAccount": "test_firebase_config.json"
        }

        logfile = 'log_' + 'all'  # symbol
        techfile = 'tech_' + 'all'  # symbol
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()
        db.child(logfile).remove()
        db.child(techfile).remove()

        last_keys = deque()
        '''
        # while True:
        try:
            # firebase = pyrebase.initialize_app(config)
            # db = firebase.database()
            ts, orders = collector(conf, pairs, limit)
            # pprint(orders)
            #last_keys.append(ts)
            # if orders['profit']/orders['amount'] > best_orders['profit']/best_orders['amount']:
            #   best_orders = orders
            # if len(last_keys) == MAX_ENTRIES + 1:
            #     first_key = last_keys.popleft()
            #     db.child(logfile).child(first_key).remove()
            #     db.child(techfile).child(first_key).remove()
            # return best_orders
            return orders
        except Exception as e:
            timestamp = int(time.time())
            # db.child(techfile).child(timestamp).set({'error': str(e)})
            print(timestamp)
            print(e)



    except FileNotFoundError as e:
        print("\t ERROR")
        print("No such file", conffile)
        exit(1)
    except json.JSONDecodeError as e:
        print("\t ERROR")
        print("File {} doesn't seem to be a valid JSON document".format(conffile))
        print("Error occurred on line {}, column {}".format(e.lineno, e.colno))
        print(e.msg)
        exit(1)
