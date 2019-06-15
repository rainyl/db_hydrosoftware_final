from scipy import interpolate
import numpy as np
import pandas as pd
import re
import sqlite3


# 插值计算
class Interpolate(object):
    @classmethod
    # x, y -> 列表，xnew -> list, x的插值点, x_tofind -> 待获取x，返回x_tofind对应tuple(x, y)
    def inter1d(cls, x: list, y: list, xnew, x_tofind, kind='quadratic'):  # kind指定插值方法，默认二次样条曲线插值
        f = interpolate.interp1d(x, y, kind=kind)
        ynew = f(xnew)
        xnew_x = np.abs(xnew - x_tofind)
        index = list(xnew_x).index(xnew_x.min())
        return (xnew[index], ynew[index])


class Reader(object):
    @classmethod
    def read(cls, file_path, sheet_name=0):
        file_type = re.split("\.", file_path)[-1]
        if file_type == 'csv':
            return cls.read_csv(file_path, sheet_name)
        elif file_type == 'xls' or file_type == 'xlsx':
            return cls.read_xls(file_path, sheet_name)
        else:
            return None

    @classmethod
    def read_csv(cls, file_path, sheet_name):
        df = pd.read_csv(file_path, sheet_name=sheet_name)
        data = np.array(df)
        return data

    @classmethod
    def read_xls(cls, file_path, sheet_name):
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        data = np.array(df)
        return data


# 划分水文年
class Hydroyear(object):
    # example mons=4 mone=3
    def __init__(self, data, mons, mone):
        self.mons = mons  # 水文年起始月
        self.mone = mone  # 水文年终止月
        self.data = np.array(data)  # 流量数据
        self._rows = len(self.data)  # 多少年

    def split(self):
        left = self.data[:, :self.mone]  # 左半边表
        right = self.data[:, self.mons-1:]  # 右半边表

        line = np.hstack((right[-1, :], left[0, :]))  # 多余的一行
        tmp = np.hstack((right[:-1, :], left[1:, :]))  # 横向合并矩阵
        new = np.vstack((tmp, line))  # 纵向合并矩阵
        return new


# 年份、月份转化
class Calenear(object):
    @classmethod
    def to_cy(cls, mons, mone):
        res = [i for i in range(1, 13)]
        tmp = res[mons-1:]
        tmp.extend(res[:mone])
        return tmp


