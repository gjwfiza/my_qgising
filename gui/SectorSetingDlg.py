# -*- coding:utf-8 -*-
'''
扇区大小设置窗口
@author: Karwai Kwok
'''
import  os, pickle
from PyQt4.QtCore import QThread, SIGNAL, Qt, QSize
from PyQt4.QtGui import QDialog, QIcon, QApplication, QLabel, QLineEdit, \
    QHBoxLayout, QVBoxLayout, QPushButton, QIntValidator, QMessageBox, \
    QRadioButton, QButtonGroup, QWidget, QScrollArea, QComboBox, QDoubleValidator


# 插件所在路径
strfilepath = os.path.realpath(__file__)
cmd_folder = "%s/" % (os.path.dirname(strfilepath),)

class SectorSetingDlg2(QDialog):
    def __init__(self, iface=None, directioy='', parent=None):
        super(SectorSetingDlg2, self).__init__()
        self.iface = iface
        self.directioy = directioy  # 项目路径
        self.parent = parent
        self.setWindowTitle(u"扇区图形设置")
        self.setWindowIcon(QIcon('images/logo.png'))
        self.resize(280, 350)
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        patternLabel = QLabel(u'请选择显示模式： ')
        paBox = QHBoxLayout()
        self.pattern1 = QRadioButton(u'指针模式 ', self)
        self.pattern1.setChecked(True)
        self.pattern2 = QRadioButton(u'扇形模式 ', self)
        paBox.addWidget(patternLabel)
        paBox.addStretch(1)
        paBox.addWidget(self.pattern1)
        paBox.addWidget(self.pattern2)

        angle_validator = QIntValidator(0, 360, self)
        len_validator = QDoubleValidator(0, 99.99999, 5, self)  # 取值范围为0~99.99999

        label = QLabel(u"请输入网络制式和频段的相应图形参数：")
        default_label = QLabel(u"默认")
        self.default_angle = QLineEdit()
        self.default_angle.setPlaceholderText(u'角度大小：20')
        self.default_angle.setValidator(angle_validator)
        self.default_len = QLineEdit()
        self.default_len.setPlaceholderText(u'长度：0.0015')
        self.default_len.setValidator(len_validator)
        default_hbox = QHBoxLayout()
        default_hbox.addWidget(default_label)
        default_hbox.setStretchFactor(default_label, 1)
        default_hbox.addWidget(self.default_angle)
        default_hbox.addWidget(self.default_len)
        default_hbox.addStretch(1)

        system = [u"网络制式", u"G", u"D", u"C",
                  u"W", u"T", u"F", u"TDS"]
        frequency = [u"频段", u"700M", u"800M", u"900M", u"1800M",
                     u"1900M", u"2100M", u"2300M", u"2600M"]

        self.system_combox_1 = QComboBox()
        self.system_combox_1.addItems(system)
        self.frequency_combox_1 = QComboBox()
        self.frequency_combox_1.addItems(frequency)
        self.angle_1 = QLineEdit()
        self.angle_1.setPlaceholderText(u'角度大小：30')
        self.angle_1.setValidator(angle_validator)
        self.len_1 = QLineEdit()
        self.len_1.setPlaceholderText(u'长度：0.0015')
        self.len_1.setValidator(len_validator)
        hbox_1 = QHBoxLayout()
        hbox_1.setSpacing(10)
        hbox_1.addWidget(self.system_combox_1)
        hbox_1.addWidget(self.frequency_combox_1)
        hbox_1.addWidget(self.angle_1)
        hbox_1.addWidget(self.len_1)

        self.system_combox_2 = QComboBox()
        self.system_combox_2.addItems(system)
        self.frequency_combox_2 = QComboBox()
        self.frequency_combox_2.addItems(frequency)
        self.angle_2 = QLineEdit()
        self.angle_2.setPlaceholderText(u'角度大小：40')
        self.angle_2.setValidator(angle_validator)
        self.len_2 = QLineEdit()
        self.len_2.setPlaceholderText(u'长度：0.0015')
        self.len_2.setValidator(len_validator)
        hbox_2 = QHBoxLayout()
        hbox_2.setSpacing(10)
        hbox_2.addWidget(self.system_combox_2)
        hbox_2.addWidget(self.frequency_combox_2)
        hbox_2.addWidget(self.angle_2)
        hbox_2.addWidget(self.len_2)

        self.system_combox_3 = QComboBox()
        self.system_combox_3.addItems(system)
        self.frequency_combox_3 = QComboBox()
        self.frequency_combox_3.addItems(frequency)
        self.angle_3 = QLineEdit()
        self.angle_3.setPlaceholderText(u'角度大小：50')
        self.angle_3.setValidator(angle_validator)
        self.len_3 = QLineEdit()
        self.len_3.setPlaceholderText(u'长度：0.0015')
        self.len_3.setValidator(len_validator)
        hbox_3 = QHBoxLayout()
        hbox_3.setSpacing(10)
        hbox_3.addWidget(self.system_combox_3)
        hbox_3.addWidget(self.frequency_combox_3)
        hbox_3.addWidget(self.angle_3)
        hbox_3.addWidget(self.len_3)

        self.system_combox_4 = QComboBox()
        self.system_combox_4.addItems(system)
        self.frequency_combox_4 = QComboBox()
        self.frequency_combox_4.addItems(frequency)
        self.angle_4 = QLineEdit()
        self.angle_4.setPlaceholderText(u'角度大小：60')
        self.angle_4.setValidator(angle_validator)
        self.len_4 = QLineEdit()
        self.len_4.setPlaceholderText(u'长度：0.0015')
        self.len_4.setValidator(len_validator)
        hbox_4 = QHBoxLayout()
        hbox_4.setSpacing(10)
        hbox_4.addWidget(self.system_combox_4)
        hbox_4.addWidget(self.frequency_combox_4)
        hbox_4.addWidget(self.angle_4)
        hbox_4.addWidget(self.len_4)

        ok = QPushButton(u"确定")
        self.connect(ok, SIGNAL("clicked()"), self.okBtnListenner)
        operator = QPushButton(u'切换设置模式', self)
        operator.clicked.connect(self.operator_setting)
        btn_hbox = QHBoxLayout()
        btn_hbox.setSpacing(15)
        btn_hbox.addWidget(ok)
        btn_hbox.addWidget(operator)

        vbox = QVBoxLayout()
        vbox.setSpacing(10)
        vbox.addWidget(label)
        vbox.addLayout(paBox)
        vbox.addLayout(default_hbox)
        vbox.addLayout(hbox_1)
        vbox.addLayout(hbox_2)
        vbox.addLayout(hbox_3)
        vbox.addLayout(hbox_4)
        vbox.addStretch(1)
        vbox.addLayout(btn_hbox)

        self.setLayout(vbox)

    def operator_setting(self):
        self.accept()
        setting_dlg = SectorSetingDlg( self.iface, self.directioy, self.parent)
        setting_dlg.show()
        setting_dlg.exec_()

    def okBtnListenner(self):

        default_angle = self.default_angle.text().strip()
        default_len = self.default_len.text().strip()

        system_1 = self.system_combox_1.currentText().strip()
        frequency_1 = self.frequency_combox_1.currentText().strip()
        angle_1 = self.angle_1.text().strip()
        len_1 = self.len_1.text().strip()

        system_2 = self.system_combox_2.currentText().strip()
        frequency_2 = self.frequency_combox_2.currentText().strip()
        angle_2 = self.angle_2.text().strip()
        len_2 = self.len_2.text().strip()

        system_3 = self.system_combox_3.currentText().strip()
        frequency_3 = self.frequency_combox_3.currentText().strip()
        angle_3 = self.angle_3.text().strip()
        len_3 = self.len_3.text().strip()

        system_4 = self.system_combox_4.currentText().strip()
        frequency_4 = self.frequency_combox_4.currentText().strip()
        angle_4 = self.angle_4.text().strip()
        len_4 = self.len_4.text().strip()

        '''扇形模式扇形大小默认设置'''
        if not self.pattern1.isChecked() and self.pattern2.isChecked():
            if default_angle:
                default_angle = int(default_angle)
            else:
                default_angle = 20
            if angle_1:
                angle_1 = int(angle_1)
            else:
                angle_1 = 30
            if angle_2:
                angle_2 = int(angle_2)
            else:
                angle_2 = 40
            if angle_3:
                angle_3 = int(angle_3)
            else:
                angle_3 = 50
            if angle_4:
                angle_4 = int(angle_4)
            else:
                angle_4 = 60

        '''指针模式扇形大小默认设置'''
        if self.pattern1.isChecked() and not self.pattern2.isChecked():
            default_angle = 2
            angle_1 = 2
            angle_2 = 2
            angle_3 = 2
            angle_4 = 2

        if default_len:
            default_len = float(default_len)
        else:
            default_len = 0.0015
        if len_1:
            len_1 = float(len_1)
        else:
            len_1 = 0.0015
        if len_2:
            len_2 = float(len_2)
        else:
            len_2 = 0.0015
        if len_3:
            len_3 = float(len_3)
        else:
            len_3 = 0.0015
        if len_4:
            len_4 = float(len_4)
        else:
            len_4 = 0.0015
        try:
            # 传出角度设置参数，传于文本文件‘sectorsetting.txt’中
            f = open(os.path.join(self.directioy, u'sectorsetting.txt'), 'w')
            sector_setting = {}
            sector_setting["type"] = 1
            sector_setting[u"默认"] = (default_angle, default_len)  # (角度大小， 长度)
            case_list = []
            if (self.system_combox_1.currentIndex() != 0) or (self.frequency_combox_1.currentIndex() != 0):
                if self.system_combox_1.currentIndex() == 0:
                    system_1 = None
                if self.frequency_combox_1.currentIndex() == 0:
                    frequency_1 = None
                case_1 = (system_1, frequency_1, angle_1, len_1)
                case_list.append(case_1)
            if (self.system_combox_2.currentIndex() != 0) or (self.frequency_combox_2.currentIndex() != 0):
                if self.system_combox_2.currentIndex() == 0:
                    system_2 = None
                if self.frequency_combox_2.currentIndex() == 0:
                    frequency_2 = None
                case_2 = (system_2, frequency_2, angle_2, len_2)
                case_list.append(case_2)
            if (self.system_combox_3.currentIndex() != 0) or (self.frequency_combox_3.currentIndex() != 0):
                if self.system_combox_3.currentIndex() == 0:
                    system_3 = None
                if self.frequency_combox_3.currentIndex() == 0:
                    frequency_3 = None
                case_3 = (system_3, frequency_3, angle_3, len_3)
                case_list.append(case_3)
            if (self.system_combox_4.currentIndex() != 0) or (self.frequency_combox_4.currentIndex() != 0):
                if self.system_combox_4.currentIndex() == 0:
                    system_4 = None
                if self.frequency_combox_4.currentIndex() == 0:
                    frequency_4 = None
                case_4 = (system_4, frequency_4, angle_4, len_4)
                case_list.append(case_4)
            sector_setting["case_list"] = case_list
            # 把字典保存于txt中
            pickle.dump(sector_setting, f)
            f.close()
            QMessageBox.information(self.parent, u'创建项目', u'创建项目成功')
        except IOError:
            QMessageBox.critical(self.parent, u"错误", u"请使用管理员身份运行QGIS软件 ")
            return


