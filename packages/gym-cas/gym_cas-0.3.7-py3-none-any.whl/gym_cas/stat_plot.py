from collections.abc import Iterable
from typing import Union

from matplotlib.cbook import boxplot_stats
from numpy import array
from spb import MB, graphics, list_2d
from spb.backends.matplotlib.renderers.renderer import MatplotlibRenderer
from spb.defaults import TWO_D_B  # type: ignore
from spb.series import BaseSeries

from .globals import ELEMENTS_IN_INTERVAL
from .stats import _check_len_groups, frekvenstabel, group_mean, group_percentile, kvartiler, percentile

# Based on
# https://sympy-plot-backends.readthedocs.io/en/latest/tutorials/tut-6.html
# https://github.com/Davide-sd/sympy-plot-backends/blob/master/spb/series.py#L1238


def _check_len_labels(x, labels):
    if len(labels) != len(x):
        msg = "Number of labels should be equal to the number of datasets."
        raise ValueError(msg)
    pass


class BoxplotSeries(BaseSeries):
    """Representation for a boxplot of ungrouped values."""

    def __init__(self, bxp_dict, **kwargs):
        super().__init__(**kwargs)
        self.bxp_dict = bxp_dict

    def get_data(self):
        return self.bxp_dict

    def __str__(self):
        return "Boxplot"


class BarplotSeries(BaseSeries):
    def __init__(self, x, y, xticks, label: Union[str, Iterable] = "", width: Union[float, Iterable] = 0.8, **kwargs):
        super().__init__(**kwargs)

        self.x = x
        self.y = y
        self.xticks = xticks

        self.rendering_kw.setdefault("edgecolor", "black")
        self.rendering_kw.setdefault("width", width)
        if label != "":
            self.rendering_kw.setdefault("label", [label] + ["_"] * (len(x) - 1))
            self.show_in_legend = True
            self.legend = True
        else:
            self.show_in_legend = False

    def get_data(self):
        return self.x, self.y, self.xticks

    def __str__(self):
        return "Barplot"


def draw_box(renderer: MatplotlibRenderer, data: list[dict]):
    p, s = renderer.plot, renderer.series
    handle = p._ax.bxp(data, **s.rendering_kw)  # type: ignore
    return handle


def draw_bar(renderer: MatplotlibRenderer, data: Iterable):
    p, s = renderer.plot, renderer.series
    x, y, xticks = data
    p.axis_center = None
    handle = p._ax.bar(x, y, **s.rendering_kw)  # type: ignore
    p._ax.set_xticks(xticks)  # type: ignore
    if s.show_in_legend:
        p.legend = True
    return handle


def update(_renderer, _data, _handle):
    raise NotImplementedError


class BoxplotRenderer(MatplotlibRenderer):
    draw_update_map = {draw_box: update}  # noqa: RUF012


class BarplotRenderer(MatplotlibRenderer):
    draw_update_map = {draw_bar: update}  # noqa: RUF012


MB.renderers_map.update({BoxplotSeries: BoxplotRenderer})  # type: ignore
MB.renderers_map.update({BarplotSeries: BarplotRenderer})  # type: ignore


