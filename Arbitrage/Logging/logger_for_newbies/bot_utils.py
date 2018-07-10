import aiohttp
import asyncio
import async_timeout
import copy
import datetime
import json
import os
import pymongo
import time
from pprint import pprint


"""
# Explanation of *data* object (input for join_and_sort and save_to_mongo)
# See concrete example in file "data_example.json"
    data = {
        'pair_1': {...},
        'pair_2': {...},
        . . . . .
    }
    
    
    data[pair] = {
        'exch_name_1': {...},
        'exch_name_2': {...},
        . . . . .
    }
    
    
    data[pair][exch] = {
        'asks': [
            [price_with_fee, volume, original_price],
            ...
        ],
        'bids': [
            [price_with_fee, volume, original_price],
            ...
        ]
    }
    
    price_with_fee is computed as
        (1+a)*original_price for asks
        (1-a)*original_price for bids
    where a is taker trading fee for current exchange

########################################################################################################################

# Explanation of *order_books* object (output of join_and_sort and get_order_books, returned by get_arb_opp)
# See concrete example in file "order_books_example.json"

    order_books = {
        'pair_1': {...},
        'pair_2': {...},
        . . . . .
    }
        
    order_books[pair] = {
        'asks': [
            [price_with_fee, volume, original_price, exchange_name],
            ...
        ],
        'bids': [
            [price_with_fee, volume, original_price, exchange_name],
            ...
        ]
    }    

########################################################################################################################

# Explanation of *current_balance* object (input for get_arb_opp)
# See concrete example in file "current_balance_example.json"

    current_balance = {
        'exch_1': {...},
        'exch_2': {...},
        . . . . .
    }
    
    current_balance[exch] = {
        'currency_1': 'balance_1',
        'currency_2': 'balance_2',
        . . . . . 
    }
    
    All balances are floats. 

########################################################################################################################

# Explanation of *our_orders* object (returned by get_arb_opp).
# See concrete example in file "our_orders_example.json"
    
    our_orders = {
        'pair_1': {...},
        'pair_2': {...},
        . . . . .
    }
    
    our_orders[pair] = {
        'buy': [],
        'sell': [],
        'required_base_amount': float,
        'required_quote_amount': float,
        'profit': float
    }

########################################################################################################################

# Explanation of *pairs* object (input for get_order_books).
# See concrete example in file "pairs_example.json"
    
    pairs = {
        'pair_1': {...},
        'pair_2': {...},
        . . . . .
    }
    
    pairs[pair] = {
        'names': [],
        'urls': [],
    }

"""


File = os.path.basename(__file__)
FETCH_TIMEOUT = 10  # number of seconds to wait
MAX_ENTRIES = 200   # maximum allowed number of entries in DB


async def _fetch_order_books(session, url, name, pair):
    """
    Performs GET request via aiohttp
    :param session: aiohttp session to process request
    :param url: url path to order book
    :param name: exchange name for which order book is being fetched
    :param pair: currency pair for which order book is being fetched
    :return: (exchange name, currency pair, deJSONified response)
    """
    try:
        with async_timeout.timeout(FETCH_TIMEOUT):
            async with session.get(url) as response:
                response_json = await response.json(content_type=None)
                return name, pair, response_json
    except asyncio.TimeoutError as e:
        Time = datetime.datetime.utcnow()
        EventType = "AsyncioTimeoutError"
        Function = "fetch_order_books"
        Explanation = "Timeout occurred while fetching order books for {} pair from {}".format(pair, name)
        EventText = e
        ExceptionType = type(e)
        print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText, ExceptionType))
        return name, pair, None
    except Exception as e:
        Time = datetime.datetime.utcnow()
        EventType = "Error"
        Function = "fetch_order_books"
        Explanation = "Error occurred while fetching order books for {} pair from {}".format(pair, name)
        EventText = e
        ExceptionType = type(e)
        print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText, ExceptionType))
        return name, pair, None


