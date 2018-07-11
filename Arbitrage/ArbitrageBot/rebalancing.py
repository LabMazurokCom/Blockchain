import datetime
import os

File = os.path.basename(__file__)

EPS = 1e-8


def make_orders(order_books, pair, current_balance, need_base, need_quote):
    """
    makes orders to rebalance assets
    :param order_books: see example at the beginning of this file
    :param pair: pair or currencies to balance assets for
    :param need_base: desired amount base currency
    :param need_quote: desired amount of quote currency
    :return: our_orders
    """
    our_orders = dict()
    # current_balance = copy.deepcopy(current_balance)

    currencies = pair.split('_')
    base_cur = currencies[0]  # base currency of current pair (BTC for BTC/USD)
    quote_cur = currencies[1]  # quote currency of current pair (USD for BTC/USD)
    # print(pair, base_cur, quote_cur)

    ax = 0
    bx = 0
    asks = order_books[pair]['asks']
    bids = order_books[pair]['bids']
    ask_count = len(asks)
    bid_count = len(bids)

    base_amount = 0  # required amount of base currency
    quote_amount = 0  # required amount of quote currency

    sell_orders = {}  # all sell_orders for current pair
    buy_orders = {}  # all buy_orders for current pair

    if need_base != 0.0: # BUY
        while ax < ask_count and need_base > EPS:
            ask_price = asks[ax][0]
            if ask_price < EPS:
                ax += 1
                continue

            ask_vol = asks[ax][1]
            if ask_vol < EPS:
                ax += 1
                continue

            ask_price_real = asks[ax][2]

            ask_exch = asks[ax][3]  # BID: base -> quote

            ask_bal = current_balance[ask_exch][quote_cur]
            if ask_bal < EPS:
                ax += 1
                continue

            try:
                m = min(ask_vol, ask_bal / ask_price_real, need_base)  # current micro-trade volume
                if m < EPS:
                    ax += 1
                    continue
                need_base -= m
                asks[ax][1] -= m
                current_balance[ask_exch][quote_cur] -= m * ask_price_real
            except ZeroDivisionError as e:
                Time = datetime.datetime.utcnow()
                EventType = "ZeroDivisionError"
                Function = "get_arb_opp"
                Explanation = "ask_price_real is equal to 0"
                EventText = e
                ExceptionType = type(e)
                print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                                    ExceptionType))
                break

            if ask_exch in buy_orders:
                buy_orders[ask_exch][0] = max(buy_orders[ask_exch][0], ask_price_real)
                buy_orders[ask_exch][1] += m
            else:
                buy_orders[ask_exch] = [ask_price_real, m]

    else: #SELL
        m = 0
        while bx < bid_count and need_quote > 1e-4:

            bid_price = bids[bx][0]
            if bid_price < EPS:
                bx += 1
                continue

            bid_vol = bids[bx][1]
            if bid_vol < EPS:
                bx += 1
                continue

            bid_price_real = bids[bx][2]

            bid_exch = bids[bx][3]  # ASK: quote -> base

            bid_bal = current_balance[bid_exch][base_cur]
            if bid_bal < EPS:
                bx += 1
                continue

            m = min(bid_vol, bid_bal, need_quote / bid_price_real)  # current micro-trade volume
            if m < EPS:
                bx += 1
                continue
            need_quote -= bid_price * m
            bids[bx][1] -= m
            current_balance[bid_exch][base_cur] -= m

            if bid_exch in sell_orders:
                sell_orders[bid_exch][0] = min(sell_orders[bid_exch][0], bid_price_real)
                sell_orders[bid_exch][1] += m
            else:
                sell_orders[bid_exch] = [bid_price_real, m]

    our_orders = {}
    our_orders['buy'] = buy_orders
    our_orders['sell'] = sell_orders
    our_orders['required_base_amount'] = base_amount
    our_orders['required_quote_amount'] = quote_amount
    our_orders['profit'] = 0

    return our_orders


def rebalance(data, order_books, total_balances, balances):
    ok = False
    orders = {}
    cur_pair = ''
    try:
        for pair in data:
            cnt = 0
            rate = 0
            for exch in data[pair]:
                if len(data[pair][exch]['bids']) != 0 and len(data[pair][exch]['asks']) != 0:
                    rate += float(data[pair][exch]['bids'][0][2])
                    rate += float(data[pair][exch]['asks'][0][2])
                    cnt += 2
            if cnt == 0:
                continue
            rate /= cnt
            base, quote = pair.split('_')
            if total_balances[base] == 0.0 and total_balances[quote] == 0.0:
                continue
            minvol, maxvol = min(total_balances[base] * rate, total_balances[quote]), max(total_balances[base] * rate, total_balances[quote])
            if minvol / maxvol < 0.8:
                ok = True
                cur_pair = pair
                if total_balances[base] * rate < total_balances[quote]:
                    orders = make_orders(order_books, pair, balances, need_base=(total_balances[quote] - total_balances[base] * rate) / 2 / rate, need_quote=0.0)
                else:
                    orders = make_orders(order_books, pair, balances, need_base=0.0, need_quote=(total_balances[base] * rate - total_balances[quote]) / 2)


    except Exception as e:
        Time = datetime.datetime.utcnow()
        EventType = "Error"
        Function = "rebalance"
        Explanation = "Fail while getting rates for currencies"
        EventText = e
        ExceptionType = type(e)
        print("{}|{}|{}|{}|{}|{}|{}".format(Time, EventType, Function, File, Explanation, EventText,
                                            ExceptionType))

    return ok, cur_pair, orders