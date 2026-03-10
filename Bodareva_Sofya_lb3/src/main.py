import time
import random
import string



def replace_cost(ch1: str, ch2: str,  special_ch: str, special_cost: int) -> int:
    if ch1 == ch2:
        return 0
    if ch1 == special_ch:
        return special_cost
    return 1

def insert_cost(cur_ch: str, special_ch: str, special_cost: int) -> int:
    if cur_ch == special_ch:
        return special_cost
    return 1

def LevenshteinDistance(str1: str, str2: str, ch_replace: str, replace: int, ch_insert: str, insert: int) -> list:
    m = len(str1)
    n = len(str2)
    current_act = ''
    previous = [x for x in range(n+1)]
    current = [0] * (n + 1)
    for i in range(1, m+1):
        current[0] = i
        print(f"Предыдущая строка: {previous}")
        print(f"Текущая строка:    {current}")
        print(f"Обрабатываемый символ: '{str1[i-1]}', (i = {i})")
        for j in range(1, n+1):
            options = (
                ('вставка', current[j-1]+insert_cost(str2[j-1], ch_insert, insert)),
                ('удаление', previous[j]+1),
                ('замена', previous[j-1] + replace_cost(str1[i-1], str2[j-1], ch_replace, replace))
            )
            current_act, current[j] = min(options, key=lambda x: x[1])
            print(f"Сравнение '{str1[i-1]}' и '{str2[j-1]}' -> действие: {current_act}-> current[{j}] = {current[j]}")
            print(f"Предыдущая строка: {previous}\n   Текущая строка: {current}")
        previous, current = current, [0 for _ in current]
        print('-'*40)
    return previous[n]


#S = [random.choice(string.ascii_letters) for _ in range(2500)]
#T = [random.choice(string.ascii_letters) for _ in range(2500)]
S = list(input())
T = list(input())
ch_r, r_cost = '', 1
ch_i, i_cost = '', 1
replace_input = input()
if replace_input:
    ch_r, r_cost = replace_input.split()
    r_cost = int(r_cost)

insert_input = input()
if insert_input:
    ch_i, i_cost = insert_input.split()
    i_cost = int(i_cost)
#start = time.time()
L = LevenshteinDistance(S, T, ch_r, r_cost, ch_i, i_cost)
print(L)
#finish = time.time()
#print(L, finish-start)