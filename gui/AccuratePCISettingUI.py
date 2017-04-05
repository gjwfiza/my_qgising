# -*- coding: utf-8 -*-
'''
精准PCI规划交互界面
@author: Karwai Kwok
'''


from PyQt4.QtGui import QDialog, QLabel, QLineEdit, QIntValidator, QDoubleValidator, \
    QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton, QMessageBox
from PyQt4.QtCore import SIGNAL, Qt
from MyQGIS.Contorls.LayerControls import getLayerByName
from MyQGIS.Contorls.AccuratePCIPlan import AccuratePCIThread

class AccuratePCISettingDlg(QDialog):
    def __init__(self, iface, parent=None):
        super(AccuratePCISettingDlg, self).__init__()
        self.iface = iface
        self.parent = parent

        self.setWindowTitle(u"PCI规划(高级)")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        label = QLabel(u"请选择算法循环次数:")
        self.Cycles = QLineEdit()
        validator = QIntValidator(0,999,self)
        self.Cycles.setValidator(validator)
        setting_grid = QGridLayout()
        setting_grid.setSpacing(15)
        setting_grid.addWidget(label, 0, 0)
        setting_grid.addWidget(self.Cycles, 0, 1)

        ok = QPushButton(u"确定")
        self.connect(ok, SIGNAL("clicked()"), self.run)
        cancel = QPushButton(u"取消")
        self.connect(cancel, SIGNAL("clicked()"), self.accept)
        btn_hbox = QHBoxLayout()
        btn_hbox.setSpacing(10)
        btn_hbox.addStretch(1)
        btn_hbox.addWidget(ok)
        btn_hbox.addWidget(cancel)
        btn_hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addLayout(setting_grid)
        vbox.addStretch(1)
        vbox.addLayout(btn_hbox)

        self.setLayout(vbox)
        self.resize(180, 80)

    def run(self):
        if not self.Cycles.text():
            QMessageBox.critical(self.parent, u"错误", u"请输入算法要循环的次数！")
            return False
        self.accept()
        cycles = int(self.Cycles.text()) # 获取循环次数
        planing = AccuratePCIThread(cycles, self.iface, self.parent)
        cellLayer = getLayerByName(u"小区", self.iface)
        cells = cellLayer.selectedFeatures()
        if not cells:
            QMessageBox.critical(self.parent, u"错误", u"请选中要配置ＰＣＩ的小区！")
            return False
        if len(cells) > 600:
            QMessageBox.critical(self.parent, u"错误", u"此功能只支持600个以内的小区！")
            return False
        if planing.run():
            QMessageBox.information(self.parent, u"成功", u"PCI规划完成!")
        else:
            return False