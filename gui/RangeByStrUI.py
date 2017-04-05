# -*- coding: utf-8 -*-
'''
按范围分类显示(针对字符)交互界面
@author: Karwai Kwok
'''

import os
from PyQt4.QtGui import QDialog, QLabel, QComboBox, QHBoxLayout, QGridLayout, \
    QVBoxLayout, QPushButton, QMessageBox, QWidget, QScrollArea, QIcon, QColor, \
    QLineEdit, QDoubleValidator, QColorDialog
from PyQt4.QtCore import SIGNAL, QSize, Qt
from qgis.gui import QgsMessageBar
from qgis.core import QgsMapLayer, QgsMapLayerStyleManager, \
    QgsGraduatedSymbolRendererV2, QgsSymbolV2, QgsRendererRangeV2, \
    QgsRendererCategoryV2, QgsCategorizedSymbolRendererV2
from MyQGIS.Contorls.LayerControls import getAllLayerName, getLayerByName

# 插件目录
strfilepath = os.path.realpath(__file__)
cmd_folder = "%s/" % (os.path.dirname(strfilepath),)

# 按值分类显示参数设置窗口（设置窗口）
class RangeByStrSettingUI(QDialog):
    def __init__(self, iface, parent=None):
        super(RangeByStrSettingUI, self).__init__()
        self.iface = iface
        self.parent = parent
        self.iface.mapCanvas().currentLayerChanged[QgsMapLayer].connect(self.LayerChanged)

        self.color_btn_list = []  # 保存各范围所设置的颜色按钮
        self.delete_btn_list = []  # 保存各范围所设置的删除按钮
        self.value_widget_list = []
        self.setting_list = []  # 保存参数设置

        self.setWindowTitle(u"分类显示")

        layer_label = QLabel(u"选择图层:")
        self.layer_combo = QComboBox()
        layers_name = getAllLayerName(self.iface)
        self.layer_combo.addItems(layers_name)
        self.layer = getLayerByName(self.layer_combo.currentText(), self.iface)
        self.connect(self.layer_combo, SIGNAL('currentIndexChanged(int)'), self.layerListener)

        field_label = QLabel(u"选择字段:")
        self.field_combo = QComboBox()
        if self.layer != None:
            fields_list = []
            for field in self.layer.pendingFields():
                fields_list.append(field.name().strip())
            self.field_combo.addItems(fields_list)

        ok = QPushButton(u"确定")
        cancel = QPushButton(u"取消")
        self.connect(ok, SIGNAL('clicked()'), self.run)
        self.connect(cancel, SIGNAL('clicked()'), self.accept)

        # 选择图层、字段Widget
        source_grid = QGridLayout()
        source_grid.setSpacing(10)
        source_grid.addWidget(layer_label, 0, 1)
        source_grid.addWidget(self.layer_combo, 0, 2)
        source_grid.addWidget(field_label, 1, 1)
        source_grid.addWidget(self.field_combo, 1, 2)
        source_widget = QWidget()
        source_widget.setLayout(source_grid)

        # 参数设置窗口（带滚动条）
        self.setting_Widget = QWidget()
        self.setting_Widget.setMinimumSize(380, 800)

        self.scroll_vbox = QVBoxLayout()
        self.scroll_vbox.setSpacing(15)

        self.setting_vbox = QVBoxLayout()
        self.setting_vbox.setSpacing(5)
        value_widget = self.createAValue()
        self.setting_vbox.addWidget(value_widget)

        self.add_range_btn = QPushButton(u"添加")
        self.connect(self.add_range_btn, SIGNAL("clicked()"), self.add_value_box)

        self.scroll_vbox.addLayout(self.setting_vbox)
        self.scroll_vbox.addWidget(self.add_range_btn)
        self.scroll_vbox.addStretch(1)

        self.setting_Widget.setLayout(self.scroll_vbox)

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.setting_Widget)
        self.scroll.setAutoFillBackground(True)
        self.scroll.setWidgetResizable(True)

        # 确定/取消 按钮 Widget
        btn_hbox = QHBoxLayout()
        btn_hbox.setSpacing(15)
        btn_hbox.addStretch(1)
        btn_hbox.addWidget(ok)
        btn_hbox.addWidget(cancel)
        btn_hbox.addStretch(1)
        btn_widget = QWidget()
        btn_widget.setLayout(btn_hbox)

        vbox = QVBoxLayout()
        vbox.setSpacing(15)
        vbox.addWidget(source_widget)
        vbox.addWidget(self.scroll)
        vbox.addWidget(btn_widget)

        self.setLayout(vbox)
        self.setFixedSize(430, 500)

    # 生成一个范围设置控件组(Wigget)
    def createAValue(self, color_value=u"yellow", value=u""):
        delete_btn = QPushButton(self)
        delete_icon = QIcon(os.path.join(cmd_folder, u"..", u'images', u'delete.png'))
        delete_btn.setIcon(delete_icon)
        delete_btn.setIconSize(QSize(25, 25))
        delete_btn.setFixedSize(30, 30)
        delete_btn.setFocusPolicy(Qt.NoFocus)
        self.connect(delete_btn, SIGNAL("clicked()"), self.delete_value_box)

        color = QColor(color_value)
        color_btn = QPushButton(self)
        color_btn.setStyleSheet('QWidget {background-color:%s}' % color.name())
        color_btn.clicked.connect(self.colordialog)

        value_edit = QLineEdit(value)  # 搜索值

        label1 = QLabel(u" : ")

        value_widget = QWidget()

        value_box = QHBoxLayout()
        value_box.setSpacing(10)
        value_box.addWidget(delete_btn)
        value_box.addWidget(color_btn)
        value_box.addWidget(label1)
        value_box.addWidget(value_edit)
        value_box.setStretchFactor(color_btn, 1.5)
        value_box.setStretchFactor(value_edit, 1)
        value_widget.setLayout(value_box)

        self.color_btn_list.append(color_btn)
        self.delete_btn_list.append(delete_btn)
        self.value_widget_list.append(value_widget)

        self.setting_list.append([color, value_edit])

        return value_widget

    # 新增一个可设置的范围
    def add_value_box(self):
        new_value_widget = self.createAValue()
        # 重新布局
        self.setting_vbox.addWidget(new_value_widget)

    # 删除一组范围设置
    def delete_value_box(self):
        delete_index = None
        delete_button = self.sender()  # 获取信号来源
        for (index, button) in enumerate(self.delete_btn_list):
            if button is delete_button:
                delete_index = index
        # 删除 widget
        if delete_index != None:
            value_widget = self.value_widget_list[delete_index]
            self.setting_vbox.removeWidget(value_widget)
            value_widget.deleteLater()
            del self.value_widget_list[delete_index]
            del self.color_btn_list[delete_index]
            del self.delete_btn_list[delete_index]
            del self.setting_list[delete_index]

    # 颜色设置对话框
    def colordialog(self):
        col = QColorDialog.getColor()
        button = self.sender()  # 获取信号来源
        if col.isValid():
            button.setStyleSheet('QWidget{background-color:%s}' % col.name())
        for b in self.color_btn_list:
            if button is b:
                bindex = self.color_btn_list.index(b)
                self.setting_list[bindex][0] = col

    def layerListener(self):
        # 先清空原有的字段选择combobox
        self.field_combo.clear()
        # 获取所选图层名字
        layer_name = self.layer_combo.currentText()
        self.layer = getLayerByName(layer_name, self.iface)
        # 获取所选图层的所有字段
        if self.layer:
            fields_list = []
            for field in self.layer.pendingFields():
                fields_list.append(field.name().strip())
            self.field_combo.addItems(fields_list)

    def run(self):
        # 先检查是否选中了图层
        if not self.layer:
            self.accept()
            QMessageBox.critical(self, u"错误", u"<b>无法选中图层! <\b>")
            return False
        # 检查范围设置是否规范
        setting_list = []  # 保存处理过的范围设置list (每个范围用元组保存)
        for (color, value_edit) in self.setting_list:
            value = value_edit.text().strip()
            # 如果上下限其中有一个为空，则提示错误
            if not value:
                QMessageBox.critical(self, u"错误", u"<b>分类范围上下限不能为空! <\b>")
                return False
            setting_list.append((color, value))

        field = self.field_combo.currentText().strip()  # 获取所设置的字段
        # 显示图例
        self.accept()
        legend = RangeByStrLegend(self.iface, self)
        legend.showLegend(self.layer, field, setting_list)
        if not legend.isVisible():
            legend.show()
            legend.exec_()

    def LayerChanged(self, currentlayer):
        if currentlayer != self.layer:
            self.iface.messageBar().pushMessage(u'提示', u'切换图层，分析停止', QgsMessageBar.INFO, 4)
            self.close()