if __name__ == '__main__':
    print(Calenear.to_cy(5, 4))

    path = '/run/media/rainy/DEV/python/pyqt/project/db_hydrosoftware_final/docs/Data.xlsx'
    data = Reader.read(path, sheet_name='Qxun')
    data_new = []
    for row in np.array(data)[1:, 1:]:
        sums = [row[i:i+3].sum()/3 for i in range(0, len(row), 3)]
        data_new.append(sums)
    data_new = np.array(data_new)
    year = np.array([[int(i), ] for i in range(1882, 1991, 1)])

    data_new = np.hstack((year, data_new))

    data = np.array(data)[1:, :]

    ave = np.zeros((109, 2))
    dd = np.hstack((data_new, ave))

    conn = sqlite3.connect('sanxia.db')
    cur = conn.cursor()

    cur.executemany("INSERT INTO 'Qmonsw'("
                    "y2y, mon1,mon2,mon3,mon4,mon5,mon6,"
                    "mon7,mon8,mon9,mon10,mon11,mon12)"
                    "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);", data_new)

    # cur.executemany("INSERT INTO 'Qxun'(year,mon1_up,mon1_mid, mon1_down,"
    #                 "mon2_up,mon2_mid, mon2_down,"
    #                 "mon3_up,mon3_mid, mon3_down,"
    #                 "mon4_up,mon4_mid, mon4_down,"
    #                 "mon5_up,mon5_mid, mon5_down,"
    #                 "mon6_up,mon6_mid, mon6_down,"
    #                 "mon7_up,mon7_mid, mon7_down,"
    #                 "mon8_up,mon8_mid, mon8_down,"
    #                 "mon9_up,mon9_mid, mon9_down,"
    #                 "mon10_up,mon10_mid, mon10_down,"
    #                 "mon11_up,mon11_mid, mon11_down,"
    #                 "mon12_up,mon12_mid, mon12_down)"
    #                 "VALUES ("
    #                 "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,"
    #                 "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,"
    #                 "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,"
    #                 "?);", data)

    conn.commit()
    # cur.execute("CREATE TABLE IF NOT EXISTS 'Qxun'("
    #             "year INT(4) UNIQUE NOT NULL PRIMARY KEY,"
    #             "mon1_up DECIMAL NOT NULL,"
    #             "mon1_mid DECIMAL NOT NULL,"
    #             "mon1_down DECIMAL NOT NULL,"
    #             "mon2_up DECIMAL NOT NULL,"
    #             "mon2_mid DECIMAL NOT NULL,"
    #             "mon2_down DECIMAL NOT NULL,"
    #             "mon3_up DECIMAL NOT NULL,"
    #             "mon3_mid DECIMAL NOT NULL,"
    #             "mon3_down DECIMAL NOT NULL,"
    #             "mon4_up DECIMAL NOT NULL,"
    #             "mon4_mid DECIMAL NOT NULL,"
    #             "mon4_down DECIMAL NOT NULL,"
    #             "mon5_up DECIMAL NOT NULL,"
    #             "mon5_mid DECIMAL NOT NULL,"
    #             "mon5_down DECIMAL NOT NULL,"
    #             "mon6_up DECIMAL NOT NULL,"
    #             "mon6_mid DECIMAL NOT NULL,"
    #             "mon6_down DECIMAL NOT NULL,"
    #             "mon7_up DECIMAL NOT NULL,"
    #             "mon7_mid DECIMAL NOT NULL,"
    #             "mon7_down DECIMAL NOT NULL,"
    #             "mon8_up DECIMAL NOT NULL,"
    #             "mon8_mid DECIMAL NOT NULL,"
    #             "mon8_down DECIMAL NOT NULL,"
    #             "mon9_up DECIMAL NOT NULL,"
    #             "mon9_mid DECIMAL NOT NULL,"
    #             "mon9_down DECIMAL NOT NULL,"
    #             "mon10_up DECIMAL NOT NULL,"
    #             "mon10_mid DECIMAL NOT NULL,"
    #             "mon10_down DECIMAL NOT NULL,"
    #             "mon11_up DECIMAL NOT NULL,"
    #             "mon11_mid DECIMAL NOT NULL,"
    #             "mon11_down DECIMAL NOT NULL,"
    #             "mon12_up DECIMAL NOT NULL,"
    #             "mon12_mid DECIMAL NOT NULL,"
    #             "mon12_down DECIMAL NOT NULL)")
    print(data)

# V_begin
# [[221.5       ]
#  [159.20267521]
#  [138.41943443]
#  [146.58099202]
#  [179.5173803 ]]
#
# [[221.5       ]
#  [159.20267521]
#  [138.41943443]
#  [146.58099202]
#  [179.5173803 ]]
#
# V_ave
# [[-140.80435845]
#  [ 190.35133761]
#  [ 148.81105482]
#  [ 142.50021323]]
#
# [[200.50869015]
#  [190.35133761]
#  [148.81105482]
#  [142.50021323]]

# Z_ave
# [[65.7053927 ]
#  [84.60341545]
#  [76.16721407]
#  [74.83813741]]
#
# [[86.35800554]
#  [84.60341545]
#  [76.16721407]
#  [74.83813741]]
#
# K
# [[8.45753124]
#  [8.95241482]
#  [8.67092863]
#  [8.62490329]]
#
# [[9.00714366]
#  [8.95241482]
#  [8.67092863]
#  [8.62490329]]
#
# Z_u
# [[130.        ]
#  [148.74976478]
#  [140.37038651]
#  [139.05250172]]
#
# [[150.65261285]
#  [148.74976478]
#  [140.37038651]
#  [139.05250172]]
#
#
# Z_d
# [[63.2946073 ]
#  [63.14634933]
#  [63.20317244]
#  [63.21436431]]
#
# [[63.2946073 ]
#  [63.14634933]
#  [63.20317244]
#  [63.21436431]]
#
# Z_ave
# [[65.7053927 ]
#  [84.60341545]
#  [76.16721407]
#  [74.83813741]]