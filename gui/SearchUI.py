# -*- coding: utf-8 -*-
'''
查询功能交互界面
@author: Karwai Kwok
'''

from PyQt4.QtGui import QDialog, QGridLayout, QHBoxLayout, QLabel, QLineEdit, \
    QIntValidator, QComboBox, QPushButton, QVBoxLayout, QMessageBox, QCheckBox, \
    QRadioButton, QButtonGroup, QColor
from PyQt4.QtCore import SIGNAL
from qgis.core import QgsFeatureRequest
from MyQGIS.Contorls.LayerControls import getLayerByName, getFeaturesBySQL

class SearchUI(QDialog):
    def __init__(self, iface, parent=None):
        super(SearchUI, self).__init__()
        self.iface = iface
        self.parent = parent
        # 获取图层对象
        self.siteLayer = getLayerByName(u'基站', self.iface)
        self.cellLayer = getLayerByName(u'小区', self.iface)

        self.initUI()

    # 初始化界面
    def initUI(self):
        self.setGeometry(200, 200, 250, 200)
        self.setWindowTitle(u'查找')

        title = QLabel(u'请选择搜索模式：')

        self.type_site_id = QRadioButton(u"基站ID ")
        self.type_site_id.setChecked(True)  # 默认查找基站ID
        self.type_site_name = QRadioButton(u"基站名 ")
        self.type_cell_id = QRadioButton(u"小区ID ")
        self.type_cell_name = QRadioButton(u"小区名 ")
        self.type_pn = QRadioButton(u"PN ")
        self.type_psc = QRadioButton(u"PSC ")
        self.type_pci = QRadioButton(u"PCI ")
        self.type_bcch = QRadioButton(u"BCCH ")

        search_type = QButtonGroup()
        search_type.addButton(self.type_site_id)
        search_type.addButton(self.type_site_name)
        search_type.addButton(self.type_cell_id)
        search_type.addButton(self.type_cell_name)
        search_type.addButton(self.type_pn)
        search_type.addButton(self.type_psc)
        search_type.addButton(self.type_pci)
        search_type.addButton(self.type_bcch)

        search_grid = QGridLayout()
        search_grid.setSpacing(10)
        search_grid.addWidget(self.type_site_id, 0, 1)
        search_grid.addWidget(self.type_site_name, 0, 2)
        search_grid.addWidget(self.type_cell_id, 0, 3)
        search_grid.addWidget(self.type_cell_name, 0, 4)
        search_grid.addWidget(self.type_pn, 1, 1)
        search_grid.addWidget(self.type_psc, 1, 2)
        search_grid.addWidget(self.type_pci, 1, 3)
        search_grid.addWidget(self.type_bcch, 1, 4)

        search_hbox = QHBoxLayout()
        search_hbox.setSpacing(10)
        search_hbox.addStretch(1)
        search_hbox.addLayout(search_grid)
        search_hbox.addStretch(1)

        self.searchText = QLineEdit()
        ok = QPushButton(u'确定')
        self.connect(ok, SIGNAL('clicked()'), self.search)
        cancel = QPushButton(u'取消')
        self.connect(cancel, SIGNAL('clicked()'), self.cancel)

        btn_hbox = QHBoxLayout()
        btn_hbox.setSpacing(10)
        btn_hbox.addStretch(1)
        btn_hbox.addWidget(ok)
        btn_hbox.addWidget(cancel)
        btn_hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.setSpacing(15)
        vbox.addWidget(title)
        vbox.addLayout(search_hbox)
        vbox.addWidget(self.searchText)
        vbox.addStretch(1)
        vbox.addLayout(btn_hbox)

        self.setLayout(vbox)
        self.resize(350, 190)

    # 取消按钮监听事件
    def cancel(self):
        self.iface.mapCanvas().setSelectionColor(QColor("yellow"))
        self.accept()

    # 重写关闭事件
    def closeEvent(self, event):
        self.iface.mapCanvas().setSelectionColor(QColor("yellow"))

    # 确定按钮绑定事件
    def search(self):
        search_text = self.searchText.text().strip()
        # 检查是否已填入搜索数据
        if search_text == "":
            QMessageBox.critical(self, u"错误", u"请输入查找内容!")
            return False

        layer = None
        if self.type_site_id.isChecked():
            layer = self.siteLayer
            sql = u'"基站ID"  =\'' + search_text + u'\''
            resultFeatures = getFeaturesBySQL(self.iface, u"基站", sql)
        elif self.type_site_name.isChecked():
            layer = self.siteLayer
            sql = u'"基站名"  LIKE \'%' + search_text + u'%\''
            resultFeatures = getFeaturesBySQL(self.iface, u"基站", sql)
        elif self.type_cell_id.isChecked():
            layer = self.cellLayer
            sql = u'"小区ID"  LIKE \'%' + search_text + u'%\''
            resultFeatures = getFeaturesBySQL(self.iface, u"小区", sql)
        elif self.type_cell_name.isChecked():
            layer = self.cellLayer
            sql = u'"小区名"  LIKE \'%' + search_text + u'%\''
            resultFeatures = getFeaturesBySQL(self.iface, u"小区", sql)
        elif self.type_pn.isChecked():
            layer = self.cellLayer
            sql = u'"PN"  =\'' + search_text + u'\''
            resultFeatures = getFeaturesBySQL(self.iface, u"小区", sql)
        elif self.type_psc.isChecked():
            layer = self.cellLayer
            sql = u'"PSC"  =\'' + search_text + u'\''
            resultFeatures = getFeaturesBySQL(self.iface, u"小区", sql)
        elif self.type_pci.isChecked():
            layer = self.cellLayer
            sql = u'"PCI"  =\'' + search_text + u'\''
            resultFeatures = getFeaturesBySQL(self.iface, u"小区", sql)
        elif self.type_bcch.isChecked():
            layer = self.cellLayer
            sql = u'"BCCH"  =\'' + search_text + u'\''
            resultFeatures = getFeaturesBySQL(self.iface, u"小区", sql)
        else:
            QMessageBox.critical(self, u"提醒", u"找不到相关信息，请重新输入或选择！")
            return False

        if len(resultFeatures) == 0:
            QMessageBox.critical(self, u"提醒", u"找不到相关基站或小区！")
            return False
        else:
            # 获取所有搜索结果features的id
            resultId_list = []
            for f in resultFeatures:
                resultId_list.append(f.id())
            # 取消现有选择
            self.cellLayer.setSelectedFeatures([])
            self.siteLayer.setSelectedFeatures([])

            layer.setSelectedFeatures(resultId_list)
            self.iface.mapCanvas().setSelectionColor(QColor("red"))
            self.iface.activeLayer = layer
            self.iface.actionZoomToSelected().trigger()
