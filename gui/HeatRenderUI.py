# -*- coding: utf-8 -*-
'''
生成热力渲染图交互界面
@author: Karwai Kwok
'''

import numpy as np
from PyQt4.QtGui import QDialog, QMessageBox, QLabel, QLineEdit, QDoubleValidator, \
    QComboBox, QGridLayout, QHBoxLayout, QVBoxLayout, QPushButton, QColor, QWidget
from PyQt4.QtCore import SIGNAL, Qt
from qgis.core import QgsVectorLayer, QgsFeature, QgsPoint,\
    QgsGeometry,QgsMapLayer,QgsSymbolV2,QgsRuleBasedRendererV2,QgsMapLayerRegistry,\
    QgsHeatmapRenderer,QgsMapLayerStyleManager,QgsFeatureRequest,QgsField,\
    QgsRendererRangeV2,QgsGraduatedSymbolRendererV2,\
    QgsRendererCategoryV2,QgsCategorizedSymbolRendererV2, QgsVectorGradientColorRampV2, \
    QgsGradientStop
from MyQGIS.Contorls.LayerControls import getLayerFieldNames

#  生成热力渲染图设置交互界面
class HeatRenderUI(QDialog):
    def __init__(self, iface, layer, StyleFromLayer, parent=None, radius=u"10.000", quality=2):
        super(HeatRenderUI, self).__init__()
        self.iface = iface
        self.layer = layer
        self.parent = parent
        self.styleManager = StyleFromLayer
        if not isinstance(radius, basestring):
            self.radius = str(radius)
        else:
            self.radius = radius
        self.quality = quality

        self.initUI()

    # 初始化界面
    def initUI(self):
        self.setWindowTitle(u"话务量渲染参数设置")

        radius_label = QLabel(u"渲染半径(mm)： ")
        self.radius_text = QLineEdit(self.radius)
        radius_validator = QDoubleValidator(0.0, 99999.9999, 4, self)
        self.radius_text.setValidator(radius_validator)
        quality_label = QLabel(u"渲染质量：")
        self.quality_combobox = QComboBox()
        self.quality_combobox.addItems([u"最好", u"较好", u"平衡", u"较快", u"最快"])
        self.quality_combobox.setCurrentIndex(self.quality)
        field_label = QLabel(u"渲染字段: ")
        self.field_conbobox = QComboBox()
        # 获取字段
        field_list = getLayerFieldNames(self.layer, True)
        if not field_list:
            QMessageBox.critical(self.parent, u"错误", u"所选图层不支持该功能！")
            self.accept()
            return
        self.field_conbobox.addItems(field_list)
        name_label = QLabel(u"图例名称：")
        self.name_text = QLineEdit()

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(radius_label, 0, 0)
        grid.addWidget(self.radius_text, 0, 1)
        grid.addWidget(quality_label, 1, 0)
        grid.addWidget(self.quality_combobox, 1, 1)
        grid.addWidget(field_label, 2, 0)
        grid.addWidget(self.field_conbobox, 2, 1)
        grid.addWidget(name_label, 3, 0)
        grid.addWidget(self.name_text, 3, 1)

        button_hbox = QHBoxLayout()
        button_hbox.addStretch(1)
        ok = QPushButton(u"确定")
        self.connect(ok, SIGNAL("clicked()"), self.run)
        button_hbox.addWidget(ok)
        cancel = QPushButton(u"取消")
        self.connect(cancel, SIGNAL("clicked()"), self.accept)
        button_hbox.addWidget(cancel)
        button_hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.setSpacing(10)
        vbox.addLayout(grid)
        vbox.addStretch(1)
        vbox.addLayout(button_hbox)

        self.setLayout(vbox)
        self.resize(300, 120)

    def run(self):
        # 非空检查
        if self.radius_text.text().strip() == u"":
            QMessageBox.critical(self, u"错误", u"请填写渲染半径！")
            return
        else:
            self.accept()
        self.radius = float(self.radius_text.text().strip())
        self.quality = self.quality_combobox.currentIndex()
        tra = QgsHeatmapRenderer()  # 设置基站为热图样式
        tra.setMaximumValue(0) # 默认渲染最大值为0（自动）
        color_ramp = QgsVectorGradientColorRampV2(QColor("white"), QColor("red"), False,
                    [QgsGradientStop(0.25, QColor("#00ffff")),
                     QgsGradientStop(0.50, QColor("#00ff00")),
                     QgsGradientStop(0.75, QColor("#ffff00"))])
        tra.setColorRamp(color_ramp)
        self.color = tra.colorRamp()
        tra.setRadius(self.radius)
        tra.setRenderQuality(self.quality)
        # 获取渲染字段
        fieldName = self.field_conbobox.currentText()
        tra.setWeightExpression(fieldName)  # 根据字段渲染
        self.layer.setRendererV2(tra)
        # 获取渲染字段的最大值
        max_value, min_value = self.getMaxAndMinValue(fieldName)
        self.iface.actionDraw().trigger()
        # 获取图例名称
        legend_name = self.name_text.text()
        legend = HeatRenderLegend(self.iface, self.styleManager, max_value, min_value, legend_name, self.parent)
        legend.show()
        legend.exec_()

    # 返回设定的参数dict
    def getSetting(self):
        Setting = {}
        Setting["radius"] = self.radius
        Setting["quality"] = self.quality
        return Setting

    # 返回阶梯详细数值
    def getMaxAndMinValue(self, fieldName):
        value_list = []
        for feature in self.layer.getFeatures():
            value_list.append(feature[fieldName])
        value_array = np.array(value_list)
        if len(value_array) == 0:
            return (0, 0)
        return (value_array.max(), value_array.min())

