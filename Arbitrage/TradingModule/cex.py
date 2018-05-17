from exchange import Exchange
import time
import hmac
import hashlib

class CEX(Exchange):

    def __init__(self, endpoint, api_key, api_secret, id):
        self.endpoint = endpoint
        self.api_key = api_key
        self.api_secret = api_secret
        self.id = id


    def _get_headers(self):

        return {}


    def _get_data(self):

        nonce = int(round(time.time() * 1000))

        params = str(nonce) + self.id + self.api_key
        params = bytes(params, encoding='utf-8')

        H = hmac.new(bytes(self.api_secret, encoding='utf-8'), params, digestmod = hashlib.sha256)
        sign = H.hexdigest().upper()

        data = {
            "key": self.api_key,
            "signature": sign,
            "nonce": str(nonce)
        }

        return data


    def place_order(self, price, amount, pair, type, order_type):

        headers = self._get_headers()

        data = self._get_data()
        data["type"] = type
        data["order_type"] = order_type
        data["amount"] = amount
        if order_type != 'market':
            data["price"] = price

        pos = pair.find('/')
        sym1 = pair[0:pos]
        sym2 = pair[pos + 1:]

        url = self.endpoint + '/place_order/{}/{}'.format(sym1, sym2)

        return url, headers, data


    def cancel_order(self, order_id):

        headers = self._get_headers()

        data = self._get_data()
        data["id"] = order_id

        url = self.endpoint + '/cancel_order/'

        return url, headers, data


    def get_order_status(self, order_id):

        headers = self._get_headers()

        data = self._get_data()
        data["id"] = order_id

        url = self.endpoint + '/get_order/'

        return url, headers, data


    def get_balance(self, currency=''):

        headers = self._get_headers()

        data = self._get_data()

        url = self.endpoint + '/balance/'

        return url, headers, data


    def get_min_lot(self):

        #????????????????????????????????

        return "TODO"