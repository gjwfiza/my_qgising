# -*- coding: utf-8 -*-
'''
模三分析图例
@author: Karwai Kwok
'''

from PyQt4.QtGui import QDialog, QWidget, QLabel, QGridLayout
from PyQt4.QtCore import Qt

class Mod3Legend(QDialog):
    def __init__(self, iface, styleManager, parent=None):
        super(Mod3Legend, self).__init__()
        self.iface = iface
        self.styleManager = styleManager # 小区样式渲染器
        self.parent = parent

        self.initUI()
    # 初始化界面
    def initUI(self):
        self.setWindowTitle(u"模三分析")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint)

        widget_0 = QWidget()
        widget_0.setStyleSheet('QWidget {background-color: red}')
        widget_0.resize(20, 20)
        label_0 = QLabel("0")

        widget_1 = QWidget()
        widget_1.setStyleSheet('QWidget {background-color: yellow}')
        widget_1.resize(20, 20)
        label_1 = QLabel("1")

        widget_2 = QWidget()
        widget_2.setStyleSheet('QWidget {background-color: #47d54c}')
        widget_2.resize(20, 20)
        label_2 = QLabel("2")

        grid = QGridLayout()
        grid.setSpacing(20)
        grid.addWidget(widget_0, 0, 0)
        grid.addWidget(label_0, 0, 1)
        grid.addWidget(widget_1, 1, 0)
        grid.addWidget(label_1, 1, 1)
        grid.addWidget(widget_2, 2, 0)
        grid.addWidget(label_2, 2, 1)


        self.setLayout(grid)
        self.setGeometry(300, 300, 250, 200)

    def closeEvent(self, event):
        self.accept()
        self.styleManager.setCurrentStyle(u"默认")  ##恢复上一级样式，即取消话务量渲染
        self.iface.actionDraw().trigger()