# -*- coding: utf-8 -*-
'''
相邻小区信息窗口
@author: Karwai Kwok
'''

from PyQt4.QtGui import QDialog, QTextEdit, QScrollArea, \
        QHBoxLayout, QPushButton, QVBoxLayout
from PyQt4.QtCore import SIGNAL

class SCellInfoUI(QDialog):
    def __init__(self, info_list=[], scell_name=u"", count1=0, count2=0):
        super(SCellInfoUI, self).__init__()
        self.info_list = info_list
        self.scell_name = scell_name
        self.count1 = count1
        self.count2 = count2

        self.initUI()

    # 初始化界面
    def initUI(self):
        self.topFiller = QTextEdit()
        self.topFiller.setReadOnly(True)
        self.topFiller.setMinimumSize(1000, 1000)

        text = self.scell_name + u" 的不对称小区有： " + str(self.count1) \
               + u" 个，对称小区有： " + str(self.count2) + u" 个" + u"\n\n"
        for (i, info) in enumerate(self.info_list):
            text = text + info + u"\n"
        self.topFiller.setText(text)

        scroll = QScrollArea()
        scroll.setWidget(self.topFiller)
        scroll.setAutoFillBackground(True)
        scroll.setWidgetResizable(True)

        hbox = QHBoxLayout()
        ok = QPushButton(u"确定")
        self.connect(ok, SIGNAL('clicked()'), self.accept)
        hbox.addStretch(1)
        hbox.addWidget(ok)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addWidget(scroll)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.setWindowTitle(u"所选服务小区信息")
        self.resize(680, 320)
