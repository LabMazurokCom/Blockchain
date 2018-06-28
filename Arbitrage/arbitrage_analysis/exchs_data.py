import aiohttp
import asyncio
import async_timeout
import datetime
import os

File = os.path.basename(__file__)

FETCH_TIMEOUT = 10  # number of seconds to wait
MAX_ENTRIES = 200   # maximum allowed number of entries in DB


async def fetch(session, url, name, pair):
    """
    Performs GET request via aiohttp
    :param session: aiohttp session to process request
    :param url: url path to order book
    :param name: exchange name for which order book is being fetched
    :param pair: currency pair for which order book is being fetched
    :return: exchange name, currency pair, deJSONified response
    """
    try:
        with async_timeout.timeout(FETCH_TIMEOUT):
            async with session.get(url) as response:
                response_json = await response.json(content_type=None)
                return name, pair, response_json
    except asyncio.TimeoutError as e:
        Time = datetime.datetime.utcnow()
        EventType = "AsyncioTimeoutError"
        Function = "fetch"
        Explanation = "Timeout occurred while fetching order books for {} pair from {}".format(pair, name)
        EventText = e
        ExceptionType = type(e)
        print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                            ExceptionType))
        return name, pair, None
    except Exception as e:
        Time = datetime.datetime.utcnow()
        EventType = "Error"
        Function = "fetch"
        Explanation = "Error occurred while fetching order books for {} pair from {}".format(pair, name)
        EventText = e
        ExceptionType = type(e)
        print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                            ExceptionType))
        return name, pair, None


async def collect_data(pairs):
    """
    Creates aiohttp session and waits till all requests are done
    :param pairs: dictionary of the form {pair_name: {"urls": [], "names": []}, ...}
    :return: array of fetch() function responses
    """
    try:
        async with aiohttp.ClientSession() as session:
            tasks = []
            for p in pairs.keys():
                for url, name in zip(pairs[p]['urls'], pairs[p]['names']):
                    tasks.append(fetch(session, url, name, p))
            return await asyncio.gather(*tasks)
    except Exception as e:
        Time = datetime.datetime.utcnow()
        EventType = "Error"
        Function = "collect_data"
        Explanation = "ClientSession failed while getting order_books from exchanges"
        EventText = e
        ExceptionType = type(e)
        print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                            ExceptionType))


def process_responses(responses, conf, pairs, limit):
    """
    :param responses: responses from exchanges in format [exch_name, pair, JSON response]
    :param conf: dictionary with exchanges' configurations
    :param pairs: dictionary of the form {pair_name: {"urls": [], "names": []}, ...}
    :param limit: number of top orders to be taken
    :return: order_books of the form {pair_name: {'orders': { 'asks': [[price, volume, exchange_name], ...],
                                                              'bids': [[], ...]
                                                            }
                                                 },
                                      ...
                                     }
    """
    order_books = dict()
    for pair in pairs.keys():
        order_books[pair] = {}

    for response in responses:
        order_books[response[1]][response[0]] = {"bids" : [], "asks" : []}

    for response in responses:
        exch = response[0]
        pair = response[1]
        data = response[2]
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
                    order_books[pair][exch]['bids'].append(
                        [float(current_bids[i][price_ix]), float(current_bids[i][volume_ix]), float(current_bids[i][price_ix])])
                for i in range(min(limit, len(current_asks))):
                    order_books[pair][exch]['asks'].append(
                        [float(current_asks[i][price_ix]), float(current_asks[i][volume_ix]), float(current_asks[i][price_ix])])
            except Exception as e:  # Some error occurred while parsing json response for current exchange
                Time = datetime.datetime.utcnow()
                EventType = "Error"
                Function = "process_responses"
                Explanation = "Some error occurred while parsing order books for {} from {}. Response text: {}".format(pair, exch, data)
                EventText = e
                ExceptionType = type(e)
                print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                                    ExceptionType))

    for pair in order_books.keys():
        for exch in order_books[pair].keys():
            for bid in order_books[pair][exch]['bids']:
                if 'fee' in conf[exch].keys():
                    alpha = conf[exch]['fee']
                else:
                    alpha = 0.0
                bid[0] *= (1 - alpha)
            for ask in order_books[pair][exch]['asks']:
                if 'fee' in conf[exch].keys():
                    alpha = conf[exch]['fee']
                else:
                    alpha = 0.0
                ask[0] *= (1 + alpha)
        # if len(order_books[pair]['orders']['bids']) > 0 and len(order_books[pair]['orders']['asks']) > 0:
        #     # bids sorted in descending order by price
        #     order_books[pair]['orders']['bids'].sort(key=lambda quadriple: quadriple[0], reverse=True)
        #     # asks sorted in ascending order by price
        #     order_books[pair]['orders']['asks'].sort(key=lambda quadriple: quadriple[0])
    return order_books


def get_order_books(pairs, limit, conf):
    """
    makes loop for async requests
    :param pairs: list of pairs to get order books for
    :param limit: number of top orders in each order book
    :param conf: JSONified configuration file
    :return: order_books of the form {pair_name: {'orders': { 'asks': [[price, volume, exchange_name], ...],
                                                              'bids': [[], ...]
                                                            }
                                                 },
                                      ...
                                     }
    """
    try:
        loop = asyncio.get_event_loop()
        responses = loop.run_until_complete(collect_data(pairs))
        return process_responses(responses, conf, pairs, limit)
    except Exception as e:
        Time = datetime.datetime.utcnow()
        EventType = "Error"
        Function = "get_order_books"
        Explanation = "Exception in get_order_books() occurred"
        EventText = e
        ExceptionType = type(e)
        print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                            ExceptionType))