async def _collect_data(pairs):
    """
    Creates aiohttp session and waits till all requests are done
    :param pairs: dictionary of the form {pair_name: {"urls": [], "names": []}, ...} (see example at the beginning of this file)
    :return: array of fetch_order_books function responses
    """
    try:
        async with aiohttp.ClientSession() as session:
            tasks = []
            for p in pairs.keys():
                for url, name in zip(pairs[p]['urls'], pairs[p]['names']):
                    tasks.append(_fetch_order_books(session, url, name, p))
            return await asyncio.gather(*tasks)
    except Exception as e:
        Time = datetime.datetime.utcnow()
        EventType = "Error"
        Function = "collect_data"
        Explanation = "ClientSession failed while getting order books from exchanges"
        EventText = e
        ExceptionType = type(e)
        print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText, ExceptionType))


def _process_responses(responses, conf, pairs, limit):
    """
    :param responses: responses from exchanges in format (exch_name, pair, JSON response)
    :param conf: dictionary with data from 'orders_config.json' file
    :param pairs: see example at the beginning of this file
    :param limit: number of top orders to be taken
    :return: data (see example at the beginning of this file)
    """
    data = dict()
    for pair in pairs.keys():
        data[pair] = {}

    for response in responses:
        data[response[1]][response[0]] = {"bids" : [], "asks" : []}

    for response in responses:
        exch = response[0]
        pair = response[1]
        response_dict = response[2]
        if response_dict is not None:
            try:
                price_ix = conf[exch]['fields']['price']
                volume_ix = conf[exch]['fields']['volume']
                path = conf[exch]["path"]
                sym = conf[exch]['converter'][pair]

                # extract orders for current exchange
                current_bids = response_dict
                for x in path["bids"]:
                    if x == "{}":
                        x = x.format(sym)
                    current_bids = current_bids[x]
                current_asks = response_dict
                for x in path["asks"]:
                    if x == "{}":
                        x = x.format(sym)
                    current_asks = current_asks[x]

                # add current orders to bids and asks arrays
                for i in range(min(limit, len(current_bids))):
                    data[pair][exch]['bids'].append(
                        [float(current_bids[i][price_ix]), float(current_bids[i][volume_ix]), float(current_bids[i][price_ix])])
                for i in range(min(limit, len(current_asks))):
                    data[pair][exch]['asks'].append(
                        [float(current_asks[i][price_ix]), float(current_asks[i][volume_ix]), float(current_asks[i][price_ix])])
            except Exception as e:  # Some error occurred while parsing json response for current exchange
                Time = datetime.datetime.utcnow()
                EventType = "Error"
                Function = "process_responses"
                Explanation = "Some error occurred while parsing order books for {} from {}. Response: {}".format(pair, exch, response_dict)
                EventText = e
                ExceptionType = type(e)
                print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText, ExceptionType))

    for pair in data.keys():
        for exch in data[pair].keys():
            for bid in data[pair][exch]['bids']:
                if 'fee' in conf[exch].keys():
                    alpha = conf[exch]['fee']
                else:
                    alpha = 0.0
                bid[0] *= (1 - alpha)
            for ask in data[pair][exch]['asks']:
                if 'fee' in conf[exch].keys():
                    alpha = conf[exch]['fee']
                else:
                    alpha = 0.0
                ask[0] *= (1 + alpha)
    return data


def _join_and_sort(data_pair, order_type):
    """
    See join_and_sort
    :param data_pair: dictionary, data[pair] (see example at the beginning of this file)
    :return: sorted array
    """
    ans = []
    for exch in data_pair:
        for order in data_pair[exch][order_type]:
            order.append(exch)
            ans.append(order)
    if order_type == 'bids':
        ans.sort(key=lambda quad: quad[0], reverse=True)   # bids sorted in descending order by price
    else:
        ans.sort(key=lambda quad: quad[0])                 # asks sorted in ascending order by price
    return ans


