import src.P3.Heisen as hs
import numpy as np


class Ploter(object):
    def __init__(self):
        self.x_std = hs.x_std

    # 绘制海森格纸
    def heisen(self, figure, x=None, xlable="$P(\%)$", ylable="$Q(m^3/s)$", title="curve"):
        if x is None:
            x = hs.normal([i/100 for i in self.x_std])
        figure.set_xticks(x)
        figure.set_xticklabels(self.x_std)
        figure.grid(True)
        figure.set_xlabel(xlable)
        figure.set_ylabel(ylable)
        figure.set_title(title)
        figure.legend()

    def plot_original_points(self, figure, y, x=None, label='original points'):
        if y is None:
            return None
        if x is None:
            x = self.order_p(y)
        px = hs.normal(x)  # 正态化以获得x值
        qy = list(y)
        qy.reverse()
        figure.plot(px, qy, 'ro', label=label)  # 绘制原始点

    # 计算顺序统计量
    def order_p(self, q):
        indexes = np.array(q).argsort()
        len_ = len(indexes)
        PP = [(p + 1) / (len_ + 1 + 1) for p in indexes]
        return PP