def boxplot(data, groups=None, label: Union[list, str] = "", **kwargs):
    """
    Visualize boxplot(s) of ungrouped observations. Typical usage examples:

    - Plotting a dataset:
        `boxplot(data,label=["data"],**kw)`

    - Plotting multiple datasets:
        `boxplot([data1,data2], **kw)`

    Parameters
    ==========
    groups : list, optional
        List of edge points in each interval. Each element can consist of a single or two edge values.
        Can either be a single list for all lists of observations or individual lists for each.

    label : string or list, optional
        Label to be shown for each dataset
    """
    show = kwargs.get("show", True)
    backend = kwargs.get("backend", TWO_D_B)

    if backend != MB:
        raise NotImplementedError

    stats = []
    if groups is not None:
        if not hasattr(data[0], "__iter__"):
            data = [data]
        if not hasattr(groups[0], "__iter__") or len(groups[0]) == ELEMENTS_IN_INTERVAL:
            groups = [groups] * len(data)
        for i, d in enumerate(data):
            _check_len_groups(d, groups[i])
            p = group_percentile(d, groups[i], [0, 25, 50, 75, 100])
            stats.append(
                {
                    "mean": group_mean(d, groups[i]),
                    "med": p[2],
                    "q1": p[1],
                    "q3": p[3],
                    "iqr": p[3] - p[1],
                    "cilo": 0,
                    "cihi": 0,
                    "whislo": p[0],
                    "whishi": p[4],
                    "fliers": [],
                }
            )

    else:
        stats = boxplot_stats(data, whis=(0, 100))  # type: ignore

    if label != "":
        if isinstance(label, str):
            label = [label]
        _check_len_labels(stats, label)
        for i, lbl in enumerate(label):
            stats[i]["label"] = lbl

    p = backend(BoxplotSeries(stats, **kwargs), **kwargs)

    if show:
        p.show()
    return p


def smallest_gap(data: list):
    data.sort()
    gaps = [x - y for x, y in zip(data[1:], data[:-1])]
    return min(gaps)


def plot_bars(data, label: Union[list, str] = "", **kwargs):
    """
    Visualize bar plot(s) of ungrouped observations. Typical usage examples:

    - Plotting a dataset:
        `plot_bars(data,label="data",**kw)`

    - Plotting multiple datasets:
        `plot_bars([data1,data2], **kw)`

    Parameters
    ==========
    label : list, optional
        Labels to be shown for each dataset

    width : float or list, optional
        Width of bars
    """
    show = kwargs.get("show", True)
    backend = kwargs.get("backend", TWO_D_B)

    if backend != MB:
        raise NotImplementedError

    kwargs.setdefault("ylabel", "Frekvens %")

    if hasattr(data[0], "__iter__"):
        series = []
        global_min = data[0][0]
        global_x = set()

        for d in data:
            f = frekvenstabel(d, show=False)
            global_x.update(f.observation)
        global_x = list(global_x)
        gap = smallest_gap(global_x)
        width = kwargs.get("width", gap / (len(data) + 1))
        start = -gap / 2 + width

        if label != "":
            _check_len_labels(data, label)
        else:
            label = [""] * len(data)

        for i, d in enumerate(data):
            f = frekvenstabel(d, show=False)
            offset = start + i * width
            x = (array(f.observation) + offset).tolist()
            xticks = kwargs.get("xticks", global_x)
            series.append(BarplotSeries(x, f.frekvens, xticks, label[i], width=width, **kwargs))
            if min(d) < global_min:
                global_min = min(d)
        p = backend(*series, **kwargs)
    else:
        f = frekvenstabel(data, show=False)
        x = f.observation
        gap = smallest_gap(x)
        width = kwargs.get("width", 0.8 * gap)
        p = backend(BarplotSeries(x, f.frekvens, x, label, width, **kwargs), **kwargs)

    if show:
        p.show()
    return p


