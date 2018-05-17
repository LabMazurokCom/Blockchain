from exchange import Exchange
import hashlib
import hmac
import time
import urllib.parse
import base64

class Kraken(Exchange):

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


    def get_order_status(self, order_id):

        # ??????????????????????????????

        # No such option. But we can receive the full list of open orders
        # or the full list of trades.

        return "TODO"


    def get_balance(self, currency=''):

        req = '/0/private/Balance'

        data = self._get_data()

        headers = self._get_headers(data, req)

        url = self.endpoint + req

        return url, headers, data


    def get_min_lot(self):

        #????????????????????????????????

        return "TODO"
