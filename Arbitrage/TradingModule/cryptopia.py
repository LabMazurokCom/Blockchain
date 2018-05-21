from exchange import Exchange
import time
import json
import hashlib
import base64
import urllib.parse
import hmac

class Cryptopia(Exchange):

    def _get_headers(self, req, dt={}):

        url = self.endpoint + req

        nonce = str(int(time.time()))

        data = json.dumps(dt).encode('utf-8')

        m = hashlib.md5()
        m.update(data)
        requestContentBase64String = base64.b64encode(m.digest()).decode('utf-8')
        signature = self.api_key + "POST" + urllib.parse.quote_plus(url).lower() + nonce + requestContentBase64String

        hmacsignature = base64.b64encode(hmac.new(base64.b64decode(self.api_secret), signature.encode('utf-8'), hashlib.sha256).digest())

        header_value = "amx " + self.api_key + ":" + hmacsignature.decode('utf-8') + ":" + nonce


        headers = {
            'Authorization': header_value,
            'Content-Type' : 'application/json; charset=utf-8'
        }

        return headers


    def _get_data(self, dt={}):

        data = json.dumps(dt).encode('utf-8')

        return data

    def place_order(self, price, amount, pair, type, order_type):

        req = '/Api/SubmitTrade'
        url = self.endpoint + req

        dt = {
            'Market': pair,
            'Type': type,
            'Amount': amount
        }
        if (order_type == 'market'):
            dt['Rate'] = price
        else:
            dt['Rate'] = '0'                # !!!!!!!!!!!!!!!!!!!!!!!!!

        data = self._get_data(dt)

        headers = self._get_headers(req, dt)

        return url, headers, data

    def cancel_order(self, order_id):

        req = '/Api/CancelTrade'
        url = self.endpoint + req

        dt = {
            'OrderId': order_id
        }

        headers = self._get_headers(req, dt)

        data = self._get_data(dt)
        # data['OrderId'] = order_id

        return url, headers, data


    def get_order_status(self, order_id):

        # NO SUCH OPTION
        # WHOLE TRADE HISTORY CAN BE TAKEN FROM HERE https://www.cryptopia.co.nz/api/GetTradeHistory
        # LIST OF TRANSACTIONS CAN BE TAKEN FROM HERE https://www.cryptopia.co.nz/api/GetTransactions
        # LIST OF OPEN ORDERS https://www.cryptopia.co.nz/api/GetOpenOrders

        return "TODO"

    def get_balance(self, currency=''):

        req = '/Api/GetBalance'
        url = self.endpoint + req

        dt = {}
        if currency != '':
            dt['Currency'] = currency

        headers = self._get_headers(req, dt)

        data = self._get_data(dt)

        return url, headers, data

    def get_min_lot(self):

        return "TODO"




