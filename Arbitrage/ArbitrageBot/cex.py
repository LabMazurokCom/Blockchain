from exchange import Exchange
import time
import hmac
import hashlib
import requests
import json
import os
import datetime
import aiohttp

File = os.path.basename(__file__)

TIMEOUT = 10


class CEX(Exchange):

    def __init__(self, endpoint, api_key, api_secret, id):
        """
        constructor
        :param endpoint: general address for api requests
        :param api_key: account api key
        :param api_secret: account api secret
        :param id: account id
        """
        self.endpoint = endpoint
        self.api_key = api_key
        self.api_secret = api_secret
        self.id = id
        self.min_lots = {}


    def _get_headers(self):
        """
        generates headers for general api post request
        :return: empty headers
        """

        return {}


    def _get_data(self):
        """
        generates data to write to body of general api post request
        :return: dictionary with data, containing api_key, signature and nonce
        """

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
        """
        generates url, headers and data to make api post request for placing order
        :param price: price of order in quote value
        :param amount: amount of order in base value
        :param pair: trading pair
        :param type: buy/sell
        :param order_type: market/limit
        :return: url, headers, data and auth for post request
        """

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

        return url, headers, data, aiohttp.BasicAuth('', '')


    def cancel_order(self, order_id):
        """
        generates url, headers and data to make api post request for cancelling order
        :param order_id: id of order to be cancelled
        :return: url, headers, data and auth to make api post request for cancelling order
        """

        headers = self._get_headers()

        data = self._get_data()
        data["id"] = order_id

        url = self.endpoint + '/cancel_order/'

        return url, headers, data, aiohttp.BasicAuth('', '')


    def get_order_status(self, order_id):
        """
        is not used. to be written later
        :param order_id:
        :return:
        """

        headers = self._get_headers()

        data = self._get_data()
        data["id"] = order_id

        url = self.endpoint + '/get_order/'

        r = requests.post(url, headers=headers, data=data)
        ans = json.loads(r.text)

        was = ans["amount"]
        remains = ans["pending"]
        if ans["status"] == 'd':
            status = 'done'
        elif ans["status"] == 'a':
            status = 'active'

        return status, was, remains


    def get_balance(self, currency=''):
        """
        generates url, headers and data
        :param currency: is not used. it is needed for universal function signature
        :return: url, headers, data and auth for api post request to get list balances
        """

        headers = self._get_headers()

        data = self._get_data()

        url = self.endpoint + '/balance/'

        return url, headers, data, aiohttp.BasicAuth('', '')


    def get_balance_from_response(self, response, currency):
        """
        handles json response from cex to get balance for given currency
        :param response: json response from cex
        :param currency: currency to get balance for
        :return: float balance for given currency
        """
        if response is not None:
            try:
                r = json.loads(response)
                return r[currency]["available"]
            except KeyError as e:
                Time = datetime.datetime.utcnow()
                EventType = "KeyError"
                Function = "get_balance_from_response"
                Explanation = "CEX failed to response, balance of {} is unknown".format(currency)
                EventText = e
                ExceptionType = type(e)
                print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                                    ExceptionType))
                return 0.0
            except Exception as e:
                Time = datetime.datetime.utcnow()
                EventType = "Error"
                Function = "get_balance_from_response"
                Explanation = "Response from CEX is not a valid json"
                EventText = e
                ExceptionType = type(e)
                print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                                    ExceptionType))
                return 0.0
        else:
            return 0.0


    def get_all_min_lots(self):
        """
        gets minimum order volumes for all tradable pairs
        :return: None
        """
        try:
            r = requests.get(self.endpoint + '/currency_limits', timeout=TIMEOUT).json()

            for x in r["data"]["pairs"]:
                self.min_lots[x["symbol1"] + '/' + x["symbol2"]] = (float(x["minLotSize"]), float(x["minLotSizeS2"]))

        except requests.exceptions.Timeout as e:
            Time = datetime.datetime.utcnow()
            EventType = "RequestsExceptionTimeoutError"
            Function = "get_all_min_lots"
            Explanation = "Response from CEX for currency_limits took too long"
            EventText = e
            ExceptionType = type(e)
            print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                                ExceptionType))
        except json.JSONDecodeError as e:
            Time = datetime.datetime.utcnow()
            EventType = "JSONDecodeError"
            Function = "get_all_min_lots"
            Explanation = "Response from CEX for currency_limits has wrong JSON"
            EventText = e
            ExceptionType = type(e)
            print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                                ExceptionType))
        except Exception as e:
            Time = datetime.datetime.utcnow()
            EventType = "Error"
            Function = "get_all_min_lots"
            Explanation = "Unable to get currency limits from CEX"
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
            return self.min_lots[pair]
        except KeyError as e:
            Time = datetime.datetime.utcnow()
            EventType = "KeyError"
            Function = "get_min_lot"
            Explanation = "Response from CEX for currency_limits doesn't contain required fields"
            EventText = e
            ExceptionType = type(e)
            print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                                ExceptionType))