from collections.abc import Iterable

from spb import plot_list


def plot_points(x: Iterable, y: Iterable, *args, **kwargs):
    kwargs.setdefault("is_point", True)
    return plot_list(x, y, *args, **kwargs)
