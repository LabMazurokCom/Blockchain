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
    # current_balance = copy.deepcopy(current_balance)

    for pair in order_books.keys():
        currencies = pair.split('_')
        base_cur = currencies[0]   # base currency of current pair (BTC for BTC/USD)
        quote_cur = currencies[1]  # quote currency of current pair (USD for BTC/USD)
        # print(pair, base_cur, quote_cur)

        ax = 0
        bx = 0
        asks = order_books[pair]['orders']['asks']
        bids = order_books[pair]['orders']['bids']
        ask_count = len(asks)
        bid_count = len(bids)

        profit = 0
        base_amount = 0  # required amount of base currency
        quote_amount = 0  # required amount of quote currency

        num = 0  # number of current micro-trade
        sell_orders = {}  # all sell_orders for current pair
        buy_orders = {}  # all buy_orders for current pair

        prev_profit = 0
        prev_quote_amount = 0

        ask_price_real = asks[ax][3]
        bid_price_real = bids[bx][3]

        while bx < bid_count and ax < ask_count and bids[bx][0] > asks[ax][0]:
            ask_price = asks[ax][0]
            bid_price = bids[bx][0]
            if ask_price == 0:
                ax += 1
                continue
            if bid_price == 0:
                bx += 1
                continue

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

            try:
                m = min(ask_vol, bid_vol, ask_bal / ask_price_real, bid_bal)  # current micro-trade volume
                current_profit = (bid_price - ask_price) * m                  # current micro-trade profit
                profit = prev_profit + current_profit
                base_amount += m
                quote_amount = prev_quote_amount + ask_price * m
                bids[bx][1] -= m
                asks[ax][1] -= m
                current_balance[ask_exch][quote_cur] -= m * ask_price_real
                current_balance[bid_exch][base_cur] -= m
            except ZeroDivisionError:
                print("ask_price_real is equal to 0 at profit point {}".format(num))
                break

            # print(ax, ask_exch, ask_bal, ' ###', ask_price, ask_vol)
            # print(bx, bid_exch, bid_bal, ' ###', bid_price, bid_vol)
            # print(m, current_profit)

            num += 1
            if num == 2:
                try:
                    first_k = (profit - prev_profit) / (quote_amount - prev_quote_amount)
                except ZeroDivisionError:
                    print("quote_amount is equal to prev_quote_amount at second profit point: {} {}".format(quote_amount, prev_quote_amount))
                    break
                except Exception as e:
                    print("Some error occurred while computing first_k")
                    print(type(e))
                    print(e)
                    break
            elif num > 2:
                try:
                    k = (profit - prev_profit) / (quote_amount - prev_quote_amount)
                except ZeroDivisionError:
                    print("quote_amount is equal to prev_quote_amount at profit point {}: {} {}".format(num, quote_amount, prev_quote_amount))
                    break
                except Exception as e:
                    print("Some error occurred while computing k at profit point {}".format(num))
                    print(type(e))
                    print(e)
                    break

                if k < first_k * alpha:
                    break

            if bid_exch in sell_orders:
                sell_orders[bid_exch][0] = min(sell_orders[bid_exch][0], bid_price_real)
                sell_orders[bid_exch][1] += m
            else:
                sell_orders[bid_exch] = [bid_price_real, m]

            if ask_exch in buy_orders:
                buy_orders[ask_exch][0] = max(buy_orders[ask_exch][0], ask_price_real)
                buy_orders[ask_exch][1] += m
            else:
                buy_orders[ask_exch] = [ask_price_real, m]
            prev_quote_amount = quote_amount
            prev_profit = profit

        our_orders[pair] = {}
        our_orders[pair]['required_base_amount'] = base_amount
        our_orders[pair]['required_quote_amount'] = quote_amount
        our_orders[pair]['profit'] = profit
        our_orders[pair]['buy'] = buy_orders
        our_orders[pair]['sell'] = sell_orders
        # print(base_amount, quote_amount, profit)
        # print(buy_orders)
        # print(sell_orders)
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
