from exchange import Exchange
import hashlib
import hmac
import time
import urllib.parse
import base64
import os
import datetime
import json

File = os.path.basename(__file__)

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
        """
        generates headers for general api post request
        :param data: data to be included into headers
        :param req: part of url after endpoint, like '/0/private/OpenOrders'
        :return: dictionary with headers containing api key and sign
        """
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
        """
        generates data of general api post request
        :return: dictionary with data, containing nonce
        """
        nonce = int(1000 * time.time())

        data = {
            'nonce': nonce
        }

        return data


    def place_order(self, price, amount, pair, type, order_type):
        """
        generates url, headers and data for api post request to place order
        :param price: price of order in quote amount
        :param amount: volume of order in base amount
        :param pair: trading pair
        :param type: buy/sell
        :param order_type: market/limit
        :return: url, headers and data for api post request to place order
        """
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
        """
        generates url, headers and data for api post request to cancel order
        :param order_id: id of order to be cancelled
        :return: url, headers and data for api post request to cancel order
        """
        req = '/0/private/CancelOrder'

        data = self._get_data()
        data['txid'] = order_id

        headers = self._get_headers(data, req)

        url = self.endpoint + req

        return url, headers, data


    def get_order_status(self, order_id=''):
        """
        isnt' used. to be writter later
        :param order_id:
        :return:
        """
        req = '/0/private/OpenOrders'

        data = self._get_data()

        headers = self._get_headers(data, req)

        url = self.endpoint + req

        return url, headers, data


    def get_balance(self, currency=''):
        """
        generates url, headers and data for api post requests to get list of balances
        :param currency: isn't used. it is needed for universal function signature
        :return: url, headers and data for api post requests to get list of balances
        """
        req = '/0/private/Balance'

        data = self._get_data()

        headers = self._get_headers(data, req)

        url = self.endpoint + req

        return url, headers, data


    def get_balance_from_response(self, response, currency):
        """
        handles json response from kraken to get balance for given currency
        :param response: json response from kraken
        :param currency: currency to get balance for
        :return: float balance for given currency
        """
        if response is not None:
            try:
                r = json.loads(response)
                if currency in r['result'].keys():
                    return r['result'][currency]
                else:
                    return 0.0
            except KeyError as e:
                Time = datetime.datetime.utcnow()
                EventType = "KeyError"
                Function = "get_balance_from_response"
                Explanation = "Kraken failed to response, balance of {} is unknown".format(currency)
                EventText = e
                ExceptionType = type(e)
                print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                                    ExceptionType))
                return 0.0
            except Exception as e:
                Time = datetime.datetime.utcnow()
                EventType = "Error"
                Function = "get_balance_from_response"
                Explanation = "Response from Kraken is not a valid json"
                EventText = e
                ExceptionType = type(e)
                print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                                    ExceptionType))
                return 0.0
        else:
            return 0.0


    def get_min_lot(self, pair):
        """
        gets minimum order volumes for base_currency and quote_currency of given pair
        :param pair: pair to get minimum volumes for
        :return: two floats - volume for base_currency and volume for quote_currency
        """
        curs = pair.split('_')
        cur1 = curs[0]
        cur2 = curs[1]
        if cur2 in self.cur_limits.keys():
            return self.cur_limits[cur1], self.cur_limits[cur2]
        else:
            return self.cur_limits[cur1], 0.0