# 按值分类显示图例（执行窗口）
class RangeByStrLegend(QDialog):
    def __init__(self, iface, parent=None):
        super(RangeByStrLegend, self).__init__()
        self.iface = iface
        self.parent = parent

        self.setGeometry(1200, 200, 200, 50)
        self.setWindowTitle(u'范围分布图')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.vbox = QVBoxLayout()
        self.cellstyle = False
        self.styleManager = None

    def showLegend(self, layer, field, setting_list):
        if not self.cellstyle:
            self.styleManager = QgsMapLayerStyleManager(layer)
            self.styleManager.addStyleFromLayer(u'默认')
            self.cellstyle = True

        ranges = []
        flabel = QLabel(field)
        fl = QHBoxLayout()
        fl.addWidget(flabel)
        self.vbox.addLayout(fl)
        for bl in setting_list:
            widget = QWidget()
            widget.setStyleSheet('QWidget {background-color:%s}' %
                                 bl[0].name())
            widget.resize(20, 20)
            label = QLabel(bl[1])
            null_label = QLabel(' ')

            c = QGridLayout()
            c.setSpacing(3)
            c.addWidget(widget, 1, 0)
            c.addWidget(null_label, 1, 1)
            c.addWidget(label, 1, 2)
            self.vbox.addLayout(c)

            sym = QgsSymbolV2.defaultSymbol(layer.geometryType())
            sym.setColor(bl[0])
            rng = QgsRendererCategoryV2(bl[1], sym, label.text())
            ranges.append(rng)

        self.vbox.addStretch(1)
        self.setLayout(self.vbox)

        renderer = QgsCategorizedSymbolRendererV2(field, ranges)
        layer.setRendererV2(renderer)
        self.iface.actionDraw().trigger()

    def closeEvent(self, event):
        if not self.styleManager == None:
            self.styleManager.setCurrentStyle(u'默认')
            self.iface.actionDraw().trigger()
            self.cellstyle = False