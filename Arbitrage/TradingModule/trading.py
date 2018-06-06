import asyncio
import aiohttp
import json
import time
import async_timeout

responses = []
reqs = []

FETCH_TIMEOUT = 5


async def fetch(url, session, headers, data, key):
    try:
        with async_timeout.timeout(FETCH_TIMEOUT):
            start = time.time()
            async with session.post(url, headers=headers, data=data) as response:
                resp_text = await response.text()
                return key, start, time.time(), resp_text
    except asyncio.TimeoutError:
        print("{} didn't respond in time (placing order)".format(key))
        return key, start, time.time(), None
    except Exception as e:
        print("Some error occurred during post request to {} (placing order)".format(key))
        print(type(e))
        print(e)
        return key, start, time.time(), None


async def place_orders(pair, orders, exs, conf):

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
            except KeyError:
                print("Invalid key somewhere *here* in place_orders")
                pass
            global responses
            responses = await asyncio.gather(*tasks)
    except Exception as e:
        print("Client session failed while placing orders to exchanges")
        print(type(e))
        print(e)

'''
async def place_minimal_orders(pair, orders, exs, conffile):

    exchs = {}
    for e in exs:
        exchs[e.__class__.__name__.lower()] = e

    conf = json.load(open(conffile))

    tasks = []
    async with aiohttp.ClientSession() as session:
        # url, headers, data = exchs['cex'].place_order('7504', '0.002', conf['cex']['converter'][pair], 'sell', 'limit')
        # reqs.append(['cex', '7504', '0.002', 'sell'])
        # task = asyncio.ensure_future(fetch(url, session, headers, data))
        # tasks.append('cex', task)

        url, headers, data = exchs['exmo'].place_order('7415', '0.002', conf['exmo']['converter'][pair], 'buy', 'limit')
        reqs.append(['exmo', '7415', '0.002', 'buy'])
        task = asyncio.ensure_future(fetch(url, session, headers, data))
        tasks.append('exmo', task)

        global responses
        responses = await asyncio.gather(*tasks)
'''

def make_all_orders(pair, orders, exchs, conffile):
    global reqs
    reqs = []
    global responses
    responses = []
    try:
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(place_orders(pair, orders, exchs, conffile))
        loop.run_until_complete(future)
    except Exception as e:
        print("Some error occurred while placing orders to exchanges")
        print(type(e))
        print(e)
    return reqs, responses