class SectorSetingDlg(QDialog):
    def __init__(self, iface=None, directioy='', parent=None):
        super(SectorSetingDlg, self).__init__()
        self.iface = iface
        self.parent = parent
        self.directioy = directioy  # 项目路径

        self.setWindowTitle(u'扇区角度设置')
        self.setWindowIcon(QIcon('images/logo.png'))
        self.resize(280, 320)
        self.initView()

    def initView(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        jsLable = QLabel(u'设置不同运营商扇形的角度和半径长度，\n方便在地图上分辨出各运营商的小区', self);
        jsBox = QHBoxLayout()
        jsBox.addWidget(jsLable)

        patternLabel = QLabel(u'请选择显示模式： ')
        paBox = QHBoxLayout()
        self.pattern1 = QRadioButton(u'指针模式 ', self)
        self.pattern1.setChecked(True)
        self.pattern2 = QRadioButton(u'扇形模式 ', self)
        paBox.addWidget(patternLabel)
        paBox.addStretch(1)
        paBox.addWidget(self.pattern1)
        paBox.addWidget(self.pattern2)

        angle_validator = QIntValidator(0, 360, self)

        ydLable = QLabel(u"角度：", self)
        self.ydInput = QLineEdit(self)
        self.ydInput.setPlaceholderText(u'移动：20')
        self.ydInput.setValidator(angle_validator)
        ydLenLable = QLabel(u'长度：', self)
        self.ydLenInput = QLineEdit(self)
        self.ydLenInput.setPlaceholderText(u'移动：0.0015')
        ydBox = QHBoxLayout()
        ydBox.addWidget(ydLable)
        ydBox.addWidget(self.ydInput)
        ydBox.addWidget(ydLenLable)
        ydBox.addWidget(self.ydLenInput)

        ltLable = QLabel(u'角度：', self)
        self.ltInput = QLineEdit(self)
        self.ltInput.setPlaceholderText(u'联通：30')
        self.ltInput.setValidator(angle_validator)
        ltLenLable = QLabel(u'长度：', self)
        self.ltLenInput = QLineEdit(self)
        self.ltLenInput.setPlaceholderText(u'联通：0.0015')
        ltBox = QHBoxLayout()
        ltBox.addWidget(ltLable)
        ltBox.addWidget(self.ltInput)
        ltBox.addWidget(ltLenLable)
        ltBox.addWidget(self.ltLenInput)

        dxLable = QLabel(u'角度：', self)
        self.dxInput = QLineEdit(self)
        self.dxInput.setPlaceholderText(u'电信：40')
        self.dxInput.setValidator(angle_validator)
        dxLenLable = QLabel(u'长度：', self)
        self.dxLenInput = QLineEdit(self)
        self.dxLenInput.setPlaceholderText(u'电信：0.0015')
        dxBox = QHBoxLayout()
        dxBox.addWidget(dxLable)
        dxBox.addWidget(self.dxInput)
        dxBox.addWidget(dxLenLable)
        dxBox.addWidget(self.dxLenInput)

        ttLable = QLabel(u'角度：', self)
        self.ttInput = QLineEdit(self)
        self.ttInput.setPlaceholderText(u'铁塔：50')
        self.ttInput.setValidator(angle_validator)
        ttLenLable = QLabel(u'长度：', self)
        self.ttLenInput = QLineEdit(self)
        self.ttLenInput.setPlaceholderText(u'铁塔：0.0015')
        ttBox = QHBoxLayout()
        ttBox.addWidget(ttLable)
        ttBox.addWidget(self.ttInput)
        ttBox.addWidget(ttLenLable)
        ttBox.addWidget(self.ttLenInput)

        okBtn = QPushButton(u'确定', self)
        okBtn.clicked.connect(self.okBtnListenner)
        custom_btn = QPushButton(u'切换设置模式', self)
        custom_btn.clicked.connect(self.custom_setting)
        btnBox = QHBoxLayout()
        btnBox.addWidget(okBtn)
        btnBox.addWidget(custom_btn)

        vBox = QVBoxLayout()
        vBox.addLayout(jsBox)
        vBox.addLayout(paBox)
        vBox.addLayout(ydBox)
        vBox.addLayout(ltBox)
        vBox.addLayout(dxBox)
        vBox.addLayout(ttBox)
        vBox.addLayout(btnBox)

        vBox.setStretchFactor(jsLable, 3)
        vBox.setStretchFactor(ydBox, 2)
        vBox.setStretchFactor(ltBox, 2)
        vBox.setStretchFactor(dxBox, 2)
        vBox.setStretchFactor(ttBox, 2)
        vBox.setStretchFactor(btnBox, 1)

        self.setLayout(vBox)

    def okBtnListenner(self):
        self.accept()
        ydR = self.ydInput.text().strip()
        ltR = self.ltInput.text().strip()
        dxR = self.dxInput.text().strip()
        ttR = self.ttInput.text().strip()

        ydL = self.ydLenInput.text().strip()
        ltL = self.ltLenInput.text().strip()
        dxL = self.dxLenInput.text().strip()
        ttL = self.ttLenInput.text().strip()

        '''扇形模式扇形大小默认设置'''
        if not self.pattern1.isChecked() and self.pattern2.isChecked():
            if ydR:
                ydR = int(ydR)
            else:
                ydR = 20
            if ltR:
                ltR = int(ltR)
            else:
                ltR = 35
            if dxR:
                dxR = int(dxR)
            else:
                dxR = 50
            if ttR:
                ttR = int(ttR)
            else:
                ttR = 65
        '''指针模式扇形大小默认设置'''
        if self.pattern1.isChecked() and not self.pattern2.isChecked():
            ydR = 2
            ltR = 2
            dxR = 2
            ttR = 2

        if ydL:
            ydL = float(ydL)
        else:
            ydL = 0.0015
        if ltL:
            ltL = float(ltL)
        else:
            ltL = 0.0015
        if dxL:
            dxL = float(dxL)
        else:
            dxL = 0.0015
        if ttL:
            ttL = float(ttL)
        else:
            ttL = 0.0015

        # 传出角度设置参数，传于文本文件‘sectorsetting.txt’中
        try:
            f = open(os.path.join(self.directioy, u'sectorsetting.txt'), 'w')
            sector_setting = {}
            sector_setting["type"] = 0
            sector_setting[u"移动"] = (ydR, ydL)  # (角度大小， 长度)
            sector_setting[u"联通"] = (ltR, ltL)
            sector_setting[u"电信"] = (dxR, dxL)
            sector_setting[u"铁塔"] = (ttR, ttL)
            # 把字典保存于txt中
            pickle.dump(sector_setting, f)
            f.close()
            QMessageBox.information(self.parent, u"创建项目", u"创建项目成功")
        except IOError:
            QMessageBox.critical(self.parent, u"错误", u"请使用管理员身份运行QGIS软件 ")
            return




    def custom_setting(self):
        self.accept()
        setting_dlg = SectorSetingDlg2(self.iface, self.directioy, self.parent)
        setting_dlg.show()
        setting_dlg.exec_()



