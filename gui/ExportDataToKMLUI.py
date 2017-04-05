# -*- coding: utf-8 -*-
'''
导出数据到KML交互界面
@author: Karwai Kwok
'''

from PyQt4 import QtGui, QtCore
from qgis._gui import QgsMessageBar
from MyQGIS.config.EnumType import KMLType
from MyQGIS.config.HeadsConfig import KML_SiteSetting, KML_CellSetting
from MyQGIS.Contorls.ExportDataToKML import exportDataToKML

# 导出数据到KML图层主界面
class ExportDataToKMLUI(QtGui.QDialog):
    def __init__(self, iface, parent=None):
        super(ExportDataToKMLUI, self).__init__()
        self.iface = iface
        self.parent = parent

        self.initUI()

    # 初始化界面
    def initUI(self):
        self.setWindowTitle(u'生成KML文件')

        self.layer_label = QtGui.QLabel(u'请选择要要生成的图层：')
        self.site_checkbox = QtGui.QCheckBox(u' 基站 ')
        self.cell_checkbox = QtGui.QCheckBox(u' 小区 ')
        self.operator_label = QtGui.QLabel(u"请选择要输出的运营商数据：")
        self.ydcheckbox = QtGui.QCheckBox(u"移动")
        self.ydcheckbox.setChecked(True)
        self.ltcheckbox = QtGui.QCheckBox(u"联通")
        self.ltcheckbox.setChecked(True)
        self.dxcheckbox = QtGui.QCheckBox(u"电信")
        self.dxcheckbox.setChecked(True)
        self.ttcheckbox = QtGui.QCheckBox(u"铁塔")
        self.ttcheckbox.setChecked(True)
        self.ok = QtGui.QPushButton(u'确定')
        self.connect(self.ok, QtCore.SIGNAL('clicked()'), self.getSetInfo)
        self.cancel = QtGui.QPushButton(u'取消')
        self.connect(self.cancel, QtCore.SIGNAL('clicked()'), self.accept)

        self.select_flag = QtGui.QCheckBox(u"只导出选中区域内的基站小区")
        self.select_flag.setChecked(False)

        layer_hbox = QtGui.QHBoxLayout()
        layer_hbox.setSpacing(10)
        layer_hbox.addWidget(self.site_checkbox)
        layer_hbox.addWidget(self.cell_checkbox)
        layer_hbox.addStretch(1)

        operator_hbox = QtGui.QHBoxLayout()
        operator_hbox.setSpacing(10)
        operator_hbox.addWidget(self.ydcheckbox)
        operator_hbox.addWidget(self.ltcheckbox)
        operator_hbox.addWidget(self.dxcheckbox)
        operator_hbox.addWidget(self.ttcheckbox)

        button_hbox = QtGui.QHBoxLayout()
        button_hbox.addStretch(5)
        button_hbox.addWidget(self.ok)
        button_hbox.addStretch(1)
        button_hbox.addWidget(self.cancel)
        button_hbox.addStretch(5)

        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.select_flag)
        vbox.addWidget(self.layer_label)
        vbox.addLayout(layer_hbox)
        vbox.addWidget(self.operator_label)
        vbox.addLayout(operator_hbox)
        vbox.addStretch(1)
        vbox.addLayout(button_hbox)
        vbox.addStretch(1)

        self.setLayout(vbox)
        self.resize(300, 180)

    '''获取输出设置'''
    def getSetInfo(self):
        self.accept()
        siteLayer = self.getLayerByName(u'基站')
        cellLayer = self.getLayerByName(u'小区')

        if self.site_checkbox.isChecked() and self.cell_checkbox.isChecked():
            if self.select_flag.isChecked():
                outputs_sites = siteLayer.selectedFeatures()
                outputs_cells = cellLayer.selectedFeatures()
                if (len(outputs_sites) == 0) and (len(outputs_cells) == 0):
                    QtGui.QMessageBox.critical(self.parent, u"错误", u"请选中要导出的基站和小区！")
                    return False
            SetInfo1 = SelKMLField(self.parent, self.iface, KMLType.Site)
            SetInfo1.show()
            SetInfo1.exec_()
            setting1 = SetInfo1.getSetting()
            SetInfo2 = SelKMLField(self.parent, self.iface, KMLType.Cell)
            SetInfo2.show()
            SetInfo2.exec_()
            setting2 = SetInfo2.getSetting()
            self.setting = (setting1, setting2)

            self.export()

        elif self.cell_checkbox.isChecked() and not self.site_checkbox.isChecked():
            if self.select_flag.isChecked():
                outputs_cells = cellLayer.selectedFeatures()
                if len(outputs_cells) == 0:
                    QtGui.QMessageBox.critical(self.parent, u"错误", u"请选中要导出的小区！")
                    return False
            self.type = KMLType.Cell
            SetInfo = SelKMLField(self.parent, self.iface, self.type)
            SetInfo.show()
            SetInfo.exec_()
            self.setting = SetInfo.getSetting()

            self.export()


        elif self.site_checkbox.isChecked() and not self.cell_checkbox.isChecked():
            if self.select_flag.isChecked():
                outputs_sites = siteLayer.selectedFeatures()
                if len(outputs_sites) == 0:
                    QtGui.QMessageBox.critical(self.parent, u"错误", u"请选中要导出的基站！")
                    return False
            self.type = KMLType.Site
            SetInfo = SelKMLField(self.parent, self.iface, self.type)
            SetInfo.show()
            SetInfo.exec_()
            self.setting = SetInfo.getSetting()

            self.export()

        else:
            QtGui.QMessageBox.critical(self.parent, u"错误", u"请选择要打出的图层！")


    '''导出'''
    def export(self):

        #判断要获取哪些图层的数据
        if self.site_checkbox.isChecked() and self.cell_checkbox.isChecked():
            self.type = KMLType.SiteAndCell
        elif self.site_checkbox.isChecked() and not self.cell_checkbox.isChecked():
            self.type = KMLType.Site
        elif not self.site_checkbox.isChecked() and self.cell_checkbox.isChecked():
            self.type = KMLType.Cell


        fileName = QtGui.QFileDialog.getSaveFileName(None, 'Export KML', '/', 'KML File (*.kml )')
        if fileName != None and fileName != '':
            datas = self.getKMLDatas()
            result = exportDataToKML(fileName, self.type, self.getKMLField(), datas, self.parent)
            if result == True:
                self.iface.messageBar().pushMessage(u'导出成功', u'已成功生成KML图层 ', QgsMessageBar.SUCCESS , 2)
            else:
                self.iface.messageBar().pushMessage(u'导出失败', u'生成KML图层失败 ', QgsMessageBar.CRITICAL , 3)


    '''获取要显示的字段'''
    def getKMLField(self):
        if self.type == KMLType.Site:
            heads = []
            for head in KML_SiteSetting:
                if self.setting.has_key(head):
                    if self.setting[head] == True:
                        heads.append(head)
            return heads
        elif self.type == KMLType.Cell:
            heads = []
            for head in KML_CellSetting:
                if self.setting.has_key(head):
                    if self.setting[head] == True:
                        heads.append(head)
            return heads
        elif self.type == KMLType.SiteAndCell:
            heads1 = []
            for head in KML_SiteSetting:
                if self.setting[0].has_key(head):
                    if self.setting[0][head] == True:
                        heads1.append(head)
            heads2 = []
            for head in KML_CellSetting:
                if self.setting[1].has_key(head):
                    if self.setting[1][head] == True:
                        heads2.append(head)

            return (heads1, heads2)


    '''根据所选模式获取数据'''
    def getKMLDatas(self):
        sitenames = []
        sitedatas = []
        sitepoints = []
        cellnames = []
        celldatas = []
        cellpoints = []
        cellInfos = []
        siteLayer = self.getLayerByName(u'基站')
        cellLayer = self.getLayerByName(u'小区')

        # 判断要输出哪些运营商的数据
        operator_list = [] # 保存要输出的运营商的名字
        if self.ydcheckbox.isChecked():
            operator_list.append(u"移动")
        if self.ltcheckbox.isChecked():
            operator_list.append(u"联通")
        if self.dxcheckbox.isChecked():
            operator_list.append(u"电信")
        if self.ttcheckbox.isChecked():
            operator_list.append(u"铁塔")

        if self.type == KMLType.Site:
            if self.select_flag.isChecked():
                outputs_sites = siteLayer.selectedFeatures()
            else:
                outputs_sites = siteLayer.getFeatures()
            for site in outputs_sites:
                # 判断是不是属于要输出的运营商数据
                '''KML设置要增添字段'''
                if site[u"运营商"] in operator_list:
                    temp = []
                    fields = self.getKMLField()
                    try:
                        for field in fields:
                            temp.append(site[field])
                    except Exception as e:
                        print (e)
                        print (field)
                        print (site[field])

                    sitenames.append(site[u'基站名'])
                    sitepoints.append(site.geometry().asPoint())
                    sitedatas.append(temp)
                    del temp
            return (sitenames, sitedatas, sitepoints)

        elif self.type == KMLType.Cell:
            if self.select_flag.isChecked():
                outputs_cells = cellLayer.selectedFeatures()
                if len(outputs_cells) == 0:
                    QtGui.QMessageBox.critical(self.parent, u"错误", u"请选中要导出的小区！")
                    return False
            else:
                outputs_cells = cellLayer.getFeatures()
            for cell in outputs_cells:
                # 判断是不是属于要输出的运营商数据
                if cell[u'运营商'] in operator_list:
                    temp = []
                    fields = self.getKMLField()
                    for field in fields:
                        temp.append(cell[field])
                    cellnames.append(cell[u'小区名'])
                    cellpoints.append(cell.geometry().asPolygon())
                    celldatas.append(temp)
                    cellInfos.append((cell[u'基站名'], cell[u'经度'], cell[u'纬度']))
                    del temp
            return  (cellnames, celldatas, cellpoints, cellInfos)

        else:
            if self.select_flag.isChecked():
                outputs_sites = siteLayer.selectedFeatures()
                outputs_cells = cellLayer.selectedFeatures()
                if (len(outputs_sites) == 0) and (len(outputs_cells) == 0):
                    QtGui.QMessageBox.critical(self.parent, u"错误", u"请选中要导出的基站或小区！")
                    return False
            else:
                outputs_sites = siteLayer.getFeatures()
                outputs_cells = cellLayer.getFeatures()

            for site in outputs_sites:
                # 判断是不是属于要输出的运营商数据
                if site[u'运营商'] in operator_list:
                    temp = []
                    fields = self.getKMLField()
                    for field in fields[0]:
                        temp.append(site[field])
                    sitenames.append(site[u'基站名'])
                    sitepoints.append(site.geometry().asPoint())
                    sitedatas.append(temp)
                    del temp

            for cell in outputs_cells:
                # 判断是不是属于要输出的运营商数据
                if cell[u"运营商"] in operator_list:
                    temp = []
                    fields = self.getKMLField()
                    for field in fields[1]:
                        temp.append(cell[field])
                    cellnames.append(cell[u'小区名'])
                    cellpoints.append(cell.geometry().asPolygon())
                    celldatas.append(temp)
                    cellInfos.append((cell[u"基站名"], cell[u'经度'], cell[u'纬度']))
                    del temp
            return ((sitenames, sitedatas, sitepoints), (cellnames, celldatas, cellpoints, cellInfos))


    '''根据图层名称，获取图层'''
    def getLayerByName(self, name):
        layers = self.iface.mapCanvas().layers()
        for layer in layers:
            if layer.name() == name:
                return layer


