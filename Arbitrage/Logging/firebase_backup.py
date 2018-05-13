import json
import pyrebase
import requests
from pprint import pprint
requests.packages.urllib3.disable_warnings()


for path in ['log_eth_btc', 'tech_eth_btc', 'log_eth_usd', 'tech_eth_usd', 'log_btc_usdt', 'tech_btc_usdt']:
    url = 'https://test-logger-96bb2.firebaseio.com/{}.json'.format(path)
    local_filename = path + '.json'

    config = {
        "apiKey": "AIzaSyDCoIgcgO-qUsc0OYXTN4hbDl0rqQhb7j8",
        "authDomain": "test-logger-96bb2.firebaseapp.com",
        "databaseURL": "https://test-logger-96bb2.firebaseio.com",
        "storageBucket": "test-logger-96bb2.appspot.com",
        "serviceAccount": "firebase_config.json"
    }
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    # db.remove()
    # break

    print('Start')
    with open(local_filename, 'w') as f:
        print('Opened file:', local_filename)
        keys = sorted(db.child(path).shallow().get().val())
        N = len(keys)
        print('There are {} entries in database'.format(N))
        m = 15000
        s = 0
        cur_i = 0
        print('{', file=f)
        while cur_i < N:
            s += m
            print('{:.2f}'.format(s / N))
            next_i = min(N-1, cur_i + m)
            r = requests.get('https://test-logger-96bb2.firebaseio.com/{}.json?orderBy="$key"&startAt="{}"&endAt="{}"'.format(path, keys[cur_i], keys[next_i]))
            r = r.json()
            r_keys = list(r.keys())
            n = len(r_keys)
            for k in range(n-1):
                print('"', end='', file=f)
                print(r_keys[k], end='', file=f)
                print('": ', end='', file=f)
                json.dump(r[r_keys[k]], f)
                print(',', file=f)
            print('"{}": '.format(r_keys[n-1]), end='', file=f)
            json.dump(r[r_keys[n-1]], f)
            cur_i = next_i
            if cur_i != N-1:
                print(',', file=f)
            else:
                break
        print('\n}', file=f)
        print('End')