def get_pairs(symbols, conf, limit, exchs=None):
    """
    Generates list of urls to be placed via async GET requests to get order_books
    :param symbols: list of currency pairs to get order_books for
    :param exchs: list of exchanges to get order books from
    :param conf: dictionary with data from 'orders_config.json' file
    :param limit: number of top orders we need to get
    :return: pairs (see example at the beginning of this file)
    """
    pairs = dict()
    for symbol in symbols:
        pairs[symbol] = dict()
    badsyms = 0
    if exchs is None:
        exchs = list(conf.keys())
    try:
        for symbol in symbols:
            pairs[symbol]['urls'] = []
            pairs[symbol]['names'] = []
            syms = dict()
            for exch in exchs:
                try:  # get exchange's symbol for user's symbol
                    sym = conf[exch]["converter"][symbol]
                    syms[exch] = sym
                    pairs[symbol]['urls'].append(conf[exch]["url"].format(sym, limit))
                    pairs[symbol]['names'].append(exch)
                except KeyError as e:
                    Time = datetime.datetime.utcnow()
                    EventType = "SafeKeyError"
                    Function = "get_pairs"
                    Explanation = "Configuration file doesn't contain required fields (converter or symbol {} for {})".format(symbol, exch)
                    EventText = e
                    ExceptionType = type(e)
                    print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText, ExceptionType))
                    pass
            if len(pairs[symbol]['names']) == 0:
                badsyms += 1
        if badsyms == len(symbols):
            Time = datetime.datetime.utcnow()
            EventType = "EXIT"
            Function = "get_pairs"
            Explanation = "None of the given symbols is supported by any exchanges"
            EventText = ""
            ExceptionType = ""
            print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                                ExceptionType))
            exit(1)
    except Exception as e:
        Time = datetime.datetime.utcnow()
        EventType = "Error"
        Function = "get_pairs"
        Explanation = "Some error occurred in get_url()"
        EventText = e
        ExceptionType = type(e)
        print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                            ExceptionType))
        exit(1)
    return pairs


def join_and_sort(data):
    """
    Processes *data* object:
        (*) transforms all orders from
                [price_with_fee, volume, original_price]
            to
                [price_with_fee, volume, original_price, exchange]
        (*) joins all asks/bids into one sorted order_book
    :param data: see example at the beginning of this file
    :return: order_books (see example at the beginning of this file)
    """
    ans = dict()
    for pair in data:
        ans[pair] = dict()
        ans[pair]['asks'] = _join_and_sort(data[pair], 'asks')
        ans[pair]['bids'] = _join_and_sort(data[pair], 'bids')
    return ans


def get_data(pairs, conf, limit):
    """
    Gets order books
    :param pairs: list of currency pairs to get order books for
    :param limit: maximum number of top orders to take from each order book
    :param conf: dictionary with data from 'orders_config.json' file
    :return: data (see example at the beginning of this file)
    """
    try:
        loop = asyncio.get_event_loop()
        responses = loop.run_until_complete(_collect_data(pairs))
        return _process_responses(responses, conf, pairs, limit)
    except Exception as e:
        Time = datetime.datetime.utcnow()
        EventType = "Error"
        Function = "get_data2"
        Explanation = "Exception in get_order_books() occurred"
        EventText = e
        ExceptionType = type(e)
        print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText, ExceptionType))


def get_order_books(pairs, conf, limit):
    """
    Gets order books
    :param pairs: list of currency pairs to get order books for
    :param limit: maximum number of top orders to take from each order book
    :param conf: dictionary with data from 'orders_config.json' file
    :return: order_books (see example at the beginning of this file)
    """
    try:
        data = get_data(pairs, conf, limit)
        return join_and_sort(data)
    except Exception as e:
        Time = datetime.datetime.utcnow()
        EventType = "Error"
        Function = "get_order_books"
        Explanation = "Exception in get_order_books() occurred"
        EventText = e
        ExceptionType = type(e)
        print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText, ExceptionType))


