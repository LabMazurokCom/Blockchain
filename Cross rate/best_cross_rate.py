import datetime
import os
import json

File = os.path.basename(__file__)
INF = 1_000_000_000


class OrderBookError(Exception):
    """
    Exception raised if there's not enouth orders in orderbook.
    :param expression: input expression in which the error occurred
    :param message: explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


def raise_order_book_error ():
    time = datetime.datetime.utcnow()
    event_type = "No orders in orderbook"
    function_where = "best_cross_rate_len_2"
    explanation = "Orders in orderbook do not have enough volume"
    event_text = ""
    exception_type = None
    print("{}|{}|{}|{}|{}|{}|{}".format(time, event_type, function_where, File, explanation, event_text,
                                        exception_type))
    raise OrderBookError("", "")


def any_path_shorter_then_direct(edge_list, v_from, v_to):
    """
    Finds the shortest path from one vertex to another in multigraph with a single pass through the cycles.

    Edge is a list with three elements: []

    :param edge_list: list of edges
    :param v_from: index of vertex we have to find the way from
    :param v_to: index of vertex we have to find the way to
    :return: the shortest path cost and the path itself as a list
    """

    def check_if_cycle(last_point):
        """
        Check if vertex last_point is in a cycle
        :param last_point: a vertex
        :return: boolean found and the cycle path (if found)
        """
        found = False
        cur_vertex = last_point
        potential_cycle_path = []
        for i in range(vertex_count):
            potential_cycle_path.append(cur_vertex)
            # If vertex has no parent or edge is already in other cycle
            if len(p[cur_vertex]) == 0 or forbidden[edge_into[cur_vertex]]:
                break

            cur_vertex = p[cur_vertex][-1]

            if cur_vertex == last_point:
                found = True
                break

        if found:
            for i in potential_cycle_path:
                forbidden[edge_into[i]] = True
        else:
            potential_cycle_path.clear()

        return found, potential_cycle_path

    # Calculating the vertex count
    vertex_set = set()
    for edge in edge_list:
        vertex_set.add(edge[0])
        vertex_set.add(edge[1])
    vertex_count = len(vertex_set)

    d = [INF for i in range(0, vertex_count)]  # distances
    d[v_from] = 0
    p = [[] for i in range(0, vertex_count)]  # list of parents for each vertex
    forbidden = [False for i in range(0, len(edge_list))]  # if edge number i is forbidden
    edge_into = [-1 for i in range(0, vertex_count)]  # index of edge which we use to get into vertex number i

    while True:
        something_changed = False
        for j in range(0, len(edge_list)):
            cur_edge = edge_list[j]
            if d[cur_edge[0]] < INF and not forbidden[j]:
                if d[cur_edge[1]] > d[cur_edge[0]] + cur_edge[2]:

                    something_changed = True

                    d[cur_edge[1]] = max(-INF, d[cur_edge[0]] + cur_edge[2])
                    p[cur_edge[1]].append(cur_edge[0])
                    edge_into[cur_edge[1]] = j

                    check_if_cycle(cur_edge[1])

        if not something_changed:
            break

    parent_path = []
    cur_v = v_to
    while len(p[cur_v]) > 0:
        parent_path.append(cur_v)
        tmp = p[cur_v][-1]
        p[cur_v].pop()
        cur_v = tmp
    parent_path.append(v_from)
    parent_path.reverse()

    """
    For debug
    print('Distance:')
    print(d[v_to])
    print('Path:')
    print(parent_path)
    print("Forbidden:")
    print(forbidden)
    print("Parents:")
    print(p)
    print("Distances:")
    print(d)
    """
    return d[v_to], parent_path


def cheapest_path_len_2(graph_matrix, v_from, v_to):
    """

    :param graph_matrix:
    :param v_from:
    :param v_to:
    :return:
    """
    min_cost = INF
    best_mid_vertex = -1
    path = [v_from]
    for i in range(0, len(graph_matrix[v_from])):
        if i != v_to and len(graph_matrix[v_from][i]) > 0 and len(graph_matrix[i][v_to]) > 0\
                and graph_matrix[v_from][i][0]['cost'] < INF:

            if min_cost > graph_matrix[v_from][i][0]['cost'] + graph_matrix[i][v_to][0]['cost']:
                min_cost = graph_matrix[v_from][i][0]['cost'] + graph_matrix[i][v_to][0]['cost']
                best_mid_vertex = i

    if min_cost < INF:
        path.append(best_mid_vertex)
        path.append(v_to)
    elif graph_matrix[v_from][v_to][0]['cost'] < INF:
        path.append(v_to)
    return path, min_cost


def cheapest_path_not_longer_than(graph_matrix, v_from, v_to, max_len):
    """

    :param graph_matrix:
    :param v_from:
    :param v_to:
    :param max_len:
    :return:
    """
    min_path = []
    min_cost = INF

    def dfs(v, cur_len, cur_path, cur_cost, max_len, aim):
        nonlocal min_cost
        nonlocal min_path
        cur_len = cur_len + 1
        if cur_len < max_len:
            if v == aim:
                # print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
                if cur_cost < min_cost:
                    min_cost = cur_cost
                    min_path = cur_path
                    return

            used[v] = True
            for k in range(0, n):
                if len(graph_matrix[v][k])>0 and graph_matrix[v][k][0]['cost']<INF and not used[k]:
                    new_path = []
                    new_path.extend(cur_path)
                    new_path.append(v)
                    dfs(k, cur_len, new_path, cur_cost+graph_matrix[v][k][0]['cost'], max_len, aim)

            used[v] = False

    n = len(graph_matrix)
    used = [False for i in range(0, n)]

    dfs(v_from, -1, [], 0, max_len, v_to)
    min_path.append(v_to)
    return min_path


def unite_orders(order_book):
    while True:
        sth_changed = False
        for i in range(0, len(order_book)-1):
            if sth_changed:
                break
            for j in range(i+1, len(order_book)):
                if sth_changed:
                    break
                if order_book[i][0] == order_book[j][0] and order_book[i][1] == order_book[j][1]:
                    sth_changed = True
                    order_book[i][3] = max(order_book[i][3], order_book[j][3])
                    order_book[i][4] = order_book[i][4] + order_book[j][4]
                    order_book.pop(j)
        if not sth_changed:
            break


def best_cross_rate_len_2(graph_matrix, v_from, v_to, vol):
    """
    a
    :param graph_matrix:
    :param v_from:
    :param v_to:
    :param vol:
    :return:
    """
    our_orders = []
    m_cost = 0
    while vol > 0:
        path, m_cost = cheapest_path_len_2(graph_matrix, v_from, v_to)
        if len(path) == 1:
            nothing = 42
            """
            raise_order_book_error()
            """
            vol = 0

        elif len(path) == 2:
            cur_vol = vol
            for order in graph_matrix[v_from][v_to]:
                if order['vol'] < cur_vol:
                    cur_vol = cur_vol - order['vol']
                else:
                    cur_vol = 0
                    our_orders.append([v_from, v_to, order['cost'], vol])
            if cur_vol > 0:
                """
                raise_order_book_error()
                """
            vol = 0
        else:
            vol_of_currency_in_1 = graph_matrix[path[0]][path[1]][0]['vol'] * graph_matrix[path[0]][path[1]][0]['cost']
            if vol_of_currency_in_1 < graph_matrix[path[1]][path[2]][0]['vol']:

                our_orders.append([path[0],
                                   path[1],
                                   graph_matrix[path[0]][path[1]][0]['cost'],
                                   graph_matrix[path[0]][path[1]][0]['vol']])

                our_orders.append([path[1],
                                   path[2],
                                   graph_matrix[path[1]][path[2]][0]['cost'],
                                   vol_of_currency_in_1])

                vol = vol - graph_matrix[path[0]][path[1]][0]['vol']

                graph_matrix[path[1]][path[2]][0]['vol'] = graph_matrix[path[1]][path[2]][0]['vol']-vol_of_currency_in_1
                graph_matrix[path[0]][path[1]].pop(0)
            else:
                vol_we_can_push = graph_matrix[path[1]][path[2]][0]['vol'] / graph_matrix[path[0]][path[1]][0]['cost']

                our_orders.append([path[0],
                                   path[1],
                                   graph_matrix[path[0]][path[1]][0]['cost'],
                                   vol_we_can_push])

                our_orders.append([path[1],
                                   path[2],
                                   graph_matrix[path[1]][path[2]][0]['cost'],
                                   graph_matrix[path[1]][path[2]][0]['vol']])

                vol = vol - vol_we_can_push

                graph_matrix[path[0]][path[1]][0]['vol'] = graph_matrix[path[0]][path[1]][0]['vol'] - vol_we_can_push
                graph_matrix[path[1]][path[2]].pop(0)

    unite_orders(our_orders)
    return our_orders, m_cost


def split_currency_pair(pair):
    """
    Example: 'btc_usd' -> 'btc', 'usd'
    :param pair: a string with pair of currencies
    :return: currency names
    """
    splitted = pair.split('_')
    return splitted[0], splitted[1]


def parse_order_book(order_book, exchange):
    """

    :param order_book:
    :param exchange:
    :return:
    """
    currency_pairs = order_book.keys()
    currency_set = set()
    for pair in currency_pairs:
        curr_a, curr_b = split_currency_pair(pair)
        currency_set.add(curr_a)
        currency_set.add(curr_b)
    currency_names_list = list(currency_set)
    currency_names_list.sort()

    edge_list = []
    for i in currency_pairs:
        cur_a, cur_b = split_currency_pair(i)
        a = currency_names_list.index(cur_a)
        b = currency_names_list.index(cur_b)
        if exchange in order_book[i]:
            for j in range(min(len(order_book[i][exchange]['bids']), len(order_book[i][exchange]['asks']))):
                edge_list.append([a, b, order_book[i][exchange]['bids'][j][0], order_book[i][exchange]['bids'][j][1]])
                edge_list.append([b, a, 1/order_book[i][exchange]['asks'][j][0], order_book[i][exchange]['asks'][j][1]])
    return edge_list, currency_names_list


def edge_list_to_matrix(edge_list):
    vertex_set = set()
    for edge in edge_list:
        vertex_set.add(edge[0])
        vertex_set.add(edge[1])
    vertex_count = max(vertex_set)

    matrix = [[[{'cost': INF, 'vol': 0}] for j in range(0, vertex_count)] for i in range(0, vertex_count)]
    for edge in edge_list:
        try:
            matrix[edge[0]][edge[1]][0]['cost'] = edge[2]
            matrix[edge[0]][edge[1]][0]['vol'] = edge[3]
        except IndexError:
            continue

    return matrix


def find_cross_rate(order_book, exchange_name, currency_from, currency_to, vol):
    """

    :param order_book:
    :param exchange_name:
    :param currency_from:
    :param currency_to:
    :param vol:
    :return:
    """
    edge_list, currency_names_list = parse_order_book(order_book, exchange_name)
    graph_matrix = edge_list_to_matrix(edge_list)
    index_1 = currency_names_list.index(currency_from)
    index_2 = currency_names_list.index(currency_to)
    orders, m_cost = best_cross_rate_len_2(graph_matrix, index_1, index_2, vol)

    for order in orders:
        order[0] = currency_names_list[order[0]]
        order[1] = currency_names_list[order[1]]

    return orders, m_cost


# Tests
test_edge_list = [[0, 1, 1],
                  [1, 2, 1],
                  [2, 3, 1],
                  [0, 2, 4],
                  [1, 3, 4],
                  [0, 3, 9]]
"""
test_edge_list = [[0, 1, 1],
                  [1, 0, -22],
                  [0, 2, 4],
                  [2, 0, 66],
                  [1, 3, 4],
                  [3, 1, 66],
                  [2, 3, 1],
                  [3, 2, 66],
                  [1, 2, 1],
                  [2, 1, -22]]
