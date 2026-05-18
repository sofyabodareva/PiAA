import random


def generate_matrix(n, symmetric=True):
    matrix = [[0] * n for x in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            weight = random.randint(1, 100)
            matrix[i][j] = weight
            if symmetric:
                matrix[j][i] = weight
            else:
                matrix[j][i] = random.randint(1, 100)
    return matrix


def save_matrix(matrix, file_name="matrix.txt"):
    n = len(matrix)
    with open(file_name, 'w') as f:
        for row in matrix:
            f.write(" ".join(map(str, row)) + "\n")


def generate_and_save(n, symmetric=False, file_name="matrix.txt"):
    matrix = generate_matrix(n, symmetric)
    save_matrix(matrix, file_name)
    return matrix
