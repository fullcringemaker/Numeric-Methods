import numpy as np

A = [[4, 1, 0, 0],
     [1, 4, 1, 0],
     [0, 1, 4, 1],
     [0, 0, 1, 4]]

d = [5, 6, 6, 5]

def diagonal_check(A):
    n = len(A)
    for i in range(1, n):
        if A[i][i] == 0:
            print('Элементы главной диагонали равны 0')
            return False
    return True

def find_vector_x(A, d):
    n = len(A)
    
    if (not diagonal_check(A)):
        return -1

    x = [0 for k in range(0, n)]

    alpha = [0 for k in range(0, n)]
    beta = [0 for k in range(0, n)]
    f = [0 for k in range(0, n)]

    f[0] = A[0][0]
    alpha[0] = - A[0][1] / f[0]
    beta[0] = d[0] / f[0]

    for i in range(1, n-1):
        f[i] = A[i][i] + A[i][i-1]*alpha[i-1]
        alpha[i] = - A[i][i+1] / f[i]
        beta[i] = (d[i]-A[i][i-1]*beta[i-1]) / f[i]

    f[n-1] = A[n-1][n-1] + A[n-1][n-2] * alpha[n-2]
    beta[n-1] = (d[n-1] - A[n-1][n-2] * beta[n-2]) / f[n-1]

    x[n-1] = beta[n-1]
    for i in range(n-1, 0, -1):
        x[i-1] = alpha[i-1] * x[i] + beta[i-1]

    for i in range(0, n):
        print(f'x[{i}] =', x[i])
    print()

find_vector_x(A, d)