test_edge_list = [[0, 1, 1],
                  [1, 2, -1],
                  [2, 3, -3],
                  [3, 1, -3],
                  [2, 4, 1]]
test_edge_list = [[0, 1, 1],
                  [1, 2, -1],
                  [2, 3, -3],
                  [3, 1, -3],
                  [2, 4, 1],
                  [1, 2, 1]]
test_edge_list = [[0, 1, 16],
                  [1, 2, -1],
                  [3, 1, -64],
                  [1, 4, -8],
                  [4, 3, -4],
                  [3, 5, 32],
                  [1, 3, -128],
                  [2, 3, -2]]"""
"""test_edge_list = [[0, 1, 0],
                  [3, 6, 0],
                  [1, 2, -1],
                  [2, 3, -1],
                  [3, 1, -1],
                  [3, 4, -2],
                  [4, 5, -2],
                  [5, 2, -2],
                  [0, 3, 0]]"""
"""
test_edge_list = [[0, 3, 0],
                  [0, 1, 0],
                  [3, 6, 0],
                  [3, 4, -2],
                  [4, 5, -2],
                  [5, 2, -2],
                  [1, 2, -1],
                  [2, 3, -1],
                  [3, 1, -1]]"""

"""
#test_o_b = json.load(open('test_order_book.json'))
#edge_list, cur_names = parse_order_book(test_o_b, 'exmo')
matr = edge_list_to_matrix(test_edge_list)
m_path = cheapest_path_not_longer_than(matr, 0, 3, 100)
print(m_path)
orders = find_cross_rate(test_o_b, 'exmo', 'btc', 'usd', 10)
print(orders)
"""