# def save_to_mongo(data, db):
#     """
#     Saves data (see example at the beginning of this file) to MongoDB:
#         (*) separate collections for different pairs
#         (*) separate documents for different exchanges
#         (*) all documents are of the form
#             {exchange_name: string, timestamp: UNIX_timestamp, asks: array, bids: array}
#     :param data: see example at the beginning of this file
#     :param auth_string: MongoDB authentication string
#     :param db_name: which database to use
#     :param overwrite: if True then overwrites database
#     :return: None
#     """
#     for pair in data:
#         col = db['ob_' + pair]
#         for exch in data[pair]:
#             d = dict()
#             d['asks'] = data[pair][exch]['asks']
#             d['bids'] = data[pair][exch]['bids']
#             d['exch'] = exch
#             d['timestamp'] = time.time()
#             col.insert_one(d)


def save_to_mongo(data, db):
    """
    Saves data (see example at the beginning of this file) to MongoDB:
        (*) separate collections for different pairs
        (*) separate documents for different exchanges
        (*) all documents are of the form
            {exchange_name: string, timestamp: UNIX_timestamp, asks: array, bids: array}
    :param data: see example at the beginning of this file
    :param auth_string: MongoDB authentication string
    :param db_name: which database to use
    :param overwrite: if True then overwrites database
    :return: None
    """
    for pair in data:
        col = db['ob_' + pair]
        d = dict()
        d['timestamp'] = time.time()
        d['data'] = data[pair]
        col.insert_one(d)


