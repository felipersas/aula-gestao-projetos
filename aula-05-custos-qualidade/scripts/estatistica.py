"""Funcoes estatisticas usadas na analise de qualidade (somente numpy; sem scipy)."""
import math
import numpy as np


def ranks(a):
    a = np.asarray(a, dtype=float)
    o = np.argsort(a, kind="stable")
    r = np.empty(len(a))
    r[o] = np.arange(1, len(a) + 1)
    for v in np.unique(a):
        m = a == v
        r[m] = r[m].mean()
    return r


def pearson(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    return float(np.corrcoef(x, y)[0, 1])


def spearman(x, y):
    return pearson(ranks(x), ranks(y))


def _betacf(a, b, x):
    tiny, qab, qap, qam = 1e-30, a + b, a + 1, a - 1
    c, d = 1.0, 1.0 - qab * x / qap
    d = 1.0 / (d if abs(d) > tiny else tiny)
    h = d
    for m in range(1, 300):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        d = 1.0 / (d if abs(d) > tiny else tiny)
        c = 1.0 + aa / c
        c = c if abs(c) > tiny else tiny
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        d = 1.0 / (d if abs(d) > tiny else tiny)
        c = 1.0 + aa / c
        c = c if abs(c) > tiny else tiny
        de = d * c
        h *= de
        if abs(de - 1.0) < 3e-12:
            break
    return h


def betainc(a, b, x):
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    front = math.exp(lbeta + a * math.log(x) + b * math.log(1 - x))
    if x < (a + 1) / (a + b + 2):
        return front * _betacf(a, b, x) / a
    return 1 - front * _betacf(b, a, 1 - x) / b


def p_valor_r(r, n):
    """p-valor bilateral do teste de H0: rho = 0 (estatistica t com n-2 gl)."""
    if n < 3 or abs(r) >= 1:
        return 0.0
    t = r * math.sqrt((n - 2) / (1 - r * r))
    gl = n - 2
    return betainc(gl / 2, 0.5, gl / (gl + t * t))


def regressao(x, y):
    """Reta de minimos quadrados y = a + b x, com r, R2 e p-valor."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    b, a = np.polyfit(x, y, 1)
    r = pearson(x, y)
    return dict(a=float(a), b=float(b), r=r, r2=r * r, p=p_valor_r(r, len(x)), n=int(len(x)))


def descritivas(v):
    v = np.asarray(v, float)
    n = len(v)
    m = v.mean()
    s = v.std(ddof=1)
    g1 = float(((v - m) ** 3).mean() / (v.std(ddof=0) ** 3)) if s > 0 else 0.0
    q = np.percentile(v, [25, 50, 75, 90])
    return dict(n=int(n), media=float(m), mediana=float(q[1]), dp=float(s), minimo=float(v.min()),
                maximo=float(v.max()), q1=float(q[0]), q3=float(q[2]), p90=float(q[3]), assimetria=g1)


def fmt(x, nd=1):
    """Formata numero em pt-BR (virgula decimal, ponto de milhar)."""
    if x is None:
        return "-"
    s = f"{x:,.{nd}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")
