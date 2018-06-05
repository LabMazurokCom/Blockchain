from exchange import Exchange
import hashlib
import hmac
import time
import urllib.parse
import base64
import requests
import json

class Kraken(Exchange):

    cur_limits = {
        "rep": 0.3,
        "btc": 0.002,
        "bch": 0.002,
        "dash": 0.03,
        "doge": 3000,
        "eos": 3,
        "eth": 0.02,
        "etc": 0.3,
        "gno": 0.03,
        "icn": 2,
        "ltc": 0.1,
        "mln": 0.1,
        "xmr": 0.1,
        "xrp": 30,
        "xlm": 30,
        "zec": 0.03,
        "usdt": 5
    }


    def _get_headers(self, data, req):

        postdata = urllib.parse.urlencode(data)
        encoded = (str(data['nonce']) + postdata).encode()
        msg = req.encode() + hashlib.sha256(encoded).digest()
        H = hmac.new(base64.b64decode(self.api_secret), msg, hashlib.sha512)
        sign = (base64.b64encode(H.digest())).decode()

        headers = {
            'API-key': self.api_key,
            'API-sign': sign
        }

        return headers


    def _get_data(self):
        nonce = int(1000 * time.time())

        data = {
            'nonce': nonce
        }

        return data


    def place_order(self, price, amount, pair, type, order_type):
        data = self._get_data()

        data['pair'] = pair
        data['type'] = type
        data['ordertype'] = order_type
        if order_type != 'market':
            data['price'] = price
        data['volume'] = amount

        req = '/0/private/AddOrder'

        headers = self._get_headers(data, req)

        url = self.endpoint + req

        return url, headers, data


    def cancel_order(self, order_id):
        req = '/0/private/CancelOrder'

        data = self._get_data()
        data['txid'] = order_id

        headers = self._get_headers(data, req)

        url = self.endpoint + req

        return url, headers, data


    def get_order_status(self, order_id=''):
        req = '/0/private/OpenOrders'

        data = self._get_data()

        headers = self._get_headers(data, req)

        url = self.endpoint + req

        return url, headers, data


    def get_balance(self, currency=''):
        req = '/0/private/Balance'

        data = self._get_data()

        headers = self._get_headers(data, req)

        url = self.endpoint + req

        return url, headers, data


    def get_balance_from_response(self, response, currency):
        if response is not None:
            try:
                r = json.loads(response)
                if currency in r['result'].keys():
                    return r['result'][currency]
                else:
                    return 0
            except KeyError:
                print("Kraken failed to response, balance of {} is unknown".format(currency))
                return 0.0
            except:
                print("Response from Kraken is not a valid json")
                return 0.0
        else:
            return 0.0


    def get_min_lot(self, pair):
        curs = pair.split('_')
        cur1 = curs[0]
        cur2 = curs[1]
        if cur2 in self.cur_limits.keys():
            return self.cur_limits[cur1], self.cur_limits[cur2]
        else:
            return self.cur_limits[cur1], 0.0
