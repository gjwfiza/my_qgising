# -*- coding: utf-8 -*-
'''
移动基站交互界面
@author: Karwai Kwok
'''

from PyQt4.QtGui import QDialog, QGridLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QVBoxLayout, QMessageBox
from PyQt4.QtCore import SIGNAL, pyqtSlot, Qt
from qgis.core import QgsPoint,QgsFeatureRequest,QgsCoordinateTransform,QgsCoordinateReferenceSystem,\
        QgsVectorLayer,QgsVectorDataProvider, QgsFeature, QgsGeometry,QGis
from MyQGIS.Contorls.FileControls import getProjectDir, getCellGraphicParam
from MyQGIS.Contorls.MapToolControls import MapTool
from MyQGIS.Contorls.LayerControls import getLayerByName, getCellListBySite
from MyQGIS.Contorls.FeaturesControls import createASiteFeature, createACellFeature, importFeaturesToLayer, \
        delFeatures
from MyQGIS.Contorls.GeometryControls import createSector, createCircle
from qgis.gui import QgsMapCanvas,QgsMapCanvasItem,QgsMapTool

class MoveSiteUI(QDialog):
    def __init__(self, iface, parent=None):
        super(MoveSiteUI, self).__init__()
        self.iface = iface
        self.parent = parent
        # 获取工程所在路径
        self.project_dir = getProjectDir(self.iface)
        # 获取操作图层对象
        self.sitelayer = getLayerByName(u'基站', self.iface)
        self.celllayer = getLayerByName(u'小区', self.iface)
        self.selectedSiteFeatures = self.sitelayer.selectedFeatures()
        self.allCellFeatures = self.celllayer.getFeatures()
        # 初始化鼠标点选事件
        self.mapTool = MapTool(self.iface.mapCanvas())
        self.mapTool.canvasClicked.connect(self.mouseClicked)
        self.iface.mapCanvas().setMapTool(self.mapTool)
        self.iface.mapCanvas().mapToolSet[QgsMapTool, QgsMapTool].connect(self.mapToolChanged)
        self.crsXform = QgsCoordinateTransform()
        self.crsXform.setDestCRS(QgsCoordinateReferenceSystem(4326))
        self.pos = None
        '''self.cellutils = FeatureUtils(u'小区', self.iface)
        self.siteutils = FeatureUtils(u'基站', self.iface)'''
        self.initUI()

    # 初始化界面
    def initUI(self):
        self.setGeometry(200, 200, 200, 100)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle(u'移动基站')

        title1 = QLabel(u'基站:')
        self.titleEdit1 = QLineEdit()
        self.titleEdit1.setReadOnly(True)

        lon_label = QLabel(u"经度:")
        self.lon_edit = QLineEdit()
        lat_label = QLabel(u"纬度:")
        self.lat_edit = QLineEdit()

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(title1, 1, 0)
        grid.addWidget(self.titleEdit1, 1, 1)
        grid.addWidget(lon_label, 2, 0)
        grid.addWidget(self.lon_edit, 2, 1)
        grid.addWidget(lat_label, 3, 0)
        grid.addWidget(self.lat_edit, 3, 1)

        ok = QPushButton(u'确定')
        self.connect(ok, SIGNAL('clicked()'), self.moveTo)
        cancel = QPushButton(u'取消')
        self.connect(cancel, SIGNAL('clicked()'), self.accept)
        btn_hbox = QHBoxLayout()
        btn_hbox.setSpacing(10)
        btn_hbox.addStretch(1)
        btn_hbox.addWidget(ok)
        btn_hbox.addWidget(cancel)
        btn_hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.setSpacing(10)
        vbox.addLayout(grid)
        vbox.addStretch(1)
        vbox.addLayout(btn_hbox)

        self.setLayout(vbox)
        self.resize(270, 150)


        # 获取选中的基站信息并填入相应格中
        self.oldcelllist = []
        for f in self.selectedSiteFeatures:
            sitename = f[u'基站名']
            id = f[u'基站ID']
            operator = f[u'运营商']
            bsc = f[u'RNC-BSC']
            self.titleEdit1.setText(sitename)
            for i in self.allCellFeatures:
                cid = i[u'基站ID']
                copetator = i[u'运营商']
                cbsc = i[u'RNC-BSC']
                if cid == id and copetator == operator and bsc == cbsc:  # 找出与基站ID相同的小区
                    self.oldcelllist.append(i.id())
        # 选中与基站相关联的小区
        if len(self.oldcelllist) != 0:
            # 先取消原有选择
            self.celllayer.selectAll()
            self.celllayer.invertSelection()
            self.celllayer.setSelectedFeatures(self.oldcelllist)
            self.selectedCellFeatures = self.celllayer.selectedFeatures()
        else:
            self.selectedCellFeatures = []

    # 鼠标点击监听器
    def mouseClicked(self, pos, button):
        if button == Qt.LeftButton:
            self.show()
            self.pos = pos
            self.geoPos = self.crsXform.transform(self.pos)
            self.x = unicode(self.geoPos.x())
            self.y = unicode(self.geoPos.y())
            self.lon_edit.setText(self.x)
            self.lat_edit.setText(self.y)

    @pyqtSlot(QgsMapTool, QgsMapTool)
    def mapToolChanged(self, mapToolNew, mapToolOld):
        if mapToolOld == self.mapTool and mapToolNew != self.mapTool:
            self.close()
            self.selectedCellFeatures = []
            self.selectedSiteFeatures = []
            self.sitelayer.selectAll()
            self.sitelayer.invertSelection()

    def moveTo(self):
        # 获取小区大小和长度设置
        setting = getCellGraphicParam(self.iface)
        # 判断是否读取到参数设置
        if not setting:
            QMessageBox.critical(self, u"错误", u"无法获取小区图形参数设置")
            self.accept()
            return

        oldsitelist = []
        sitefeatures = []
        cellfeatures = []

        if len(self.selectedSiteFeatures) == 1:
            for f in self.selectedSiteFeatures:
                oldsitelist.append(f.id())
                siteAttrs = f.attributes()
                del siteAttrs[0]
                siteAttrs[3] = self.lon_edit.text()
                siteAttrs[4] = self.lat_edit.text()
                self.titleEdit1.setText(unicode(siteAttrs[1]))
                siteFeature = createASiteFeature(QgsPoint(float(siteAttrs[3]), float(siteAttrs[4])), siteAttrs)
                sitefeatures.append(siteFeature)
                for c in self.selectedCellFeatures:
                    cellAttrs = c.attributes()
                    del cellAttrs[0]  # 删除唯一标识符，创建新feature后会重新生成，避免重复
                    cellAttrs[8] = self.lon_edit.text()
                    cellAttrs[9] = self.lat_edit.text()
                    # 识别图形设置
                    operator = cellAttrs[18]
                    if setting["type"] == 0:
                        if operator == u'移动':
                            szAngle = setting[u"移动"][0]
                            szLength = setting[u"移动"][1]
                        elif operator == u'联通':
                            szAngle = setting[u"联通"][0]
                            szLength = setting[u"联通"][1]
                        elif operator == u'电信':
                            szAngle = setting[u"电信"][0]
                            szLength = setting[u"电信"][1]
                        else:
                            szAngle = setting[u"铁塔"][0]
                            szLength = setting[u"铁塔"][1]
                    else:
                        # 自定义
                        system = cellAttrs[10]
                        frequency = cellAttrs[12]
                        # 获取默认设置
                        szAngle = setting[u"默认"][0]
                        szLength = setting[u"默认"][1]
                        # 获取分类
                        case_list = setting["case_list"]
                        for (c_system, c_frequency, c_angle, c_length) in case_list:
                            if c_system and (not c_frequency):
                                if system == c_system:
                                    szAngle = c_angle
                                    szLength = c_length
                            elif (not c_system) and c_frequency:
                                if frequency == c_frequency:
                                    szAngle = c_angle
                                    szLength = c_length
                            elif c_system and c_frequency:
                                if (system == c_system) and (frequency == c_frequency):
                                    szAngle = c_angle
                                    szLength = c_length
                    # 生成小区扇形geometry
                    cellGeometry = createSector(QgsPoint(float(cellAttrs[8]), float(cellAttrs[9])), szLength, self.iface, True,
                                                cellAttrs[7], szAngle)
                    cellFeature = createACellFeature(cellGeometry, cellAttrs)
                    cellfeatures.append(cellFeature)
        else:
            QMessageBox.critical(self, u"提醒", u"需且仅需选择一个基站！")
            self.accept()
            return False

        button = QMessageBox.question(self, "Question",
                                            u"移动后将无法撤回，是否继续?",
                                            QMessageBox.Ok | QMessageBox.Cancel,
                                            QMessageBox.Ok)
        if button == QMessageBox.Ok:
            # 先删除旧features再往图层上添加新features
            delFeatures(self.sitelayer, oldsitelist)
            importFeaturesToLayer(self.sitelayer, sitefeatures)
            delFeatures(self.celllayer, self.oldcelllist)
            importFeaturesToLayer(self.celllayer, cellfeatures)
            self.iface.actionDraw().trigger()
            self.selectedSiteFeatures = []
            self.selectedCellFeatures = []
            self.sitelayer.selectAll()
            self.sitelayer.invertSelection()
        else:
            return False
        self.accept()