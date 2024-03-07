from typing import Callable, Union

from numpy import corrcoef
from numpy.polynomial import Polynomial
from spb import plot, plot_list
from spb.defaults import TWO_D_B  # type: ignore
from sympy import Lambda, N, exp, ln, simplify
from sympy.abc import t, x


def reg_poly(x_points, y_points, deg):
    p = Polynomial.fit(x_points, y_points, deg)
    ps = simplify(p(x))
    return Lambda(t, ps.subs(x, t))


def reg_pow(x_points, y_points, _):
    x_log = [float(N(ln(x))) for x in x_points]
    y_log = [float(N(ln(y))) for y in y_points]

    p = Polynomial.fit(x_log, y_log, 1)
    ps = exp(p.convert().coef[0]) * x ** p.convert().coef[1]
    return Lambda(t, ps.subs(x, t))


def reg_exp(x_points, y_points, _):
    y_log = [float(N(ln(y))) for y in y_points]

    p = Polynomial.fit(x_points, y_log, 1)
    ps = exp(p.convert().coef[0]) * exp(p.convert().coef[1]) ** x
    return Lambda(t, ps.subs(x, t))


def regression(
    x_points: list[float],
    y_points: list[float],
    deg: int,
    method: Callable[[list[float], list[float], int], Lambda],
    *,
    show=True,
    return_r2=False,
    return_plot=False,
) -> Union[tuple[Lambda, float, TWO_D_B], tuple[Lambda, Union[float, TWO_D_B]], tuple[Lambda, float], Lambda]:
    fun = method(x_points, y_points, deg)
    yp = [float(N(fun(x))) for x in x_points]
    r2 = float(corrcoef(yp, y_points)[0][1] ** 2)
    if show or return_plot:
        p1 = plot_list(x_points, y_points, is_point=True, show=False, title=f"Forklaringsgrad $R^2 = {r2:.3}$")
        p2 = plot(fun(x), (x, min(x_points), max(x_points)), show=False)
        plt = p1 + p2
        if show:
            plt.show()
        if return_plot:
            if return_r2:
                return fun, r2, plt
            return fun, plt

    if return_r2:
        return fun, r2

    return fun


def regression_poly(
    x_points: list[float], y_points: list[float], deg: int, *, show=True, return_r2=False, return_plot=False
):
    """
    Polynomial regression.

    Parameters
    ==========

    x_points, y_points : list
        Datapoints

    deg : int
        Degree of polynomial. Use deg = 1 for linear interpolation

    show : bool, default = True
        Whether to show plot

    return_r2: bool, default = False
        Whether to return the r2 value

    return_plot: bool, default = False
        Whether to return the plot
    """
    return regression(x_points, y_points, deg, reg_poly, show=show, return_r2=return_r2, return_plot=return_plot)


def regression_power(x_points: list[float], y_points: list[float], *, show=True, return_r2=False, return_plot=False):
    """
    Power regression.

    Parameters
    ==========

    x_points, y_points : list
        Datapoints

    show : bool, default = True
        Whether to show plot

    return_r2: bool, default = False
        Whether to return the r2 value

    return_plot: bool, default = False
        Whether to return the plot
    """
    return regression(x_points, y_points, 1, reg_pow, show=show, return_r2=return_r2, return_plot=return_plot)


def regression_exp(x_points: list[float], y_points: list[float], *, show=True, return_r2=False, return_plot=False):
    """
    Exponential regression.

    Parameters
    ==========

    x_points, y_points : list
        Datapoints

    show : bool, default = True
        Whether to show plot

    return_r2: bool, default = False
        Whether to return the r2 value

    return_plot: bool, default = False
        Whether to return the plot
    """
    return regression(x_points, y_points, 1, reg_exp, show=show, return_r2=return_r2, return_plot=return_plot)


if __name__ == "__main__":
    f, p1 = regression_poly([1, 2, 3], [3, 6, 12], 1, show=False, return_plot=True)  # type: ignore
    print(f(x))
    print(f(2.0))

    p, p2 = regression_poly([1, 2, 3, 4], [3, 6, 12, 4], 2, show=False, return_plot=True)  # type: ignore
    print(p(x))
    print(p(2.0))

    f2, p3 = regression_power([1, 2, 3], [3, 6, 12], show=False, return_plot=True)  # type: ignore
    print(f2(x))
    print(f2(2.0))

    f3, r2, p4 = regression_exp([1, 2, 3], [3, 6, 12], return_r2=True, return_plot=True, show=False)  # type: ignore
    print(f3(x))
    print(f3(2.0))
    print(r2)

    p = p1 + p2 + p3 + p4
    p.xlim = (0, 5)
    p.show()
