import json


def generate_pairs(currencies, exchanges, min_num=None, verbose=False, conf_file='orders_config.json'):
    """
    Generates list of pairs among given currencies such that each pair is traded on each given exchange.
    :param currencies: list of currencies to be considered
    :param exchanges: list of exchanges to be considered
    :param min_num: minimum number of exchanges trading current pair required to include this pair in resulting list
    :param verbose: print all pairs that are considered and which exchanges trade which pairs
    :param conf_file: configuration file with description oh how pairs are currencies are named on each exchange
    :return: list of trading pairs
    ATTENTION: FINAL PAIRS MUST BE HAND-CHANGED TO BE IN THE FORM 'basePair_quotePair' !!!
    """

    try:
        d = json.load(open(conf_file))
    except FileNotFoundError:
        print('File {} not found'.format(conf_file))
        exit(1)
    except json.JSONDecodeError as e:
        print('File {} is not a correct JSON file'.format(conf_file))
        print('ERROR MESSAGE:', e)
        exit(1)
    else:
        n = len(currencies)
        result = []
        if min_num is None:
            min_num = len(exchanges)
        for i in range(n):
            for j in range(i+1, n):
                cur1 = currencies[i]
                cur2 = currencies[j]
                pair = cur1 + '_' + cur2
                if verbose:
                    print('\t', pair)
                cnt = 0
                for exch in exchanges:
                    if verbose:
                        print(exch, end='')
                        if pair in d[exch]['converter']:
                            cnt += 1
                            print(' +')
                        else:
                            print(' --')
                    else:
                        if pair in d[exch]['converter']:
                            cnt += 1
                if cnt >= min_num:
                    result.append(pair)
        return result


currencies = ['btc', 'bch', 'usd', 'eth', 'xrp', 'dash', 'ltc', 'xmr', 'xlm']
exchanges = ['cex', 'exmo', 'kraken']
res = generate_pairs(currencies, exchanges)
for pair in sorted(res):
    print(pair)
