# -*- coding:utf-8 -*-
'''
新建项目窗口
@author: Karwai Kwok
'''
from PyQt4.QtCore import Qt, SIGNAL
import os, time, traceback
from PyQt4.QtGui import *
from MyQGIS.Contorls.InitProject import InitProject
from MyQGIS.config.EnumType import Operator
from MyQGIS.config.HeadsConfig import SiteANDCellHead

class InitProjectDlg(QDialog):
    def __init__(self, iface, parent=None):
        super(InitProjectDlg, self).__init__()
        self.iface = iface
        self.parent = parent

        self.setWindowTitle(u"新建工程")
        self.setWindowIcon(QIcon('icon/1.png'))

        self.file_path = None  # 项目保存位置
        self.file_dir = None  # 项目保存路径
        # 默认运营商的图层的颜色
        self.ydcolor = 'yellow'
        self.ltcolor = 'green'
        self.dxcolor = 'darkcyan'
        self.ttcolor = 'blue'

        self.initUI()

    def initUI(self):
        "生成界面"
        file_path_label = QLabel(u"文件名称")
        self.file_path_edit = QLineEdit()
        file_path_button = QPushButton(u"浏览...")
        self.connect(file_path_button, SIGNAL("clicked()"), self.getFilePath)

        file_grid = QGridLayout()
        file_grid.setSpacing(10)
        file_grid.addWidget(file_path_label, 0, 0)
        file_grid.addWidget(self.file_path_edit, 1, 0)
        file_grid.addWidget(file_path_button, 1, 1)

        color_label = QLabel(u"颜色设置")
        ydsiteLable = QLabel(u'移动：', self)
        self.ydsiteBtn = QPushButton(self)
        self.ydsiteBtn.setStyleSheet('QPushButton{background-color:' + self.ydcolor + '}')
        self.ydsiteBtn.clicked.connect(self.ydsiteListener)
        ltsiteLable = QLabel(u'联通：')
        self.ltsiteBtn = QPushButton(self)
        self.ltsiteBtn.setStyleSheet('QPushButton{background-color:' + self.ltcolor + '}')
        self.ltsiteBtn.clicked.connect(self.ltsiteListener)
        dxsiteLable = QLabel(u'电信：')
        self.dxsiteBtn = QPushButton(self)
        self.dxsiteBtn.setStyleSheet('QPushButton{background-color:' + self.dxcolor + '}')
        self.dxsiteBtn.clicked.connect(self.dxsiteListener)
        ttsiteLable = QLabel(u'铁塔：')
        self.ttsiteBtn = QPushButton(self)
        self.ttsiteBtn.setStyleSheet('QPushButton{background-color:' + self.ttcolor + '}')
        self.ttsiteBtn.clicked.connect(self.ttsiteListener)

        color_hbox1 = QHBoxLayout()
        color_hbox1.setSpacing(10)
        color_hbox1.addWidget(ydsiteLable)
        color_hbox1.addWidget(self.ydsiteBtn)
        color_hbox1.setStretchFactor(self.ydsiteBtn, 2)
        color_hbox1.addWidget(ltsiteLable)
        color_hbox1.addWidget(self.ltsiteBtn)
        color_hbox1.setStretchFactor(self.ltsiteBtn, 2)

        color_hbox2 = QHBoxLayout()
        color_hbox2.setSpacing(10)
        color_hbox2.addWidget(dxsiteLable)
        color_hbox2.addWidget(self.dxsiteBtn)
        color_hbox2.setStretchFactor(self.dxsiteBtn, 2)
        color_hbox2.addWidget(ttsiteLable)
        color_hbox2.addWidget(self.ttsiteBtn)
        color_hbox2.setStretchFactor(self.ttsiteBtn, 2)

        color_vbox = QVBoxLayout()
        color_vbox.addLayout(color_hbox1)
        color_vbox.addLayout(color_hbox2)

        btn_Hbox = QHBoxLayout()
        btn_Hbox.setSpacing(15)
        ok_btn = QPushButton(u"确定")
        ok_btn.clicked.connect(self.okListener)
        btn_Hbox.addWidget(ok_btn)
        cancel_btn = QPushButton(u"取消")
        cancel_btn.clicked.connect(self.cancelListener)
        btn_Hbox.addWidget(cancel_btn)

        vbox = QVBoxLayout()
        vbox.setSpacing(10)
        vbox.addLayout(file_grid)
        vbox.addLayout(color_vbox)
        vbox.addLayout(btn_Hbox)

        self.setLayout(vbox)
        self.resize(300,100)


    def getFilePath(self):
        file_path = QFileDialog.getSaveFileName(self, u'项目保存为', '/', 'QGIS File(*.qgs)')
        if file_path:
            self.file_path_edit.setText(file_path)
            self.file_path = file_path
            self.file_dir = os.path.dirname(file_path)

    def ydsiteListener(self):
        self.__showColorDlg(self.ydsiteBtn)

    def ltsiteListener(self):
        self.__showColorDlg(self.ltsiteBtn)

    def dxsiteListener(self):
        self.__showColorDlg(self.dxsiteBtn)

    def ttsiteListener(self):
        self.__showColorDlg(self.ttsiteBtn)

    def __showColorDlg(self, curBtn):
        pa = curBtn.palette()
        curColor = QColorDialog.getColor(pa.color(QPalette.Button), self)
        if curBtn is self.ydsiteBtn:
            self.ydcolor = curColor
        elif curBtn is self.ltsiteBtn:
            self.ltcolor = curColor
        elif curBtn is self.dxsiteBtn:
            self.dxcolor=curColor
        else:
            self.ttcolor = curColor
        curBtn.setStyleSheet('QPushButton{background-color:' + curColor.name() + '}')

    def cancelListener(self):
        "取消按钮监听事件"
        self.close()

    def okListener(self):
        "确定按钮监听事件"
        # 检查是否已经填写了项目保存路径
        file_path = self.file_path_edit.text()
        if not file_path:
            QMessageBox.critical(self.parent, u"提示", u"请选择项目保存路径!")
            return
        file_dir = os.path.split(file_path)[0]
        if not os.path.exists(file_dir):
            QMessageBox.critical(self.parent, u"错误", u"请选择正确的项目保存路径!")
            return
        self.accept()
        file_name = os.path.split(file_path)[1]
        # 新建空白项目
        self.iface.newProject()
        # 整理各运营商的颜色
        color_dict = {}
        color_dict[Operator.YD] = self.ydcolor
        color_dict[Operator.LT] = self.ltcolor
        color_dict[Operator.DX] = self.dxcolor
        color_dict[Operator.TT] = self.ttcolor
        # 创建图层
        initProject = InitProject(self.iface, file_path, color_dict, SiteANDCellHead, self.parent)
        initProject.initLayer()



