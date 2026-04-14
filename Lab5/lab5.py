import math

x = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
y = [0.86, 0.97, 0.65, 0.75, 1.60, 0.65, 1.34, 1.62, 1.01]

def z_first(t):
    return 0.45 * math.exp(0.18 * t) + 0.2

def special_values(x, y, z):
    x0 = x[0]
    xn = x[-1]
    y0 = y[0]
    yn = y[-1]
    x_a = (x0 + xn) / 2
    x_g = math.sqrt(x0 * xn)
    x_h = 2 / (1 / x0 + 1 / xn)
    y_a = (y0 + yn) / 2
    y_g = math.sqrt(y0 * yn)
    y_h = 2 / (1 / y0 + 1 / yn)
    z_xa = z(x_a)
    z_xg = z(x_g)
    z_xh = z(x_h)
    return x_a, x_g, x_h, y_a, y_g, y_h, z_xa, z_xg, z_xh

def delta_values(y_a, y_g, y_h, z_xa, z_xg, z_xh):
    δ = {
        1: abs(z_xa - y_a),
        2: abs(z_xg - y_g),
        3: abs(z_xa - y_g),
        4: abs(z_xg - y_a),
        5: abs(z_xh - y_a),
        6: abs(z_xa - y_h),
        7: abs(z_xh - y_h),
        8: abs(z_xh - y_g),
        9: abs(z_xg - y_h),
    }
    return δ

def linear_fit_for_exp(x, y):
    n = len(x)
    X = x[:]
    Y = [math.log(v) for v in y]
    sum_x = sum(X)
    sum_y = sum(Y)
    sum_x2 = sum(t * t for t in X)
    sum_xy = sum(a * b for a, b in zip(X, Y))
    b = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
    ln_a = (sum_y - b * sum_x) / n
    a = math.exp(ln_a)
    return a, b

def z_final_function(a, b):
    return lambda t: a * math.exp(b * t)

def sum_of_squares(x, y, z):
    return sum((yi - z(xi)) ** 2 for xi, yi in zip(x, y))

def rms_deviation(x, y, z):
    return math.sqrt(sum_of_squares(x, y, z) / len(x))

def print_table(x, y, z):
    print()
    print(f"{'x_i'} {'y_i':>10} {'z(x_i)':>12} {'|y_i-z(x_i)|':>17}")
    for xi, yi in zip(x, y):
        zi = z(xi)
        di = abs(yi - zi)
        print(f"{xi:.1f} {yi:>10.2f} {zi:>12.6f} {di:>15.6f}")

x_a, x_g, x_h, y_a, y_g, y_h, z_xa, z_xg, z_xh = special_values(x, y, z_first)
δ = delta_values(y_a, y_g, y_h, z_xa, z_xg, z_xh)

min_δ_number = 2
min_δ_value = δ[2]
for k in range(3, 10):
    if δ[k] < min_δ_value:
        min_δ_value = δ[k]
        min_δ_number = k

a, b = linear_fit_for_exp(x, y)
z_final = z_final_function(a, b)

s_final = sum_of_squares(x, y, z_final)
rms_final = rms_deviation(x, y, z_final)

s_first = sum_of_squares(x, y, z_first)
rms_first = rms_deviation(x, y, z_first)

diff_rms = rms_first - rms_final

print("Специальные значения:")
print(f"x_a = {x_a:.3f}")
print(f"x_g = {x_g:.3f}")
print(f"x_h = {x_h:.3f}")
print(f"y_a = {y_a:.3f}")
print(f"y_g = {y_g:.3f}")
print(f"y_h = {y_h:.3f}")
print(f"z(x_a) = {z_xa:.3f}")
print(f"z(x_g) = {z_xg:.3f}")
print(f"z(x_h) = {z_xh:.3f}")
print()
print("Значения δ:")
for k in range(1, 10):
    print(f"δ{k} = {δ[k]:.3f}")
print(f"Наименьшая нелинейная δ: δ{min_δ_number} = {min_δ_value:.3f}")
print()
print("Полученные коэффициенты:")
print(f"a = {a:.6f}")
print(f"b = {b:.6f}")
print(f"Итоговый вид уравнения: z(x)={a:.6f}*e^({b:.6f}*x)")
print_table(x, y, z_final)
print()
print(f"Сумма квадратов отклонений для z_first = {s_first:.6f}")
print(f"Среднеквадратическое отклонение для z_first = {rms_first:.6f}")
print(f"Сумма квадратов отклонений для z_final = {s_final:.6f}")
print(f"Среднеквадратическое отклонение для z_final = {rms_final:.6f}")
print(f"Разность среднеквадратических отклонений функций = {diff_rms:.6f}")
