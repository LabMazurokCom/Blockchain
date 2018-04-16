import aiohttp
import asyncio
import async_timeout
import os
import time
from random import randint

FETCH_TIMEOUT = 50
DATA = dict()

async def fetch(session, url, name):
    with async_timeout.timeout(FETCH_TIMEOUT):
        async with session.get(url) as response:
            response_json = await response.json(content_type=None)
            return name, response_json


async def main(loop):
    urls = ["https://api.binance.com/api/v1/depth?symbol=BTCUSDT&limit=50",
            "https://www.bitstamp.net/api/v2/order_book/btcusd/",
            "https://cex.io/api/order_book/BTC/USD/?depth=50",
            "https://api.exmo.com/v1/order_book/?pair=BTC_USD&limit=50",
            "https://api.gdax.com/products/BTC-USD/book?level=2",
            "https://api.kucoin.com/v1/open/orders?symbol=BTC-USDT&limit=50"]
    names = ["binance", "bitstamp", "cex", "exmo", "gdax", "kucoin"]
    async with aiohttp.ClientSession(loop=loop) as session:
        tasks = []
        for url, name in zip(urls, names):
            tasks.append(fetch(session, url, name))
        return await asyncio.gather(*tasks)


if __name__ == '__main__':
    with open('logs.txt', 'a+') as logs, open('error.txt', 'a+') as errors:
        i = 0
        while i < 10:
            i += 1
            start = time.time()
            loop = asyncio.get_event_loop()
            # loop.run_until_complete(main(loop))
            try:
                data = loop.run_until_complete(asyncio.wait_for(main(loop), 50))
            except asyncio.TimeoutError:
                logs.write('TimeoutError occurred at {}'.format(time.time()))
            finally:
                print(i, '{:.3f}'.format(time.time() - start))