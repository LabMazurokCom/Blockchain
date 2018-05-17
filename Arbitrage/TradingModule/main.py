import aiohttp
import asyncio
from cex import CEX
from exmo import EXMO
from kraken import Kraken
import time
import configs as cf

cex = CEX(cf.cex_endpoint, cf.cex_api_key, cf.cex_api_secret, cf.cex_id)
exmo = EXMO(cf.exmo_endpoint, cf.exmo_api_key, cf.exmo_api_secret)
kraken = Kraken(cf.kraken_endpoint, cf.kraken_api_key, cf.kraken_api_secret)

exchs = [cex, exmo, kraken]

async def fetch(url, session, headers, data):
    async with session.post(url, headers=headers, data=data) as response:
        return await response.text()

async def run():
    tasks = []
    start = time.time()
    async with aiohttp.ClientSession() as session:
        for e in exchs:
            url, headers, data = e.get_balance()
            task = asyncio.ensure_future(fetch(url, session, headers, data))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        print(time.time() - start)
        for x in responses:
            print(x)


loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run())
loop.run_until_complete(future)
#loop.run_until_complete(run())