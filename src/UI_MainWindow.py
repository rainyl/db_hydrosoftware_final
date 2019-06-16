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
        about = '''
        <!DOCTYPE html><html><head>
      <title>about</title>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <style> 
      /**
 * prism.js Github theme based on GitHub's theme.
 * @author Sam Clarke
 */
code[class*="language-"],
pre[class*="language-"] {
  color: #333;
  background: none;
  font-family: Consolas, "Liberation Mono", Menlo, Courier, monospace;
  text-align: left;
  white-space: pre;
  word-spacing: normal;
  word-break: normal;
  word-wrap: normal;
  line-height: 1.4;

  -moz-tab-size: 8;
  -o-tab-size: 8;
  tab-size: 8;

  -webkit-hyphens: none;
  -moz-hyphens: none;
  -ms-hyphens: none;
  hyphens: none;
}

/* Code blocks */
pre[class*="language-"] {
  padding: .8em;
  overflow: auto;
  /* border: 1px solid #ddd; */
  border-radius: 3px;
  /* background: #fff; */
  background: #f5f5f5;
}

/* Inline code */
:not(pre) > code[class*="language-"] {
  padding: .1em;
  border-radius: .3em;
  white-space: normal;
  background: #f5f5f5;
}

.token.comment,
.token.blockquote {
  color: #969896;
}

.token.cdata {
  color: #183691;
}

.token.doctype,
.token.punctuation,
.token.variable,
.token.macro.property {
  color: #333;
}

.token.operator,
.token.important,
.token.keyword,
.token.rule,
.token.builtin {
  color: #a71d5d;
}

.token.string,
.token.url,
.token.regex,
.token.attr-value {
  color: #183691;
}

.token.property,
.token.number,
.token.boolean,
.token.entity,
.token.atrule,
.token.constant,
.token.symbol,
.token.command,
.token.code {
  color: #0086b3;
}

.token.tag,
.token.selector,
.token.prolog {
  color: #63a35c;
}

.token.function,
.token.namespace,
.token.pseudo-element,
.token.class,
.token.class-name,
.token.pseudo-class,
.token.id,
.token.url-reference .token.variable,
.token.attr-name {
  color: #795da3;
}

.token.entity {
  cursor: help;
}

.token.title,
.token.title .token.punctuation {
  font-weight: bold;
  color: #1d3e81;
}

.token.list {
  color: #ed6a43;
}

.token.inserted {
  background-color: #eaffea;
  color: #55a532;
}

.token.deleted {
  background-color: #ffecec;
  color: #bd2c00;
}

.token.bold {
  font-weight: bold;
}

.token.italic {
  font-style: italic;
}


/* JSON */
.language-json .token.property {
  color: #183691;
}

.language-markup .token.tag .token.punctuation {
  color: #333;
}

/* CSS */
code.language-css,
.language-css .token.function {
  color: #0086b3;
}

/* YAML */
.language-yaml .token.atrule {
  color: #63a35c;
}

code.language-yaml {
  color: #183691;
}

/* Ruby */
.language-ruby .token.function {
  color: #333;
}

/* Markdown */
.language-markdown .token.url {
  color: #795da3;
}

/* Makefile */
.language-makefile .token.symbol {
  color: #795da3;
}

.language-makefile .token.variable {
  color: #183691;
}

.language-makefile .token.builtin {
  color: #0086b3;
}

/* Bash */
.language-bash .token.keyword {
  color: #0086b3;
}

/* highlight */
pre[data-line] {
  position: relative;
  padding: 1em 0 1em 3em;
}
pre[data-line] .line-highlight-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  background-color: transparent;
  display: block;
  width: 100%;
}

pre[data-line] .line-highlight {
  position: absolute;
  left: 0;
  right: 0;
  padding: inherit 0;
  margin-top: 1em;
  background: hsla(24, 20%, 50%,.08);
  background: linear-gradient(to right, hsla(24, 20%, 50%,.1) 70%, hsla(24, 20%, 50%,0));
  pointer-events: none;
  line-height: inherit;
  white-space: pre;
}

pre[data-line] .line-highlight:before, 
pre[data-line] .line-highlight[data-end]:after {
  content: attr(data-start);
  position: absolute;
  top: .4em;
  left: .6em;
  min-width: 1em;
  padding: 0 .5em;
  background-color: hsla(24, 20%, 50%,.4);
  color: hsl(24, 20%, 95%);
  font: bold 65%/1.5 sans-serif;
  text-align: center;
  vertical-align: .3em;
  border-radius: 999px;
  text-shadow: none;
  box-shadow: 0 1px white;
}

pre[data-line] .line-highlight[data-end]:after {
  content: attr(data-end);
  top: auto;
  bottom: .4em;
}html body{font-family:"Helvetica Neue",Helvetica,"Segoe UI",Arial,freesans,sans-serif;font-size:16px;line-height:1.6;color:#333;background-color:#fff;overflow:initial;box-sizing:border-box;word-wrap:break-word}html body>:first-child{margin-top:0}html body h1,html body h2,html body h3,html body h4,html body h5,html body h6{line-height:1.2;margin-top:1em;margin-bottom:16px;color:#000}html body h1{font-size:2.25em;font-weight:300;padding-bottom:.3em}html body h2{font-size:1.75em;font-weight:400;padding-bottom:.3em}html body h3{font-size:1.5em;font-weight:500}html body h4{font-size:1.25em;font-weight:600}html body h5{font-size:1.1em;font-weight:600}html body h6{font-size:1em;font-weight:600}html body h1,html body h2,html body h3,html body h4,html body h5{font-weight:600}html body h5{font-size:1em}html body h6{color:#5c5c5c}html body strong{color:#000}html body del{color:#5c5c5c}html body a:not([href]){color:inherit;text-decoration:none}html body a{color:#08c;text-decoration:none}html body a:hover{color:#00a3f5;text-decoration:none}html body img{max-width:100%}html body>p{margin-top:0;margin-bottom:16px;word-wrap:break-word}html body>ul,html body>ol{margin-bottom:16px}html body ul,html body ol{padding-left:2em}html body ul.no-list,html body ol.no-list{padding:0;list-style-type:none}html body ul ul,html body ul ol,html body ol ol,html body ol ul{margin-top:0;margin-bottom:0}html body li{margin-bottom:0}html body li.task-list-item{list-style:none}html body li>p{margin-top:0;margin-bottom:0}html body .task-list-item-checkbox{margin:0 .2em .25em -1.8em;vertical-align:middle}html body .task-list-item-checkbox:hover{cursor:pointer}html body blockquote{margin:16px 0;font-size:inherit;padding:0 15px;color:#5c5c5c;border-left:4px solid #d6d6d6}html body blockquote>:first-child{margin-top:0}html body blockquote>:last-child{margin-bottom:0}html body hr{height:4px;margin:32px 0;background-color:#d6d6d6;border:0 none}html body table{margin:10px 0 15px 0;border-collapse:collapse;border-spacing:0;display:block;width:100%;overflow:auto;word-break:normal;word-break:keep-all}html body table th{font-weight:bold;color:#000}html body table td,html body table th{border:1px solid #d6d6d6;padding:6px 13px}html body dl{padding:0}html body dl dt{padding:0;margin-top:16px;font-size:1em;font-style:italic;font-weight:bold}html body dl dd{padding:0 16px;margin-bottom:16px}html body code{font-family:Menlo,Monaco,Consolas,'Courier New',monospace;font-size:.85em !important;color:#000;background-color:#f0f0f0;border-radius:3px;padding:.2em 0}html body code::before,html body code::after{letter-spacing:-0.2em;content:"\00a0"}html body pre>code{padding:0;margin:0;font-size:.85em !important;word-break:normal;white-space:pre;background:transparent;border:0}html body .highlight{margin-bottom:16px}html body .highlight pre,html body pre{padding:1em;overflow:auto;font-size:.85em !important;line-height:1.45;border:#d6d6d6;border-radius:3px}html body .highlight pre{margin-bottom:0;word-break:normal}html body pre code,html body pre tt{display:inline;max-width:initial;padding:0;margin:0;overflow:initial;line-height:inherit;word-wrap:normal;background-color:transparent;border:0}html body pre code:before,html body pre tt:before,html body pre code:after,html body pre tt:after{content:normal}html body p,html body blockquote,html body ul,html body ol,html body dl,html body pre{margin-top:0;margin-bottom:16px}html body kbd{color:#000;border:1px solid #d6d6d6;border-bottom:2px solid #c7c7c7;padding:2px 4px;background-color:#f0f0f0;border-radius:3px}@media print{html body{background-color:#fff}html body h1,html body h2,html body h3,html body h4,html body h5,html body h6{color:#000;page-break-after:avoid}html body blockquote{color:#5c5c5c}html body pre{page-break-inside:avoid}html body table{display:table}html body img{display:block;max-width:100%;max-height:100%}html body pre,html body code{word-wrap:break-word;white-space:pre}}.markdown-preview{width:100%;height:100%;box-sizing:border-box}.markdown-preview .pagebreak,.markdown-preview .newpage{page-break-before:always}.markdown-preview pre.line-numbers{position:relative;padding-left:3.8em;counter-reset:linenumber}.markdown-preview pre.line-numbers>code{position:relative}.markdown-preview pre.line-numbers .line-numbers-rows{position:absolute;pointer-events:none;top:1em;font-size:100%;left:0;width:3em;letter-spacing:-1px;border-right:1px solid #999;-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none}.markdown-preview pre.line-numbers .line-numbers-rows>span{pointer-events:none;display:block;counter-increment:linenumber}.markdown-preview pre.line-numbers .line-numbers-rows>span:before{content:counter(linenumber);color:#999;display:block;padding-right:.8em;text-align:right}.markdown-preview .mathjax-exps .MathJax_Display{text-align:center !important}.markdown-preview:not([for="preview"]) .code-chunk .btn-group{display:none}.markdown-preview:not([for="preview"]) .code-chunk .status{display:none}.markdown-preview:not([for="preview"]) .code-chunk .output-div{margin-bottom:16px}.scrollbar-style::-webkit-scrollbar{width:8px}.scrollbar-style::-webkit-scrollbar-track{border-radius:10px;background-color:transparent}.scrollbar-style::-webkit-scrollbar-thumb{border-radius:5px;background-color:rgba(150,150,150,0.66);border:4px solid rgba(150,150,150,0.66);background-clip:content-box}html body[for="html-export"]:not([data-presentation-mode]){position:relative;width:100%;height:100%;top:0;left:0;margin:0;padding:0;overflow:auto}html body[for="html-export"]:not([data-presentation-mode]) .markdown-preview{position:relative;top:0}@media screen and (min-width:914px){html body[for="html-export"]:not([data-presentation-mode]) .markdown-preview{padding:2em calc(50% - 457px + 2em)}}@media screen and (max-width:914px){html body[for="html-export"]:not([data-presentation-mode]) .markdown-preview{padding:2em}}@media screen and (max-width:450px){html body[for="html-export"]:not([data-presentation-mode]) .markdown-preview{font-size:14px !important;padding:1em}}@media print{html body[for="html-export"]:not([data-presentation-mode]) #sidebar-toc-btn{display:none}}html body[for="html-export"]:not([data-presentation-mode]) #sidebar-toc-btn{position:fixed;bottom:8px;left:8px;font-size:28px;cursor:pointer;color:inherit;z-index:99;width:32px;text-align:center;opacity:.4}html body[for="html-export"]:not([data-presentation-mode])[html-show-sidebar-toc] #sidebar-toc-btn{opacity:1}html body[for="html-export"]:not([data-presentation-mode])[html-show-sidebar-toc] .md-sidebar-toc{position:fixed;top:0;left:0;width:300px;height:100%;padding:32px 0 48px 0;font-size:14px;box-shadow:0 0 4px rgba(150,150,150,0.33);box-sizing:border-box;overflow:auto;background-color:inherit}html body[for="html-export"]:not([data-presentation-mode])[html-show-sidebar-toc] .md-sidebar-toc::-webkit-scrollbar{width:8px}html body[for="html-export"]:not([data-presentation-mode])[html-show-sidebar-toc] .md-sidebar-toc::-webkit-scrollbar-track{border-radius:10px;background-color:transparent}html body[for="html-export"]:not([data-presentation-mode])[html-show-sidebar-toc] .md-sidebar-toc::-webkit-scrollbar-thumb{border-radius:5px;background-color:rgba(150,150,150,0.66);border:4px solid rgba(150,150,150,0.66);background-clip:content-box}html body[for="html-export"]:not([data-presentation-mode])[html-show-sidebar-toc] .md-sidebar-toc a{text-decoration:none}html body[for="html-export"]:not([data-presentation-mode])[html-show-sidebar-toc] .md-sidebar-toc ul{padding:0 1.6em;margin-top:.8em}html body[for="html-export"]:not([data-presentation-mode])[html-show-sidebar-toc] .md-sidebar-toc li{margin-bottom:.8em}html body[for="html-export"]:not([data-presentation-mode])[html-show-sidebar-toc] .md-sidebar-toc ul{list-style-type:none}html body[for="html-export"]:not([data-presentation-mode])[html-show-sidebar-toc] .markdown-preview{left:300px;width:calc(100% -  300px);padding:2em calc(50% - 457px -  150px);margin:0;box-sizing:border-box}@media screen and (max-width:1274px){html body[for="html-export"]:not([data-presentation-mode])[html-show-sidebar-toc] .markdown-preview{padding:2em}}@media screen and (max-width:450px){html body[for="html-export"]:not([data-presentation-mode])[html-show-sidebar-toc] .markdown-preview{width:100%}}html body[for="html-export"]:not([data-presentation-mode]):not([html-show-sidebar-toc]) .markdown-preview{left:50%;transform:translateX(-50%)}html body[for="html-export"]:not([data-presentation-mode]):not([html-show-sidebar-toc]) .md-sidebar-toc{display:none}
/* Please visit the URL below for more information: */
/*   https://shd101wyy.github.io/markdown-preview-enhanced/#/customize-css */
 
      </style>
    </head>
    <body for="html-export">
      <div class="mume markdown-preview  ">
      <h2 class="mume-header" id="21-%E6%B0%B4%E5%BA%93%E7%AD%89%E5%87%BA%E5%8A%9B%E8%AE%A1%E7%AE%97%E8%BE%85%E5%8A%A9%E8%BD%AF%E4%BB%B6">21-&#x6C34;&#x5E93;&#x7B49;&#x51FA;&#x529B;&#x8BA1;&#x7B97;&#x8F85;&#x52A9;&#x8F6F;&#x4EF6;</h2>

<ul>
<li>&#x5355;&#x4F4D;&#xFF1A;&#x6B66;&#x6C49;&#x5927;&#x5B66;&#x6C34;&#x5229;&#x6C34;&#x7535;&#x5B66;&#x9662;</li>
<li>&#x4E13;&#x4E1A;&#xFF1A;&#x6C34;&#x6587;&#x4E0E;&#x6C34;&#x8D44;&#x6E90;&#x5DE5;&#x7A0B;</li>
<li>&#x4F5C;&#x8005;&#xFF1A;&#x5218;&#x5F66;&#x9F99;&#x3001;&#x767D;&#x6C5D;&#x51B0;&#x3001;&#x4F55;&#x5A67;&#x6E90;</li>
<li>&#x6307;&#x5BFC;&#x6559;&#x5E08;&#xFF1A;&#x827E;&#x5B66;&#x5C71;&#x3001;&#x4E07;&#x98DA;</li>
<li>&#x5F00;&#x53D1;&#x65F6;&#x95F4;&#xFF1A;2019&#x5E74;6&#x6708;</li>
</ul>

      </div>
    </body></html>'''
        # self.msgbox_about.setText('''
        #     --- 水库等出力调节计算软件 --- \n
        #     --- 学校：武汉大学\n
        #     --- 专业：水文与水资源工程\n
        #     --- 作者：刘彦龙、白汝冰、何婧源\n
        #     --- 指导教师：艾学山、万飚\n
        # ''')
        self.msgbox_about.setText(about)
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
        self.setWindowTitle(_tr("MainWindow", "21-水库等出力计算辅助软件-武汉大学水利水电学院-Rainyl's Team-"))
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
