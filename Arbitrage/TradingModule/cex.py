from exchange import Exchange
import time
import hmac
import hashlib
import requests
import json


TIMEOUT = 5


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

        headers = self._get_headers()

        data = self._get_data()

        url = self.endpoint + '/balance/'

        return url, headers, data


    def get_balance_from_response(self, response, currency):
        if response is not None:
            try:
                r = json.loads(response)
                return r[currency]["available"]
            except KeyError:
                print("CEX failed to response, balance of {} is unknown".format(currency))
                return 0.0
            except:
                print("Response from CEX is not a valid json")
                return 0.0
        else:
            return 0.0


    def get_min_lot(self, pair):
        try:
            r = requests.get(self.endpoint + '/currency_limits', timeout=TIMEOUT).json()
            syms = pair.split('/')
            sym1 = syms[0]
            sym2 = syms[1]
            minlot1 = 0
            minlot2 = 0

            for x in r["data"]["pairs"]:
                if x["symbol1"] == sym1 and x["symbol2"] == sym2:
                    minlot1 = float(x["minLotSize"])
                    minlot2 = float(x["minLotSizeS2"])
                    break

            return minlot1, minlot2
        except requests.exceptions.Timeout:
            print("Response from CEX for currency_limits took too long")
        except json.JSONDecodeError:
            print("Response from CEX for currency_limits has wrong JSON")
        except KeyError:
            print("Response from CEX for currency_limits doesn't contain required fields")
        except Exception as e:
            print("Unable to get currency limits from CEX")
            print(type(e))
            print(e)
