from cex import CEX
from exmo import EXMO
from kraken import Kraken
from gdax import Gdax
import aiohttp
import asyncio
import async_timeout
import datetime
import os

balances = {}
limits = {}
exchs = set()
responses = []

FETCH_TIMEOUT = 10

File = os.path.basename(__file__)

def init(pairs, config, credentials, exchanges_names):
    """
    :param pairs: list of pairs to be monitored
    :param config: dict with data about pairs, currencies and API of exchanges
    :param credentials: dict with exchanges' credentials
    :return: list of exchanges' classes and list of minimum allowed ordered volumes
    {
        "exch1" : {
            "pair1" : [minlot1, minlot2],
            "pair2" : [minlot1, minlot2],
            ...
        },
        ...
    }
    """
    try:
        cex = CEX(credentials['cex_endpoint'], credentials['cex_api_key'], credentials['cex_api_secret'], credentials['cex_id'])
        exmo = EXMO(credentials['exmo_endpoint'], credentials['exmo_api_key'], credentials['exmo_api_secret'])
        kraken = Kraken(credentials['kraken_endpoint'], credentials['kraken_api_key'], credentials['kraken_api_secret'])
        gdax = Gdax(credentials['gdax_endpoint'], credentials['gdax_api_key'], credentials['gdax_api_secret'], credentials['gdax_passphrase'])
        all_exchs = {
            "cex": cex,
            "exmo": exmo,
            "gdax": gdax,
            "kraken": kraken
        }

        global exchs
        exchs = set()
        for exch_name in exchanges_names:
            exchs.add(all_exchs[exch_name])
        bad_exchs = set()
        try:
            for e in exchs:
                ename = e.__class__.__name__.lower()
                e.get_all_min_lots()
                limits[ename] = {}
                for pair in pairs:
                    if pair in config[ename]['converter']:
                        if e == kraken:
                            min_lots = e.get_min_lot(pair)
                        else:
                            min_lots = e.get_min_lot(config[ename]['converter'][pair])

                        if min_lots is None:
                            bad_exchs.add(e)
                        else:
                            limits[ename][pair] = min_lots
            for bad_exch in bad_exchs:
                exchs.remove(bad_exch)
        except KeyError as e:
            Time = datetime.datetime.utcnow()
            EventType = "KeyError"
            Function = "init"
            Explanation = "One or more of required keys in configuration file doesn't exist"
            EventText = e
            ExceptionType = type(e)
            print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                                ExceptionType))
            return {}, {}
        except Exception as e:
            Time = datetime.datetime.utcnow()
            EventType = "Error"
            Function = "init"
            Explanation = "Some error occurred while getting minimum lots"
            EventText = e
            ExceptionType = type(e)
            print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                                ExceptionType))
            return {}, {}
        return exchs, limits
    except KeyError as e:
        Time = datetime.datetime.utcnow()
        EventType = "KeyError"
        Function = "init"
        Explanation = "One or more of exchanges' credentials doesn't exist or has incorrect name"
        EventText = e
        ExceptionType = type(e)
        print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                            ExceptionType))
        return {}, {}
    except Exception as e:
        Time = datetime.datetime.utcnow()
        EventType = "Error"
        Function = "init"
        Explanation = "Some error occurred during initialization of exchanges"
        EventText = e
        ExceptionType = type(e)
        print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                            ExceptionType))
        return {}, {}


async def fetch(url, session, headers, data, exch, auth):
    """
    posts request for getting balance
    :param url: url path for getting balance
    :param session: aiohttp session for getting balance
    :param headers: headers of request for getting balance
    :param data: data of requests for getting balance
    :param exch: exchange name for placing order to
    :param auth: authentication data
    :return: text of response from exchange
    """
    try:
        with async_timeout.timeout(FETCH_TIMEOUT):
            if exch == "Gdax":
                async with session.get(url, headers=headers, data=data, auth=auth) as response:
                    return await response.text()
            else:
                async with session.post(url, headers=headers, data=data, auth=auth) as response:
                    return await response.text()
    except asyncio.TimeoutError as e:
        Time = datetime.datetime.utcnow()
        EventType = "Error"
        Function = "fetch"
        Explanation = "{} didn't respond in time (getting balance)".format(exch)
        EventText = e
        ExceptionType = type(e)
        print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                            ExceptionType))
    except Exception as e:
        Time = datetime.datetime.utcnow()
        EventType = "Error"
        Function = "fetch"
        Explanation = "Some error occurred during post request to {} (getting balance)".format(exch)
        EventText = e
        ExceptionType = type(e)
        print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                            ExceptionType))