def plot_sum(data, groups=None, label: Union[list, str] = "", **kwargs):
    """
    Visualize Cumulative Distribution Function (CDF) of discrete observations. Typical usage examples:

    - Plotting a ungrouped dataset:
        `plot_sum(data,label="data",**kw)`

    - Plotting multiple grouped datasets:
        `plot_sum([data1,data2],groups=[1, 2, 3, 4, 5], **kw)`

    Parameters
    ==========
    groups : list, optional
        List of edge points in each interval. Each element can consist of a single or two edge values.
        Can either be a single list for all lists of observations or individual lists for each.

    label : list, optional
        Labels to be shown for each dataset
    """
    kwargs.setdefault("ylabel", "Kumuleret Frekvens %")
    kwargs.setdefault("ylim", [0, 100])

    datasets = []
    if not hasattr(data[0], "__iter__"):
        if groups is None:
            q = kvartiler(data)
        else:
            q = percentile(data, [0, 25, 50, 75, 100])
        low = min(data)
        for i in range(1, 4):
            datasets.append(
                list_2d([low, q[i], q[i]], [25 * i, 25 * i, 0], rendering_kw={"color": "gray", "linestyle": ":"})
            )
        data = [data]

    if label != "":
        if isinstance(label, str):
            label = [label]
        _check_len_labels(data, label)
    else:
        label = [""] * len(data)

    if groups is not None:
        if not hasattr(groups[0], "__iter__") or len(groups[0]) == ELEMENTS_IN_INTERVAL:
            groups = [groups] * len(data)
        for idx, d in enumerate(data):
            _check_len_groups(d, groups[idx])
            f = frekvenstabel(d, groups[idx], show=False)
            xx, yy = [f.observation[0][0]], [0]
            for i, kf in enumerate(f.kumuleret_frekvens):
                xx.append(f.observation[i][1])
                yy.append(kf)
            datasets.append(list_2d(xx, yy, label[idx]))

    else:
        for idx, d in enumerate(data):
            f = frekvenstabel(d, show=False)
            xx, yy = [f.observation[0]], [0]
            for i, kf in enumerate(f.kumuleret_frekvens):
                if i > 0:
                    xx.append(f.observation[i])
                    yy.append(f.kumuleret_frekvens[i - 1])
                xx.append(f.observation[i])
                yy.append(kf)
            datasets.append(list_2d(xx, yy, label[idx]))

    return graphics(*datasets, **kwargs)


def plot_hist(data, groups, **kwargs):
    """
    Visualize histogram of ungrouped observations. Typical usage examples:

    - Plotting a dataset:
        `plot_hist(data, group, **kw)`

    Parameters
    ==========
    groups : list, optional
        List of edge points in each interval. Each element can consist of a single or two edge values.
        Can either be a single list for all lists of observations or individual lists for each.
    """
    show = kwargs.get("show", True)
    backend = kwargs.get("backend", TWO_D_B)

    if backend != MB:
        raise NotImplementedError

    kwargs.setdefault("ylabel", "Frekvensdensitet")

    f = frekvenstabel(data, groups, show=False)
    x, y, w, g = [], [], [], [f.observation[0][0]]
    for i, ff in enumerate(f.frekvens):
        width = f.observation[i][1] - f.observation[i][0]
        w.append(width)
        x.append((f.observation[i][1] + f.observation[i][0]) / 2)
        y.append(ff / width)
        g.append(f.observation[i][1])

    series = BarplotSeries(x, y, g, width=w, **kwargs)
    series.rendering_kw.setdefault("linewidth", 3)
    p = backend(series, **kwargs)
    if show:
        p.show()
    return p


if __name__ == "__main__":
    pass
    # boxplot([1, 2, 3, 4, 5, 6, 6, 100])
    # a = boxplot([[1, 2, 3, 10], [1, 2, 3, 8]], label=[]"hej", "dav"])
    # print(a)
    # boxplot([[1, 2, 3, 10], [1, 2, 3, 8]], groups=[1, 2, 3, 4, 5], label=["test","test2"])

    # plot_bars([1, 2, 3, 3], label="hejsa")
    # a = plot_bars([[1, 2, 3, 10, 10], [1, 2, 2, 3, 6, 8], [1, 2, 2, 3, 6, 8]], label=["hejsa", "davs der", "3"])
    # print(a.series[0].get_data())

    a = plot_sum([1, 2, 3, 3], label="hejsa")
    print(a.series)
    graphics(a[3:])
    # plot_sum([[1, 2, 3, 3], [2, 0, 4, 0]], groups=[1, 2, 3, 4, 5], label=["hejsa", "test2"])
    # a = plot_sum([[1, 2, 3, 10, 10], [1, 2, 2, 3, 10], [1, 2, 2, 3, 6, 8]], label=["hejsa", "davs der", "3"])

    # plot_hist([1, 3, 2], [1, 2, 3, 9])
