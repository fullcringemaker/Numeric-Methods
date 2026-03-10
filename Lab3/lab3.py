import math

a = 0.25
b = 2.0
eps = 0.001
I = I = math.log(10 / 3)

def f(x):
    return 1/(x + x**2)

def middle_rectangles_method(n):
    h = (b - a) / n
    s = 0.0
    for i in range(1, n + 1):
        x_mid = a + (i - 0.5) * h
        s += f(x_mid)
    return h * s

def trapezoids_method(n):
    h = (b - a) / n
    s = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        s += f(a + i * h)
    return h * s

def simpsons_method(n):
    h = (b - a) / n
    middle_sum = 0.0
    for i in range(1, n + 1):
        x_mid = a + (i - 0.5) * h
        middle_sum += f(x_mid)
    node_sum = 0.0
    for i in range(1, n):
        x_i = a + i * h
        node_sum += f(x_i)

    return (h / 6.0) * (f(a) + f(b) + 4.0 * middle_sum + 2.0 * node_sum)

def richardson(I_h, I_h2, k):
    return (I_h2 - I_h) / (2**k - 1)

def clarification_with_richardson(method_func, k, n_start=2):
    n = n_start
    I_h = method_func(n)
    while True:
        n = n * 2
        I_h2 = method_func(n)
        R = richardson(I_h, I_h2, k)
        I_refined = I_h2 + R
        if abs(R) < eps:
            return n, I_h2, R, I_refined
        I_h = I_h2

print("Функция: f(x) = 1/(x + x^2)")
print(f"Промежуток: [a, b] = [{a}, {b}]")
print(f"Точность: eps = {eps}")
print(f"Аналитическое значение: I = {I}\n")

results = []

n, I_star, R, I_ref = clarification_with_richardson(middle_rectangles_method, k=2, n_start=2)
results.append(("Метод средних прямоугольников", n, I_star, R, I_ref, abs(I - I_ref)))

n, I_star, R, I_ref = clarification_with_richardson(trapezoids_method, k=2, n_start=2)
results.append(("Метод трапеций", n, I_star, R, I_ref, abs(I - I_ref)))

n, I_star, R, I_ref = clarification_with_richardson(simpsons_method, k=4, n_start=2)
results.append(("Метод Симпсона", n, I_star, R, I_ref, abs(I - I_ref)))

print("Метод                             n         I*             R          I* + R      |I-(I*+R)|")
for name, n, I_star, R, I_ref, err in results:
    print(f"{name:<30} {n:>4d}   {I_star:>12.10f}  {R:>12.10f}  {I_ref:>12.10f}  {err:>12.10f}")