async def get_bal():
    """
    gets list of balances for every exchange via aiohttp session
    :return: makes list of responses from exchanges
    """
    tasks = []
    global responses
    responses = []
    try:
        async with aiohttp.ClientSession() as session:
            for exch in exchs:
                url, headers, data, auth = exch.get_balance()
                task = asyncio.ensure_future(fetch(url, session, headers, data, exch.__class__.__name__, auth))
                tasks.append(task)
            responses = await asyncio.gather(*tasks)
    except Exception as e:
        Time = datetime.datetime.utcnow()
        EventType = "Error"
        Function = "get_bal"
        Explanation = "ClientSession failed while getting balances from exchanges"
        EventText = e
        ExceptionType = type(e)
        print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                            ExceptionType))


def get_balances(pairs, config):
    """
    gets balances for all currencies from all exchanges
    :param pairs: list of pairs to be potentially traded later
    :param config: JSONified configuration file
    :return: list of balances for all exchanges in format {
                                                             'binance': {
                                                                 'btc': btc_balance,
                                                                 'usd': usd_balance,
                                                                 ...-
                                                             },
                                                             'cex': {
                                                                 'btc': btc_balance,
                                                                 'usd': usd_balance,
                                                                 ...
                                                             },
                                                             ...
                                                         }
    """
    balances_for_db = {}
    global balances
    balances = {}
    currencies = set()
    for pair in pairs:
        curs = pair.split('_')
        currencies.add(curs[0])
        currencies.add(curs[1])
    try:
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(get_bal())
        loop.run_until_complete(future)
    except Exception as e:
        Time = datetime.datetime.utcnow()
        EventType = "Error"
        Function = "get_balances"
        Explanation = "Some error occurred while getting balances from exchanges"
        EventText = e
        ExceptionType = type(e)
        print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                            ExceptionType))
    try:
        for exch in exchs:
            ename = exch.__class__.__name__.lower()
            balances[ename] = {}
            balances_for_db[ename] = {}
            for c in currencies:
                balances[ename][c] = 0.0
                balances_for_db[ename][c] = 0.0
        for r, exch in zip(responses, exchs):
            ename = exch.__class__.__name__.lower()
            ok = False
            for c in currencies:
                if c in config[ename]['currency_converter'].keys():
                    balances[ename][c] = float(exch.get_balance_from_response(r, config[ename]['currency_converter'][c]))
                    if balances[ename][c] != 0.0:
                        ok = True
            if ok:
                for c in balances[ename]:
                    balances_for_db[ename][c] = balances[ename][c]
            else:
                for c in balances[ename]:
                    balances_for_db[ename][c] = -1
        return balances, balances_for_db
    except Exception as e:
        Time = datetime.datetime.utcnow()
        EventType = "Error"
        Function = "get_balances"
        Explanation = "Some error occurred while getting balances"
        EventText = e
        ExceptionType = type(e)
        print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                            ExceptionType))


def get_urls(symbols, conf, limit):
    """
    generates list of urls to be placed via async post requests to get order_books
    :param symbols: list of pairs to get order_books for
    :param conf: JSONified configuration file
    :param limit: number of top orders we need to get
    :return: list of urls and exchange names for every pair in format {
                                                                        "pair1" : {
                                                                                    "urls" : [],
                                                                                    "names" : []
                                                                                  },
                                                                         ...
                                                                      }
    """
    pairs = dict()
    for symbol in symbols:
        pairs[symbol] = dict()
    badsyms = 0
    try:
        for symbol in symbols:
            pairs[symbol]['urls'] = []
            pairs[symbol]['names'] = []
            syms = dict()
            for exch in exchs:
                ename = exch.__class__.__name__.lower()
                try:  # get exchange's symbol for user's symbol
                    sym = conf[ename]["converter"][symbol]
                    syms[ename] = sym
                    pairs[symbol]['urls'].append(conf[ename]["url"].format(sym, limit))
                    pairs[symbol]['names'].append(ename)
                except KeyError as e:
                    Time = datetime.datetime.utcnow()
                    EventType = "KeyError"
                    Function = "get_urls"
                    Explanation = "Configuration file doesn't contain required fields (converter or symbol {})".format(symbol)
                    EventText = e
                    ExceptionType = type(e)
                    print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                                        ExceptionType))
                    pass
            if len(pairs[symbol]['names']) <= 1:
                badsyms += 1
        if badsyms == len(symbols):
            Time = datetime.datetime.utcnow()
            EventType = "EXIT"
            Function = "get_urls"
            Explanation = "None of the given symbols is supported by any exchanges"
            EventText = ""
            ExceptionType = ""
            print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                                ExceptionType))
            exit(1)
    except Exception as e:
        Time = datetime.datetime.utcnow()
        EventType = "Error"
        Function = "get_urls"
        Explanation = "Some error occurred in get_url()"
        EventText = e
        ExceptionType = type(e)
        print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                            ExceptionType))
        exit(1)
    return pairs
