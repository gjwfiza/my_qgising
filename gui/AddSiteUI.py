# -*- coding: utf-8 -*-
'''
添加基站交互界面
@author: Karwai Kwok
'''

import random
from PyQt4.QtGui import QDialog, QGridLayout, QHBoxLayout, QLabel, QLineEdit, \
    QIntValidator, QComboBox, QPushButton, QVBoxLayout, QMessageBox, QCheckBox
from PyQt4.QtCore import SIGNAL, QObject, pyqtSignal, pyqtSlot, Qt
from qgis.core import QgsPoint,QgsFeatureRequest,QgsCoordinateTransform,QgsCoordinateReferenceSystem,\
        QgsVectorLayer,QgsVectorDataProvider, QgsFeature, QgsGeometry,QGis
from MyQGIS.Contorls.FileControls import getProjectDir, getCellGraphicParam
from MyQGIS.Contorls.MapToolControls import MapTool
from MyQGIS.Contorls.LayerControls import getLayerByName
from MyQGIS.Contorls.FeaturesControls import createASiteFeature, createACellFeature, importFeaturesToLayer
from MyQGIS.Contorls.GeometryControls import createSector, createCircle

class AddSiteUI(QDialog):
    mouseClicked = pyqtSignal(QgsPoint, Qt.MouseButton)
    def __init__(self, iface, parent=None):
        super(AddSiteUI, self).__init__()
        self.iface = iface
        self.parent = parent
        # 获取项目路径
        self.project_dir = getProjectDir(self.iface)
        # 绑定鼠标单击操作
        self.mapTool = MapTool(self.iface.mapCanvas())
        self.mapTool.canvasClicked.connect(self.mouseClicked)
        self.iface.mapCanvas().setMapTool(self.mapTool)
        self.crsXform = QgsCoordinateTransform()
        self.crsXform.setDestCRS(QgsCoordinateReferenceSystem(4326))

        self.initUI()

    # 初始化界面
    def initUI(self):
        self.setGeometry(200, 200, 260, 150)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle(u'添加基站')
        # 用grid布局
        grid1 = QGridLayout()
        grid1.setSpacing(10)
        grid2 = QGridLayout()
        grid2.setSpacing(10)
        grid3 = QGridLayout()
        grid3.setSpacing(10)
        grid4 = QGridLayout()
        grid4.setSpacing(10)

        lonlat_hobx = QHBoxLayout()
        lonlat_hobx.setSpacing(10)
        site_label = QLabel(u"<b>基站信息:  <\b>")
        grid1.addWidget(site_label, 1, 0)
        SiteId_label = QLabel(u"基站ID:")
        grid1.addWidget(SiteId_label, 2, 0)
        self.site_id = QLineEdit()
        site_id_validator = QIntValidator(0, 999999999, self)  # SiteId只能为最多9位的纯数字
        self.site_id.setValidator(site_id_validator)
        self.site_id.setPlaceholderText(u'必填（只能为最多9位的纯数字）')
        grid1.addWidget(self.site_id, 2, 1)
        SiteNmae_label = QLabel(u"基站名字:")
        grid1.addWidget(SiteNmae_label, 3, 0)
        self.site_name = QLineEdit()
        self.site_name.setPlaceholderText(u'必填')
        grid1.addWidget(self.site_name, 3, 1)
        RNCBSC_label = QLabel(u"RNC-BSC:")
        grid1.addWidget(RNCBSC_label, 4, 0)
        self.rnc_bsc = QLineEdit()
        self.rnc_bsc.setPlaceholderText(u'若不填则为随机数')
        grid1.addWidget(self.rnc_bsc, 4, 1)

        lon_label = QLabel(u"经度:")
        lonlat_hobx.addWidget(lon_label)
        self.lon = QLineEdit()
        lonlat_hobx.addWidget(self.lon)
        lat_label = QLabel(u"纬度:")
        lonlat_hobx.addWidget(lat_label)
        self.lat = QLineEdit()
        lonlat_hobx.addWidget(self.lat)

        operator_label = QLabel(u'运营商:')
        grid2.addWidget(operator_label, 1, 0)
        self.operator = QComboBox(self)  # 运营商选择下拉框
        self.operator.addItems([u"移动", u"联通", u"电信", u"铁塔"])
        grid2.addWidget(self.operator, 1, 1)
        region_label = QLabel(u'区域类型:')
        grid2.addWidget(region_label, 1, 2)
        self.region = QComboBox(self)  # 区域类型选择下拉框
        self.region.addItems([u"普通市区", u"密集市区", u"郊区乡镇", u"农村"])
        grid2.addWidget(self.region, 1, 3)
        system_label = QLabel(u"网络制式:")
        grid2.addWidget(system_label, 2, 0)
        self.system = QComboBox(self)  # 网络制式选择下拉框
        self.system.addItems([u"900", u"1800", u"CDMA", u"WCDMA",
                              u"TD-LTE", u"FDD-LTE", u"TDSCDMA"])
        grid2.addWidget(self.system, 2, 1)
        frequency_label = QLabel(u"频段:")
        grid2.addWidget(frequency_label, 2, 2)
        self.frequency = QComboBox(self)  # 频段选择下拉框
        self.frequency.addItems([u"700M", u"800M", u"900M", u"1800M",
                                 u"1900M", u"2100M", u"2300M", u"2600M"])
        grid2.addWidget(self.frequency, 2, 3)

        # cell_label = QtGui.QLabel(u"<b>小区信息:  <\b>(若不需要添加小区请自行把下列的角度信息删除)")
        self.add_cell_checkbox = QCheckBox(u"添加小区")
        self.add_cell_checkbox.setChecked(False)
        grid3.addWidget(self.add_cell_checkbox, 1, 0)
        QObject.connect(self.add_cell_checkbox, SIGNAL("clicked()"), self.add_cell_checkChange)

        azimuth_1_label = QLabel(u'Azimuth 1:')
        grid4.addWidget(azimuth_1_label, 1, 0)
        azimuth_validator = QIntValidator(0, 360, self)
        self.azimuth_1 = QLineEdit()
        self.azimuth_1.setEnabled(False)
        self.azimuth_1.setValidator(azimuth_validator)
        grid4.addWidget(self.azimuth_1, 1, 1)
        titl_1_label = QLabel(u'TILT')
        grid4.addWidget(titl_1_label, 2, 0)
        self.tilt_1 = QLineEdit()
        self.tilt_1.setEnabled(False)
        grid4.addWidget(self.tilt_1, 2, 1)
        etilt_1_label = QLabel(u'ETILT')
        grid4.addWidget(etilt_1_label, 2, 2)
        self.etilt_1 = QLineEdit()
        self.etilt_1.setEnabled(False)
        grid4.addWidget(self.etilt_1, 2, 3)
        mtilt_1_label = QLabel(u"MTILT")
        grid4.addWidget(mtilt_1_label, 2, 4)
        self.mtilt_1 = QLineEdit()
        self.mtilt_1.setEnabled(False)
        grid4.addWidget(self.mtilt_1, 2, 5)

        azimuth_2_label = QLabel(u'Azimuth 2:')
        grid4.addWidget(azimuth_2_label, 3, 0)
        self.azimuth_2 = QLineEdit()
        self.azimuth_2.setEnabled(False)
        self.azimuth_2.setValidator(azimuth_validator)
        grid4.addWidget(self.azimuth_2, 3, 1)
        titl_2_label = QLabel(u'TILT')
        grid4.addWidget(titl_2_label, 4, 0)
        self.tilt_2 = QLineEdit()
        self.tilt_2.setEnabled(False)
        grid4.addWidget(self.tilt_2, 4, 1)
        etitl_2_label = QLabel(u'ETILT')
        grid4.addWidget(etitl_2_label, 4, 2)
        self.etilt_2 = QLineEdit()
        self.etilt_2.setEnabled(False)
        grid4.addWidget(self.etilt_2, 4, 3)
        mtilt_2_label = QLabel(u'MTILT')
        grid4.addWidget(mtilt_2_label, 4, 4)
        self.mtilt_2 = QLineEdit()
        self.mtilt_2.setEnabled(False)
        grid4.addWidget(self.mtilt_2, 4, 5)

        azimuth_3_label = QLabel(u'Azimuth 3:')
        grid4.addWidget(azimuth_3_label, 5, 0)
        self.azimuth_3 = QLineEdit()
        self.azimuth_3.setEnabled(False)
        self.azimuth_3.setValidator(azimuth_validator)
        grid4.addWidget(self.azimuth_3, 5, 1)
        titl_3_label = QLabel(u'TILT')
        grid4.addWidget(titl_3_label, 6, 0)
        self.tilt_3 = QLineEdit()
        self.tilt_3.setEnabled(False)
        grid4.addWidget(self.tilt_3, 6, 1)
        etitl_3_label = QLabel(u'ETILT')
        grid4.addWidget(etitl_3_label, 6, 2)
        self.etilt_3 = QLineEdit()
        self.etilt_3.setEnabled(False)
        grid4.addWidget(self.etilt_3, 6, 3)
        mtilt_3_label = QLabel(u'MTILT')
        grid4.addWidget(mtilt_3_label, 6, 4)
        self.mtilt_3 = QLineEdit()
        self.mtilt_3.setEnabled(False)
        grid4.addWidget(self.mtilt_3, 6, 5)

        azimuth_4_label = QLabel(u'Azimuth 4:')
        grid4.addWidget(azimuth_4_label, 7, 0)
        self.azimuth_4 = QLineEdit()
        self.azimuth_4.setEnabled(False)
        self.azimuth_4.setValidator(azimuth_validator)
        grid4.addWidget(self.azimuth_4, 7, 1)
        titl_4_label = QLabel(u'TILT')
        grid4.addWidget(titl_4_label, 8, 0)
        self.tilt_4 = QLineEdit()
        self.tilt_4.setEnabled(False)
        grid4.addWidget(self.tilt_4, 8, 1)
        etitl_4_label = QLabel(u'ETILT')
        grid4.addWidget(etitl_4_label, 8, 2)
        self.etilt_4 = QLineEdit()
        self.etilt_4.setEnabled(False)
        grid4.addWidget(self.etilt_4, 8, 3)
        mtilt_4_label = QLabel(u'MTILT')
        grid4.addWidget(mtilt_4_label, 8, 4)
        self.mtilt_4 = QLineEdit()
        self.mtilt_4.setEnabled(False)
        grid4.addWidget(self.mtilt_4, 8, 5)

        btn_hbox = QHBoxLayout()
        ok = QPushButton(u"添加")
        self.connect(ok, SIGNAL('clicked()'), self.add)
        cancel = QPushButton(u"取消")
        self.connect(cancel, SIGNAL('clicked()'), self.accept)
        btn_hbox.addStretch(1)
        btn_hbox.addWidget(ok)
        btn_hbox.addWidget(cancel)
        btn_hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addLayout(grid1)
        vbox.addLayout(lonlat_hobx)
        vbox.addLayout(grid2)
        vbox.addLayout(grid3)
        vbox.addLayout(grid4)
        vbox.addStretch(1)
        vbox.addLayout(btn_hbox)
        self.setLayout(vbox)
        self.resize(500, 510)

    # 鼠标单击事件
    def mouseClicked(self, pos, button):
            if button == Qt.LeftButton:
                self.show()
                self.geoPos = self.crsXform.transform(pos)
                self.lon.setText(unicode(self.geoPos.x()))
                self.lat.setText(unicode(self.geoPos.y()))

    # 选中添加小区改变事件
    def add_cell_checkChange(self):
        if self.add_cell_checkbox.isChecked():
            # 如果要连带添加小区
            self.azimuth_1.setEnabled(True)
            self.azimuth_1.setText(u"0")
            self.tilt_1.setEnabled(True)
            self.tilt_1.setText(u"4")
            self.etilt_1.setEnabled(True)
            self.etilt_1.setText(u"2")
            self.mtilt_1.setEnabled(True)
            self.mtilt_1.setText(u"2")

            self.azimuth_2.setEnabled(True)
            self.azimuth_2.setText(u"120")
            self.tilt_2.setEnabled(True)
            self.tilt_2.setText(u"4")
            self.etilt_2.setEnabled(True)
            self.etilt_2.setText(u"2")
            self.mtilt_2.setEnabled(True)
            self.mtilt_2.setText(u"2")

            self.azimuth_3.setEnabled(True)
            self.azimuth_3.setText(u"240")
            self.tilt_3.setEnabled(True)
            self.tilt_3.setText(u"4")
            self.etilt_3.setEnabled(True)
            self.etilt_3.setText(u"2")
            self.mtilt_3.setEnabled(True)
            self.mtilt_3.setText(u"2")

            self.azimuth_4.setEnabled(True)
            self.tilt_4.setEnabled(True)
            self.etilt_4.setEnabled(True)
            self.mtilt_4.setEnabled(True)

        else:
            # 把小区信息变回不可编辑状态
            self.azimuth_1.setEnabled(False)
            self.azimuth_1.setText("")
            self.tilt_1.setEnabled(False)
            self.tilt_1.setText("")
            self.etilt_1.setEnabled(False)
            self.etilt_1.setText("")
            self.mtilt_1.setEnabled(False)
            self.mtilt_1.setText("")

            self.azimuth_2.setEnabled(False)
            self.azimuth_2.setText("")
            self.tilt_2.setEnabled(False)
            self.tilt_2.setText("")
            self.etilt_2.setEnabled(False)
            self.etilt_2.setText("")
            self.mtilt_2.setEnabled(False)
            self.mtilt_2.setText("")

            self.azimuth_3.setEnabled(False)
            self.azimuth_3.setText("")
            self.tilt_3.setEnabled(False)
            self.tilt_3.setText("")
            self.etilt_3.setEnabled(False)
            self.etilt_3.setText("")
            self.mtilt_3.setEnabled(False)
            self.mtilt_3.setText("")

            self.azimuth_4.setEnabled(False)
            self.azimuth_4.setText("")
            self.tilt_4.setEnabled(False)
            self.tilt_4.setText("")
            self.etilt_4.setEnabled(False)
            self.etilt_4.setText("")
            self.mtilt_4.setEnabled(False)
            self.mtilt_4.setText("")

    # 点击确定按钮事件
    def add(self):
        # 获取并处理填写的信息
        site_id = self.site_id.text().strip() # 基站ID（新建基站ID前自动添加N）
        site_name = self.site_name.text().strip() # 基站名字
        rnc_bsc = self.rnc_bsc.text().strip() # RNC-BSC
        operator = self.operator.currentText().strip() # 运营商
        region = self.region.currentText().strip() # 区域类型
        system = self.system.currentText().strip() # 网络制式
        frequency = self.frequency.currentText().strip() # 频段
        system_flag = u"W" # 默认 W
        if system == u"900":
            system_flag = u"G"
        elif system == u"1800":
            system_flag = u"D"
        elif system == u"CDMA":
            system_flag = u"C"
        elif system == u"WCDMA":
            system_flag = u"W"
        elif system == u"TD-LTE":
            system_flag = u"T"
        elif system == u"FDD-LTE":
            system_flag = u"F"
        elif system == u"TDSCDMA":
            system_flag = u"TDS"
        lon = self.lon.text().strip() # 经度
        lat =self.lat.text().strip() # 纬度
        azimuth_1 = self.azimuth_1.text().strip()
        tilt_1 = self.tilt_1.text().strip()
        etilt_1 = self.etilt_1.text().strip()
        mtilt_1 = self.mtilt_1.text().strip()
        azimuth_2 = self.azimuth_2.text().strip()
        tilt_2 = self.tilt_2.text().strip()
        etilt_2 = self.etilt_2.text().strip()
        mtilt_2 = self.mtilt_2.text().strip()
        azimuth_3 = self.azimuth_3.text().strip()
        tilt_3 = self.tilt_3.text().strip()
        etilt_3 = self.etilt_3.text().strip()
        mtilt_3 = self.mtilt_3.text().strip()
        azimuth_4 = self.azimuth_4.text().strip()
        tilt_4 = self.tilt_4.text().strip()
        etilt_4 = self.etilt_4.text().strip()
        mtilt_4 = self.mtilt_4.text().strip()
        # 判断必填项是否已填
        if site_name == "":
            QMessageBox.critical(self,u"提示",u"请填写基站名字！")
            return False
        if site_id == "":
            QMessageBox.critical(self,u"提示",u"请填写基站ID！")
            return False
        if rnc_bsc == "":
            # 赋值随机数
            rnc_bsc = str(random.randint(1, 9999))
        if (lon == "") or (lat == ""):
            QMessageBox.critical(self,u"提示",u"请填写经纬度，或通过点击画布选择坐标！")
            return False
        # 先添加基站
        # 检查ID和名字是否重复
        self.sitelayer = getLayerByName(u'基站', self.iface) # 基站图层
        allsite = self.sitelayer.getFeatures()
        for site in allsite:
            if site_name == site[u'基站名']:
                QMessageBox.critical(self,u"提示",u"所填写的基站名与项目中的数据有重复，请更改！")
                return False
            if site_id == site[u'基站ID']:
                QMessageBox.critical(self,u"提示",u"所填写的基站ID与项目中的数据有重复，请更改！")
                return False

        siteFeatureAttrs = ['NULL'] * 20
        siteFeatureAttrs[0] = site_id
        siteFeatureAttrs[1] = site_name
        siteFeatureAttrs[2] = rnc_bsc
        siteFeatureAttrs[3] = lon
        siteFeatureAttrs[4] = lat
        siteFeatureAttrs[5] = system_flag
        siteFeatureAttrs[6] = region
        siteFeatureAttrs[8] = operator
        # 生成基站Feature
        add_site_list = []
        siteFeature = createASiteFeature(QgsPoint(float(lon), float(lat)), siteFeatureAttrs)
        add_site_list.append(siteFeature)

        # 判断是否需要顺带添加小区
        azimuth_list = []
        if azimuth_1 != "":
            if not tilt_1:
                tilt_1 = None
            if not etilt_1:
                etilt_1 = None
            if not mtilt_1:
                mtilt_1 = None
            azimuth_1_info = (int(azimuth_1), tilt_1, etilt_1, mtilt_1)
            azimuth_list.append(azimuth_1_info)
        if azimuth_2 != "":
            if not tilt_2:
                tilt_2 = None
            if not etilt_2:
                etilt_2 = None
            if not mtilt_2:
                mtilt_2 = None
            azimuth_2_info = (int(azimuth_2), tilt_2, etilt_2, mtilt_2)
            azimuth_list.append(azimuth_2_info)
        if azimuth_3 != "":
            if not tilt_3:
                tilt_3 = None
            if not etilt_3:
                etilt_3 = None
            if not mtilt_3:
                mtilt_3 = None
            azimuth_3_info = (int(azimuth_3), tilt_3, etilt_3, mtilt_3)
            azimuth_list.append(azimuth_3_info)
        if azimuth_4 != "":
            if not tilt_4:
                tilt_4 = None
            if not etilt_4:
                etilt_4 = None
            if not mtilt_4:
                mtilt_4 = None
            azimuth_4_info = (int(azimuth_4), tilt_4, etilt_4, mtilt_4)
            azimuth_list.append(azimuth_4_info)


        if len(azimuth_list) != 0:
            # 获取小区大小和长度设置
            setting = getCellGraphicParam(self.iface)
            # 判断是否读取到参数设置
            if not setting:
                QMessageBox.Critical(self.parent, u"错误", u"无法获取小区图形参数设置")
                return

            add_cell_list = [] # 要添加的小区list
            # 若填写了小区
            for index, azimuth_info in enumerate(azimuth_list):
                cell_feature = ['NULL'] * 54
                cell_feature[0] = site_id  # 基站ID
                cell_feature[1] = site_name  # 所属基站名字
                cell_id = u"%s%s" % (site_id, str(index+1))  # 小区ID
                cell_feature[2] = cell_id  # 小区ID
                cell_name = u"%s-%s" % (site_name, str(index + 1))  # # 小区名字
                cell_feature[3] = cell_name
                cell_feature[4] = index  # Sector ID
                cell_feature[6] = rnc_bsc
                cell_feature[7] = azimuth_info[0] # Azimuth
                cell_feature[8] = lon
                cell_feature[9] = lat
                cell_feature[10] = system_flag
                cell_feature[11] = region  # 典型环境
                cell_feature[12] = frequency # 频段
                cell_feature[13] = azimuth_info[1]
                cell_feature[14] = azimuth_info[2]
                cell_feature[15] = azimuth_info[3]
                cell_feature[18] = operator

                # 识别图形设置
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
                    elif operator == u'铁塔':
                        szAngle = setting[u"铁塔"][0]
                        szLength = setting[u"铁塔"][1]
                else:
                    # 自定义
                    system = cell_feature[10]
                    frequency = cell_feature[12]
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
                cellGeometry = createSector(QgsPoint(float(lon), float(lat)), szLength, self.iface, True, cell_feature[7], szAngle)

                # 判断小区名字和小区ID是否已于现有数据中
                self.celllayer = getLayerByName(u'小区', self.iface)  # 小区图层
                # 检查是否已勾选了小图特曾
                if not self.celllayer:
                    QMessageBox.critical(self.parent, u"错误", u"没有找到小区图层！")
                    return False
                allcell = self.celllayer.getFeatures()
                for cell in allcell:
                    if cell_name == cell[u'小区名']:
                        QMessageBox.critical(self.parent, u"提示", u"生成的小区名: " + cell_name + u" 与项目中的数据有重复，请更改！")
                        return False
                    if cell_id == cell[u"小区ID"]:
                        QMessageBox.critical(self.parent, u"提示", u"生成的小区ID: " + cell_id + u" 与项目中的数据有重复，请更改！")
                        return False
                # 生成小区feature并添加到list中
                cell = createACellFeature(cellGeometry, cell_feature)
                add_cell_list.append(cell)

        button = QMessageBox.question(self, "Question",
                                            u"添加后将无法撤回，是否继续?",
                                            QMessageBox.Ok | QMessageBox.Cancel,
                                            QMessageBox.Ok)
        if button == QMessageBox.Ok:
            # 向图层中导入新增的数据
            if len(add_site_list) != 0:
                siteLayer = getLayerByName(u"基站", self.iface)
                result1 = importFeaturesToLayer(siteLayer, add_site_list)
                if len(add_cell_list) != 0 and result1:
                    cellLayer = getLayerByName(u"小区", self.iface)
                    result2 = importFeaturesToLayer(cellLayer, add_cell_list)
                    if not result2:
                        QMessageBox.critical(self, u"添加基站", u"添加基站数据失败！")
                        self.accept()
                        return
                elif not result1:
                    QMessageBox.critical(self, u"添加基站", u"添加基站数据失败！")
                    self.accept()
                    return
            self.iface.actionDraw().trigger()  # 刷新地图
        else:
            return
        if result1 or result2:
            QMessageBox.information(self, u"添加基站", u"添加基站数据成功！")
        self.accept()