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

def LevenshteinDistance(str1: str, str2: str, ch_replace: str, replace: int, ch_insert: str, insert: int) -> int:
    m = len(str1)
    n = len(str2)
    previous = [x for x in range(n+1)]
    current = [0] * (n + 1)
    for i in range(1, m+1):
        current[0] = i
        for j in range(1, n+1):
            current[j] = min(current[j-1]+insert_cost(str2[j-1], ch_insert, insert),
                            previous[j]+1,
                            previous[j-1] + replace_cost(str1[i-1], str2[j-1], ch_replace, replace))
        previous, current = current, previous
    return previous[n]

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
 
print(LevenshteinDistance(S, T, ch_r, r_cost, ch_i, i_cost))