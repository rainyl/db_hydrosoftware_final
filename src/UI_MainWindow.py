# -*- coding: utf-8 -*-

# app for database and hydrosoftware final work
# author: rainyl
# update: 2019-3-27


from PyQt5.QtWidgets import (QMainWindow, QMenuBar, QMenu, QAction, QStatusBar,
                             QLabel, QGroupBox, QHBoxLayout, QVBoxLayout, QGridLayout,
                             QPushButton, QCheckBox, QComboBox, QLineEdit, QFormLayout,
                             QWidget, QTableWidget, QTextBrowser, QTabWidget, QSplitter,
                             QMessageBox)
from PyQt5.QtCore import (QCoreApplication, QRect, QTimer, QDateTime, Qt, pyqtSignal, QRegExp)
from PyQt5.QtGui import QIcon, QDoubleValidator, QRegExpValidator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from src.SSSetter import *
import res.res
import src.qss
import logging
from src.Namer import Namer


class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QTextBrowser(parent)

    def emit(self, record):
        msg = self.format(record)
        self.widget.append(msg)
        with open('log.log', 'a') as f:
            f.write(msg+"\n")
        f.close()


class UI_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1200, 800)
        self.setStyleSheet(FlatWhite.get_qss())
        self.setWindowIcon(QIcon(":/images/icon"))
        self._tr = QCoreApplication.translate
        self.centralwidget = QWidget()
        self.layout_global = QGridLayout()
        # self.layout_global.setColumnStretch(0, 1)
        # self.layout_global.setColumnStretch(1, 2)
        # self.layout_global.setColumnStretch(2, 1)
        self.centralwidget.setLayout(self.layout_global)
        self.setCentralWidget(self.centralwidget)

        self.draw()

        self.timer_time = QTimer(self)
        self.timer_time.start(1000)
        self.timer_time.timeout.connect(self.on_time_updated)
        self.copyright = QLabel()
        self.copyright.setStatusTip("https://github.com/rainyl")
        self.statusbar.addPermanentWidget(self.copyright)

        self.retranslate_ui()

    def draw(self):
        self.draw_menu()
        self.draw_content()
        self.draw_statusbar()

    def draw_menu(self):
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 800, 30))

        self.menu_files = QMenu()
        self.menu_tools = QMenu()
        self.menu_help = QMenu()

        self.menu_team = QMenu("小组")
        self.action_lyl = QAction("刘彦龙")
        self.action_lyl.setObjectName(Namer.action_lyl)
        self.action_brb = QAction("白汝冰")
        self.action_brb.setObjectName(Namer.action_brb)
        self.action_hjy = QAction("何婧源")
        self.action_hjy.setObjectName(Namer.action_hjy)
        self.menu_team.addActions([self.action_lyl, self.action_brb, self.action_hjy])

        self.menu_open = QMenu()
        self.action_open_db = QAction()
        self.action_open_db.setObjectName(Namer.action_open_db)
        self.menu_open.addActions([self.action_open_db])

        self.action_exit = QAction()
        self.action_exit.setObjectName(Namer.action_exit)

        self.msgbox_about = QMessageBox()
        self.msgbox_about.setText('''
            --- 水库等出力调节计算软件 --- \n
            --- 学校：武汉大学\n
            --- 专业：水文与水资源工程\n
            --- 作者：刘彦龙、白汝冰、何婧源\n
            --- 指导教师：艾学山、万飚\n
        ''')
        self.msgbox_about.setWindowTitle("关于")

        self.action_about = QAction()
        self.action_about.triggered.connect(lambda: self.msgbox_about.show())
        self.action_manul = QAction()

        self.menubar.addMenu(self.menu_files)
        self.menubar.addMenu(self.menu_help)
        self.menubar.addMenu(self.menu_team)

        self.menu_help.addActions([self.action_manul, self.action_about])
        self.menu_files.addMenu(self.menu_open)
        self.menu_files.addActions([self.action_exit])

        self.setMenuBar(self.menubar)

    def draw_statusbar(self):
        self.statusbar = QStatusBar(self)

        self.setStatusBar(self.statusbar)

    def draw_content(self):
        self.draw_input()
        self.draw_index()
        self.draw_show_figs()

    def draw_input(self):
        pass

    def draw_show_figs(self):
        pass

    def draw_index(self):
        # left
        self.lbl_nsl = QLabel()
        self.ledt_nsl = QLineEdit()
        self.ledt_nsl.setStatusTip(self._tr("normal storage level", "正常蓄水位"))
        self.ledt_nsl.setObjectName(Namer.ledt_nsl)
        self.ledt_nsl.setValidator(QDoubleValidator(0, 1000000, 10))
        self.lbl_dsl = QLabel()
        self.ledt_dsl = QLineEdit()
        self.ledt_dsl.setStatusTip(self._tr("dead storage level", "死水位"))
        self.ledt_dsl.setObjectName(Namer.ledt_dsl)
        self.ledt_dsl.setValidator(QDoubleValidator(0, 1000000, 10))
        self.lbl_K = QLabel()
        self.ledt_K = QLineEdit()
        self.ledt_K.setStatusTip(self._tr("K", "自动插值"))
        self.ledt_K.setPlaceholderText(self._tr("K", "自动插值"))
        self.ledt_K.setDisabled(True)
        self.ledt_K.setObjectName(Namer.ledt_K)
        self.lbl_error = QLabel()
        self.ledt_error = QLineEdit()
        self.ledt_error.setPlaceholderText(self._tr("error", "默认0.1"))
        self.ledt_error.setStatusTip(self._tr("error", "计算精度, 默认0.1,最大10位小数"))
        self.ledt_error.setValidator(QDoubleValidator(0, 1000000, 10))
        self.lbl_next_N = QLabel(self._tr("Next N", "出力(万kW)"))
        self.ledt_next_N = QLineEdit()
        self.ledt_next_N.setPlaceholderText("下一阶段出力")
        self.ledt_next_N.setStatusTip("下一阶段出力，单位为[万kW]")
        self.ledt_next_N.setValidator(QDoubleValidator(0, 1000000, 10))
        self.btn_next_N = QPushButton(self._tr("Go on", "继续计算"))
        self.btn_write_db = QPushButton(self._tr("write", "写入数据库"))
        self.btn_next_N.setStatusTip("继续计算出力，请先进行等出力计算")
        self.btn_next_N.setDisabled(True)

        vbox_args_left = QHBoxLayout()
        fmlt_args_left = QFormLayout()
        fmlt_args_left.addRow(self.lbl_nsl, self.ledt_nsl)
        fmlt_args_left.addRow(self.lbl_dsl, self.ledt_dsl)
        fmlt_args_left.addRow(self.lbl_next_N, self.ledt_next_N)
        fmlt_args_r = QFormLayout()
        fmlt_args_r.addRow(self.lbl_K, self.ledt_K)
        fmlt_args_r.addRow(self.lbl_error, self.ledt_error)
        fmlt_args_r.addRow(self.btn_next_N, self.btn_write_db)
        vbox_args_left.addLayout(fmlt_args_left)
        vbox_args_left.addLayout(fmlt_args_r)
        fmlt_args = QFormLayout()
        fmlt_args.addRow(vbox_args_left)
        grpbox_args = QGroupBox(self._tr("config args", "配置参数"))
        grpbox_args.setLayout(fmlt_args)

        self.lbl_ddy = QLabel()
        self.cmbox_ddy = QComboBox()
        self.cmbox_ddy.setStatusTip("设计枯水年的年份")
        self.lbl_desq = QLabel(self._tr("Des Q", "设计年径流"))
        self.ledt_desq = QLineEdit()
        self.ledt_desq.setPlaceholderText("设计年径流")
        self.ledt_desq.setStatusTip("设计年径流")
        self.ledt_desq.setValidator(QDoubleValidator(0, 1000000, 10))
        self.lbl_ddym = QLabel()
        self.cmbox_ddyms = QComboBox()
        self.cmbox_ddyms.setStatusTip("水文年起止月份")
        self.cmbox_ddyms.addItems([str(m) for m in range(1, 13)])
        lbl_mid = QLabel(self._tr("to", '月 至'))
        lbl_right = QLabel(self._tr("mon", '月'))
        self.cmbox_ddyme = QComboBox()
        self.cmbox_ddyme.addItems([str(m) for m in range(1, 13)])
        layout_cmbox_ddym = QHBoxLayout()
        layout_cmbox_ddym.addWidget(self.cmbox_ddyms)
        layout_cmbox_ddym.addWidget(lbl_mid)
        layout_cmbox_ddym.addWidget(self.cmbox_ddyme)
        layout_cmbox_ddym.addWidget(lbl_right)

        lbl_gsq = QLabel("供水期")
        self.ledt_gsq = QLineEdit()
        self.ledt_gsq.setValidator(QRegExpValidator(QRegExp(r"([0-9]{1,2}\,)+")))
        self.ledt_gsq.setPlaceholderText('12,1,2,3,4')
        lbl_xsq = QLabel("蓄水期")
        self.ledt_xsq = QLineEdit()
        self.ledt_xsq.setValidator(QRegExpValidator(QRegExp(r"([0-9]{1,2}\,)+")))
        self.ledt_xsq.setPlaceholderText('7,8,9,10')
        layout_monk = QHBoxLayout()
        layout_monk.addWidget(lbl_gsq)
        layout_monk.addWidget(self.ledt_gsq)
        layout_monk.addWidget(lbl_xsq)
        layout_monk.addWidget(self.ledt_xsq)

        layout_flood_cls = QFormLayout()
        layout_desq = QHBoxLayout()
        layout_desq.addWidget(self.lbl_ddy)
        layout_desq.addWidget(self.cmbox_ddy)
        layout_desq.addWidget(self.lbl_desq)
        layout_desq.addWidget(self.ledt_desq)
        layout_flood_cls.addRow(layout_desq)
        layout_flood_cls.addRow(self.lbl_ddym, layout_cmbox_ddym)
        layout_flood_cls.addRow(layout_monk)
        grpbox_flood_cls = QGroupBox(self._tr("Design dry year", "设计枯水年"))
        grpbox_flood_cls.setLayout(layout_flood_cls)

        self.btn_reg_go = QPushButton("&Regular go")
        self.btn_reg_go.setStatusTip("等出力计算")
        self.btn_curve_fit = QPushButton(self._tr("curve fit", "适线"))
        self.btn_curve_fit.setStatusTip("利用枯水期资料进行适线")
        self.btn_stop = QPushButton("停止")
        # self.btn_split_sw = QPushButton(self._tr("Split", "划分水文年"))
        # self.btn_split_sw.setStatusTip("对月流量资料进行水文年的划分")
        layout_btn_go = QFormLayout()
        layout_btn_go_1 = QHBoxLayout()
        layout_btn_go_1.addWidget(self.btn_curve_fit)
        layout_btn_go_1.addWidget(self.btn_reg_go)
        layout_btn_go_1.addWidget(self.btn_stop)
        # layout_btn_go_1.addWidget(self.btn_split_sw)
        layout_btn_go.addRow(layout_btn_go_1)
        grpbox_go = QGroupBox(self._tr("Go", "计算"))
        grpbox_go.setLayout(layout_btn_go)

        self.chkbox_zv = QCheckBox(self._tr("zv", "库容曲线"))
        self.chkbox_zv.setObjectName(Namer.chkbox_zv)
        self.chkbox_zo = QCheckBox(self._tr("zo", "下泄流量曲线"))
        self.chkbox_zo.setObjectName(Namer.chkbox_zo)
        self.chkbox_K = QCheckBox(self._tr("K", "出力系数曲线"))
        self.chkbox_K.setObjectName(Namer.chkbox_K)
        self.chkbox_dh = QCheckBox(self._tr("dh", "水头损失"))
        self.chkbox_dh.setObjectName(Namer.chkbox_dh)
        self.chkbox_n = QCheckBox(self._tr('n', "出力过程"))
        self.chkbox_n.setObjectName(Namer.chkbox_n)
        self.btn_draw = QPushButton(self._tr("Draw", "绘图"))
        layout_draw_l = QFormLayout()
        layout_draw_l.addRow(self.chkbox_zv)
        layout_draw_l.addRow(self.chkbox_zo)
        layout_draw_m = QFormLayout()
        layout_draw_m.addRow(self.chkbox_K)
        layout_draw_m.addRow(self.chkbox_dh)
        layout_draw_r = QFormLayout()
        layout_draw_r.addRow(self.chkbox_n)
        layout_draw_r.addRow(self.btn_draw)
        hbox_draw = QHBoxLayout()
        hbox_draw.addLayout(layout_draw_l)
        hbox_draw.addLayout(layout_draw_m)
        hbox_draw.addLayout(layout_draw_r)
        layout_draw = QFormLayout()
        layout_draw.addRow(hbox_draw)
        grpbox_draw = QGroupBox(self._tr("Draw", "绘图"))
        grpbox_draw.setLayout(layout_draw)

        layout_log = QVBoxLayout()
        self.logger = QTextEditLogger(self)
        self.logger.widget.setText("---LOG---\n若未知枯水年请按【适线】自动选定\n"
                                   "适线采用枯水期平均流量确定枯水年\n"
                                   "但是本软件暂时不包括优化")
        self.logger.setFormatter(
            logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt="%Y-%m-%d %H:%M:%S"))
        layout_log.addWidget(self.logger.widget)
        grpbox_log = QGroupBox(self._tr("Log", "日志"))
        grpbox_log.setLayout(layout_log)

        # spliter_left = QSplitter(Qt.Vertical)
        # spliter_left.addWidget(grpbox_args)
        # spliter_left.addWidget(grpbox_flood_cls)
        # spliter_left.addWidget(grpbox_go)
        # spliter_left.addWidget(grpbox_draw)
        # spliter_left.addWidget(grpbox_log)

        vbox_layout_left = QVBoxLayout()
        vbox_layout_left.addWidget(grpbox_args)
        vbox_layout_left.addWidget(grpbox_flood_cls)
        vbox_layout_left.addWidget(grpbox_go)
        vbox_layout_left.addWidget(grpbox_draw)
        vbox_layout_left.addWidget(grpbox_log)

        grpbox_left = QGroupBox(self._tr("func", "功能"))
        grpbox_left.setLayout(vbox_layout_left)

        # for middle
        self.table_data = QTableWidget()
        self.table_data.setRowCount(2)
        self.table_data.setHorizontalHeaderLabels(["No", "Q_in", "Water level"])

        self.fig = Figure()
        ax = self.fig.add_subplot(111)
        ax.set_title("fit")
        self.canvas = FigureCanvas(self.fig)
        self.fig_zv = Figure()
        self.canvas_zv = FigureCanvas(self.fig_zv)
        self.fig_zo = Figure()
        self.canvas_zo = FigureCanvas(self.fig_zo)
        self.fig_k = Figure()
        self.canvas_k = FigureCanvas(self.fig_k)
        self.fig_dh = Figure()
        self.canvas_dh = FigureCanvas(self.fig_dh)
        self.tab_fig = QTabWidget()
        self.fig_n = Figure()
        self.canvas_n = FigureCanvas(self.fig_n)
        self.tab_fig.addTab(self.canvas, self._tr("fit", "适线"))
        self.tab_fig.addTab(self.canvas_zv, self._tr("zv", "库容曲线"))
        self.tab_fig.addTab(self.canvas_zo, self._tr("zo", "下泄流量曲线"))
        self.tab_fig.addTab(self.canvas_k, self._tr("K", "出力系数曲线"))
        self.tab_fig.addTab(self.canvas_dh, self._tr("dh", "水头损失"))
        self.tab_fig.addTab(self.canvas_n, self._tr("n", "出力过程"))

        spliter_mid = QSplitter(Qt.Vertical)
        spliter_mid.addWidget(self.table_data)
        spliter_mid.addWidget(self.tab_fig)

        vbox_layout_mid = QVBoxLayout()
        vbox_layout_mid.addWidget(spliter_mid)
        grpbox_right = QGroupBox(self._tr("tables and figures", "表格与绘图"))
        grpbox_right.setLayout(vbox_layout_mid)
        # vbox_layout_mid.addWidget(self.table_data)
        # vbox_layout_mid.addWidget(self.tab_fig)

        spliter_global = QSplitter(Qt.Horizontal)
        spliter_global.addWidget(grpbox_left)
        spliter_global.addWidget(grpbox_right)

        self.layout_global.addWidget(spliter_global)
        # self.layout_global.addWidget(spliter_left, 0, 0, Qt.AlignCenter)
        # self.layout_global.addLayout(v, 0, 0, Qt.AlignCenter)
        # self.layout_global.addLayout(vbox_layout_mid, 0, 1, Qt.AlignCenter)
        # self.layout_global.addWidget(spliter_mid, 0, 1, Qt.AlignCenter)

    def retranslate_ui(self):
        _tr = QCoreApplication.translate

        # fro menu
        self.setWindowTitle(_tr("MainWindow", "主界面"))
        self.menu_files.setTitle(_tr("&Files", "文件"))
        self.menu_help.setTitle(_tr("&Help", "帮助"))
        self.menu_open.setTitle(_tr("&Open", "打开"))
        self.action_open_db.setText(_tr("Database", "数据库"))
        self.action_about.setText(_tr("&About", "关于"))
        self.action_manul.setText(_tr("&Manul", "使用手册"))
        self.action_exit.setText(_tr("&Exit", "退出"))

        # for left index
        self.lbl_dsl.setText(_tr("dead storage level(m)", "死水位(m)"))
        self.lbl_nsl.setText(_tr("normal storage level(m)", "正常蓄水位(m)"))
        self.lbl_K.setText(_tr("K", "出力系数K"))
        self.lbl_error.setText(_tr("error", "计算精度"))

        self.lbl_ddy.setText(_tr("design dry year", "设计枯水年"))
        self.lbl_ddym.setText(_tr("water year", "水文年起止"))

        self.btn_reg_go.setText(_tr("&Go", "等出力计算"))

    # 设置时间
    def on_time_updated(self):
        current_time = QDateTime.currentDateTime()
        self.copyright.setText(
            "<a href='https://github.com/rainyl'>©2019 Rainyl's Team All Rights Reserved " + "</a>" + current_time.toString(
                " hh:mm:ss"))
