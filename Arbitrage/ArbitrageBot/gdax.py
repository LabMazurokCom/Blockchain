from exchange import Exchange
import time
import base64
import hmac
import hashlib
import requests
from requests.auth import AuthBase
from pprint import pprint
import json
import os
import datetime
import aiohttp

File = os.path.basename(__file__)

TIMEOUT = 10

class GdaxAuth(aiohttp.BasicAuth):

    def __init__(self, api_key, api_secret, passphrase):
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase

    def __call__(self, r):
        nonce = str(time.time())
        msg = nonce + r.method + r.path_url + ''
        msg = msg.encode('ascii')
        hmac_key = base64.b64decode(self.api_secret)
        signature = hmac.new(hmac_key, msg, hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest()).decode('ascii')
        r.headers.update({
            'Content-Type': "application/json",
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': nonce,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase
        })
        return r


class Gdax(Exchange):

    def __init__(self, endpoint, api_key, api_secret, passphrase):
        """
        constructor
        :param endpoint: general address for api requests
        :param api_key: account api key
        :param api_secret: account api secret
        :param passphrase: account passphrase
        """
        self.endpoint = endpoint
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase
        self.min_lots = {}

    def _get_headers(self, method, req, body):
        """
        generates headers for general api post request
        :return: None
        """
        nonce = str(time.time())
        msg = nonce + method + req + body
        msg = msg.encode('utf-8')
        hmac_key = base64.b64decode(self.api_secret)
        signature = hmac.new(hmac_key, msg, hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest()).decode('utf-8')
        headers = {
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': nonce,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': "application/json"
        }
        return headers

    def _get_auth(self):
        auth = GdaxAuth(self.api_key, self.api_secret, self.passphrase)
        return auth

    def _get_data(self):
        """
        generates data to write to body of general api post request
        :return: empty dictionary
        """

        return {}


    def place_order(self, price, amount, pair, type, order_type):
        """
        generates url, headers, data and auth to make api post request for placing order
        :param price: price of order in quote value
        :param amount: amount of order in base value
        :param pair: trading pair
        :param type: buy/sell
        :param order_type: market/limit
        :return: url, headers, data and auth for post request
        """

        data = self._get_data()
        data["type"] = order_type
        data["side"] = type
        data["size"] = amount
        if order_type != 'market':
            data["price"] = price
        data["product_id"] = pair
        headers = self._get_headers('POST', '/orders', json.dumps(data))



        auth = None
        url = self.endpoint + 'orders'

        return url, headers, json.dumps(data), auth


    def cancel_order(self, order_id):
        """
        generates url, headers and data to make api post request for cancelling order
        :param order_id: id of order to be cancelled
        :return: url, headers, data and auth to make api post request for cancelling order
        """

        data = self._get_data()
        headers = self._get_headers('DELETE', '/orders/{}'.format(order_id), '')

        auth = None
        url = self.endpoint + 'orders/{}'.format(order_id)
        return url, headers, data, auth

    #
    # def get_order_status(self, order_id):
    #     """
    #     is not used. to be written later
    #     :param order_id:
    #     :return:
    #     """
    #
    #     headers = self._get_headers()
    #
    #     data = self._get_data()
    #     data["id"] = order_id
    #
    #     url = self.endpoint + '/get_order/'
    #
    #     r = requests.post(url, headers=headers, data=data)
    #     ans = json.loads(r.text)
    #
    #     was = ans["amount"]
    #     remains = ans["pending"]
    #     if ans["status"] == 'd':
    #         status = 'done'
    #     elif ans["status"] == 'a':
    #         status = 'active'
    #
    #     return status, was, remains
    #
    #
    def get_balance(self, currency=''):
        """
        generates url, headers, data and auth
        :param currency: is not used. it is needed for universal function signature
        :return: url, headers, data and auth for api post request to get list balances
        """

        headers = self._get_headers('GET', '/accounts', '')
        data = self._get_data()
        url = self.endpoint + 'accounts'
        auth = None
        return url, headers, data, auth


    def get_balance_from_response(self, response, currency):
        """
        handles json response from gdax to get balance for given currency
        :param response: json response from gdax
        :param currency: currency to get balance for
        :return: float balance for given currency
        """
        if response is not None:
            response = json.loads(response)
            try:
                for resp in response:
                    if resp['currency'] == currency:
                        return float(resp['available'])
            except KeyError as e:
                Time = datetime.datetime.utcnow()
                EventType = "KeyError"
                Function = "get_balance_from_response"
                Explanation = "Gdax failed to response, balance of {} is unknown".format(currency)
                EventText = e
                ExceptionType = type(e)
                print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                                    ExceptionType))
                return 0.0
            except Exception as e:
                Time = datetime.datetime.utcnow()
                EventType = "Error"
                Function = "get_balance_from_response"
                Explanation = "Response from Gdax is not a valid json"
                EventText = e
                ExceptionType = type(e)
                print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                                    ExceptionType))
                return 0.0
        else:
            return 0.0


    def get_all_min_lots(self):
        """
        gets minimum order volumes for all tradable currencies
        :return: None
        """
        try:
            r = requests.get(self.endpoint + 'products', timeout=TIMEOUT).json()

            for x in r:
                self.min_lots[x["base_currency"]] = float(x["base_min_size"])

        except requests.exceptions.Timeout as e:
            Time = datetime.datetime.utcnow()
            EventType = "RequestsExceptionTimeoutError"
            Function = "get_all_min_lots"
            Explanation = "Response from Gdax for currency_limits took too long"
            EventText = e
            ExceptionType = type(e)
            print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                                ExceptionType))
        except json.JSONDecodeError as e:
            Time = datetime.datetime.utcnow()
            EventType = "JSONDecodeError"
            Function = "get_all_min_lots"
            Explanation = "Response from Gdax for currency_limits has wrong JSON"
            EventText = e
            ExceptionType = type(e)
            print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                                ExceptionType))
        except Exception as e:
            Time = datetime.datetime.utcnow()
            EventType = "Error"
            Function = "get_all_min_lots"
            Explanation = "Unable to get currency limits from Gdax"
            EventText = e
            ExceptionType = type(e)
            print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                                ExceptionType))

    def get_min_lot(self, pair):
        """
        gets minimum order volumes for base_currency and quote_currency of given pair
        :param pair: pair to get minimum volumes for
        :return: two floats - volume for base_currency and volume for quote_currency
                 None if Cex didn't response or some other error occurred
        """
        try:
            sym1, sym2 = pair.split('-')
            if sym2 in self.min_lots.keys():
                return self.min_lots[sym1], self.min_lots[sym2]
            else:
                return self.min_lots[sym1], 0
        except KeyError as e:
            Time = datetime.datetime.utcnow()
            EventType = "KeyError"
            Function = "get_min_lot"
            Explanation = "Response from Gdax for currency_limits doesn't contain required fields"
            EventText = e
            ExceptionType = type(e)
            print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                                ExceptionType))

    def get_open_orders(self):
        """
        generates url, headers, data and auth to get list of open orders
        :return: url, headers, data and auth to get list of open orders
        """
        headers = self._get_headers('GET', '/orders', '')
        data = self._get_data()
        url = self.endpoint + 'orders'
        auth = None
        return url, headers, data, auth

    def cancel_open_orders(self, open_orders):
        """
        generates list of urls, headers, data, and auths to cancel all open orders
        :param open_orders: response from exchange with open orders
        :return: list of urls, headers, data, and auths to cancel all open orders
        """
        headers = self._get_headers('DELETE', '/orders', '')
        data = self._get_data()
        url = self.endpoint + 'orders'
        auth = None

        return [(url, headers, data, auth)]