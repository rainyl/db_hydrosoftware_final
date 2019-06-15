import sqlite3
import numpy as np


def make_data_dict():
    gsq = '12,1,2,3,4'
    xsq = '7,8,9,10'
    gsq = [int(i) for i in gsq.split(',')]
    xsq = [int(i) for i in xsq.split(',')]
    bxbg = np.array([i if i not in gsq and i not in xsq else -1 for i in range(1, 13)])
    bxbg = bxbg[bxbg > 0]

    desq = 6323

    year = 1883
    y2y = (str(year) + "-" + str(year + 1),)
    conn = sqlite3.connect('sanxia.db')
    cur = conn.cursor()
    try:
        cur.execute(u"SELECT * FROM Qmonsw WHERE y2y=?;", y2y)
    except Exception as e:
        pass
    data = list(cur.fetchall()[0])[2:]
    data = [i * desq / data[-1] for i in data]
    _dict = {
        'gsq': {},
        'xsq': {},
        'bxbg': {}
    }
    for m in gsq:
        _idx = map_[m]
        _dict['gsq'][m] = data[_idx - 1]
    for m in xsq:
        _idx = map_[m]
        _dict['xsq'] = data[_idx - 1]
    for m in bxbg:
        _idx = map_[m]
        _dict['bxbq'] = data[_idx - 1]
    return _dict


if __name__ == '__main__':
    map_ = {
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
    print(make_data_dict())
