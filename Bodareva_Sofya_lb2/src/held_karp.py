import generate_matrix


def held_karp(matrix):
    n = len(matrix)
    INF = float('inf')
    cost_cache = {}
    def mask_to_vertices(S):
        return [i for i in range(n) if S >> i & 1]
    def min_cost(S, v):
        print(f"Ищем минимальную стоимость пути по вершинам {mask_to_vertices(S)}, заканчивающегося в вершине {v}")
        if S == 1 and v == 0:
            print("Базовый случай: стартуем в вершине 0, стоимость = 0")
            return 0
        if (S, v) in cost_cache:
            print(f"Берём из кэша: минимальная стоимость пути по вершинам {mask_to_vertices(S)}, заканчивающегося в {v}, равна {cost_cache[(S, v)]}")
            return cost_cache[(S, v)]
        result = INF
        for u in range(n):
            if not (S >> u & 1) or u == v or matrix[u][v] == 0:
                continue
            reduced_S = S ^ (1 << v)
            print(f"Рассматриваем переход из вершины {u} в вершину {v}")
            prev_cost = min_cost(reduced_S, u)
            cost = prev_cost + matrix[u][v]
            print(f"Стоимость пути до вершины {u}: {prev_cost}, стоимость ребра {u}->{v}: {matrix[u][v]}, общая стоимость: {cost}")
            if cost < result:
                result = cost
                parent[(S, v)] = u
                print(f"Это лучший вариант для вершины {v}")
        cost_cache[(S, v)] = result
        print(f"Минимальная стоимость пути по вершинам {mask_to_vertices(S)}, заканчивающегося в {v}: {result}")
        return result
    parent = {}
    full = (1 << n) - 1
    print(f"Все вершины графа: {mask_to_vertices(full)}")
    print("Начинаем поиск оптимального гамильтонова цикла")
    best_cost = INF
    last = -1
    for v in range(1, n):
        if matrix[v][0] == 0:
            continue
        print(f"Проверяем маршрут, который заканчивается в вершине {v}")
        path_cost = min_cost(full, v)
        total_cost = path_cost + matrix[v][0]
        print(f"Стоимость маршрута до вершины {v}: {path_cost}, возврат в вершину 0: {matrix[v][0]}, полная стоимость цикла: {total_cost}")
        if total_cost < best_cost:
            best_cost = total_cost
            last = v
    if best_cost == INF:
        print("Гамильтонов цикл не найден")
        return INF, "no path"
    print("Восстанавливаем оптимальный путь")
    path = []
    S = full
    v = last
    while v != -1:
        print(f"Добавляем вершину {v} в путь")
        path.append(v)
        prev = parent.get((S, v), -1)
        S ^= 1 << v
        v = prev
    path.reverse()
    path.append(0)
    print(f"Оптимальный путь: {path}")
    print(f"Минимальная стоимость: {best_cost}")
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
    generate_matrix.generate_and_save(3)
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