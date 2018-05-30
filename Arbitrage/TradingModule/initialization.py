from cex import CEX
from exmo import EXMO
from kraken import Kraken
import json
import aiohttp
import asyncio


balances = {}
limits = {}
exchs = []
responses = []


def init(pairs, conffile, exchsfile):
    cf = json.load(open(exchsfile))
    cex = CEX(cf['cex_endpoint'], cf['cex_api_key'], cf['cex_api_secret'], cf['cex_id'])
    exmo = EXMO(cf['exmo_endpoint'], cf['exmo_api_key'], cf['exmo_api_secret'])
    kraken = Kraken(cf['kraken_endpoint'], cf['kraken_api_key'], cf['kraken_api_secret'])

    global exchs
    exchs = [cex, exmo, kraken]

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

    return exchs, limits


async def fetch(url, session, headers, data):
    async with session.post(url, headers=headers, data=data) as response:
        return await response.text()


async def get_bal():

    tasks = []
    async with aiohttp.ClientSession() as session:
        for e in exchs:
            url, headers, data = e.get_balance()
            task = asyncio.ensure_future(fetch(url, session, headers, data))
            tasks.append(task)

        global responses
        responses = await asyncio.gather(*tasks)


def get_balances(pairs, conffile):

    currencies = set()
    for x in pairs:
        pos = x.find('_')
        currencies.add(x[:pos])
        currencies.add(x[pos + 1:])

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_bal())
    loop.run_until_complete(future)

    with open(conffile, 'r') as fp:
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

    return balances
