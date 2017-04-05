# -*- coding: utf-8 -*-
'''
优化自动规划基站类
@author: Karwai Kwok
'''

import os
from PyQt4.QtCore import QObject, pyqtSignal, SIGNAL
from qgis._core import QgsDistanceArea, QgsPoint, QgsSpatialIndex, QGis, \
    QgsVectorFileWriter, QgsVectorLayer, QgsMapLayerRegistry, QgsFeatureRequest
from MyQGIS.gui.Progress import Progess
from MyQGIS.Contorls.GeometryControls import createARectangleByCenterPoint
from MyQGIS.Contorls.FeaturesControls import createABasicPointFeature
from MyQGIS.Contorls.FileControls import getProjectDir, deleteShapefile
from MyQGIS.Contorls.LayerControls import getLayerByName, getFeaturesList
from MyQGIS.Contorls.FeaturesControls import delAllFeatures, importFeaturesToLayer, \
    delFeatures

# 自动规划所得基站合并
class OptimizateNewSite(object):
    def __init__(self, layer, parent=None):
        super(OptimizateNewSite, self).__init__()
        self.parent = parent
        self.nsiteLayer = layer

    def run(self):
        area_type_dict = {}  # (key: area_type, value: nsite index list)
        d = QgsDistanceArea()  # 计算距离
        allNSiteFeatures = getFeaturesList(self.nsiteLayer)
        # 把所有的nsite按区域类型分类
        for nsiteFeature in allNSiteFeatures:
            area_type = nsiteFeature[u"区域类型"]
            if area_type not in [u"普通市区", u"密集市区", u"农村", u"郊区乡镇"]:
                area_type = u"普通市区"
            if not area_type_dict.has_key(area_type):
                area_type_dict[area_type] = [nsiteFeature]
            else:
                t = area_type_dict[area_type]
                t.append(nsiteFeature)
                area_type_dict[area_type] = t
                del t
        total = len(allNSiteFeatures)  # 写进度条
        progess = Progess(self.parent, total, u"优化中...")
        progess.show()
        delete_list = []  # 要删除的 nsiteFeaures.id() list
        for (area_type, nsiteFeatures_list) in area_type_dict.items():
            if area_type == u"密集市区":
                mergeDis = 200
            elif area_type == u"郊区乡镇":
                mergeDis = 500
            elif area_type == u"农村":
                mergeDis = 800
            else:
                # 默认普通市区
                mergeDis = 300
            for nsiteFeatures1 in nsiteFeatures_list:
                progess.count()
                lon1 = nsiteFeatures1[u"经度"]
                lat1 = nsiteFeatures1[u"纬度"]
                point1 = QgsPoint(float(lon1), float(lat1))
                rectangle = createARectangleByCenterPoint(point1, 2000)
                if nsiteFeatures1.id() in delete_list:
                    progess.count()
                    continue
                else:
                    request = QgsFeatureRequest()
                    request.setFilterRect(rectangle)
                    for nsiteFeature2 in self.nsiteLayer.getFeatures(request):
                        if nsiteFeatures1.id() == nsiteFeature2.id():
                            continue
                        if nsiteFeature2.id() in delete_list:
                            continue
                        lon2 = nsiteFeatures1[u"经度"]
                        lat2 = nsiteFeatures1[u"纬度"]
                        point2 = QgsPoint(float(lon2), float(lat2))
                        distance = d.convertMeasurement(
                            d.measureLine(point1, point2), 2, 0, False)[0]
                        if distance <= mergeDis:
                            delete_list.append(nsiteFeature2.id())
                            break
        progess.kill()
        # 删除features
        delFeatures(self.nsiteLayer, delete_list)
        return True
