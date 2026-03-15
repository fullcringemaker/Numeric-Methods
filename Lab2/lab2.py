import math

def exact_solution(x):
    return math.exp(x) + math.sin(x)

def p(x):
    return 1.0

def q(x):
    return -2.0

def f(x):
    return math.cos(x) - 3.0 * math.sin(x)

def print_method_table(title, x_values, y_exact, y_num, errors):
    print(title)
    print(f"{'x':<10}{'y':<22}{'y*':<22}{'|y_i - y*_i|':<22}")
    for i in range(len(x_values)):
        print(
            f"{x_values[i]:<10.1f}"
            f"{y_exact[i]:<22.15f}"
            f"{y_num[i]:<22.15f}"
            f"{errors[i]:<22.15f}"
        )
    print()
    print(f"||y - y*|| = max|y_i - y*_i| = {max(errors):.15f}")
    print()

def running_method():
    a = 0.0
    b = 1.0
    n = 10
    h = (b - a) / n
    y_left = 1.0
    y_right = math.exp(1.0) + math.sin(1.0)
    x_values = [a + i * h for i in range(n + 1)]
    alpha = [0.0] * (n + 1)
    beta = [0.0] * (n + 1)
    y_num = [0.0] * (n + 1)
    for i in range(1, n):
        xi = x_values[i]
        A = 1.0 - p(xi) * h / 2.0
        B = q(xi) * h * h - 2.0
        C = 1.0 + p(xi) * h / 2.0
        D = f(xi) * h * h
        if i == 1:
            alpha[i] = -C / B
            beta[i] = (D - A * y_left) / B
        else:
            denominator = A * alpha[i - 1] + B
            alpha[i] = -C / denominator
            beta[i] = (D - A * beta[i - 1]) / denominator
    y_num[0] = y_left
    y_num[n] = y_right
    y_num[n - 1] = alpha[n - 1] * y_num[n] + beta[n - 1]
    for i in range(n - 2, 0, -1):
        y_num[i] = alpha[i] * y_num[i + 1] + beta[i]
    y_exact = [exact_solution(x) for x in x_values]
    errors = [abs(y_exact[i] - y_num[i]) for i in range(n + 1)]

    return x_values, y_exact, y_num, errors

def shooting_method():
    a = 0.0
    b = 1.0
    n = 10
    h = (b - a) / n
    y_left = 1.0
    y_right = math.exp(1.0) + math.sin(1.0)
    x_values = [a + i * h for i in range(n + 1)]
    y0 = [0.0] * (n + 1)
    y1 = [0.0] * (n + 1)
    y0[0] = y_left
    y0[1] = y_left + h
    y1[0] = 0.0
    y1[1] = h
    for i in range(1, n):
        xi = x_values[i]
        denominator = 1.0 + p(xi) * h / 2.0
        y0[i + 1] = (
            f(xi) * h * h
            + (2.0 - q(xi) * h * h) * y0[i]
            - (1.0 - p(xi) * h / 2.0) * y0[i - 1]
        ) / denominator
        y1[i + 1] = (
            (2.0 - q(xi) * h * h) * y1[i]
            - (1.0 - p(xi) * h / 2.0) * y1[i - 1]
        ) / denominator
    c1 = (y_right - y0[n]) / y1[n]
    y_num = [y0[i] + c1 * y1[i] for i in range(n + 1)]
    y_exact = [exact_solution(x) for x in x_values]
    errors = [abs(y_exact[i] - y_num[i]) for i in range(n + 1)]

    return x_values, y_exact, y_num, errors

def print_comparison_table(x_values, y_exact, y_num_1, y_num_2, errors_1, errors_2):
    print("Сравнение методов")
    print(
        f"{'x':<10}"
        f"{'y':<22}"
        f"{'y*_1':<22}"
        f"{'y*_2':<22}"
        f"{'|y_i - y*_i|_1':<22}"
        f"{'|y_i - y*_i|_2':<22}"
    )
    for i in range(len(x_values)):
        print(
            f"{x_values[i]:<10.1f}"
            f"{y_exact[i]:<22.15f}"
            f"{y_num_1[i]:<22.15f}"
            f"{y_num_2[i]:<22.15f}"
            f"{errors_1[i]:<22.15f}"
            f"{errors_2[i]:<22.15f}"
        )

def main():
    x1, y1, y_num_1, err_1 = running_method()
    x2, y2, y_num_2, err_2 = shooting_method()
    print_method_table("Метод прогонки (1 метод)", x1, y1, y_num_1, err_1)
    print_method_table("Метод стрельбы (2 метод)", x2, y2, y_num_2, err_2)
    print_comparison_table(x1, y1, y_num_1, y_num_2, err_1, err_2)

if __name__ == "__main__":
    main()
