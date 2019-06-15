#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 水文频率曲线拟合
# 计算部分
import numpy as np
from scipy.special import gammaincinv
import src.P3.Heisen as hs
from scipy import interpolate
import logging


class Flood(object):
    def __init__(self, data, x_std=None):
        self.x_std = hs.x_std
        try:
            self.data = [float(i) for i in data]
        except Exception as e:
            logging.error("value error")
            raise ValueError("data is not nums")
        self.data.sort()  # 排序
        self.n = len(self.data)
        self.x, self.y = None, None
        self.x_ori, self.y_ori = None, None
        self.p, self.alpha = None, None
        self.fac = 2
        self.ave = np.array(self.data).sum() / len(self.data)
        self.Cv = self.cv()
        self.Cs = self.Cv * self.fac

    def set_data(self, ave=None, cv=None, fac=None, data=None):
        if ave is not None:
            self.ave = ave
        if cv is not None:
            self.Cv = cv
        if fac is not None:
            self.fac = fac
        if data is not None:
            self.data = data

    # 计算流程
    def go(self):
        self.alpha = 4 / (self.Cv * self.fac) ** 2
        self.p = [m / (self.n+1) for m in range(1, self.n + 1)]
        self.x_ori = hs.normal(self.p)  # x轴概率对应正态化后的值
        self.y_ori = list(self.data)
        self.y_ori.reverse()
        # self.y_ori = self.xp(x=[x * 100 for x in self.p])  # 计算对应Y值
        self.x = hs.normal([i/100 for i in hs.x_std])  # x轴概率对应正态化后的值
        self.y = self.xp(x=hs.x_std)  # 计算对应Y值

    def optimize(self, xnew, kind='quadratic'):
        f = interpolate.interp1d(list(self.x_ori), list(self.y_ori), kind=kind)
        ynew = f(xnew)
        return ynew

    # 计算Cv
    def cv(self):
        Ki = [x/self.ave for x in self.data]  # 模比系数
        up = np.array([(ki-1)**2 for ki in Ki]).sum()
        down = len(self.data) - 1
        Cv = np.sqrt(up/down)
        return Cv

    # 计算中间量 逆函数，计算参考 《水文频率曲线简捷计算和绘图技巧》，林莺，李世才，广西壮族自治区南宁水利电力设计院，2002
    def tp(self, x=None):
        if x is None:
            x = [1 - x_ / 100 for x_ in hs.x_std]
        xx = [1 - x_ / 100 for x_ in x]
        tp_ = [gammaincinv(self.alpha, p) for p in xx]
        return tp_

    def xp(self, x=None):
        _ac = [0.5 * self.Cs * t - 2 / self.Cs for t in self.tp(x)]
        _xp = [self.ave * (self.Cv * ac + 1) for ac in _ac]
        return _xp
