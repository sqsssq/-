# -*- coding: utf-8 -*-
# @Time    : 2020/6/13 9:25
# @Author  : SanZhi
# @File    : main.py.py
# @Software: PyCharm
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
import cv2
import k

class parentWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.main_ui = k.Ui_MainWindow()
        self.main_ui.setupUi(self, cv2.VideoCapture(0))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # MainWindow = QMainWindow()
    # ui = k.Ui_MainWindow()
    # ui.setupUi(MainWindow, cv2.VideoCapture(0))
    # MainWindow.show()

    window = parentWindow()
    # child = childWindow()

    # 通过toolButton将两个窗体关联
    # btn = window.main_ui.pushButton_2
    # btn.clicked.connect(child.show)

    # 显示
    window.show()

    sys.exit(app.exec_())