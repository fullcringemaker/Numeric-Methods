import math

def thomas(a, b, c, d):
    n = len(b)
    cp = [0.0] * n
    dp = [0.0] * n

    cp[0] = c[0] / b[0]
    dp[0] = d[0] / b[0]

    for i in range(1, n):
        denom = b[i] - a[i] * cp[i - 1]
        cp[i] = (c[i] / denom) if i < n - 1 else 0.0
        dp[i] = (d[i] - a[i] * dp[i - 1]) / denom

    x = [0.0] * n
    x[-1] = dp[-1]
    for i in range(n - 2, -1, -1):
        x[i] = dp[i] - cp[i] * x[i + 1]
    return x

def build_spline(f, a0=0.0, b0=1.0, n=10):
    h = (b0 - a0) / n
    xs = [a0 + i * h for i in range(n + 1)]
    ys = [f(x) for x in xs]

    m = n - 1
    if m > 0:
        aa = [0.0] * m
        bb = [4.0] * m
        cc = [0.0] * m
        dd = [0.0] * m

        for i in range(m):
            aa[i] = 1.0 if i > 0 else 0.0
            cc[i] = 1.0 if i < m - 1 else 0.0
            k = i + 1
            dd[i] = 3.0 * (ys[k + 1] - 2.0 * ys[k] + ys[k - 1]) / (h * h)

        cint = thomas(aa, bb, cc, dd)
    else:
        cint = []

    c = [0.0] * (n + 1)
    for i in range(1, n):
        c[i] = cint[i - 1]
    c[0] = 0.0
    c[n] = 0.0

    A = [0.0] * n
    B = [0.0] * n
    C = [0.0] * n
    D = [0.0] * n

    for i in range(n):
        A[i] = ys[i]
        C[i] = c[i]
        B[i] = (ys[i + 1] - ys[i]) / h - h * (2.0 * c[i] + c[i + 1]) / 3.0
        D[i] = (c[i + 1] - c[i]) / (3.0 * h)

    return xs, ys, (A, B, C, D), h

def spline_value(x, xs, coefs, h):
    A, B, C, D = coefs
    n = len(A)
    if x <= xs[0]:
        i = 0
    elif x >= xs[-1]:
        i = n - 1
    else:
        i = int((x - xs[0]) / h)
        if i >= n:
            i = n - 1
    dx = x - xs[i]
    return A[i] + B[i] * dx + C[i] * dx * dx + D[i] * dx * dx * dx

def fmt(v):
    return f"{v:.16f}"

f = math.exp
xs, ys, coefs, h = build_spline(f, 0.0, 1.0, 10)

print("TABLE 1 (in nodes)")
print(f"{'x':>20} {'S(x)':>25} {'y(x)':>25} {'|S(x)-y|':>25}")
for i, x in enumerate(xs):
    s = spline_value(x, xs, coefs, h)
    y = ys[i]
    print(f"{fmt(x):>20} {fmt(s):>25} {fmt(y):>25} {fmt(abs(s - y)):>25}")

print("\nTABLE 2 (at midpoints)")
print(f"{'x':>20} {'S(x)':>25} {'y(x)':>25} {'|S(x)-y|':>25}")

midpoints = [xs[0]] + [xs[i] - h / 2.0 for i in range(1, len(xs))]
for x in midpoints:
    s = spline_value(x, xs, coefs, h)
    y = f(x)
    print(f"{fmt(x):>20} {fmt(s):>25} {fmt(y):>25} {fmt(abs(s - y)):>25}")