#  热力渲染图图例
class HeatRenderLegend(QDialog):
    def __init__(self, iface, styleManager, max_value, min_value, legend_name, parent=None):
        super(HeatRenderLegend, self).__init__()
        self.iface = iface
        self.styleManager = styleManager # 当前图层的样式管理器
        if max_value:
            self.max_value = max_value
        else:
            self.max_value = 0.0
        if min_value:
            self.min_value = min_value
        else:
            self.min_value = 0.0
        if legend_name:
            self.legend_name = legend_name
        else:
            self.legend_name = u"渲染图例"
        self.parent = parent

        delta = self.max_value - self.min_value

        self.setWindowTitle(self.legend_name)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint)

        widget_100 = QWidget()
        widget_100.setStyleSheet('QWidget {background-color: red}')
        widget_100.resize(20, 20)
        label_100 = QLabel("%.4f" % (float(self.max_value)))

        widget_75 = QWidget()
        widget_75.setStyleSheet('QWidget {background-color: #ffff00}')
        widget_75.resize(20, 20)
        label_75 = QLabel("%.4f" % (float(delta * 0.75) + self.min_value))

        widget_50 = QWidget()
        widget_50.setStyleSheet('QWidget {background-color: #00ff00}')
        widget_50.resize(20, 20)
        label_50 = QLabel("%.4f" % (float(delta * 0.50 + self.min_value)))

        widget_25 = QWidget()
        widget_25.setStyleSheet('QWidget {background-color: #00ffff}')
        widget_25.resize(20, 20)
        label_25 = QLabel("%.4f" % float((delta * 0.25 + self.min_value)))

        grid = QGridLayout()
        grid.setSpacing(20)
        grid.addWidget(widget_100, 0, 0)
        grid.addWidget(label_100, 0, 1)
        grid.addWidget(widget_75, 1, 0)
        grid.addWidget(label_75, 1, 1)
        grid.addWidget(widget_50, 2, 0)
        grid.addWidget(label_50, 2, 1)
        grid.addWidget(widget_25, 3, 0)
        grid.addWidget(label_25, 3, 1)

        self.setLayout(grid)
        self.setGeometry(300, 300, 250, 200)

    def closeEvent(self, event):
        self.accept()
        self.styleManager.setCurrentStyle(u"默认")  ##恢复上一级样式，即取消话务量渲染
        self.iface.actionDraw().trigger()