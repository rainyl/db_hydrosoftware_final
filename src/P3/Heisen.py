#!../venv/bin/python3
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


x_std = [0.01, 0.05, 0.1, 0.5, 1.0, 2, 3, 4, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 85, 90, 95, 99, 99.5, 99.9]  #x刻度标准


# 计算格纸横坐标
def normal(arry, std=None):
    if std is None:
        std = norm.ppf(0.0001, 0, 1)
    aa = norm.ppf(arry, 0, 1)
    return np.array([a - std for a in aa])


# 计算顺序统计量
def order_p(Q):
    indexes = np.array(Q).argsort()
    len_ = len(indexes)
    PP = [(p+1)/(len_+1+1) for p in indexes]
    return PP


# 绘制原始点，q_为流量，p_ori为原始点概率， 如果不提供p_ori，则自动计算其顺序统计量
def plot_ori_union(q_, p_ori=None, label="original points"):
    if p_ori is None:
        p_ori = order_p(q_)
    px = normal(p_ori)  # 正态化以获得x值
    qy = list(q_)
    qy.reverse()
    plt.plot(px, qy, 'ro', label=label)  # 绘制原始点


# 绘制格纸
def heisen(x_stdd=None, xlable="P(%)", ylable="Q(m3/s)", title="freq curve"):
    if x_stdd is None:
        x_stdd = x_std
    xx = normal([x / 100 for x in x_stdd])
    # plt.plot(xx, xx*0)
    plt.xticks(xx, x_stdd)  # 设置x刻度与label
    plt.grid(True)
    plt.xlabel(xlable)
    plt.ylabel(ylable)
    plt.legend()
    plt.title(title)


def show():
    plt.show()
