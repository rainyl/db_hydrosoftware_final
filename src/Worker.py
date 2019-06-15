from src.utils import Interpolate
import numpy as np
import sqlite3
import pandas as pd


class Worker(object):
    def __init__(self, data, error, z_s, z_d, zo, k, zv, odh, mon_d=30.4):
        # 接受参数 data-> 数据
        # data = {
        #   'gsq':{mon1:Q1, mon2:Q2, mon3:Q3},
        #   'xsq':{mon1:Q1, mon2:Q2, mon3:Q3},
        #   'bxbg':{mon1:Q1, mon2:Q2, mon3:Q3},
        # }
        # error->误差, Z_s->高水位，Z_d->死水位
        # 常参定义
        self.zo_x = zo[:, 1]
        self.zo_y = zo[:, 0]

        self.K_H = k[:, 0]
        self.K_K = k[:, 1]

        self.zv_x = zv[:, 0]
        self.zv_y = zv[:, 1]

        self.odh_q = odh[:, 0]
        self.odh_dh = odh[:, 1]

        self.error = error
        # self.des_q = des_q
        self.mon_d = mon_d
        self.Z_s = z_s  # 正常蓄水位
        self.Z_d = z_d  # 死水位
        self.data = data  # 枯水年径流过程
        xnew = np.linspace(self.zv_x.min(), self.zv_x.max(), len(self.zv_x) * 100)
        self.V_s = Interpolate.inter1d(list(self.zv_x), list(self.zv_y), xnew, self.Z_s)[1]  # V蓄
        self.V_d = Interpolate.inter1d(list(self.zv_x), list(self.zv_y), xnew, self.Z_d)[1]  # V死
        self.V_x = np.array(self.V_s) - np.array(self.V_d)  # V兴
        self.dh = 1  # 水头损失
        self.matrix = None  # 结果矩阵

        # 月份映射关系
        self.map = {
            5: 1,
            6: 2,
            7: 3,
            8: 4,
            9: 5,
            10: 6,
            11: 7,
            12: 8,
            1: 9,
            2: 10,
            3: 11,
            4: 12
        }

        # 变参数定义
        self.N = 600*10000
        self.N_eq = self.N
        self.N_chk = np.zeros((13, 1))  # 检验出力
        self.Q_na = np.zeros((13, 1))  # 来水
        self.Q_y = np.zeros((13, 1))  # 引用流量
        self.qy()  # 初始化Q引
        self.Q_xg = np.zeros((13, 1))  # 蓄水供水流量
        self.V_xg = np.zeros((13, 1))  # 蓄水供水水量
        self.V_begin = np.zeros((13, 1))  # 时段初水量
        self.V_begin[0] = self.V_d
        self.Z_u = np.zeros((13, 1))  # 上游均水头
        self.Z_d = np.zeros((13, 1))  # 下游均水头
        self.Z_ave = np.zeros((13, 1))  # 平均水头
        self.V_ave = np.zeros((13, 1))  # 时段平均水量
        self.K = np.zeros((13, 1))  # 出力系数
        self.dh = np.zeros((13, 1))  # 损失水头
        mons = [0]
        mons.extend(list(self.map.keys()))
        self.mon = np.array(mons, dtype=float).reshape((13, 1))

    # 供水期引用流量计算
    def qy_g(self):
        gsq = self.data['gsq']
        _len = len(gsq)
        w_g = sum(gsq.values())
        qy = (w_g + self.V_x*10**8/3600/24/self.mon_d) / _len
        for k in gsq:
            _i = self.map[k]
            self.Q_y[_i] = qy
            self.Q_na[_i] = gsq[k]
        return

    # 蓄水期引用流量计算
    def qy_x(self):
        xsq = self.data['xsq']
        _len = len(xsq)
        w_x = sum(xsq.values())
        qy = (w_x - self.V_x*10**8/3600/24/self.mon_d) / _len
        for k in xsq:
            _i = self.map[k]
            self.Q_y[_i] = qy
            self.Q_na[_i] = xsq[k]
        return

    # 初始化Q引
    def qy(self):
        self.qy_g()  # 供水期引用流量
        self.qy_x()  # 蓄水期引用流量
        for k in self.data['bxbg']:
            _i = self.map[k]
            self.Q_y[_i] = self.data['bxbg'][k]
            self.Q_na[_i] = self.data['bxbg'][k]

    # 查下游水位
    def h_d(self, q):
        xnew = np.linspace(self.zo_x.min(), self.zo_x.max(), len(self.zo_x)*100)
        h = Interpolate.inter1d(list(self.zo_x), list(self.zo_y), xnew, q)
        return h

    # 查上游水位
    def h_u(self, v):
        xnew = np.linspace(self.zv_y.min(), self.zv_y.max(), len(self.zv_y)*100)
        h = Interpolate.inter1d(list(self.zv_y), list(self.zv_x), xnew, v)
        return h

    # 查K
    def _k(self, h):
        xnew = np.linspace(self.K_H.min(), self.K_H.max(), len(self.K_H)*100)
        k = Interpolate.inter1d(self.K_H, self.K_K, xnew, h)
        return k

    # 查dh
    def _dh(self, q):
        xnew = np.linspace(self.odh_q.min(), self.odh_q.max(), len(self.odh_q)*100)
        dh = Interpolate.inter1d(self.odh_q, self.odh_dh, xnew, q)
        return dh

    def set_n(self, n):
        self.N_eq = n

    def run(self, _time='xsq'):
        self.qy()  # 重置Q引
        for m in self.data['bxbg']:
            self.bxbg_sq(m)
        if _time == 'xsq':
            for m in self.data['xsq']:
                self.g_x_sq(m)
            return
        elif _time == 'gsq':
            for m in self.data['gsq']:
                self.g_x_sq(m)
            return
        else:
            raise ValueError("_time must in 'xsq' or 'gsq'")

    def witch(self, mon):
        if mon in self.data['gsq']:
            return 'gsq'
        elif mon in self.data['xsq']:
            return 'xsq'
        elif mon in self.data['bxbg']:
            return 'bxbg'
        else:
            return None

    # 供水期蓄水期计算
    def g_x_sq(self, _m):
        # 小循环
        _idx = self.map[_m]
        i_x = min([self.map[i] for i in self.data['gsq']])
        self.V_begin[i_x - 1] = self.V_s
        while True:
            self.Q_xg[_idx] = self.Q_na[_idx] - self.Q_y[_idx]
            self.V_xg[_idx] = self.Q_xg[_idx] * 3600 * 24 * self.mon_d / 10**8
            # self.V_begin[_idx] = min(self.V_begin[_idx - 1] + self.V_xg[_idx], self.V_s)  # 时段初蓄水量
            self.V_begin[_idx] = self.V_begin[_idx - 1] + self.V_xg[_idx]  # 时段初蓄水量
            self.V_ave[_idx] = (self.V_begin[_idx - 1] + self.V_begin[_idx]) / 2  # 时段平均蓄水量
            self.Z_u[_idx] = self.h_u(self.V_ave[_idx])[1]  # 上游水位
            self.Z_d[_idx] = self.h_d(self.Q_y[_idx])[1]  # 下游水位
            self.dh[_idx] = self._dh(self.Q_y[_idx])[1]  # 水头损失
            self.Z_ave[_idx] = self.Z_u[_idx] - self.Z_d[_idx] - self.dh[_idx]  # 平均水位
            self.K[_idx] = self._k(self.Z_ave[_idx])[1]  # 出力系数，由水头-出力曲线插值查得
            self.N_chk[_idx] = self.K[_idx] * self.Z_ave[_idx] * self.Q_y[_idx] / 10000  # 检验出力 万kW
            b = abs(self.N_eq / (self.K[_idx] * self.Z_ave[_idx]) - self.Q_y[_idx])  # 误差
            # matrix = self.make_matrix()
            if b < self.error:  # 若误差小于给定精度
                break
            else:
                self.Q_y[_idx] = (self.N_eq / (self.K[_idx] * self.Z_ave[_idx]) + self.Q_y[_idx]) / 2  # 若未达到精度
                # self.Q_y[_idx] = (self.N_eq / (self.K[_idx] * self.Z_ave[_idx]) - self.Q_y[_idx]) / 2  # 若未达到精度

    # 不蓄不供
    def bxbg_sq(self, _m):
        _idx = self.map[_m]
        self.Q_xg[_idx] = self.Q_na[_idx] - self.Q_y[_idx]
        self.V_xg[_idx] = self.Q_xg[_idx] * 3600 * 24 * self.mon_d / 10 ** 8
        # self.V_begin[_idx] = min(self.V_begin[_idx - 1] + self.V_xg[_idx], self.V_s)  # 时段初蓄水量
        self.V_begin[_idx] = self.V_begin[_idx - 1] + self.V_xg[_idx]  # 时段初蓄水量
        self.V_ave[_idx] = (self.V_begin[_idx - 1] + self.V_begin[_idx]) / 2  # 时段平均蓄水量
        self.Z_u[_idx] = self.h_u(self.V_ave[_idx])[1]  # 上游水位
        self.Z_d[_idx] = self.h_d(self.Q_y[_idx])[1]  # 下游水位
        self.dh[_idx] = self._dh(self.Q_y[_idx])[1]  # 水头损失
        self.Z_ave[_idx] = self.Z_u[_idx] - self.Z_d[_idx] - self.dh[_idx]  # 平均水位
        self.K[_idx] = self._k(self.Z_ave[_idx])[1]  # 出力系数，由水头-出力曲线插值查得
        self.N_chk[_idx] = self.K[_idx] * self.Z_ave[_idx] * self.Q_y[_idx] / 10000  # 检验出力 万kW

    # 合并矩阵
    def make_matrix(self):
        self.matrix = np.hstack((self.mon, self.Q_na, self.Q_y, self.Q_xg,
                                 self.V_xg, self.V_begin, self.V_ave,
                                 self.Z_u, self.Z_d, self.dh, self.Z_ave,
                                 self.K, self.N_chk))
        return self.matrix

    def is_matrix_valid(self):
        if self.matrix is None:
            return False
        return True

    # 检验是否达到精度
    def is_ok(self, _time='gsq'):
        last = None
        if _time == 'gsq':
            last = max([self.map[m] for m in self.data['gsq']])
            return abs(self.V_begin[last] - self.V_d) < self.error
        elif _time == 'xsq':
            last = max([self.map[m] for m in self.data['xsq']])
            return abs(self.V_begin[last] - self.V_s) < self.error
        else:
            raise ValueError("_time must in 'xsq' or 'gsq'")

    # True -> N小了，增大
    def over(self, _time='gsq'):
        # 供水期最后一个月的索引
        last = None
        if _time == 'gsq':
            last = max([self.map[m] for m in self.data['gsq']])
            return self.V_begin[last] > self.V_d
        elif _time == 'xsq':
            last = max([self.map[m] for m in self.data['xsq']])
            return self.V_begin[last] > self.V_s
        else:
            raise ValueError("_time must be 'xsq' or 'gsq'")


