import aiohttp
import async_timeout
import asyncio
import datetime
import os
import time

File = os.path.basename(__file__)


responses = []
reqs = []

FETCH_TIMEOUT = 5


async def fetch(url, session, headers, data, key):
    """
    Sends POST request to make an order
    :param url: url path for placing order
    :param session: aiohttp session to place order
    :param headers: headers of post request to place order
    :param data: data of post request to place order
    :param key: exchange name
    :return: exchange name, time of start and end of post request, response from exchange
    """
    try:
        with async_timeout.timeout(FETCH_TIMEOUT):
            start = time.time()
            async with session.post(url, headers=headers, data=data) as response:
                resp_text = await response.text()
                return key, start, time.time(), resp_text
    except asyncio.TimeoutError as e:
        Time = datetime.datetime.utcnow()
        EventType = "TimeoutError"
        Function = "fetch"
        Explanation = "{} didn't respond in time (placing order)".format(key)
        EventText = e
        ExceptionType = type(e)
        print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText, ExceptionType))
        return key, start, time.time(), None
    except Exception as e:
        Time = datetime.datetime.utcnow()
        EventType = "Error"
        Function = "fetch"
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
                    url, headers, data = exchs[key].place_order(str(value[0]), str(value[1]), conf[key]['converter'][pair], 'sell', 'limit')
                    reqs.append([key, str(value[0]), str(value[1]), 'sell'])
                    task = asyncio.ensure_future(fetch(url, session, headers, data, key))
                    tasks.append(task)
                for key, value in orders['buy'].items():
                    url, headers, data = exchs[key].place_order(str(value[0]), str(value[1]), conf[key]['converter'][pair], 'buy', 'limit')
                    reqs.append([key, str(value[0]), str(value[1]), 'buy'])
                    task = asyncio.ensure_future(fetch(url, session, headers, data, key))
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