# 选择要导出的KML图层的字段界面
class SelKMLField(QtGui.QDialog):
    def __init__(self, parent=None, iface=None, type=KMLType.Site):
        super(SelKMLField, self).__init__()
        self.iface = iface
        self.parent = parent
        self.type = type
        self.head = None

        self.initUI()

        # 初始化界面
    def initUI(self):
        if self.type == KMLType.Site:
            self.setWindowTitle(u'导出设置')

            label = QtGui.QLabel(u"<b>请选择要显示的基站信息</b>")
            self.site_cb_list = []
            self.site_cb1 = self.getCheckBox(u'基站ID', True, False) # SiteId
            self.site_cb_list.append(self.site_cb1)
            self.site_cb2 = self.getCheckBox(u'基站名称', True, False) # SiteName
            self.site_cb_list.append(self.site_cb2)
            self.site_cb3 = self.getCheckBox(u'System', True, False) # System
            self.site_cb_list.append(self.site_cb3)
            self.site_cb4 = self.getCheckBox(u'经度', True, False) # Lon
            self.site_cb_list.append(self.site_cb4)
            self.site_cb5 =self.getCheckBox(u'纬度', True, False) # Lat
            self.site_cb_list.append(self.site_cb5)
            self.site_cb6 = self.getCheckBox(u'运营商', False, True) # Operator
            self.site_cb_list.append(self.site_cb6)
            self.site_cb7 = self.getCheckBox(u'基站ID2', False, True) # SiteID2
            self.site_cb_list.append(self.site_cb7)
            self.site_cb8 = self.getCheckBox(u'基站类型', False, True) # SiteType
            self.site_cb_list.append(self.site_cb8)
            self.site_cb9 = self.getCheckBox(u'基站英文名', False, True) # Vendor
            self.site_cb_list.append(self.site_cb9)
            self.site_cb10 = self.getCheckBox(u'典型环境', True, False) # Region
            self.site_cb_list.append(self.site_cb10)
            self.site_cb11 = self.getCheckBox(u'站点地址', True, False) # Address
            self.site_cb_list.append(self.site_cb11)

            ok = QtGui.QPushButton(u'确定')
            self.connect(ok, QtCore.SIGNAL('clicked()'), self.accept)
            cancel = QtGui.QPushButton(u'取消')
            self.connect(cancel, QtCore.SIGNAL('clicked()'), self.reject)

            vbox1 = QtGui.QVBoxLayout()
            vbox1.addStretch(1)
            vbox1.addWidget(self.site_cb1)
            vbox1.addWidget(self.site_cb2)
            vbox1.addWidget(self.site_cb3)
            vbox1.addWidget(self.site_cb4)
            vbox1.addWidget(self.site_cb5)
            vbox1.addWidget(self.site_cb10)
            vbox1.addWidget(self.site_cb11)
            vbox1.addStretch(1)

            vbox2 = QtGui.QVBoxLayout()
            vbox1.addStretch(1)
            vbox2.addWidget(self.site_cb6)
            vbox2.addWidget(self.site_cb7)
            vbox2.addWidget(self.site_cb8)
            vbox2.addWidget(self.site_cb9)
            vbox1.addStretch(1)

            hbox1 = QtGui.QHBoxLayout()
            hbox1.addStretch(1)
            hbox1.addLayout(vbox1)
            hbox1.addLayout(vbox2)
            hbox1.addStretch(1)

            hbox2 = QtGui.QHBoxLayout()
            hbox2.addStretch(5)
            hbox2.addWidget(ok)
            hbox2.addStretch(1)
            hbox2.addWidget(cancel)
            hbox2.addStretch(5)

            vbox = QtGui.QVBoxLayout()
            vbox.addStretch(1)
            vbox.addWidget(label)
            vbox.addLayout(hbox1)
            vbox.addStretch(1)
            vbox.addLayout(hbox2)
            vbox.addStretch(1)

            self.setLayout(vbox)

        elif self.type == KMLType.Cell:
            self.setWindowTitle(u'导出设置')

            label = QtGui.QLabel(u"<b>请选择要显示的基站信息</b>")
            self.cell_cb_list = []
            #不可选设置
            self.cell_cb1 = self.getCheckBox(u'小区ID', True, False) # CellId
            self.cell_cb_list.append(self.cell_cb1)
            self.cell_cb2 = self.getCheckBox(u'扇区ID', True, False) # SectorId
            self.cell_cb_list.append(self.cell_cb2)
            self.cell_cb3 = self.getCheckBox(u'小区类型', True, False) # CellType
            self.cell_cb_list.append(self.cell_cb3)
            self.cell_cb4 = self.getCheckBox(u'方向角', True, False) # Azimuth
            self.cell_cb_list.append(self.cell_cb4)
            self.cell_cb5 =self.getCheckBox(u'经度', True, False) # Lon
            self.cell_cb_list.append(self.cell_cb5)
            self.cell_cb6 = self.getCheckBox(u'纬度', True, False) # Lat
            self.cell_cb_list.append(self.cell_cb6)
            self.cell_cb25 = self.getCheckBox(u'基站ID', True, False)# SiteId
            self.cell_cb_list.append(self.cell_cb25)
            self.cell_cb26 = self.getCheckBox(u'基站名', True, False)# site_name
            self.cell_cb_list.append(self.cell_cb26)
            self.cell_cb7 = self.getCheckBox(u'小区名', True, False) # CellName
            self.cell_cb_list.append(self.cell_cb7)
            self.cell_cb8 = self.getCheckBox(u'天线挂高', True, False) # AntHeight
            self.cell_cb_list.append(self.cell_cb8)
            self.cell_cb9 = self.getCheckBox(u'总下倾', True, False) # TILT
            self.cell_cb_list.append(self.cell_cb9)
            self.cell_cb10 = self.getCheckBox(u'电子下倾', True, False) # ETILT
            self.cell_cb_list.append(self.cell_cb10)
            self.cell_cb11 = self.getCheckBox(u'机械下倾', True, False) # MTILT
            self.cell_cb_list.append(self.cell_cb11)
            #可选设置
            self.cell_cb12 = self.getCheckBox(u'RAC', False, True) # RAC
            self.cell_cb_list.append(self.cell_cb12)
            self.cell_cb13 = self.getCheckBox(u'MSC', False, True) # Msc
            self.cell_cb_list.append(self.cell_cb13)
            self.cell_cb14 = self.getCheckBox(u'RNC-BSC', False, True) # RNC-BSC
            self.cell_cb_list.append(self.cell_cb14)
            self.cell_cb15 = self.getCheckBox(u'LAC', False, True) # LAC
            self.cell_cb_list.append(self.cell_cb15)
            self.cell_cb16 = self.getCheckBox(u'PN', False, True) # CDMA-PN
            self.cell_cb_list.append(self.cell_cb16)
            self.cell_cb17 = self.getCheckBox(u'PSC', False, True) # WCDMA-PSC
            self.cell_cb_list.append(self.cell_cb17)
            self.cell_cb18 = self.getCheckBox(u'TAC', False, True) # LTE-TAC
            self.cell_cb_list.append(self.cell_cb18)
            self.cell_cb19 = self.getCheckBox(u'PCI', False, True) # LTE-PCI
            self.cell_cb_list.append(self.cell_cb19)
            self.cell_cb20 = self.getCheckBox(u'频段', False, True) # FreBand
            self.cell_cb_list.append(self.cell_cb20)
            self.cell_cb21 = self.getCheckBox(u'LTE-PA', False, True) # CDMA-PN
            self.cell_cb_list.append(self.cell_cb21)
            self.cell_cb22 = self.getCheckBox(u'LTE-PB', False, True) # LTE-PCI
            self.cell_cb_list.append(self.cell_cb22)
            self.cell_cb23 = self.getCheckBox(u'BCCH', False, True) # GSM-BCCH
            self.cell_cb_list.append(self.cell_cb23)
            self.cell_cb24 = self.getCheckBox(u'BSIC', False, True) # GSM-BSIC
            self.cell_cb_list.append(self.cell_cb24)

            ok = QtGui.QPushButton(u'确定')
            self.connect(ok, QtCore.SIGNAL('clicked()'), self.accept)
            cancel = QtGui.QPushButton(u'取消')
            self.connect(cancel, QtCore.SIGNAL('clicked()'), self.reject)

            vbox1 = QtGui.QVBoxLayout()
            vbox1.addStretch(1)
            vbox1.addWidget(self.cell_cb1)
            vbox1.addWidget(self.cell_cb2)
            vbox1.addWidget(self.cell_cb3)
            vbox1.addWidget(self.cell_cb4)
            vbox1.addWidget(self.cell_cb5)
            vbox1.addWidget(self.cell_cb6)
            vbox1.addWidget(self.cell_cb25)
            vbox1.addWidget(self.cell_cb26)
            vbox1.addWidget(self.cell_cb7)
            vbox1.addWidget(self.cell_cb8)
            vbox1.addWidget(self.cell_cb9)
            vbox1.addWidget(self.cell_cb10)
            vbox1.addWidget(self.cell_cb11)
            vbox1.addStretch(1)

            vbox2 = QtGui.QVBoxLayout()
            vbox2.addStretch(1)
            vbox2.addWidget(self.cell_cb12)
            vbox2.addWidget(self.cell_cb13)
            vbox2.addWidget(self.cell_cb14)
            vbox2.addWidget(self.cell_cb15)
            vbox2.addWidget(self.cell_cb16)
            vbox2.addWidget(self.cell_cb17)
            vbox2.addWidget(self.cell_cb18)
            vbox2.addWidget(self.cell_cb19)
            vbox2.addWidget(self.cell_cb20)
            vbox2.addWidget(self.cell_cb21)
            vbox2.addWidget(self.cell_cb22)
            vbox2.addWidget(self.cell_cb23)
            vbox2.addWidget(self.cell_cb24)
            vbox2.addStretch(1)

            hbox1 = QtGui.QHBoxLayout()
            hbox1.addStretch(1)
            hbox1.addLayout(vbox1)
            hbox1.addLayout(vbox2)
            hbox1.addStretch(1)

            hbox2 = QtGui.QHBoxLayout()
            hbox2.addStretch(5)
            hbox2.addWidget(ok)
            hbox2.addStretch(1)
            hbox2.addWidget(cancel)
            hbox2.addStretch(5)

            vbox = QtGui.QVBoxLayout()
            vbox.addStretch(1)
            vbox.addWidget(label)
            vbox.addLayout(hbox1)
            vbox.addStretch(1)
            vbox.addLayout(hbox2)
            vbox.addStretch(1)

            self.setLayout(vbox)



    '''生成设置选项checkbox'''
    def getCheckBox(self, name=u'', checked=False, checkable=True):
        cb = QtGui.QCheckBox(name)
        cb.setChecked(checked)
        '''所有checkbox都可选'''
        cb.setCheckable(True)
        return cb

    '''获取设置'''
    def getSetting(self):
        setting = {}
        if self.type == KMLType.Site:
            for (i, cb) in enumerate(self.site_cb_list):
                setting[KML_SiteSetting[i]] = cb.isChecked()
        elif self.type == KMLType.Cell:
            for (i, cb) in enumerate(self.cell_cb_list):
                setting[KML_CellSetting[i]] = cb.isChecked()
        return setting