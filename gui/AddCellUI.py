# -*- coding: utf-8 -*-
'''
添加小区交互界面
@author: Karwai Kwok
'''

from PyQt4.QtGui import QDialog, QGridLayout, QHBoxLayout, QLabel, QLineEdit, \
    QIntValidator, QComboBox, QPushButton, QVBoxLayout, QMessageBox, QCheckBox
from PyQt4.QtCore import SIGNAL, QObject, pyqtSignal, pyqtSlot, Qt
from qgis.core import QgsPoint,QgsFeatureRequest,QgsCoordinateTransform,QgsCoordinateReferenceSystem,\
        QgsVectorLayer,QgsVectorDataProvider, QgsFeature, QgsGeometry,QGis
from MyQGIS.Contorls.FileControls import getProjectDir, getCellGraphicParam
from MyQGIS.Contorls.MapToolControls import MapTool
from MyQGIS.Contorls.LayerControls import getLayerByName, getCellListBySite
from MyQGIS.Contorls.FeaturesControls import createASiteFeature, createACellFeature, importFeaturesToLayer
from MyQGIS.Contorls.GeometryControls import createSector, createCircle


class AddCellUI(QDialog):
    def __init__(self, iface, parent=None):
        super(AddCellUI, self).__init__()
        self.iface = iface
        self.parent = parent
        # 获取工程所在路径
        self.project_dir = getProjectDir(self.iface)

        self.initUI()

    # 初始化界面
    def initUI(self):
        self.setGeometry(200, 200, 260, 150)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle(u'添加基站小区')
        # 用grid布局
        grid1 = QGridLayout()
        grid1.setSpacing(10)
        grid2 = QGridLayout()
        grid2.setSpacing(10)
        grid3 = QGridLayout()
        grid3.setSpacing(10)
        grid4 = QGridLayout()
        grid4.setSpacing(10)
        grid5 = QGridLayout()
        grid5.setSpacing(10)

        site_label = QLabel(u"<b>基站信息:  <\b>")
        grid1.addWidget(site_label, 1, 0)
        SiteId_label = QLabel(u"基站ID:")
        grid1.addWidget(SiteId_label, 2, 0)
        self.site_id = QLineEdit()
        site_id_validator = QIntValidator(0, 999999999, self)  # SiteId只能为最多9位的纯数字
        self.site_id.setValidator(site_id_validator)
        self.site_id.setPlaceholderText(u'必填')
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
        grid2.addWidget(lon_label, 1, 0)
        self.lon = QLineEdit()
        grid2.addWidget(self.lon, 1, 1)
        lat_label = QLabel(u"纬度:")
        grid2.addWidget(lat_label, 1, 2)
        self.lat = QLineEdit()
        grid2.addWidget(self.lat, 1, 3)
        operator_label = QLabel(u'运营商:')
        grid2.addWidget(operator_label, 2, 0)
        self.operator = QComboBox(self)  # 运营商选择下拉框
        self.operator.addItem(u"移动") # CurrentIndex = 0
        self.operator.addItem(u"联通") # CurrentIndex = 1
        self.operator.addItem(u"电信") # CurrentIndex = 2
        self.operator.addItem(u"铁塔") # CurrentIndex = 3
        grid2.addWidget(self.operator, 2, 1)
        region_label = QLabel(u'区域类型:')
        grid2.addWidget(region_label, 2, 2)
        self.region = QComboBox(self)  # 区域类型选择下拉框
        self.region.addItem(u"普通市区") # CurrentIndex = 0
        self.region.addItem(u"密集市区") # CurrentIndex = 1
        self.region.addItem(u"郊区乡镇") # CurrentIndex = 2
        self.region.addItem(u"农村") # CurrentIndex = 3
        grid2.addWidget(self.region, 2, 3)
        system_label = QLabel(u"网络制式:")
        grid2.addWidget(system_label, 3, 0)
        self.system = QComboBox(self)  # 网络制式选择下拉框
        self.system.addItems([u"900", u"1800", u"CDMA", u"WCDMA",
                              u"TD-LTE", u"FDD-LTE", u"TDSCDMA"])
        grid2.addWidget(self.system, 3, 1)
        frequency_label = QLabel(u"频段:")
        grid2.addWidget(frequency_label, 3, 2)
        self.frequency = QComboBox(self)  # 频段选择下拉框
        self.frequency.addItems([u"700M", u"800M", u"900M", u"1800M",
                                 u"1900M", u"2100M", u"2300M", u"2600M"])
        grid2.addWidget(self.frequency, 3, 3)

        cell_label = QLabel(u"<b>小区信息:  <\b>")
        grid3.addWidget(cell_label, 1, 0)

        azimuth_1_label = QLabel(u'Azimuth 1:')
        grid4.addWidget(azimuth_1_label, 1, 0)
        azimuth_validator = QIntValidator(0, 360, self)
        self.azimuth_1 = QLineEdit()
        self.azimuth_1.setValidator(azimuth_validator)
        grid4.addWidget(self.azimuth_1, 1, 1)
        titl_1_label = QLabel(u'TILT')
        grid4.addWidget(titl_1_label, 2, 0)
        self.tilt_1 = QLineEdit()
        grid4.addWidget(self.tilt_1, 2, 1)
        etilt_1_label = QLabel(u'ETILT')
        grid4.addWidget(etilt_1_label, 2, 2)
        self.etilt_1 = QLineEdit()
        grid4.addWidget(self.etilt_1, 2, 3)
        mtilt_1_label = QLabel(u"MTILT")
        grid4.addWidget(mtilt_1_label, 2, 4)
        self.mtilt_1 = QLineEdit()
        grid4.addWidget(self.mtilt_1, 2, 5)

        azimuth_2_label = QLabel(u'Azimuth 2:')
        grid4.addWidget(azimuth_2_label, 3, 0)
        self.azimuth_2 = QLineEdit()
        self.azimuth_2.setValidator(azimuth_validator)
        grid4.addWidget(self.azimuth_2, 3, 1)
        titl_2_label = QLabel(u'TILT')
        grid4.addWidget(titl_2_label, 4, 0)
        self.tilt_2 = QLineEdit()
        grid4.addWidget(self.tilt_2, 4, 1)
        etitl_2_label = QLabel(u'ETILT')
        grid4.addWidget(etitl_2_label, 4, 2)
        self.etilt_2 = QLineEdit()
        grid4.addWidget(self.etilt_2, 4, 3)
        mtilt_2_label = QLabel(u'MTILT')
        grid4.addWidget(mtilt_2_label, 4, 4)
        self.mtilt_2 = QLineEdit()
        grid4.addWidget(self.mtilt_2, 4, 5)

        azimuth_3_label = QLabel(u'Azimuth 3:')
        grid4.addWidget(azimuth_3_label, 5, 0)
        self.azimuth_3 = QLineEdit()
        self.azimuth_3.setValidator(azimuth_validator)
        grid4.addWidget(self.azimuth_3, 5, 1)
        titl_3_label = QLabel(u'TILT')
        grid4.addWidget(titl_3_label, 6, 0)
        self.tilt_3 = QLineEdit()
        grid4.addWidget(self.tilt_3, 6, 1)
        etitl_3_label = QLabel(u'ETILT')
        grid4.addWidget(etitl_3_label, 6, 2)
        self.etilt_3 = QLineEdit()
        grid4.addWidget(self.etilt_3, 6, 3)
        mtilt_3_label = QLabel(u'MTILT')
        grid4.addWidget(mtilt_3_label, 6, 4)
        self.mtilt_3 = QLineEdit()
        grid4.addWidget(self.mtilt_3, 6, 5)

        azimuth_4_label = QLabel(u'Azimuth 4:')
        grid4.addWidget(azimuth_4_label, 7, 0)
        self.azimuth_4 = QLineEdit()
        self.azimuth_4.setValidator(azimuth_validator)
        grid4.addWidget(self.azimuth_4, 7, 1)
        titl_4_label = QLabel(u'TILT')
        grid4.addWidget(titl_4_label, 8, 0)
        self.tilt_4 = QLineEdit()
        grid4.addWidget(self.tilt_4, 8, 1)
        etitl_4_label = QLabel(u'ETILT')
        grid4.addWidget(etitl_4_label, 8, 2)
        self.etilt_4 = QLineEdit()
        grid4.addWidget(self.etilt_4, 8, 3)
        mtilt_4_label = QLabel(u'MTILT')
        grid4.addWidget(mtilt_4_label, 8, 4)
        self.mtilt_4 = QLineEdit()
        grid4.addWidget(self.mtilt_4, 8, 5)

        hbox = QHBoxLayout()
        ok = QPushButton(u"添加")
        self.connect(ok, SIGNAL('clicked()'), self.add)
        cancel = QPushButton(u"取消")
        self.connect(cancel, SIGNAL('clicked()'), self.accept)
        hbox.addStretch(1)
        hbox.addWidget(ok)
        hbox.addWidget(cancel)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addLayout(grid1)
        vbox.addLayout(grid2)
        vbox.addLayout(grid3)
        vbox.addLayout(grid4)
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.resize(500, 510)

        # 填入选中的基站信息
        self.setSiteInfo()

    # 把选中的基站信息填入信息框中
    def setSiteInfo(self):
        siteLayer = getLayerByName(u"基站", self.iface)
        selected_sites_list = siteLayer.selectedFeatures()
        for selected_site in selected_sites_list:
            self.site_id.setText(selected_site[u'基站ID'])
            self.site_id.setReadOnly(True)
            self.site_name.setText(selected_site[u'基站名'])
            self.site_name.setReadOnly(True)
            self.rnc_bsc.setText(selected_site[u'RNC-BSC'])
            self.rnc_bsc.setReadOnly(True)
            if selected_site[u"运营商"] == u"移动":
                self.operator.setCurrentIndex(0)
            elif selected_site[u"运营商"] == u"联通":
                self.operator.setCurrentIndex(1)
            elif selected_site[u"运营商"] == u"电信":
                self.operator.setCurrentIndex(2)
            elif selected_site[u"运营商"] == u"铁塔":
                self.operator.setCurrentIndex(3)
            else:
                QMessageBox.critical(self, u"错误", u"请检查所选中的基站的运营商填写是否规范！")
                self.accept()
                return False
            if selected_site[u"典型环境"] == u"普通市区":
                self.region.setCurrentIndex(0)
            elif selected_site[u"典型环境"] == u"密集市区":
                self.region.setCurrentIndex(1)
            elif selected_site[u"典型环境"] == u"郊区乡镇":
                self.region.setCurrentIndex(2)
            elif selected_site[u"典型环境"] == u"农村":
                self.region.setCurrentIndex(3)
            else:
                raise u"所选中的基站的区域类型填写格式不规范！"


            self.lon.setText(str(selected_site[u"经度"]))
            self.lon.setReadOnly(True)
            self.lat.setText(str(selected_site[u"纬度"]))
            self.lat.setReadOnly(True)
            if selected_site[u"网络制式"].strip() == u"G":
                self.system.setCurrentIndex(0)
            elif selected_site[u"网络制式"].strip() == u"D":
                self.system.setCurrentIndex(1)
            elif selected_site[u"网络制式"].strip() == u"C":
                self.system.setCurrentIndex(2)
            elif selected_site[u"网络制式"].strip() == u"W":
                self.system.setCurrentIndex(3)
            elif selected_site[u"网络制式"].strip() == u"T":
                self.system.setCurrentIndex(4)
            elif selected_site[u"网络制式"].strip() == u"D":
                self.system.setCurrentIndex(5)
            elif selected_site[u"网络制式"].strip() == u"TDS":
                self.system.setCurrentIndex(6)

    # 确定按钮绑定时间
    def add(self):
        # 获取并处理填写的信息
        site_id = self.site_id.text().strip()  # 基站ID（新建基站ID前自动添加N）
        site_name = self.site_name.text().strip()  # 基站名字
        rnc_bsc = self.rnc_bsc.text().strip()  # RNC-BSC
        operator = self.operator.currentText().strip()  # 运营商
        region = self.region.currentText().strip()  # 区域类型
        lon = self.lon.text().strip()  # 经度
        lat = self.lat.text().strip()  # 纬度
        system  = self.system.currentText().strip() # 网络制式
        system_flag = u"W"  # 默认 W
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
        frequency = self.frequency.currentText().strip() # 频段
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
            QMessageBox.critical(self, u"提示", u"请填写基站名字！")
            return False
        if site_id == "":
            QMessageBox.critical(self, u"提示", u"请填写基站ID！")
            return False
        if rnc_bsc == "":
            # 赋值随机数
            rnc_bsc = range(1, 9999)
        if (lon == "") or (lat == ""):
            QMessageBox.critical(self, u"提示", u"请填写经纬度，或通过点击画布选择坐标！")
            return False

        # 获取填写的小区信息
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
        # 如果添加的小区没有填写的话则提示错误
        if len(azimuth_list) == 0:
            QMessageBox.critical(self, u"提示", u"请填写要添加的小区角度！")
            return False

        # 获取小区大小和长度设置
        setting = getCellGraphicParam(self.iface)
        # 判断是否读取到参数设置
        if not setting:
            QMessageBox.critical(self, u"错误", u"无法获取小区图形参数设置")
            return

        # 在小区表中寻找已有的小区信息
        existing_cell_list = getCellListBySite(self.iface, site_id, rnc_bsc, operator)
        # 判断是否该基站还能够添加小区(最多九个)
        if len(existing_cell_list) + len(azimuth_list) > 9:
            QMessageBox.critical(self, u"提示", u"所设置的基站已有"
                                       + str(len(existing_cell_list)) + u"个小区, 最多只能再添加"
                                       + str(9-len(existing_cell_list)) + u"个小区")
            return False
        else:
            existing_cell_id_list = []
            existing_cell_name_list = []
            existing_cell_sectorId_list = []
            for existing_cell in existing_cell_list:
                existing_cell_id_list.append(existing_cell[u'小区ID'])
                existing_cell_name_list.append(existing_cell[u'小区名'])
                existing_cell_sectorId_list.append(existing_cell[u"扇区ID"])

        if len(azimuth_list) != 0:
            # 生成要添加的小区feature
            add_cell_list = []
            add_cell_id_list = []
            add_cell_name_list = []
            for index, azimuth_info in enumerate(azimuth_list):
                cell_feature = ['NULL'] * 54
                cell_id = u"%s%s" % (site_id, str(index + 1))  # 小区ID
                # 判断 cell_id 是否会与现存的冲突，若冲突则自动改变 cel_id 命名
                while (cell_id in existing_cell_id_list) or (cell_id in add_cell_id_list):
                    cell_id = list(cell_id)
                    cell_id[-1] = str(int(cell_id[-1]) + 1)
                    if int(cell_id[-1]) > 9:
                        QMessageBox.critical(self, u"错误", u"生成的小区ID与现有的信息冲突")
                        return False
                    else:
                        temp = ''.join(cell_id)
                        del temp
                cell_feature[2] = cell_id  # 小区ID
                # 分配 Sector Id
                sector_id_range = [i for i in range(0,9)] # 取值范围为0~8
                for sector_id in sector_id_range:
                    if sector_id not in existing_cell_sectorId_list:
                        cell_feature[4] = sector_id
                        existing_cell_sectorId_list.append(sector_id)
                        break
                cell_feature[7] = azimuth_info[0]  # Azimuth
                cell_feature[8] = lon
                cell_feature[9] = lat
                cell_feature[0] = site_id  # 基站ID
                cell_feature[1] = site_name  # 所属基站名字
                cell_feature[18] = operator
                cell_name = u"%s-%s" % (site_name, str(index + 1))  # # 小区名字
                # 判断 cell_name 是否会与现存的冲突，若冲突则自动改变 cell_name 命名
                while (cell_name in existing_cell_name_list) or (cell_id in add_cell_name_list):
                    cell_name = list(cell_name)
                    cell_name[-1] = str(int(cell_name[-1]) + 1)
                    if int(cell_name[-1]) > 9:
                        QMessageBox.critical(self, u"错误", u"生成的小区名字与现有的信息冲突")
                        return False
                    else:
                        temp = ''.join(cell_name)
                        del temp
                cell_feature[3] = cell_name
                cell_feature[11] = region  # 典型环境
                cell_feature[6] = rnc_bsc
                cell_feature[10] = system_flag # 网络制式
                cell_feature[12] = frequency # 频段
                cell_feature[13] = azimuth_info[1]
                cell_feature[14] = azimuth_info[2]
                cell_feature[15] = azimuth_info[3]

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

                #生成小区扇形geometry
                cellGeometry = createSector(QgsPoint(float(lon), float(lat)), szLength, self.iface, True,
                                            cell_feature[7], szAngle)
                # 生成小区feature并添加到list中
                cell = createACellFeature(cellGeometry, cell_feature)
                add_cell_list.append(cell)

        button = QMessageBox.question(self, "Question",
                                            u"添加后将无法撤回，是否继续?",
                                            QMessageBox.Ok | QMessageBox.Cancel,
                                            QMessageBox.Ok)
        if button == QMessageBox.Ok:
            if len(add_cell_list) != 0:
                cellLayer = getLayerByName(u"小区", self.iface)
                result = importFeaturesToLayer(cellLayer, add_cell_list)
                if result:
                    self.iface.actionDraw().trigger()  # 刷新地图
                    QMessageBox.information(self, u"添加小区", u"添加小区数据成功！")
                else:
                    QMessageBox.critical(self, u"添加小区", u"添加小区数据失败！")
        else:
            return False
        self.accept()