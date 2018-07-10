def shortest_path(edge_list, v_from, v_to):
    """
    Finds the shortest path from one vertex to another in multigraph with a single pass through the cycles
    (without taking volumes into account).
    :param edge_list: list of edges
    :param v_from: index of vertex we have to find the way from
    :param v_to: index of vertex we have to find the way to
    :return: resulting path ``length`` and the shortest path
    """

    def check_if_cycle(last_point):
        found = False
        cur_vertex = last_point
        cc_path = []
        for i in range(vertex_count):
            cc_path.append(cur_vertex)

            if len(p[cur_vertex]) == 0:
                break

            if used[edge_into[cur_vertex]]:
                break

            cur_vertex = p[cur_vertex][-1]
            if cur_vertex == last_point:
                found = True
                break

        if found:
            #########################
            print('CYCLE FOUND')
            #########################
            for i in cc_path:
                #############
                print(edge_into[i])
                #############
                used[edge_into[i]] = True

        return found



    INF = 1_000_000_000

    vertex_set = set()
    for edge in edge_list:
        vertex_set.add(edge[0])
        vertex_set.add(edge[1])

    vertex_count = len(vertex_set)

    d = [INF for i in range(0, vertex_count)]  # distances
    d[v_from] = 0
    p = [[] for i in range(0, vertex_count)]  # parents
    used = [False for i in range(0, len(edge_list))]  # if edge number i is already used
    edge_into = [-1 for i in range(0, vertex_count)]  # index of edge which we use to get into vertex number i
    last_popped_parent = -1

    while True:
        something_changed = False
        for j in range(0, len(edge_list)):
            cur_edge = edge_list[j]
            if d[cur_edge[0]] < INF and not used[j]:
                if d[cur_edge[1]] > d[cur_edge[0]] + cur_edge[2]:

                    something_changed = True

                    d[cur_edge[1]] = max(-INF, d[cur_edge[0]] + cur_edge[2])
                    ###p[cur_edge[1]] = cur_edge[0]
                    if len(p[cur_edge[1]]) > 0:
                        last_popped_parent = p[cur_edge[1]].pop()
                    p[cur_edge[1]].append(cur_edge[0])

                    edge_into[cur_edge[1]] = j

                    found_cycle = check_if_cycle(cur_edge[1])
                    if found_cycle and last_popped_parent != 0:
                        p[cur_edge[1]].insert(-2, last_popped_parent)

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

    ################################################
    print('Distance:')
    print(d[v_to])
    print('Path:')
    print(parent_path)
    print("Used:")
    print(used)
    print("Parents:")
    print(p)
    print("Distances:")
    print(d)
    ################################################

    return d[v_to], parent_path


edge_example = [0, 1, 42]
"""test_edge_list = [[0, 1, 1],
                  [1, 2, 1],
                  [2, 3, 1],
                  [0, 2, 4],
                  [1, 3, 4],
                  [0, 3, 9]]"""
"""test_edge_list = [[0, 1, 1],
                  [1, 0, -22],
                  [0, 2, 4],
                  [2, 0, 66],
                  [1, 3, 4],
                  [3, 1, 66],
                  [2, 3, 1],
                  [3, 2, 66],
                  [1, 2, 1],
                  [2, 1, -22]]"""
"""test_edge_list = [[0, 1, 1],    Very bad
                  [1, 2, -1],
                  [2, 3, -3],
                  [3, 1, -3],
                  [2, 4, 1]]"""
"""test_edge_list = [[0, 1, 1],
                  [1, 2, -1],
                  [2, 3, -3],
                  [3, 1, -3],
                  [2, 4, 1],
                  [1, 2, 1]]"""
test_edge_list = [[0, 1, 16],
                  [1, 2, -1],
                  [2, 3, -2],
                  [3, 1, -64],
                  [1, 4, -8],
                  [4, 3, -4],
                  [3, 5, 32],
                  [1, 3, -128]]
shortest_path(test_edge_list, 0, 5)
