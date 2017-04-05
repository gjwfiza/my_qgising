# -*- coding: utf-8 -*-
'''
添加自动规划基站待选站点交互界面
@author: Karwai Kwok
'''

import os, processing
from PyQt4.QtGui import QDialog, QIntValidator, QLabel, QLineEdit, \
    QMessageBox, QGridLayout, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt4.QtCore import Qt, SIGNAL, QVariant
from MyQGIS.Contorls.LayerControls import getLayerByName, getAllLayerName
from MyQGIS.Contorls.AddNSites import AddNewSites


class AddNSitesUI(QDialog):
    def __init__(self, iface, parent=None):
        super(AddNSitesUI, self).__init__()
        self.iface = iface
        self.parent = parent
        # 判断是否存在泰森结点图层
        if u"泰森结点" not in getAllLayerName(self.iface):
            self.accept()
            QMessageBox.critical(self.parent, u"错误", u"请先执行自动规划基站功能！")
            return False
        # 判断是否选中正确图层
        self.layer = self.iface.activeLayer()
        if self.layer.name() != u"泰森结点":
            self.accept()
            QMessageBox.critical(self.parent, u"错误", u"请选择泰森结点图层！")
            return False
        self.result_layer = getLayerByName(u"规划基站结果", self.iface)
        if not self.result_layer:
            self.accept()
            QMessageBox.critical(self.parent, u"错误", u"找不到规划基站结果！")
            return False

        self.initUI()

    # 初始化界面
    def initUI(self):
        self.setGeometry(200, 200, 250, 200)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle(u'自动规划基站设置')

        validator = QIntValidator(1, 10000, self)  # 设置以下几行输入限制为整数
        title1 = QLabel(u'分区角度:')
        self.titleEdit1 = QLineEdit()
        self.titleEdit1.setPlaceholderText('60')
        self.titleEdit1.setValidator(validator)
        title2 = QLabel(u'最大辐射范围:')
        self.titleEdit2 = QLineEdit()
        self.titleEdit2.setPlaceholderText('2000')
        self.titleEdit2.setValidator(validator)
        title3 = QLabel(u'农村(最小站间距)')
        self.titleEdit3 = QLineEdit()
        self.titleEdit3.setPlaceholderText('800')
        self.titleEdit3.setValidator(validator)
        title4 = QLabel(u'郊区乡镇(最小站间距)')
        self.titleEdit4 = QLineEdit()
        self.titleEdit4.setPlaceholderText('500')
        self.titleEdit4.setValidator(validator)
        title5 = QLabel(u'普通市区(最小站间距)')
        self.titleEdit5 = QLineEdit()
        self.titleEdit5.setPlaceholderText('350')
        self.titleEdit5.setValidator(validator)
        title6 = QLabel(u'密集市区(最小站间距)')
        self.titleEdit6 = QLineEdit()
        self.titleEdit6.setPlaceholderText('200')
        self.titleEdit6.setValidator(validator)

        grid1 = QGridLayout()
        grid1.setSpacing(10)

        grid1.addWidget(title1, 1, 0)
        grid1.addWidget(self.titleEdit1, 1, 1)
        grid1.addWidget(title2, 2, 0)
        grid1.addWidget(self.titleEdit2, 2, 1)
        grid1.addWidget(title3, 3, 0)
        grid1.addWidget(self.titleEdit3, 3, 1)
        grid1.addWidget(title4, 4, 0)
        grid1.addWidget(self.titleEdit4, 4, 1)
        grid1.addWidget(title5, 5, 0)
        grid1.addWidget(self.titleEdit5, 5, 1)
        grid1.addWidget(title6, 6, 0)
        grid1.addWidget(self.titleEdit6, 6, 1)

        ok = QPushButton(u'确定')
        cancel = QPushButton(u'取消')

        hbox = QHBoxLayout()
        hbox.setSpacing(15)
        hbox.addStretch(1)
        hbox.addWidget(ok)
        hbox.addWidget(cancel)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addLayout(grid1)
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.resize(300, 270)

        self.connect(ok, SIGNAL('clicked()'), self.settingtext)
        self.connect(cancel, SIGNAL('clicked()'), self.accept)

    def settingtext(self):
        #获取所有设置参数
        text1=self.titleEdit1.text().strip()
        text2=self.titleEdit2.text().strip()
        text3=self.titleEdit3.text().strip()
        text4=self.titleEdit4.text().strip()
        text5=self.titleEdit5.text().strip()
        text6=self.titleEdit6.text().strip()

        if text1=='':
            text1=60
        if type(text1) != int:
            text1=int(text1)
        if text2=='':
            text2=2000             #最大辐射范围默认值为2000米
        if type(text2) != int:
            text2=int(text2)
        if text3=='':
            text3= 800                  #农村最小辐射范围默认值为800米
        if type(text3) != int:
            text3 = int(text3)
        if text4=='':
            text4=500               #郊区乡镇辐射范围默认值为500米
        if type(text4) != int:
            text4 = int(text4)
        if text5=='':
            text5=350               #普通市区最小辐射范围默认值为350米
        if type(text5) != int:
            text5 = int(text5)
        if text6=='':
            text6=200               #密集市区最小辐射范围默认值为200米
        if type(text6) != int:
            text6 = int(text6)
        #传值给dialog
        self.tlist=[text1,text2,text3,text4,text5,text6] #定义存放所有参数的列表
        self.accept()
        addNewSites = AddNewSites(self.iface,self.tlist)
        if addNewSites.run():
            QMessageBox.information(self.parent, u"成功", u"添加候选站点成功！")
        else:
            QMessageBox.critical(self.parent, u"错误", u"添加候选站点失败！")
