# -*- coding: utf-8 -*-
'''
快速PCI规划交互界面
@author: Karwai Kwok
'''

from PyQt4.QtGui import QDialog, QLabel, QLineEdit, QIntValidator, QDoubleValidator, \
    QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton, QMessageBox
from PyQt4.QtCore import SIGNAL
from MyQGIS.Contorls.QuickPCIPlan import QuickPCIPlan

# 快速PCI规划参数设置交互窗口
class QuickPCISettingDlg(QDialog):
    def __init__(self, iface, parent=None):
        super(QuickPCISettingDlg, self).__init__()
        self.iface = iface
        self.parent = parent

        self.setWindowTitle(u"全网PCI规划设置")

        self.marco_label = QLabel(u"宏站PSS： ")
        self._label1 = QLabel(u"-")
        self.marco_edit0 = QLineEdit(u"0")
        marco_validator0 = QIntValidator(0, 166, self)  # 取值范围为0~166
        self.marco_edit0.setValidator(marco_validator0)
        self.marco_edit1 = QLineEdit(u"99")
        marco_validator1 = QIntValidator(1, 167, self)  # 取值范围为1~167
        self.marco_edit1.setValidator(marco_validator1)

        self.room_label = QLabel(u"室分PSS： ")
        self._label2 = QLabel(u"-")
        self.room_edit0 = QLineEdit(u"100")
        room_validator0 = QIntValidator(0, 166, self)  # 取值范围为0~166
        self.room_edit0.setValidator(room_validator0)
        self.room_edit1 = QLineEdit(u"150")
        room_validator1 = QIntValidator(1, 167, self)  # 取值范围为1~167
        self.room_edit1.setValidator(room_validator1)

        self.drip_label = QLabel(u"滴灌PSS： ")
        self._label3 = QLabel(u"-")
        self.drip_edit0 = QLineEdit(u"151")
        drip_validator0 = QIntValidator(0, 166, self)  # 取值范围为0~166
        self.drip_edit0.setValidator(drip_validator0)
        self.drip_edit1 = QLineEdit(u"167")
        drip_validator1 = QIntValidator(1, 167, self)  # 取值范围为1~167
        self.drip_edit1.setValidator(drip_validator1)

        self.coverage_label = QLabel(u"小区覆盖范围（km）： ")
        self.coverage_edit = QLineEdit(u"2")
        coverage_validator = QDoubleValidator(0.0, 9999.9999, 4, self)  # 取值范围为0~9999.9999
        self.coverage_edit.setValidator(coverage_validator)
        coverage_hbox = QHBoxLayout()
        coverage_hbox.setSpacing(10)
        coverage_hbox.addWidget(self.coverage_label)
        coverage_hbox.addWidget(self.coverage_edit)
        coverage_hbox.addStretch(1)

        PCI_Range_grid = QGridLayout()
        PCI_Range_grid.setSpacing(10)
        PCI_Range_grid.addWidget(self.marco_label, 0, 0)
        PCI_Range_grid.addWidget(self.marco_edit0, 0, 1)
        PCI_Range_grid.addWidget(self._label1, 0, 2)
        PCI_Range_grid.addWidget(self.marco_edit1, 0, 3)
        PCI_Range_grid.addWidget(self.room_label, 1, 0)
        PCI_Range_grid.addWidget(self.room_edit0, 1, 1)
        PCI_Range_grid.addWidget(self._label2, 1, 2)
        PCI_Range_grid.addWidget(self.room_edit1, 1, 3)
        PCI_Range_grid.addWidget(self.drip_label, 2, 0)
        PCI_Range_grid.addWidget(self.drip_edit0, 2, 1)
        PCI_Range_grid.addWidget(self._label3, 2, 2)
        PCI_Range_grid.addWidget(self.drip_edit1, 2, 3)

        ok = QPushButton(u"确定")
        self.connect(ok, SIGNAL('clicked()'), self.run)
        cancel = QPushButton(u"取消")
        self.connect(cancel, SIGNAL('clicked()'), self.accept)
        btn_hbox = QHBoxLayout()
        btn_hbox.setSpacing(15)
        btn_hbox.addStretch(1)
        btn_hbox.addWidget(ok)
        btn_hbox.addWidget(cancel)
        btn_hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addLayout(PCI_Range_grid)
        vbox.addLayout(coverage_hbox)
        vbox.addStretch(1)
        vbox.addLayout(btn_hbox)

        self.setLayout(vbox)
        self.resize(280,150)


    def checkSetting(self):
        # 检查非空并转换类型
        marco_edit0 = self.marco_edit0.text()
        marco_edit1 = self.marco_edit1.text()
        if (not marco_edit0) or (not marco_edit1):
            QMessageBox.critical(self, u"错误", u"宏站PSS范围不能为空！")
            return False
        else:
            marco_edit0 = int(marco_edit0)
            marco_edit1 = int(marco_edit1)

        room_edit0 = self.room_edit0.text()
        room_edit1 = self.room_edit1.text()
        if (not room_edit0) or (not room_edit1):
            QMessageBox.critical(self, u"错误", u"室分PSS范围不能为空！")
            return False
        else:
            room_edit0 = int(room_edit0)
            room_edit1 = int(room_edit1)

        drip_edit0 = self.drip_edit0.text()
        drip_edit1 = self.drip_edit1.text()
        if (not drip_edit0) or (not drip_edit1):
            QMessageBox.critical(self, u"错误", u"滴灌PSS范围不能为空！")
            return False
        else:
            drip_edit0 = int(drip_edit0)
            drip_edit1 = int(drip_edit1)

        coverage_edit = self.coverage_edit.text()
        if not coverage_edit:
            QMessageBox.critical(self, u"错误", u"小区覆盖范围不能为空！")
            return False


        # 检查范围填写是否冲突
        if marco_edit0 >= marco_edit1:
            QMessageBox.critical(self, u"错误", u"宏站PSS范围有误!")
            return False
        marco_range = set([i for i in range(marco_edit0, marco_edit1+1)])

        if room_edit0 >= room_edit1:
            QMessageBox.critical(self, u"错误", u"室分PSS范围有误!")
            return False
        room_range = set([i for i in range(room_edit0, room_edit1 + 1)])

        if drip_edit0 >= drip_edit1:
            QMessageBox.critical(self, u"错误", u"室分PSS范围有误!")
            return False
        drip_range = set([i for i in range(drip_edit0, drip_edit1 + 1)])

        if marco_range & room_range:
            QMessageBox.critical(self, u"错误", u"宏站PSS与室分PSS范围有冲突")
            return False
        elif marco_range & drip_range:
            QMessageBox.critical(self, u"错误", u"宏站PSS与滴灌PSS范围有冲突")
            return False
        elif room_range & drip_range:
            QMessageBox.critical(self, u"错误", u"室分PSS与滴灌PSS范围有冲突")
            return False
        else:
            del marco_range, room_range, drip_range
            return True

    def getSetting(self):
        # 返回PSS范围列表和小区覆盖半径（m）
        marco_low = int(self.marco_edit0.text())
        marco_up = int(self.marco_edit1.text())
        marco_range = (marco_low, marco_up)

        room_low = int(self.room_edit0.text())
        room_up = int(self.room_edit1.text())
        room_range = (room_low, room_up)

        drip_low = int(self.drip_edit0.text())
        drip_up = int(self.drip_edit1.text())
        drip_range = (drip_low, drip_up)

        coverage = float(self.coverage_edit.text())
        coverage = self.KilometerToMeter(coverage)

        return (marco_range, room_range, drip_range, coverage)



    # 米到千米的单位换算
    def MeterToKilometer(self, meter=0.0):
        if type(meter) != float:
            meter = float(meter)
        if meter < 0:
            meter = -meter
        if meter == 0.0:
            return 0.0
        else:
            kilometer = meter / 1000.0
            return kilometer

    # 千米到米的单位换算
    def KilometerToMeter(self, kilometer=0.0):
        meter =  kilometer*1000
        return meter

    def run(self):
        if not self.checkSetting():
            return False
        self.accept()
        (marco_range, room_range, drip_range, coverage) = self.getSetting()
        pci = QuickPCIPlan(self.iface, self.parent)
        pci.setParameters(marco_range, room_range, drip_range, coverage)
        if pci.run():
            QMessageBox.information(self, u"成功", u"全网PCI规划完成！")
        else:
            QMessageBox.critical(self, u"错误", u"全网规划PCI失败！")