def get_arb_opp(order_books, current_balance, alpha=0.1, copy_balance=False, copy_order_books=False):
    """
    Tries to find arbitrage (based on order books received from exchanges and available balances on these exchanges)
    :param order_books: see example at the beginning of this file
    :param current_balance: see example at the beginning of this file
    :param alpha: heuristic parameter used to find best investment/profit ratio
    :param copy_balance: if False then current_balance object passed to function may be changed during the execution
    :return: our_orders (see example at the beginning of this file)
    """
    our_orders = dict()
    if copy_balance:
        current_balance = copy.deepcopy(current_balance)

    for pair in order_books.keys():
        currencies = pair.split('_')
        base_cur = currencies[0]   # base currency of current pair (BTC for BTC/USD)
        quote_cur = currencies[1]  # quote currency of current pair (USD for BTC/USD)
        # print(pair, base_cur, quote_cur)

        ax = 0
        bx = 0
        asks = order_books[pair]['asks']
        bids = order_books[pair]['bids']
        if copy_order_books:
            asks = copy.deepcopy(asks)
            bids = copy.deepcopy(bids)
        ask_count = len(asks)
        bid_count = len(bids)

        profit = 0
        base_amount = 0  # required amount of base currency
        quote_amount = 0  # required amount of quote currency

        num = 0  # number of current micro-trade
        sell_orders = {}  # all sell_orders for current pair
        buy_orders = {}  # all buy_orders for current pair

        prev_profit = 0
        prev_quote_amount = 0

        while bx < bid_count and ax < ask_count and bids[bx][0] > asks[ax][0]:
            ask_price = asks[ax][0]
            bid_price = bids[bx][0]
            if ask_price == 0:
                ax += 1
                continue
            if bid_price == 0:
                bx += 1
                continue

            ask_vol = asks[ax][1]
            bid_vol = bids[bx][1]
            if ask_vol == 0:
                ax += 1
                continue
            if bid_vol == 0:
                bx += 1
                continue

            ask_price_real = asks[ax][2]
            bid_price_real = bids[bx][2]

            ask_exch = asks[ax][3]  # BID: base -> quote
            bid_exch = bids[bx][3]  # ASK: quote -> base

            ask_bal = current_balance[ask_exch][quote_cur]
            bid_bal = current_balance[bid_exch][base_cur]
            if ask_bal == 0:
                ax += 1
                continue
            if bid_bal == 0:
                bx += 1
                continue

            try:
                m = min(ask_vol, bid_vol, ask_bal / ask_price_real, bid_bal)  # current micro-trade volume
                current_profit = (bid_price - ask_price) * m                  # current micro-trade profit
                if m < 1e-8:
                    ax += 1
                    bx += 1
                    continue
                profit = prev_profit + current_profit
                base_amount += m
                quote_amount = prev_quote_amount + ask_price * m
                bids[bx][1] -= m
                asks[ax][1] -= m
                current_balance[ask_exch][quote_cur] -= m * ask_price_real
                current_balance[bid_exch][base_cur] -= m
            except ZeroDivisionError as e:
                Time = datetime.datetime.utcnow()
                EventType = "ZeroDivisionError"
                Function = "get_arb_opp"
                Explanation = "ask_price_real is equal to 0 at profit point {}".format(num)
                EventText = e
                ExceptionType = type(e)
                print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText, ExceptionType))
                break

            num += 1
            if num == 2:
                try:
                    first_k = (profit - prev_profit) / (quote_amount - prev_quote_amount)
                except ZeroDivisionError as e:
                    Time = datetime.datetime.utcnow()
                    EventType = "ZeroDivisionError"
                    Function = "get_arb_opp"
                    Explanation = "quote_amount is equal to prev_quote_amount at second profit point: {} {}".format(quote_amount, prev_quote_amount)
                    EventText = e
                    ExceptionType = type(e)
                    print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                                        ExceptionType))
                    break
                except Exception as e:
                    Time = datetime.datetime.utcnow()
                    EventType = "ZeroDivisionError"
                    Function = "get_arb_opp"
                    Explanation = "Some error occurred while computing first_k"
                    EventText = e
                    ExceptionType = type(e)
                    print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText, ExceptionType))
                    break
            elif num > 2:
                try:
                    k = (profit - prev_profit) / (quote_amount - prev_quote_amount)
                except ZeroDivisionError as e:
                    Time = datetime.datetime.utcnow()
                    EventType = "ZeroDivisionError"
                    Function = "get_arb_opp"
                    Explanation = "quote_amount is equal to prev_quote_amount at profit point {}: {} {}, ask_price = {}, m = {}".format(
                                                                        num, quote_amount, prev_quote_amount, ask_price, m)
                    EventText = e
                    ExceptionType = type(e)
                    print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText, ExceptionType))
                    break
                except Exception as e:
                    Time = datetime.datetime.utcnow()
                    EventType = "Error"
                    Function = "get_arb_opp"
                    Explanation = "Some error occurred while computing k at profit point {}".format(num)
                    EventText = e
                    ExceptionType = type(e)
                    print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText, ExceptionType))
                    break

                if k < first_k * alpha:
                    break

            if bid_exch in sell_orders:
                sell_orders[bid_exch][0] = min(sell_orders[bid_exch][0], bid_price_real)
                sell_orders[bid_exch][1] += m
            else:
                sell_orders[bid_exch] = [bid_price_real, m]

            if ask_exch in buy_orders:
                buy_orders[ask_exch][0] = max(buy_orders[ask_exch][0], ask_price_real)
                buy_orders[ask_exch][1] += m
            else:
                buy_orders[ask_exch] = [ask_price_real, m]
            prev_quote_amount = quote_amount
            prev_profit = profit

        our_orders[pair] = {}
        our_orders[pair]['required_base_amount'] = base_amount
        our_orders[pair]['required_quote_amount'] = quote_amount
        our_orders[pair]['profit'] = profit  # in quote currency
        our_orders[pair]['buy'] = buy_orders
        our_orders[pair]['sell'] = sell_orders
        # print(base_amount, quote_amount, profit)
        # print(buy_orders)
        # print(sell_orders)
    return our_orders


# data = json.load(open('data_example.json'))
# # save_to_mongo(data, "mongodb://admin:415096396771@40.121.22.249/admin", 'test')
# json.dump(join_and_sort(data), open('order_books_example.json', 'w'), indent=4)
