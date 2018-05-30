import copy

# order_books = {
#     'btc_usd': {
#         'orders': {
#             'asks': [[price, volume, exchange_name], ...],
#             'bids': [[], ...]
#         }
#     },
#     'eth_btc': {
#         'orders': {
#             'asks': [[], ...],
#             'bids': [[], ...]
#         }
#     },
#     ...
# }


# current_balance = {
#     'binance': {
#         'btc': btc_balance,
#         'usd': usd_balance,
#         ...-
#     },
#     'cex': {
#         'btc': btc_balance,
#         'usd': usd_balance,
#         ...
#     },
#     ...
# }


#         our_orders[pair] = {
#             'asks': [],
#             'bids': [],
#             'required_base_amount': float,
#             'required_quote_amount': float,
#             'profit': float
#         }


def get_arb_opp(order_books, current_balance, alpha=0.1):
    our_orders = dict()
    current_balance = copy.deepcopy(current_balance)

    for pair in order_books.keys():
        currencies = pair.split('_')
        base_cur = currencies[0]  # base currency of current pair (BTC for BTC/USD)
        quote_cur = currencies[1] # quote currency of current pair (USD for BTC/USD)
        # print(pair, base_cur, quote_cur)

        ax = 0
        bx = 0
        asks = order_books[pair]['orders']['asks']
        bids = order_books[pair]['orders']['bids']
        ask_count = len(asks)
        bid_count = len(bids)

        profit = 0
        base_amount = 0   # required amount of base currency
        quote_amount = 0  # required amount of quote currency

        num = 0           # number of current micro-trade
        bid_orders = {}   # all bid_orders for current pair
        ask_orders = {}   # all ask_orders for current pair
        ok = True

        while bx < bid_count and ax < ask_count and bids[bx][0] > asks[ax][0]:
            # print()
            ask_price = asks[ax][0]
            bid_price = bids[bx][0]

            ask_vol = asks[ax][1]
            bid_vol = bids[bx][1]
            if ask_vol == 0:
                ax += 1
                continue
            if bid_vol == 0:
                bx += 1
                continue

            ask_exch = asks[ax][2]  # BID: base -> quote
            bid_exch = bids[bx][2]  # ASK: quote -> base

            ask_bal = current_balance[ask_exch][quote_cur]
            bid_bal = current_balance[bid_exch][base_cur]
            if ask_bal == 0:
                ax += 1
                continue
            if bid_bal == 0:
                bx += 1
                continue

            m = min(ask_vol, bid_vol, ask_bal, bid_bal)        # current micro-trade volume
            current_profit = (bid_price - ask_price) * m   # current micro-trade profit
            profit += current_profit
            base_amount += m
            quote_amount += ask_price * m
            bids[bx][1] -= m
            asks[ax][1] -= m
            current_balance[ask_exch][quote_cur] -= m
            current_balance[bid_exch][base_cur] -= m

            # print(ax, ask_exch, ask_bal, ' ###', ask_price, ask_vol)
            # print(bx, bid_exch, bid_bal, ' ###', bid_price, bid_vol)
            # print(m, current_profit)

            num += 1
            if num == 2:
                first_k = (profit - prev_profit) / (quote_amount - prev_quote_amount)
            elif num > 2:
                k = (profit - prev_profit) / (quote_amount - prev_quote_amount)
                if k / first_k < alpha:
                    ok = False
                if not ok:
                    break

            if bid_exch in bid_orders:
                bid_orders[bid_exch][0] = min(bid_orders[bid_exch][0], bid_price)
                bid_orders[bid_exch][1] += m
            else:
                bid_orders[bid_exch] = [bid_price, m]
            
            if ask_exch in ask_orders:
                ask_orders[ask_exch][0] = max(ask_orders[ask_exch][0], ask_price)
                ask_orders[ask_exch][1] += m
            else:
                ask_orders[ask_exch] = [ask_price, m]
            prev_quote_amount = quote_amount
            prev_profit = profit

        our_orders[pair] = {}
        our_orders[pair]['required_base_amount'] = base_amount
        our_orders[pair]['required_quote_amount'] = quote_amount
        our_orders[pair]['profit'] = profit
        our_orders[pair]['asks'] = ask_orders
        our_orders[pair]['bids'] = bid_orders
        # print(base_amount, quote_amount, profit)
        # print(ask_orders)
        # print(bid_orders)
    return our_orders

'''
order_books = {
    'btc_usd': {
        'orders': {
            'asks': [[10, 1, 'a'], [10.5, 0.2, 'a'], [11.5, 0.3, 'b']],
            'bids': [[11, 0.8, 'b'], [10.3, 0.3, 'b']]
        }
    }
}

current_balances = {'a': {'btc': 1.1, 'usd': 10}, 'b': {'btc': 1, 'usd': 18}}

print(get_arb_opp(order_books, current_balances))
'''
