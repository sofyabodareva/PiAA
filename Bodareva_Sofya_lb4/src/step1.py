def prefix_func(p: str)-> list:
    pi = [0] * len(p)
    j, i = 0, 1
    while i < len(p):
        if p[j] == p[i]:
            pi[i] = j + 1
            j += 1
            i += 1
        else:
            if j == 0:
                pi[i] = 0
                i += 1
            else:
                j = pi[j-1]
    return pi
    

def kmp(p: str, t: str) -> str:
    pi = prefix_func(p)
    print(f"Префикс функция от строки p: {pi}")
    solve = []
    i, j = 0, 0
    n, m = len(t), len(p)
    while i < n:
        if n - i < m - j:
            print(f"В тексте осталось: {n-i} символ(-ов), в образце - {m-j}. Сравнение окончено")
            break
        print("-"*40)
        print(f"Сравнение {i} символа исходного текста: '{t[i]}' и {j} символа образца: '{p[j]}'")
        if t[i] == p[j]:
            i += 1
            j += 1
            print(f"Символы совпадают")
            if j == len(p):
                solve.append(str(i-j))
                print(f"Образец найден. Индекс вхождения: {i-j}. ")
                j = pi[j-1]
        else:
            if j > 0:
                j = pi[j-1]
                print(f"Символы не совпали, сравнение продолжится с {j} символа образца и {i} символа исходного текста")
            else:
                i += 1
                print(f"Символы не совпали, продолжаем сравнение с {i} символа исходного текста и {j} символа образца")
    if not solve:
            print("Образец не входит в текст.")
            return "-1"
    print("Образец входит в текст. Индекс(ы) вхождения:", end=' ')
    return ','.join(solve)



p = input()
t = input()
print(kmp(p, t))