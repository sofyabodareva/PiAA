import generate_matrix


def held_karp(matrix):
    n = len(matrix)
    INF = float('inf')
    cost_cache = {}
    def min_cost(S, v):
        if S == 1 and v == 0:
            return 0
        if (S, v) in cost_cache:
            return cost_cache[(S, v)]
        result = INF
        for u in range(n):
            if not (S >> u & 1) or u == v or matrix[u][v] == 0:
                continue
            cost = min_cost(S ^ (1 << v), u) + matrix[u][v]
            if cost < result:
                result = cost
                parent[(S, v)] = u
        cost_cache[(S, v)] = result
        return result
    parent = {}
    full = (1 << n) - 1
    best_cost = INF
    last = -1
    for v in range(1, n):
        if matrix[v][0] == 0:
            continue
        cost = min_cost(full, v) + matrix[v][0]
        if cost < best_cost:
            best_cost = cost
            last = v
    if best_cost == INF:
        return INF, "no path"
    path = []
    S = full
    v = last
    while v != -1:
        path.append(v)
        prev = parent.get((S, v), -1)
        S = S ^ (1 << v)
        v = prev
    path.reverse()
    path.append(0)

    return best_cost, path



def console_input():
    n = int(input())
    matrix = []
    for i in range(n):
        row = list(map(int, input().split()))
        matrix.append(row)
    min_cost, path = held_karp(matrix)
    if min_cost < float('inf'):
        print(min_cost, ' '.join(map(str, path)), sep='\n')
    else:
        print(path)


def file_input():
    generate_matrix.generate_and_save(5)
    f = open("./matrix.txt", 'r')
    matrix = []
    for line in f:
        row = list(map(int, line.split()))
        matrix.append(row)
    for i in range(len(matrix)):
        print(' '.join(map(str, matrix[i])))
    min_cost, path = held_karp(matrix)
    if min_cost < float('inf'):
        print(min_cost, ' '.join(map(str, path)), sep='\n')
    else:
        print(path)



file_input()
#console_input()