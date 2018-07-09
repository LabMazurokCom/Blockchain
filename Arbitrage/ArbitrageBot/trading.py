import aiohttp
import async_timeout
import asyncio
import datetime
import os
import time

File = os.path.basename(__file__)


responses = []
reqs = []
open_orders = []
resps_for_cancelling = []
FETCH_TIMEOUT = 5


async def fetch(url, session, headers, data, key, auth, get_open=False, cancel=False):
    """
    Sends POST request to make an order, to get list of open orders or to cancel order
    :param url: url path for placing/getting/cancelling order
    :param session: aiohttp session to place/get/cancel order
    :param headers: headers of post request to place/get/cancel order
    :param data: data of post request to place/get/cancel order
    :param key: exchange name
    :param auth: authentication data
    :param get_open: shows if we try to get open orders
    :param cancel: shows if we try to cancel an order(s)
    :return: exchange name, time of start and end of post request, response from exchange
    """
    try:
        with async_timeout.timeout(FETCH_TIMEOUT):
            start = time.time()
            if get_open and key == "gdax":
                async with session.get(url, headers=headers, data=data, auth=auth) as response:
                    resp_text = await response.text()
                    return key, start, time.time(), resp_text
            elif cancel and key == "gdax":
                async with session.delete(url, headers=headers, data=data, auth=auth) as response:
                    resp_text = await response.text()
                    return key, start, time.time(), resp_text
            else:
                async with session.post(url, headers=headers, data=data, auth=auth) as response:
                    resp_text = await response.text()
                    return key, start, time.time(), resp_text
    except asyncio.TimeoutError as e:
        Time = datetime.datetime.utcnow()
        EventType = "TimeoutError"
        Function = "fetch"
        if get_open:
            Explanation = "{} didn't respond in time (getting open orders)".format(key)
        elif cancel:
            Explanation = "{} didn't respond in time (cancelling orders)".format(key)
        else:
            Explanation = "{} didn't respond in time (placing order)".format(key)
        EventText = e
        ExceptionType = type(e)
        print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText, ExceptionType))
        return key, start, time.time(), None
    except Exception as e:
        Time = datetime.datetime.utcnow()
        EventType = "Error"
        Function = "fetch"
        if get_open:
            Explanation = "Some error occurred during post request to {} (getting open orders)".format(key)
        elif cancel:
            Explanation = "Some error occurred during post request to {} (cancelling orders)".format(key)
        else:
            Explanation = "Some error occurred during post request to {} (placing order)".format(key)
        EventText = e
        ExceptionType = type(e)
        print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText, ExceptionType))
        return key, start, time.time(), None


async def place_orders(pair, orders, exs, conf):
    """
    :param pair: pair to be traded
    :param orders: list of orders to be placed in format {
                                                             'asks': [],
                                                             'bids': [],
                                                             'required_base_amount': float,
                                                             'required_quote_amount': float,
                                                             'profit': float
                                                         }
    :param exs: list of exchanges
    :param conf: JSONified configuration file
    :return: collect responses
    """
    exchs = {}
    for e in exs:
        exchs[e.__class__.__name__.lower()] = e

    tasks = []
    try:
        async with aiohttp.ClientSession() as session:
            try:
                for key, value in orders['sell'].items():
                    tmp = str(value[1])
                    pos = tmp.find('.')
                    tmp = tmp[:pos+9]
                    url, headers, data, auth = exchs[key].place_order(str(value[0]), tmp, conf[key]['converter'][pair], 'sell', 'limit')
                    reqs.append([key, str(value[0]), tmp, 'sell'])
                    task = asyncio.ensure_future(fetch(url, session, headers, data, key, auth))
                    tasks.append(task)
                for key, value in orders['buy'].items():
                    tmp = str(value[1])
                    pos = tmp.find('.')
                    tmp = tmp[:pos + 9]
                    url, headers, data, auth = exchs[key].place_order(str(value[0]), tmp, conf[key]['converter'][pair], 'buy', 'limit')
                    reqs.append([key, str(value[0]), tmp, 'buy'])
                    task = asyncio.ensure_future(fetch(url, session, headers, data, key, auth))
                    tasks.append(task)
            except KeyError as e:
                Time = datetime.datetime.utcnow()
                EventType = "KeyError"
                Function = "place_orders"
                Explanation = "Invalid key somewhere in place_orders"
                EventText = e
                ExceptionType = type(e)
                print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                                    ExceptionType))
                pass
            global responses
            responses = await asyncio.gather(*tasks)
    except Exception as e:
        Time = datetime.datetime.utcnow()
        EventType = "Error"
        Function = "place_orders"
        Explanation = "Client session failed while placing orders to exchanges"
        EventText = e
        ExceptionType = type(e)
        print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                            ExceptionType))


async def get_all_open_orders(exchs):
    tasks = []
    try:
        async with aiohttp.ClientSession() as session:
            try:
                for exch in exchs:
                    ename = exch.__class__.__name__.lower()
                    url, headers, data, auth = exch.get_open_orders()
                    task = asyncio.ensure_future(fetch(url, session, headers, data, ename, auth, get_open=True))
                    tasks.append(task)
            except Exception as e:
                Time = datetime.datetime.utcnow()
                EventType = "Error"
                Function = "get_all_open_orders"
                Explanation = "Some error occurred while getting requests for cancelling open orders"
                EventText = e
                ExceptionType = type(e)
                print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                                    ExceptionType))
                pass
            global open_orders
            open_orders = await asyncio.gather(*tasks)
    except Exception as e:
        Time = datetime.datetime.utcnow()
        EventType = "Error"
        Function = "get_all_open_orders"
        Explanation = "Client session failed getting open orders"
        EventText = e
        ExceptionType = type(e)
        print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                            ExceptionType))


