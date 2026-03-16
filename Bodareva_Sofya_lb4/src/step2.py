def prefix_func(b: str)-> list:
    pi = [0] * len(b)
    j, i = 0, 1
    while i < len(b):
        if b[j] == b[i]:
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
    

def shift_kmp(a: str, b: str) -> int:
    if len(a) != len(b):
        print("Длины строк не равны, одна не может быть сдвигом другой")
        return -1
    pi = prefix_func(b)
    print(f"Префикс-функция от строки B: {pi}")
    i, j = 0, 0
    n = len(a)              
    while i < 2*n:
        print("-"*40)
        print(f"Сравниваем {i%n} символ строки A: '{a[i%n]}' и {j} символ строки B: '{b[j]}'")
        if a[i % n] == b[j]:
            i += 1
            j += 1
            print("Символы совпали")
            if j == len(b):
                print("Строка A - циклический сдвиг строки B. Индекс начала B в A:", end=' ')
                return (i % n)
        else:
            if j > 0:
                j = pi[j-1]
            else:
                i += 1
            print(f"Символы не совпали. Сравнение продолжится с {i%n} символа A и {j} символа B")
    print("Сравнение окончено.")
    return -1



a = input()             
b = input()
print(shift_kmp(a, b))