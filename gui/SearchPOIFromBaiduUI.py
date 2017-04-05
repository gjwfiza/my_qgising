# -*- coding: utf-8 -*-
'''
从百度地图中抓取地理信息交互界面
@author: Karwai Kwok
'''

import numpy as np
import win32con
import win32clipboard as w
from PyQt4.QtGui import *
from PyQt4.Qt import *
from qgis.core import QgsPoint, QgsCoordinateTransform, QgsCoordinateReferenceSystem, QGis
from qgis.gui import QgsMapToolIdentify, QgsMessageBar
from MyQGIS.Contorls.LayerControls import getAllLayerName
from MyQGIS.Contorls.SearchPOIFromBaidu import SearchPOIFromBaidu

# 从百度地图中抓取地理信息交互界面
class SearchPOIFromBaiduUI(QDialog):
    mouseClicked = pyqtSignal(QgsPoint, Qt.MouseButton)
    def __init__(self, iface, parent=None):
        super(SearchPOIFromBaiduUI, self).__init__()
        self.iface = iface
        self.parent = parent

        self.initUI()
    # 初始化界面
    def initUI(self):
        self.setWindowTitle(u"搜索热点")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        key_label = QLabel(u"请输入关键字:")
        self.key_text = QLineEdit()
        h1 = QHBoxLayout()
        h1.setSpacing(15)
        h1.addWidget(key_label)
        h1.addWidget(self.key_text)

        density_label = QLabel(u"搜索密度：")
        self.density_text = QLineEdit(u"0.1")
        validator = QDoubleValidator(0.00001, 1.00000, 5, self)
        self.density_text.setValidator(validator)
        self.setBounds_btn = QPushButton(u"获取选中区域坐标")
        self.connect(self.setBounds_btn, SIGNAL('clicked()'), self.setBounds)
        h2 = QHBoxLayout()
        h2.setSpacing(15)
        h2.addWidget(density_label)
        h2.addWidget(self.density_text)
        h2.addWidget(self.setBounds_btn)

        BottomLeft_label = QLabel(u"左下角坐标：")
        self.bottom_left_text = QLineEdit()
        self.bottom_left_text.setPlaceholderText(u"经度,纬度")
        UpperRight_label = QLabel(u"右上角坐标：")
        self.upper_right_text = QLineEdit()
        self.upper_right_text.setPlaceholderText(u"经度,纬度")
        h3 = QHBoxLayout()
        h3.addWidget(BottomLeft_label)
        h3.addWidget(self.bottom_left_text)
        h3.addWidget(UpperRight_label)
        h3.addWidget(self.upper_right_text)

        ak_label = QLabel(u"请输入你的百度API密钥")
        self.ak_text = QLineEdit()
        self.ak_text.setText(u"hMewuKtRymsWRjqOYeshC0pREUgi1Ur7")
        h5 = QHBoxLayout()
        h5.setSpacing(15)
        h5.addWidget(ak_label)
        h5.addWidget(self.ak_text)

        savePath_label = QLabel(u"请输入生成结果图层名称：")
        self.saveName_edit = QLineEdit()
        h6 = QHBoxLayout()
        h6.setSpacing(15)
        h6.addWidget(savePath_label)
        h6.addWidget(self.saveName_edit)

        self.link_label = QLabel(u"百度地图秘钥申请链接: http://lbsyun.baidu.com/apiconsole/key ")
        self.apply_link_label = QLabel(u"http://lbsyun.baidu.com/apiconsole/key")
        self.link_button = QPushButton(u"复制")
        self.connect(self.link_button, SIGNAL("clicked()"), self.copyLink)
        link_hbox = QHBoxLayout()
        link_hbox.setSpacing(10)
        link_hbox.addStretch(1)
        link_hbox.addWidget(self.link_label)
        link_hbox.addWidget(self.link_button)
        link_hbox.addStretch(1)

        ok = QPushButton(u"确定")
        self.connect(ok, SIGNAL("clicked()"), self.run)
        cancel = QPushButton(u"取消")
        self.connect(cancel, SIGNAL("clicked()"), self.accept)
        btn_hbox = QHBoxLayout()
        btn_hbox.addStretch(1)
        btn_hbox.addWidget(ok)
        btn_hbox.addWidget(cancel)
        btn_hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addLayout(h1)
        vbox.addLayout(h2)
        vbox.addLayout(h3)
        vbox.addLayout(h5)
        vbox.addLayout(h6)
        vbox.addLayout(link_hbox)
        vbox.addStretch(1)
        vbox.addLayout(btn_hbox)
        self.setLayout(vbox)

    def setBounds(self):
        # 获取选中的区域范围
        layer = self.iface.activeLayer()
        if layer:
            # 先检查选中的区域geometry是否为Polygon
            if layer.geometryType() != QGis.Polygon:
                QMessageBox.critical(self, u"错误", u"当前选中的要素不是Polygon！")
                return False
            fs = layer.selectedFeatures()
            lon_list = []
            lat_list = []
            for f in fs:
                for polygon in f.geometry().asPolygon():
                    for point in polygon:
                        lon_list.append(point[0])
                        lat_list.append(point[1])
            lon_array = np.array(lon_list)
            lat_array = np.array(lat_list)
            if len(lon_array) > 1 and len(lat_array) > 1:
                self.bottom_left_text.clear()
                self.upper_right_text.clear()
                self.bottom_left_text.setText(str(lon_array.min()) + "," + str(lat_array.min()))
                self.upper_right_text.setText(str(lon_array.max()) + "," + str(lat_array.max()))
            else:
                self.bottom_left_text.clear()
                self.upper_right_text.clear()
                QMessageBox.critical(self, u"错误", u"所选中的区域格式有误！")
                return False
        else:
            QMessageBox.critical(self, u"错误", u"请选中图层！")
            return False

    # 将api申请链接复制到剪贴板
    def copyLink(self):
        apply_link = "http://lbsyun.baidu.com/apiconsole/key"
        w.OpenClipboard()
        w.EmptyClipboard()
        w.SetClipboardData(win32con.CF_TEXT, apply_link)
        w.CloseClipboard()
        # QtGui.QMessageBox.information(self.iface.mainWindow(), u"成功", u"已复制链接！")
        self.iface.messageBar().pushMessage(u'复制成功', u'已复制链接到剪切板 ', QgsMessageBar.SUCCESS, 3)

    # 判断搜索模式（0为以所选polygon为准，1为按所输入矩形为准）
    def getSearchType(self, current_searchRange):
        type = 1
        current_bottom_left = current_searchRange[0]
        current_upper_right = current_searchRange[1]
        layer = self.iface.activeLayer()
        if layer:
            # 先检查选中的区域geometry是否为Polygon
            if layer.geometryType() != QGis.Polygon:
                QMessageBox.critical(self, u"错误", u"当前选中的要素不是Polygon！")
                return False
            fs = layer.selectedFeatures()
            lon_list = []
            lat_list = []
            for f in fs:
                for polygon in f.geometry().asPolygon():
                    for point in polygon:
                        lon_list.append(point[0])
                        lat_list.append(point[1])
            lon_array = np.array(lon_list)
            lat_array = np.array(lat_list)
            bottom_left = (lon_array.min(),lat_array.min())
            upper_right = (lon_array.max(),lat_array.max())
            if current_bottom_left == bottom_left and current_upper_right == upper_right:
                type = 0
        return type

    def getSaveName(self):
        saveName = self.saveName_edit.text().strip()
        if not saveName:
            QMessageBox.critical(self, u"错误", u"请输入生成的结果图层名称!")
            return False
        else:
            for layer in self.iface.mapCanvas().layers():
                if layer.name() == saveName:
                    QMessageBox.critical(self, u"错误", u"所输入的图层名称已存在，请重新输入!")
                    return False
            return saveName

    def run(self):
        # 检查是否已填写好设置
        keywords = self.key_text.text().strip()
        if not keywords:
            QMessageBox.critical(self, u"错误", u"请输入要查找的关键字!")
            return False
        # 整理keywords
        keywords_list = keywords.split()
        # 获取搜索范围
        searchRange = None
        bottom_left_text  = self.bottom_left_text.text().strip()
        upper_right_text = self.upper_right_text.text().strip()
        # 检查非空
        if not bottom_left_text or not upper_right_text:
            self.accept()
            QMessageBox.critical(self, u"错误", u"请先在图层上选中要所搜的范围或自行填写搜索范围!")
            return False
        # 格式化搜索范围坐标
        # 先去除多余空格
        bottom_left_text = " ".join(bottom_left_text.split())
        upper_right_text = " ".join(upper_right_text.split())
        # 空格替换为“,”
        bottom_left_text = bottom_left_text.replace(u" ", u",")
        upper_right_text = upper_right_text.replace(u" ", u",")
        # 中文逗号替换为英文逗号
        bottom_left_text = bottom_left_text.replace(u"，", u",")
        upper_right_text = upper_right_text.replace(u"，", u",")
        # 检查经纬度分割方式是否正确
        if len(bottom_left_text.split(u",")) != 2 or len(upper_right_text.split(u",")) != 2:
            QMessageBox.critical(self, u"错误", u"所填写的搜索范围格式不正确!")
            return False
        # 检查是否为数字
        try:
            bottom_left_lon = float(bottom_left_text.split(u",")[0])
            bottom_left_lat = float(bottom_left_text.split(u",")[1])
            upper_right_lon = float(upper_right_text.split(u",")[0])
            upper_right_lat = float(upper_right_text.split(u",")[1])
        except TypeError, e:
            print e
            QMessageBox.critical(self, u"错误", u"所填写的搜索范围格式不正确!")
            return False
        # 检查经纬度范围是否正确
        if not -180 < bottom_left_lon < 180:
            QMessageBox.critical(self, u"错误", u"左下角坐标范围有误!")
            return False
        if not -180 < upper_right_lon < 180:
            QMessageBox.critical(self, u"错误", u"右上角坐标范围有误!")
            return False
        if not -90 < bottom_left_lat < 90:
            QMessageBox.critical(self, u"错误", u"左下角坐标范围有误!")
            return False
        if not -90 < upper_right_lat < 90:
            QMessageBox.critical(self, u"错误", u"右上角坐标范围有误!")
            return False
        if bottom_left_lon > upper_right_lon or bottom_left_lat > upper_right_lat:
            QMessageBox.critical(self, u"错误", u"请检查左下角坐标和右上角填写是否符合标准!")
            return False
        bottom_left = (bottom_left_lon, bottom_left_lat)
        upper_right = (upper_right_lon, upper_right_lat)
        searchRange = (bottom_left, upper_right)
        # 获取搜索密度
        try:
            density = float(self.density_text.text().strip())
        except TypeError, e:
            QMessageBox.critical(self, u"错误", u"搜索密度填写格式不正确!")
            return False
        # 获取ak码
        ak = self.ak_text.text().strip()
        if not ak:
            QMessageBox.critical(self, u"错误", u"请输入百度API密钥!")
            return False
        # 获取保存图层名
        save_layer_name = self.getSaveName()
        # 检查是否为空
        if not save_layer_name:
            QMessageBox.critical(self, u"错误", u"请输入输出图层名称!")
            return False
        exist_layer_names = getAllLayerName(self.iface)
        if save_layer_name in exist_layer_names:
            QMessageBox.critical(self, u"错误", u"所输入的输出图层名称已存在!")
            return False
        selectedLayer = self.iface.activeLayer()
        self.accept()
        # 判断搜索模式是自定义矩形还是所选中的polygon
        searchType = self.getSearchType(searchRange)
        search = SearchPOIFromBaidu(self.iface, keywords_list, searchRange, searchType, selectedLayer,
                           density, save_layer_name, ak, self.parent)
        search.run()