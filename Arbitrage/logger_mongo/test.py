# a = sorted(['bch_btc', 'bch_usd', 'dash_btc', 'eth_btc', 'btc_usd', 'xrp_btc', 'dash_usd', 'eth_usd', 'xrp_usd'])
# for x in a:
#     print('"{}"'.format(x))

import requests
from pprint import pprint
r = requests.get('http://0.0.0.0:5000/?pair=bch_btc') #&pretty=1')
pprint(r.headers)