# -*- coding: utf-8 -*-

# app for database and hydrosoftware final work
# author: rainyl
# update: 2019-3-27


from src.UI_MainWindow import UI_MainWindow
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog, QMessageBox
from PyQt5.QtCore import QCoreApplication, QThread, pyqtSignal
import numpy as np
from src.Worker import Worker
from src.Namer import Namer
from src.P3.Flood import Flood
from src.ploter import Ploter
import logging
import sqlite3
import sys
import time
import subprocess


class MainWindow(UI_MainWindow):
    def __init__(self):
        super().__init__()
        self.slots()
        self._tr = QCoreApplication.translate

        self.db = None
        self._time = 'gsq'
        self.worker = None
        self.work_thread = MyThread(parent=self)
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

        logging.getLogger().addHandler(self.logger)
        logging.getLogger().setLevel(logging.INFO)
        print('hi')

    def slots(self):
        self.action_open_db.triggered.connect(self.on_action_triggered)
        self.action_exit.triggered.connect(self.on_action_triggered)
        self.action_lyl.triggered.connect(self.on_action_triggered)
        self.action_brb.triggered.connect(self.on_action_triggered)
        self.action_hjy.triggered.connect(self.on_action_triggered)
        self.btn_next_N.clicked.connect(self.on_btn_next_n_clicked)
        self.btn_curve_fit.clicked.connect(self.on_btn_curve_fit_clicked)
        self.btn_reg_go.clicked.connect(self.on_btn_go_clicked)
        # self.btn_split_sw.clicked.connect(self.on_btn_split_clicked)
        self.btn_stop.clicked.connect(self.on_btn_stop_clicked)
        self.btn_draw.clicked.connect(self.on_btn_draw_clicked)
        self.btn_write_db.clicked.connect(self.on_btn_write_db_clicked)

    def on_action_triggered(self):
        sender = self.sender()
        if sender.objectName() == Namer.action_open_db:
            db_path = QFileDialog.getOpenFileName(self,
                                                  self._tr("database", "选择数据库"),
                                                  '.',
                                                  filter="database (*.db *.db3 *.sqlite *.sqlite3)")
            if len(db_path[0]) != 0:
                self.db = db_path[0]
                conn = sqlite3.connect(self.db)
                cur = conn.cursor()
                logging.info("正在读取数年平均流量...")
                cur.execute("SELECT year FROM Qmon")
                years = [str(y[0]) for y in cur.fetchall()]
                self.cmbox_ddy.addItems(years)
        elif sender.objectName() == Namer.action_exit:
            sys.exit(0)
        elif sender.objectName() == Namer.action_lyl:
            # output = None
            # print(output)
            output = subprocess.getoutput('.\\lyl.exe')
            # print(output)
        elif sender.objectName() == Namer.action_brb:
            pass
        elif sender.objectName() == Namer.action_hjy:
            pass
        else:
            logging.warning("No such object")

    def on_btn_draw_clicked(self):
        if self.db_isnone():
            QMessageBox.warning(self, "警告", "数据库为空")
            return
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        checked = [self.chkbox_zv.isChecked(), self.chkbox_zo.isChecked(),
                   self.chkbox_K.isChecked(), self.chkbox_dh.isChecked(),
                   self.chkbox_n.isChecked()]
        if True in checked:
            # 绘制库容曲线
            if self.chkbox_zv.isChecked():
                cur.execute("SELECT * FROM zv")
                data = np.array(cur.fetchall())[:, 1:]
                self.fig_zv.clear()
                ax = self.fig_zv.add_subplot(111)
                ax.plot(data[:, 0], data[:, 1], 'o--', label='Z-V')
                ax.set_title("Z-V")
                ax.set_xlabel("$Z(m)$")
                ax.set_ylabel("$V(10^8m^3)$")
                ax.grid()
                ax.legend()
                self.canvas_zv.draw()
            else:
                self.fig_zv.clear()
                self.canvas_zv.draw()
            # 绘制等出力过程
            if self.chkbox_n.isChecked():
                cur.execute("SELECT mon,vbegin FROM eqn;")
                data = np.array(cur.fetchall())
                mon, vbegin = list(data[1:, 0]), data[1:, 1]
                x = [i for i in range(len(vbegin))]
                self.fig_n.clear()
                ax = self.fig_n.add_subplot(111)
                ax.plot(x, vbegin, 'o--', label='T-V')
                ax.set_xticks(mon)
                # ax.xlim = (0, 12)
                # ax.ylim = (vbegin.min(), vbegin.max())
                ax.set_title("T-V")
                ax.set_xlabel("$T$")
                ax.set_ylabel("$V(10^8m^3)$")
                ax.grid()
                ax.legend()
                self.canvas_n.draw()
            else:
                self.fig_zv.clear()
                self.canvas_zv.draw()
            # 绘制尾水曲线
            if self.chkbox_zo.isChecked():
                cur.execute("SELECT * FROM zo")
                data = np.array(cur.fetchall())[:, 1:]
                self.fig_zo.clear()
                ax = self.fig_zo.add_subplot(111)
                ax.plot(data[:, 1], data[:, 0], 'o--', label='Z-O')
                ax.set_title("Z-O")
                ax.set_xlabel("$Z(m)$")
                ax.set_ylabel("$O(10^8m^3)$")
                ax.grid()
                ax.legend()
                self.canvas_zo.draw()
            else:
                self.fig_zo.clf()
                self.canvas_zo.draw()
            # 绘制出力系数
            if self.chkbox_K.isChecked():
                cur.execute("SELECT * FROM K")
                data = np.array(cur.fetchall())[:, 1:]
                self.fig_k.clear()
                ax = self.fig_k.add_subplot(111)
                ax.plot(data[:, 0], data[:, 1], 'o--', label='K')
                ax.set_title("K")
                ax.set_xlabel("$H(m)$")
                ax.set_ylabel("$K$")
                ax.grid()
                ax.legend()
                self.canvas_k.draw()
            else:
                self.fig_k.clf()
                self.canvas_k.draw()
            # 绘制水头损失
            if self.chkbox_dh.isChecked():
                cur.execute("SELECT * FROM odh")
                data = np.array(cur.fetchall())[:, 1:]
                self.fig_dh.clear()
                ax = self.fig_dh.add_subplot(111)
                ax.plot(data[:, 0], data[:, 1], 'o--', label='dh')
                ax.set_title("dh")
                ax.set_xlabel("$Q(m^3/s)$")
                ax.set_ylabel("$dh(m)$")
                ax.grid()
                ax.legend()
                self.canvas_dh.draw()
            else:
                self.fig_dh.clf()
                self.canvas_dh.draw()
        else:
            # 清除所有
            self.fig_zv.clf()
            self.canvas_zv.draw()
            self.fig_zo.clf()
            self.canvas_zo.draw()
            self.fig_k.clf()
            self.canvas_k.draw()
            QMessageBox.warning(self, "提示", "未选择曲线！")
            return
        conn.close()

    def on_btn_write_db_clicked(self):
        if self.db_isnone():
            QMessageBox.warning(self, "警告", "数据库为空")
            return
        if not self.worker.is_matrix_valid():
            QMessageBox.warning(self, "警告", "出力计算错误")
            return
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS 'eqn'("
                    "id INTEGER UNIQUE, "
                    "year INT,"
                    "mon INT(2),"
                    "qcom DECIMAL ,"
                    "qy DECIMAL ,"
                    "qxg DECIMAL ,"
                    "vxg DECIMAL ,"
                    "vbegin DECIMAL ,"
                    "vave DECIMAL ,"
                    "zu DECIMAL ,"
                    "zd DECIMAL ,"
                    "dh DECIMAL ,"
                    "zave DECIMAL ,"
                    "k DECIMAL ,"
                    "n DECIMAL )")
        matrix = self.worker.matrix
        _id = np.array([i for i in range(1, len(matrix)+1)]).reshape((len(matrix), 1))
        _year = np.array([self.worker.data['year'] for i in range(len(matrix))]).reshape((len(matrix), 1))
        _matrix = np.hstack((_id, _year, matrix))
        try:
            cur.executemany("INSERT INTO 'eqn' "
                            "VALUES(?,?,?,?,?,?,?,"
                            "?,?,?,?,?,?,?,?);", _matrix)
        except Exception as e:
            logging.warning(e)
            logging.warning("插入错误,尝试更新")
        _matrix = np.hstack((_year, matrix, _id))
        try:
            cur.executemany("UPDATE 'eqn' SET "
                            "year=?,"
                            "mon=?,"
                            "qcom=?,"
                            "qy=?,"
                            "qxg=?,"
                            "vxg=?,"
                            "vbegin=?,"
                            "vave=?,"
                            "zu=?,"
                            "zd=?,"
                            "dh=?,"
                            "zave=?,"
                            "k=?,"
                            "n=? WHERE "
                            "id=?;", _matrix)
        except Exception as e:
            logging.warning(e)
            logging.warning("更新错误")
        conn.commit()
        conn.close()
        logging.info("写入完成")

    def on_btn_go_clicked(self):
        # 读取枯水年流量数据
        if self.db_isnone():
            QMessageBox.warning(self, "警告", "数据库为空")
            return
        conn = sqlite3.connect(self.db)
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

        error = self.ledt_error.text()
        if len(error) == 0:
            error = 0.1
        else:
            try:
                error = float(error)
            except Exception as e:
                logging.error(e)
                QMessageBox.warning(self, "警告", "输入有误！")
                return
        # 获取水位
        # try:
        #     Z_s, Z_d = int(self.ledt_nsl.text()), int(self.ledt_dsl.text())
        # except Exception as e:
        #     logging.error(e)
        #     QMessageBox.warning(self, "警告", "水位输入错误")
        #     return
        z_s = 175
        z_d = 145
        # 合成数据字典
        # _data = self.make_data_dict()
        _data = {
            'year': 1883,
            'xsq': {
                7: 32705,
                8: 30557,
                9: 33819,
                10: 31605
            },
            'gsq': {
                1: 5280,
                2: 4490,
                3: 6967,
                4: 8152
            },
            'bxbg': {
                12: 8133,
                5: 19827,
                6: 26992,
                11: 13990
            }
        }

        self.worker = Worker(_data, error, z_s, z_d, zo, kh, zv, odh)
        self.worker.run(self._time)
        self.show_table()
        if self.worker.is_ok(self._time):
            logging.info("计算完成！")
        elif self.worker.over(self._time):
            logging.info("N={},N过小,请增大:".format(round(self.worker.N_eq/10000, 3)))
        else:
            logging.info("N={},N过大,请减小:".format(round(self.worker.N_eq/10000, 3)))
        self.btn_next_N.setDisabled(False)

    def on_btn_next_n_clicked(self,):
        if self.worker is None:
            QMessageBox.warning(self, "警告", "请先进行等出力计算！")
            return
        try:
            n = float(self.ledt_next_N.text()) * 10000
        except Exception as e:
            logging.error(e)
            QMessageBox.warning(self, "警告", "输入有误！")
            return

        if self.worker.over(self._time):
            self.worker.set_n(n)
            self.worker.run(self._time)
            if self.worker.over(self._time):
                logging.warning("输入过小，请增大N")
                return
        else:
            self.worker.set_n(n)
            self.worker.run(self._time)
            if not self.worker.over(self._time):
                logging.warning("输入过大，请减小N")
                return

        # 二分法逼近
        n_pre = min(self.worker.N, n)
        n_nex = max(self.worker.N, n)
        # work_thread = MyThread(parent=self)
        self.work_thread.set_obj(self.worker, n_pre, n_nex, self._time)
        # 启动线程进行计算，防止阻塞主线程
        self.work_thread.start()
        # 链接线程的signal，处理计算完毕的数据同步
        self.work_thread.finished.connect(self.work_finished)
        self.work_thread.working.connect(lambda s: logging.info(s))

    def on_btn_stop_clicked(self):
        self.work_thread.quit()
        self.work_thread.terminate()
        self.work_thread.wait(3000)
        logging.warning("已强制停止")

    def work_finished(self, obj):
        self.worker = obj  # 同步对象
        self.show_table()  # 绘制表格

    def show_table(self):
        matrix = self.worker.make_matrix()
        headers = ['月份', "天然来水", "引用流量", "蓄/供流量", "蓄/供水量", "时段初水量",
                   "时段均水量", "上游均水头", "下游均水头", "水头损失", "均水头", "出力系数", "出力"]
        self.table_data.setRowCount(len(matrix))
        self.table_data.setColumnCount(len(headers))
        self.table_data.setHorizontalHeaderLabels(headers)
        for r in range(len(matrix)):
            for c in range(len(headers)):
                self.table_data.setItem(r, c, QTableWidgetItem(str(round(self.worker.matrix[r][c], 2))))
        self.table_data.show()

    # 去掉这个功能
    # def on_btn_split_clicked(self):
    #     mons = int(self.cmbox_ddyms.currentText())  # 水文年起
    #     mone = int(self.cmbox_ddyme.currentText())  # 水文年止
    #     if self.db_isnone():
    #         QMessageBox.warning(self, "警告", "请选择数据库")
    #         return
    #     conn = sqlite3.connect(self.db)
    #     cur = conn.cursor()
    #
    #     logging.info("正在从数据表Qmon读取径流数据...")
    #     cur.execute("SELECT * FROM Qmon")
    #     data_ori = np.array(cur.fetchall())
    #     data = data_ori[:, 1:-1]
    #     logging.info("读取完成，正在计算...")
    #     hydroyear = Hydroyear(data=data, mons=mons, mone=mone)  # 划分水文年
    #     hy = hydroyear.split()  # 水文年划分结果
    #     avey = np.array([[row.sum()/len(row), ] for row in hy])  # 水文年均值
    #     # print(hy[0][monks-mons:monke-mons+13])
    #     aved = np.array([[row[monks-mons:monke-mons+13].sum()/(12-monks+monke+1), ] for row in hy])  # 枯水期均值
    #     year = [str(int(i)) for i in data_ori[:, 0]]
    #     year_str = "-".join(year)
    #     y2y = [year_str[i:i+9] for i in range(0, len(year_str)-8, 5)]
    #     y2y.append(year_str[-4:]+"-"+year_str[:4])
    #
    #     id = np.array([[str(i), ] for i in range(1, len(y2y)+1)])
    #     qmonsw = np.hstack((np.array([[s, ] for s in y2y]), hy, avey, aved, id))  # 水文年表
    #
    #     logging.info("正在写入数据库...")
    #     # 初始化的时候插入记录
    #     try:
    #         cur.executemany("INSERT INTO Qmonsw(y2y, mon1, mon2, mon3, mon4,mon5,mon6,"
    #                         "mon7,mon8,mon9,mon10,mon11,mon12,"
    #                         "avey,aved) VALUES("
    #                         "?,?,?,?,?,?,?,?,?,"
    #                         "?,?,?,?,?,?);", qmonsw)
    #     # 若插入失败则已经存在，更新记录
    #     except Exception as e:
    #         logging.warning(e)
    #         cur.executemany("UPDATE Qmonsw SET y2y=?,"
    #                         "mon1=?, mon2=?, mon3=?, mon4=?, mon5=?, mon6=?, "
    #                         "mon7=?, mon8=?, mon9=?, mon10=?, mon11=?, mon12=?,"
    #                         "avey=?, aved=?"
    #                         "WHERE id=? ;", qmonsw)
    #
    #     conn.commit()
    #     conn.close()
    #     logging.info("写入数据库完成,数据表为Qmonsw")
    #     print('ko')

    def on_btn_curve_fit_clicked(self):
        if self.db is None:
            QMessageBox.warning(self, self._tr("Warning", '警告'), self._tr("database is none", "数据库为空"))
            return
        try:
            conn = sqlite3.connect(self.db)
            cur = conn.cursor()
            logging.info("正在读取数年平均流量...")
            cur.execute("SELECT y2y,aved FROM Qmonsw;")
            data_ori = np.array(cur.fetchall())
            data = data_ori[:, 1].copy()
            conn.close()
        except Exception as e:
            logging.error(e)
            QMessageBox.warning(self, self._tr("Warning", '警告'), self._tr("database error!", "数据库错误！"))
            return

        logging.info("正在计算...")
        flooder = Flood(data=data)
        flooder.go()
        # TODO 优化适线
        # xnew = np.linspace(np.array(flooder1.x_ori).min(), np.array(flooder1.x_ori).max(), len(flooder1.x_ori)*10)
        # ynew = flooder1.optimize(xnew)
        # flooder = Flood(data=ynew)
        # flooder.go()
        ploter = Ploter()

        rows_max = max(len(flooder.y_ori), len(flooder.y))
        self.table_data.setRowCount(rows_max)
        self.table_data.setColumnCount(6)
        self.table_data.setHorizontalHeaderLabels(["经验频率(%)", '流量(m3/s)', '理论频率(%)', '流量(m3/s)', "年份", '流量(m3/s)'])
        logging.info("正在绘制表格...")
        for r in range(len(flooder.y_ori)):
            self.table_data.setItem(r, 0, QTableWidgetItem(str(round(flooder.p[r]*100, 3))))
            self.table_data.setItem(r, 1, QTableWidgetItem(str(round(flooder.y_ori[r], 3))))
        for r in range(len(flooder.x_std)):
            self.table_data.setItem(r, 2, QTableWidgetItem(str(round(flooder.x_std[r], 3))))
            self.table_data.setItem(r, 3, QTableWidgetItem(str(round(flooder.y[r], 3))))
        for r in range(len(data_ori[:, 0])):
            self.table_data.setItem(r, 4, QTableWidgetItem(str(data_ori[r, 0])))
            self.table_data.setItem(r, 5, QTableWidgetItem(str(round([float(i) for i in data_ori[:, 1]][r], 3))))
        self.table_data.show()

        logging.info("正在绘图...")
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ploter.heisen(ax)
        ax.plot(flooder.x_ori, flooder.y_ori, 'ro', label='original')
        ax.plot(flooder.x, flooder.y, 'b--', label='fit')

        self.canvas.draw()
        logging.info("适线完成！")

    def db_isnone(self):
        if self.db is None or len(self.db) == 0:
            return True
        return False

    def make_data_dict(self):
        gsq = self.ledt_gsq.text()
        xsq = self.ledt_xsq.text()
        if not all([gsq, xsq]):
            QMessageBox.warning(self, "警告", '输入错误！')
            return
        gsq = [int(i) for i in gsq.split(',')]
        xsq = [int(i) for i in xsq.split(',')]
        bxbg = np.array([i if i not in gsq and i not in xsq else -1 for i in range(1, 13)])
        bxbg = bxbg[bxbg>0]

        desq = self.ledt_desq.text()
        try:
            desq = float(desq)
        except Exception as e:
            logging.error(e)
            QMessageBox.warning(self, "警告", "设计径流输入错误！")
            return

        year = int(self.cmbox_ddy.currentText())
        y2y = (str(year) + "-" + str(year + 1),)
        try:
            conn = sqlite3.connect(self.db)
            cur = conn.cursor()
            cur.execute(u"SELECT * FROM Qmonsw WHERE y2y=?;", y2y)
        except Exception as e:
            logging.error(e)
            QMessageBox.warning(self, "警告", "数据库错误")
            return
        data = list(cur.fetchall()[0])[2:]
        data = [i*desq/data[-1] for i in data]
        _dict = {
            'year': year,
            'gsq': {},
            'xsq': {},
            'bxbg': {}
        }
        for m in gsq:
            _idx = self.map[m]
            _dict['gsq'][m] = data[_idx-1]
        for m in xsq:
            _idx = self.map[m]
            _dict['xsq'] = data[_idx-1]
        for m in bxbg:
            _idx = self.map[m]
            _dict['bxbq'] = data[_idx - 1]
        return _dict