if __name__ == '__main__':
    _data = {'xsq': {7: 32705, 8: 30557, 9: 33819, 10: 31605},
             'gsq': {12: 8133, 1: 5280, 2: 4490, 3: 6967, 4: 8152},
             'bxbg': {5: 19827, 6: 26992,  11: 13990}}
    conn = sqlite3.connect('sanxia.db')
    cur = conn.cursor()
    cur.execute("SELECT H,K FROM K")
    kh = np.array(cur.fetchall())
    cur.execute("SELECT z,v FROM zv")
    zv = np.array(cur.fetchall())
    cur.execute("SELECT z,q FROM zo")
    zo = np.array(cur.fetchall())
    cur.execute("SELECT q,dh FROM odh")
    odh = np.array(cur.fetchall())
    conn.close()
    worker = Worker(_data, 0.1, 175, 145, zo, kh, zv, odh)
    columns = ['月份', '来水', '引水',
               'Q蓄水/供水', 'V蓄水/供水', '初蓄水', '均蓄水',
               '上游水位', '下游水位', '水头损失', '均水位',
               '出力系数', '检验出力']
    n_pre = 10*10000
    n_nex = 20000*10000
    # _time = 'gsq'
    _time = 'xsq'
    while True:
        # worker.set_n(float(input('请输入:\t')))
        worker.run(_time)
        matrix = worker.make_matrix()
        df = pd.DataFrame(matrix, columns=columns)
        if worker.is_ok(_time):
            print("计算结束,N={}".format(worker.N_eq))
            break
        if worker.over(_time):
            print("N={}过小".format(worker.N_eq))
            n_pre = worker.N_eq
        else:
            print("N={}过大".format(worker.N_eq))
            n_nex = worker.N_eq
        worker.set_n(np.average((n_pre, n_nex)))
        print("DEBUG")
    # df.to_excel('test_matrix.xls')
    print(matrix)
