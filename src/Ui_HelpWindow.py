from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtCore import QRect, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView


class Ui_HelpWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Help')
        self.setGeometry(QRect(200, 200, 800, 600))
        self.setupUi()

    def setupUi(self):
        self.browser = QWebEngineView()
        self.browser.load(QUrl('https://github.com/rainyl/db_hydrosoftware_final/blob/master/README.md'))
        layout = QHBoxLayout()
        layout.addWidget(self.browser)

        self.setLayout(layout)
