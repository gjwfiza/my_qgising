# -*- coding: utf-8 -*-
'''
修改小区方向角交互界面
@author: Karwai Kwok
'''

from PyQt4.QtGui import QDialog, QMessageBox, QLabel, QIntValidator, QLineEdit, \
        QGridLayout, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt4.QtCore import Qt, SIGNAL
from qgis.core import QgsPoint,QgsFeatureRequest,QgsCoordinateTransform,QgsCoordinateReferenceSystem,\
        QgsVectorLayer,QgsVectorDataProvider, QgsFeature, QgsGeometry,QGis
from MyQGIS.Contorls.FileControls import getProjectDir, getCellGraphicParam
from MyQGIS.Contorls.LayerControls import getLayerByName
from MyQGIS.Contorls.GeometryControls import createSector, createCircle
from MyQGIS.Contorls.FeaturesControls import createACellFeature, delFeatures, importFeaturesToLayer

class ModifyAzimuthUI(QDialog):
    def __init__(self, iface, parnet):
        super(ModifyAzimuthUI, self).__init__()
        self.iface = iface
        self.parent = parnet
        # 获取工程所在路径
        self.project_dir = getProjectDir(self.iface)
        # 获取小区图层对象
        self.cellLayer = getLayerByName(u'小区', self.iface)
        self.initUI()

    # 初始化界面
    def initUI(self):
        self.setGeometry(300, 300, 200, 100)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle(u'修改')

        title = QLabel(u'新的扇区角度：')

        validator = QIntValidator(0, 360, self)
        self.titleEdit = QLineEdit()
        self.titleEdit.setValidator(validator)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(title, 1, 0)
        grid.addWidget(self.titleEdit, 1, 1)

        ok = QPushButton(u'确定')
        cancel = QPushButton(u'取消')

        hbox = QHBoxLayout()
        hbox.setSpacing(10)
        hbox.addStretch(1)
        hbox.addWidget(ok)
        hbox.addWidget(cancel)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addLayout(grid)
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.resize(240, 100)

        self.connect(ok, SIGNAL('clicked()'), self.NewAngle)
        self.connect(cancel, SIGNAL('clicked()'), self.accept)

    # 确定按钮绑定时间
    def NewAngle(self):
        # 获取小区大小和长度设置
        setting = getCellGraphicParam(self.iface)
        # 判断是否读取到参数设置
        if not setting:
            QMessageBox.critical(self, u"错误", u"无法获取小区图形参数设置")
            return

        newangle = self.titleEdit.text().strip()

        selection = self.cellLayer.selectedFeatures()
        ilist = []
        cellfeatures = []
        # 判断是否填入了角度
        if not newangle:
            QMessageBox.critical(self, u"提醒", u"请输入数值！")
            return False
        # 判断是否选中了要修改的小区
        if len(selection) == 0:
            QMessageBox.critical(self, u"错误", u"<b>请选择要修改的小区<\b>！")
            return False

        # 根据输入值创建新的扇区feature
        for f in selection:
            ilist.append(f.id())
            cellAttrs = f.attributes()
            del cellAttrs[0]
            cellAttrs[7] = int(newangle)
            operator = cellAttrs[18]
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
            cellGeometry = createSector(QgsPoint(float(cellAttrs[8]), float(cellAttrs[9])), szLength,
                                        self.iface, True,
                                        cellAttrs[7], szAngle)
            cellFeature = createACellFeature(cellGeometry, cellAttrs)
            cellfeatures.append(cellFeature)
            break
        else:
            QMessageBox.critical(self, u"提醒", u"请选择至少一个扇区！")
            return False

        button = QMessageBox.question(self, "Question",
                                            u"修改后将无法撤回，是否继续?",
                                            QMessageBox.Ok | QMessageBox.Cancel,
                                            QMessageBox.Ok)
        if button == QMessageBox.Ok:

            # 删除原角度扇区feature
            delRessult = delFeatures(self.cellLayer, ilist)
            if delRessult:
                impResult = importFeaturesToLayer(self.cellLayer, cellfeatures)
                if impResult:
                    QMessageBox.information(self, u"修改小区方向角", u"修改小区方向角成功！")
                else:
                    QMessageBox.critical(self, u"修改小区方向角", u"修改小区方向角失败！")
                    self.close()
                    return
            else:
                QMessageBox.critical(self, u"修改小区方向角", u"修改小区方向角失败！")
                self.close()
                return
            self.iface.actionDraw().trigger()
        else:
            return False
        self.accept()