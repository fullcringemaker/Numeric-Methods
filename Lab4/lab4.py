import math
import numpy as np

EPS = 0.01

X0 = -0.2
Y0 = 0.5

def f(x, y):
    return np.array([
        math.sin(y + 1) - x - 1.2,
        2 * y + math.cos(x) - 2
    ], dtype=float)

def jacobian(x, y):
    return np.array([
        [-1.0, math.cos(y + 1)],
        [-math.sin(x), 2.0]
    ], dtype=float)

def newton(x0, y0, eps=EPS, max_iter=100):
    x = x0
    y = y0
    for i in range(1, max_iter):
        delta = np.linalg.solve(jacobian(x, y), -f(x, y))
        x_new = x + delta[0]
        y_new = y + delta[1]
        if max(abs(x_new - x), abs(y_new - y)) < eps:
            return x_new, y_new, i
        x, y = x_new, y_new
    return x, y, max_iter

def main():
    x, y, iterations = newton(X0, Y0)

    print("Решение, полученное графически:")
    print(f"x = {X0:.5f}, y = {Y0:.5f}")
    print()
    print("Решение методом Ньютона:")
    print(f"x = {x:.15f}, y = {y:.15f}")
    print()
    print("Погрешность:")
    print(f"Для f1: {2 - (2 * y + math.cos(x)):.15f}")
    print(f"Для f2: {1.2 - (math.sin(y + 1) - x):.15f}")
    print()
    print(f"Количество выполненных итераций: {iterations}")

if __name__ == "__main__":
    main()
