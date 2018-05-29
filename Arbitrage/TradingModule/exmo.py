from exchange import Exchange
import hashlib
import hmac
import time
import urllib.parse
import requests
import json

class EXMO(Exchange):

    def _get_headers(self, data):

        H = hmac.new(key=bytes(self.api_secret, encoding='utf-8'), digestmod=hashlib.sha512)
        H.update(data.encode('utf-8'))
        sign = H.hexdigest()

        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "key": self.api_key,
            "Sign": sign
        }

        return headers


    def _get_data(self):
        nonce = int(round(time.time() * 1000))

        data = {}
        data['nonce'] = nonce

        return data


    def place_order(self, price, amount, pair, type, order_type):

        data = self._get_data()
        data["pair"] = pair
        data["quantity"] = amount
        if order_type != 'market':
            data["price"] = price
            data["type"] = type
        else:
            data["price"] = '0'
            data["type"] = 'market_' + type
        data = urllib.parse.urlencode(data)

        headers = self._get_headers(data)

        url = self.endpoint + '/v1/order_create'

        return url, headers, data


    def cancel_order(self, order_id):

        data = self._get_data()
        data["order_id"] = order_id
        data = urllib.parse.urlencode(data)

        headers = self._get_headers(data)

        url = self.endpoint + '/v1/order_cancel'

        return url, headers, data


    def get_order_status(self, order_id=''):

        data = self._get_data()
        data = urllib.parse.urlencode(data)

        headers = self._get_headers(data)

        url = self.endpoint + '/v1/user_open_orders'

        return url, headers, data


    def get_balance(self, currency=''):

        data = self._get_data()
        data = urllib.parse.urlencode(data)

        headers = self._get_headers(data)

        url = self.endpoint + '/v1/user_info'

        return url, headers, data

    def get_balance_from_response(self, response, currency):

        r = json.loads(response)
        return r["balances"][currency]


    def get_min_lot(self, pair):

        r = requests.get(self.endpoint + '/v1/pair_settings').json()
        minlot1 = r[pair]["min_quantity"]
        minlot2 = r[pair]["min_amount"]

        return minlot1, minlot2