class MyThread(QThread):
    working = pyqtSignal(str)  # 阶段计算完毕的信号，发射参数为字符串
    finished = pyqtSignal(object)  # 计算完成的信号，发射参数为对象

    def __init__(self, parent=None):
        super(MyThread, self).__init__(parent)
        self.worker = None
        self._time = None
        self.n_pre, self.n_nex = None, None
        self.timeout = 30

    def set_obj(self, worker, n_pre, n_nex, _time):
        self.worker = worker
        self._time = _time
        self.n_pre, self.n_nex = n_pre, n_nex

    def run(self):
        self.working.emit("线程启动，使用二分法开始计算，请稍候...")
        start = time.time()
        while True:
            if time.time() - start > self.timeout:
                self.working.emit("计算超时")
                self.finished.emit(self.worker)
                return
            # 二分法逼近
            mid = (self.n_pre + self.n_nex) / 2
            self.worker.set_n(mid)
            self.worker.run(self._time)
            if self.worker.is_ok(self._time):
                self.working.emit("计算完成，出力N = {}"
                                  .format(round(self.worker.N_eq/10000, 3)))
                break
            elif self.worker.over(self._time):
                self.n_pre = mid
                self.working.emit("出力N过小，增大N = [{}-{}] 万kW"
                                  .format(round(self.n_pre/10000, 3), round(self.n_nex/10000, 3)))
            else:
                self.n_nex = mid
                self.working.emit("出力N过大，减小N = [{}-{}] 万kW"
                                  .format(round(self.n_pre/10000, 3), round(self.n_nex/10000, 3)))
        self.finished.emit(self.worker)
