import generate_matrix

def alsh1(matrix):
    n = len(matrix)
    INF = float('inf')

    def min_incoming(v):
        result = INF
        for i in range(n):
            if i != v and not visited[i] and matrix[i][v] != 0:
                if matrix[i][v] < result:
                    result = matrix[i][v]
        return result

    def min_outgoing(v):
        result = INF
        for j in range(n):
            if j != v and not visited[j] and matrix[v][j] != 0:
                if matrix[v][j] < result:
                    result = matrix[v][j]
        return result

    def compute_L():
        print(f"Вычисляем нижнюю оценку для пути {path}")
        total = 0.0
        for v in range(n):
            if not visited[v]:
                inc = min_incoming(v)
                out = min_outgoing(v)
                print(f"Для непосещённой вершины {v}: минимальный вход = {inc}, минимальный выход = {out}")
                if inc == INF or out == INF:
                    continue
                total += inc + out
        inc = min_incoming(path[0])
        out = min_outgoing(path[-1])
        print(f"Для начала пути {path[0]}: минимальный вход = {inc}")
        print(f"Для конца пути {path[-1]}: минимальный выход = {out}")
        if inc == INF or out == INF:
            L = total / 2.0
            print(f"Нижняя оценка L = {L}")
            return L
        total += inc + out
        L = total / 2.0
        print(f"Нижняя оценка L = {L}")
        return L

    visited = [0] * n
    path = [0]
    visited[0] = 1
    best_cost = 0
    print(f"Начинаем построение маршрута")
    print(f"Текущий путь: {path}")
    for i in range(n - 1):
        print(f"Шаг {i + 1}")
        best_next = -1
        best_value = INF
        for candidate in range(n):
            if visited[candidate] or matrix[path[-1]][candidate] == 0:
                continue
            s = matrix[path[-1]][candidate]
            print(f"Пробуем добавить вершину {candidate}")
            print(f"Стоимость перехода {path[-1]} -> {candidate}: {s}")
            visited[candidate] = 1
            path.append(candidate)
            L = compute_L()
            path.pop()
            visited[candidate] = 0
            print(f"Суммарная оценка: {s} + {L} = {s + L}")
            if s + L < best_value:
                best_value = s + L
                best_next = candidate
                print(f"Это лучший кандидат на данный момент")
        if best_next == -1:
            print("Подходящая вершина не найдена")
            return INF, "no path"
        print(f"Выбираем вершину {best_next}")
        best_cost += matrix[path[-1]][best_next]
        print(f"Добавляем стоимость {matrix[path[-1]][best_next]}")
        print(f"Накопленная стоимость: {best_cost}")
        visited[best_next] = 1
        path.append(best_next)
        print(f"Текущий путь: {path}")
    if matrix[path[-1]][0] == 0:
        print("Невозможно вернуться в стартовую вершину")
        return INF, "no path"
    print(f"Возвращаемся из вершины {path[-1]} в вершину 0")
    print(f"Стоимость возврата: {matrix[path[-1]][0]}")
    best_cost += matrix[path[-1]][0]
    path.append(0)
    print(f"Итоговый путь: {path}")
    print(f"Полная стоимость: {best_cost}")
    return best_cost, path



def console_input():
    n = int(input())
    matrix = []
    for i in range(n):
        row = list(map(int, input().split()))
        matrix.append(row)
    min_cost, path = alsh1(matrix)
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
    min_cost, path = alsh1(matrix)
    if min_cost < float('inf'):
        print(min_cost, ' '.join(map(str, path)), sep='\n')
    else:
        print(path)


file_input()
#console_input()