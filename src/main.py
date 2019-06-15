# -*- coding: utf-8 -*-

# app for database and hydrosoftware final work
# author: rainyl
# update: 2019-3-27

import sys
from PyQt5.QtWidgets import QApplication
from src.MainWindow import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()

    sys.exit(app.exec_())
