from cex import CEX
from exmo import EXMO
from kraken import Kraken
import json
import aiohttp
import asyncio
import async_timeout
import time


balances = {}
limits = {}
exchs = {}
responses = []

FETCH_TIMEOUT = 2


def init(pairs, config, credentials):
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
        global exchs
        exchs = {cex, exmo, kraken}
        try:
            for e in exchs:
                ename = e.__class__.__name__.lower()
                limits[ename] = {}
                for pair in pairs:
                    if pair in config[ename]['converter'].keys():
                        if e == kraken:
                            min_lots = e.get_min_lot(pair)
                        else:
                            min_lots = e.get_min_lot(config[ename]['converter'][pair])

                        if min_lots is None:
                            exchs.remove(e)
                        else:
                            limits[ename][pair] = min_lots
        except KeyError:
            print("One or more of required keys in configuration file doesn't exist")
            return {}, {}
        except Exception as e:
            print("Some error occurred while getting minimum lots")
            print(type(e))
            print(e)
            return {}, {}
        return exchs, limits
    except KeyError:
        print("One or more of exchanges' credentials doesn't exist or has incorrect name in")
        return {}, {}
    except Exception as e:
        print("Some error occurred during initialization of exchanges")
        print(type(e))
        print(e)
        return {}, {}


async def fetch(url, session, headers, data, exch):
    try:
        with async_timeout.timeout(FETCH_TIMEOUT):
            async with session.post(url, headers=headers, data=data) as response:
                return await response.text()
    except asyncio.TimeoutError:
        print("{} didn't respond in time (getting balance)".format(exch))
    except Exception as e:
        print("Some error occurred during post request to {} (getting balance)".format(exch))
        print(type(e))
        print(e)


async def get_bal():
    tasks = []
    try:
        async with aiohttp.ClientSession() as session:
            for exch in exchs:
                url, headers, data = exch.get_balance()
                task = asyncio.ensure_future(fetch(url, session, headers, data, exch.__class__.__name__))
                tasks.append(task)
            global responses
            responses = await asyncio.gather(*tasks)
    except Exception as e:
        print("ClientSession failed while getting balances from exchanges")
        print(type(e))
        print(e)


def get_balances(pairs, config):
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
        print("Some error occurred while getting balances from exchanges")
        print(type(e))
        print(e)

    try:
        for exch in config.keys():
            balances[exch] = {}
            for c in currencies:
                balances[exch][c] = 0.0
        for r, exch in zip(responses, exchs):
            ename = exch.__class__.__name__.lower()
            for c in currencies:
                if c in config[ename]['currency_converter'].keys():
                    balances[ename][c] = float(
                        exch.get_balance_from_response(r, config[ename]['currency_converter'][c]))
        return balances
    except Exception as e:
        print("Some error occurred while getting balances")
        print(type(e))
        print(e)


# start = time.time()
# init(['btc_usd', 'eth_usd'], "orders_config.json", "exchs_credentials.json")
# print(get_balances(['btc_usd', 'eth_usd'], "orders_config.json"))
# print('{:.3f}'.format(time.time() - start))
