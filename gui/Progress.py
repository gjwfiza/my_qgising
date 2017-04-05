# -*- coding: utf-8 -*-
'''
Qt进度条
Created on 2015年03月25日

@author: Karwai Kwok
'''

from PyQt4 import QtGui, QtCore
import sys

class Progess(QtGui.QDialog):
    def __init__(self, parent=None, total=0, title = u"数据转换中..."):
        super(Progess, self).__init__()
        self.parent = parent
        self.total = total

        self.setWindowTitle(title)
        self.pbar = QtGui.QProgressBar(self)
        self.pbar.setGeometry(30, 30, 200, 25)
        self.pbar.setMinimum(0)
        self.pbar.setMaximum(self.total)

        self.step = 0

    # 显示进度
    def count(self):
        if self.step >= self.total:
            self.accept()
        self.step = self.step + 1
        #print self.step
        self.pbar.setValue(self.step)

    # 直接关闭进度条
    def kill(self):
       self.pbar.setValue(self.total)
       self.accept()
