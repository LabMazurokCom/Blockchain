import json


def generate_pairs(currencies, exchanges, verbose=False):
    """
    Generates list of pairs among given currencies such that each pair is traded on each given exchange.
    """
    d = json.load(open('orders_config.json'))
    n = len(currencies)
    result = []
    for i in range(n):
        for j in range(i+1, n):
            cur1 = currencies[i]
            cur2 = currencies[j]
            pair = cur1 + '_' + cur2
            if verbose:
                print('\t', pair)
            ok = True
            for exch in exchanges:
                if verbose:
                    print(exch, end='')
                    if pair not in d[exch]['converter']:
                        ok = False
                        print(' --')
                    else:
                        print(' +')
                else:
                    if pair not in d[exch]['converter']:
                        ok = False
                        break
            if ok:
                result.append(pair)
    return result


currencies = ['btc', 'bch', 'usd', 'eth', 'xrp', 'dash', 'ltc', 'xmr', 'xlm']
exchanges = ['cex', 'exmo', 'kraken']
res = generate_pairs(currencies, exchanges)
print(sorted(res))
