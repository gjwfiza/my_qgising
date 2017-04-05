# -*- coding: utf-8 -*-
'''
地图工具操作类
@author: Karwai Kwok
'''
from qgis.gui import QgsMapToolEmitPoint, QgsMapToolIdentifyFeature

# 点操作类
class MapTool(QgsMapToolEmitPoint):
    def __init__(self, canvas):
        self.canvas = canvas
        super(MapTool, self).__init__(self.canvas)

#features改变类
class MapToolSelect(QgsMapToolIdentifyFeature):
    def __init__(self, canvas):
        self.canvas = canvas
        super(MapToolSelect, self).__init__(self.canvas)

























