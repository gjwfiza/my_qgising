# -*- coding:utf-8 -*-
'''
导出数据到搜狗地图交互界面
@author: Karwai Kwok
'''

from PyQt4 import QtGui, QtCore
from qgis._gui import QgsMessageBar
from MyQGIS.Contorls.LayerControls import getLayerByName
from MyQGIS.config.EnumType import SogoType
from MyQGIS.config.HeadsConfig import Sogo_SiteFields, Sogo_CellFields
from MyQGIS.Contorls.ExportDataToSogo import exportDataToSogo

class ExportDataToSogoUI(QtGui.QDialog):
    def __init__(self, iface=None, parent=None):
        super(ExportDataToSogoUI, self).__init__()
        self.iface = iface
        self.parent = parent

        self.initUI()

    # 初始化界面
    def initUI(self):
        self.setWindowTitle(u'生成html文件')
        self.select_flag = QtGui.QCheckBox(u"只导出选中区域内的基站小区")
        self.select_flag.setChecked(False)
        self.label2 = QtGui.QLabel(u'<b>请选择要要生成的图层</b>')
        self.site_button = QtGui.QRadioButton(u' 基站 ')
        self.site_button.setChecked(True)
        self.cell_button = QtGui.QRadioButton(u' 小区(仅支持少量数据) ')

        self.ok = QtGui.QPushButton(u'确定')
        self.connect(self.ok, QtCore.SIGNAL('clicked()'), self.export)
        self.cancel = QtGui.QPushButton(u'取消')
        self.connect(self.cancel, QtCore.SIGNAL('clicked()'), self.accept)

        self.operator_label = QtGui.QLabel(u"请选择要输出的运营商数据：")
        self.ydcheckbox = QtGui.QCheckBox(u"移动")
        self.ydcheckbox.setChecked(True)
        self.ltcheckbox = QtGui.QCheckBox(u"联通")
        self.ltcheckbox.setChecked(True)
        self.dxcheckbox = QtGui.QCheckBox(u"电信")
        self.dxcheckbox.setChecked(True)
        self.ttcheckbox = QtGui.QCheckBox(u"铁塔")
        self.ttcheckbox.setChecked(True)

        button_hbox = QtGui.QHBoxLayout()
        button_hbox.setSpacing(10)
        button_hbox.addStretch(1)
        button_hbox.addWidget(self.ok)
        button_hbox.addWidget(self.cancel)
        button_hbox.addStretch(1)

        operator_hbox = QtGui.QHBoxLayout()
        operator_hbox.setSpacing(10)
        operator_hbox.addWidget(self.ydcheckbox)
        operator_hbox.addWidget(self.ltcheckbox)
        operator_hbox.addWidget(self.dxcheckbox)
        operator_hbox.addWidget(self.ttcheckbox)

        layer_hbox = QtGui.QHBoxLayout()
        layer_hbox.setSpacing(10)
        layer_hbox.addWidget(self.site_button)
        layer_hbox.addWidget(self.cell_button)
        layer_hbox.addStretch(1)

        vbox = QtGui.QVBoxLayout()
        vbox.setSpacing(10)
        vbox.addStretch(1)
        vbox.addWidget(self.select_flag)
        vbox.addWidget(self.label2)
        vbox.addLayout(layer_hbox)
        vbox.addWidget(self.operator_label)
        vbox.addLayout(operator_hbox)
        vbox.addStretch(1)
        vbox.addLayout(button_hbox)
        vbox.addStretch(1)

        self.setLayout(vbox)
        self.resize(420, 170)

    '''导出'''
    def export(self):
        self.accept()
        # 判断要获取哪些图层的数据
        if self.site_button.isChecked():
            self.type = SogoType.Site
        else:
            self.type = SogoType.Cell
        filedir = QtGui.QFileDialog.getExistingDirectory(None, 'Export ', '/')
        if filedir != None and filedir != '':
            datas = self.getDatas()
            result = exportDataToSogo(filedir, self.type, datas, self.parent)
            if result == True:
                self.iface.messageBar().pushMessage(u'导出成功', u'已成功生成html ', QgsMessageBar.SUCCESS, 3)
            else:
                self.iface.messageBar().pushMessage(u'导出失败', u'生成html失败 ', QgsMessageBar.CRITICAL, 3)

    '''获取数据'''
    def getDatas(self):
        sitedatas = []  # [SiteName, SiteId]
        sitepoints = []
        celldatas = []  # [CellName, CellId, site_name, SiteId, Lon, Lat, WCDMA-PSC, LTE-PCI, CDMA-PN, GSM-BCCH, Azimuth, TILT, AntHeigth, RNC-BSC]
        cellpoints = []
        siteLayer = getLayerByName(u'基站', self.iface)
        cellLayer = getLayerByName(u'小区', self.iface)

        # 判断要输出哪些运营商的数据
        operator_list = []  # 保存要输出的运营商的名字
        if self.ydcheckbox.isChecked():
            operator_list.append(u"移动")
        if self.ltcheckbox.isChecked():
            operator_list.append(u"联通")
        if self.dxcheckbox.isChecked():
            operator_list.append(u"电信")
        if self.ttcheckbox.isChecked():
            operator_list.append(u"铁塔")

        if self.type == SogoType.Site:
            # 判断是否只导出选中的基站
            if self.select_flag.isChecked():
                outputSites = siteLayer.selectedFeatures()
            else:
                outputSites = siteLayer.getFeatures()
            for site in outputSites:
                # 判断是不是属于要输出的运营商数据
                if site[u'运营商'] in operator_list:
                    temp = []
                    for field in Sogo_SiteFields:
                        temp.append(site[field].strip())
                    sitepoints.append(site.geometry().asPoint())
                    sitedatas.append(temp)
                    del temp
            return (sitedatas, sitepoints)

        elif self.type == SogoType.Cell:
            # 判断是否只导出选中的小区
            if self.select_flag.isChecked():
                outputCells = cellLayer.selectedFeatures()
            else:
                outputCells = cellLayer.getFeatures()
            for cell in outputCells:
                # 判断是不是属于要输出的运营商数据
                if cell[u'运营商'] in operator_list:
                    temp = []
                    for field in Sogo_CellFields:
                        if cell[field] != None:
                            if type(cell[field]) == basestring:
                                temp.append(cell[field].strip())
                            else:
                                temp.append(cell[field])
                        else:
                            temp.append(u'NULL')

                    cellpoints.append(cell.geometry().asPolygon()[0])
                    celldatas.append(temp)
                    del temp
            return (celldatas, cellpoints)


