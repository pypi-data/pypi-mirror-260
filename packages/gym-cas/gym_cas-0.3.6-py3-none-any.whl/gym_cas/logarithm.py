from sympy import N, log


def log10(x: float):
    return N(log(x, 10.0))