async def cancel_open_orders(orders_to_cancel, exchs):
    tasks = []
    try:
        async with aiohttp.ClientSession() as session:
            try:
                for exch in exchs:
                    ename = exch.__class__.__name__.lower()
                    if ename in orders_to_cancel:
                        exch_requests = exch.cancel_open_orders(orders_to_cancel[ename])
                        for exch_req in exch_requests:
                            url = exch_req[0]
                            headers = exch_req[1]
                            data = exch_req[2]
                            auth = exch_req[3]
                            print(ename, url, headers, data, auth)
                            task = asyncio.ensure_future(fetch(url, session, headers, data, ename, auth, cancel=True))
                            tasks.append(task)
            except Exception as e:
                Time = datetime.datetime.utcnow()
                EventType = "Error"
                Function = "cancel_open_orders"
                Explanation = "Some error occurred while cancelling open orders"
                EventText = e
                ExceptionType = type(e)
                print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                                    ExceptionType))
                pass
            global resps_for_cancelling
            resps_for_cancelling = await asyncio.gather(*tasks)
    except Exception as e:
        Time = datetime.datetime.utcnow()
        EventType = "Error"
        Function = "cancel_open_orders"
        Explanation = "Client session failed while cancelling orders"
        EventText = e
        ExceptionType = type(e)
        print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                            ExceptionType))


def cancel_all_open_orders(exchs):
    """
    gets and then cancels all open orders on all exchanges
    :param exchs: set of exchanges
    :return:
    """
    try:
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(get_all_open_orders(exchs))
        loop.run_until_complete(future)

        orders_to_cancel = {}
        for open_order in open_orders:
            orders_to_cancel[open_order[0]] = open_order[3]
        '''
        orders_to_cancel = {
            'gdax': '[{"id": "d0c5340b-6d6c-49d9-b567-48c4bfca13d2"},{"id": "8b99b139-58f2-4ab2-8e7a-c11c846e3022"}]',
            'cex': '[{"id": "13837040"},{"id": "16452929"}]',
            'exmo': '{"BTC_USD": [{"order_id" : "14"}]}',
            'kraken': '{"error":[],"result":{"open":{}}}'
        }
        '''
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(cancel_open_orders(orders_to_cancel, exchs))
        loop.run_until_complete(future)

        print(resps_for_cancelling)

        print("finished")

    except Exception as e:
        Time = datetime.datetime.utcnow()
        EventType = "Error"
        Function = "cancel_all_open_orders"
        Explanation = "Some error occurred while cancelling open orders"
        EventText = e
        ExceptionType = type(e)
        print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                            ExceptionType))


def filter_orders(pair, orders, minvolumes):
    """
    fetch orders with appropriate sizes
    :param pair: trading pair
    :param orders: dict with orders in form {
                                                 'asks': [],
                                                 'bids': [],
                                                 'required_base_amount': float,
                                                 'required_quote_amount': float,
                                                 'profit': float
                                             }
    :param minvolumes: dict with minimal orders' sizes in form {
                                                                    "exch1" : {
                                                                        "pair1" : [minlot1, minlot2],
                                                                        "pair2" : [minlot1, minlot2],
                                                                        ...
                                                                    },
                                                                    ...
                                                                }
    :return: dict with orders with correct sizes in form {
                                                             'asks': [],
                                                             'bids': [],
                                                             'required_base_amount': float,
                                                             'required_quote_amount': float,
                                                             'profit': float
                                                         }
    """
    final_orders = {"buy": {}, "sell": {}, "profit": orders["profit"],
                    "required_base_amount": orders["required_base_amount"],
                    "required_quote_amount": orders["required_quote_amount"]}
    for exch in orders["buy"].keys():
        if orders["buy"][exch][1] >= minvolumes[exch][pair][0]:
            final_orders["buy"][exch] = orders["buy"][exch]
    for exch in orders["sell"].keys():
        if orders["sell"][exch][1] >= minvolumes[exch][pair][0]:
            final_orders["sell"][exch] = orders["sell"][exch]
    return final_orders


def make_all_orders(pair, orders, exchs, conffile):
    """
    :param pair: name of pair to be traded
    :param orders: list of orders for pair in format {
                                                         'asks': [],
                                                         'bids': [],
                                                         'required_base_amount': float,
                                                         'required_quote_amount': float,
                                                         'profit': float
                                                     }
    :param exchs: list of exchanges
    :param conffile: JSONified configuration file
    :return: list of requests to exchanges in format [exchange_name, price, amount, 'buy'/'sell'],
             list of responses from exchanges in format [exchange name, time of start and end of post request, response from exchange]
    """
    global reqs
    reqs = []
    global responses
    responses = []
    try:
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(place_orders(pair, orders, exchs, conffile))
        loop.run_until_complete(future)
    except Exception as e:
        Time = datetime.datetime.utcnow()
        EventType = "Error"
        Function = "make_all_orders"
        Explanation = "Some error occurred while placing orders to exchanges"
        EventText = e
        ExceptionType = type(e)
        print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                            ExceptionType))
    return reqs, responses