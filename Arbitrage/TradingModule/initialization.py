from cex import CEX
from exmo import EXMO
from kraken import Kraken
import json
import aiohttp
import asyncio
import async_timeout


balances = {}
limits = {}
exchs = {}
responses = []

FETCH_TIMEOUT = 5

def init(pairs, conffile, exchsfile):
    try:
        cf = json.load(open(exchsfile))
        cex = CEX(cf['cex_endpoint'], cf['cex_api_key'], cf['cex_api_secret'], cf['cex_id'])
        exmo = EXMO(cf['exmo_endpoint'], cf['exmo_api_key'], cf['exmo_api_secret'])
        kraken = Kraken(cf['kraken_endpoint'], cf['kraken_api_key'], cf['kraken_api_secret'])

        global exchs
        exchs = [cex, exmo, kraken]

        try:
            with open(conffile, 'r') as fp:
                ocf = json.load(fp)

                for e in exchs:
                    ename = e.__class__.__name__.lower()
                    limits[ename] = {}
                    for p in pairs:
                        if p in ocf[ename]['converter'].keys():
                            if e == kraken:
                                ml1, ml2 = e.get_min_lot(p)
                            else:
                                ml1, ml2 = e.get_min_lot(ocf[ename]['converter'][p])
                            limits[ename][p] = [float(ml1), float(ml2)]
        except FileNotFoundError:
            print("Exchanges' configuration file doesn't exist or bot_config.json contains wrong name")
            return {}, {}
        except KeyError:
            print("One or more of required keys in exchanges configuration file doesn't exist")
            return {}, {}
        except Exception as e:
            print(type(e))
            print(e)
            return {}, {}

        return exchs, limits
    except FileNotFoundError:
        print("Exchanges' credentials file doesn't exist or bot_config.json contains wrong name")
        return {}, {}
    except KeyError:
        print("One or more of exchanges' credentials doesn't exist or has incorrect name")
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
        return "{} didn't respond in time".format(exch)
    except:
        return "Some error occurred during post request to {}".format(exch)


async def get_bal():

    tasks = []
    try:
        async with aiohttp.ClientSession() as session:
            for e in exchs:
                url, headers, data = e.get_balance()
                task = asyncio.ensure_future(fetch(url, session, headers, data, e.__class__.__name__))
                tasks.append(task)

            global responses
            responses = await asyncio.gather(*tasks)
    except:
        print("ClientSession failed while getting balances from exchanges")


def get_balances(pairs, conffile):

    currencies = set()
    for x in pairs:
        pos = x.find('_')
        if(pos == -1):
            print("Wrong format of pair {} in bot_config.json".format(x))
            continue
        else:
            currencies.add(x[:pos])
            currencies.add(x[pos + 1:])

    try:
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(get_bal())
        loop.run_until_complete(future)
    except:
        print("Some error occurred while getting balances from exchanges")

    #for r in responses:
    #    print(r)

    #print()

    try:
        with open(conffile, 'r') as fp:
            try:
                ocf = json.load(fp)
                for e in ocf.keys():
                    balances[e] = {}
                    for c in currencies:
                        balances[e][c] = 0.0
                for r, e in zip(responses, exchs):
                    ename = e.__class__.__name__.lower()
                    for c in currencies:
                        if c in ocf[ename]['currency_converter'].keys():
                            balances[ename][c] = float(e.get_balance_from_response(r, ocf[ename]['currency_converter'][c]))
            except:
                print("Exchanges' configuration file is not a valid json")
    except FileNotFoundError:
        print("Wrong name of exchanges' configuration file")
    except Exception as ex:
        print(type(ex))
        print(ex)

    return balances