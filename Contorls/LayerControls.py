# -*- coding: utf-8 -*-
'''
@author: Karwai Kwok
图层相关操作合集
'''

from qgis.core import QgsPoint,QgsFeatureRequest,QgsCoordinateTransform,QgsCoordinateReferenceSystem,\
        QgsVectorLayer,QgsVectorDataProvider, QgsFeature, QgsGeometry,QGis

#根据图层名称，获取图层
def getLayerByName(name, iface):
    layers = iface.mapCanvas().layers()
    for layer in layers:
        if layer.name() == name:
            return layer

#获取所有的图层名字(返回列表)"
def getAllLayerName(iface):
    layers_name_list = []
    layers = iface.mapCanvas().layers()
    for layer in layers:
        if layer.name():
            layers_name_list.append(layer.name())
    return layers_name_list

# 获取输入图层的所有字段名
def getLayerFieldNames(layer, NoString=False):
    if layer:
        fields = layer.pendingFields()
        if NoString:
            field_names = []
            for field in fields:
                if field.typeName() != u"String":
                    field_names.append(field.name())
        else:
            field_names = [field.name() for field in fields]
        return field_names
    else:
        return []

# 根据指定要素找出对应Features列表
def getFeaturesByValue(iface, layername, fieldname, value):
    layer = getLayerByName(layername, iface)
    results = [] # 符合结果的feature列表
    features = layer.getFeatures()
    for feature in features:
        if feature[fieldname] == value:
            results.append(feature)
    return results

# 获取指定图层下所选中的features列表
def getSelectedFeatures(iface, layername):
    layer = getLayerByName(layername, iface)
    selected_sites_list = layer.selectedFeatures()
    if selected_sites_list == None:
        selected_sites_list = []
    return list(selected_sites_list)

# 判断是否只选中了一个基站
def isSelectedASite(iface):
    selectedFeatures_list = getSelectedFeatures(iface, u"基站")
    if len(selectedFeatures_list) == 1:
        return True
    else:
        return False

#通过SQL语句向指定图层中查询features
def getFeaturesBySQL(iface, layerName, sql):
    layer = getLayerByName(layerName, iface)
    request = QgsFeatureRequest()
    request.setFilterExpression(sql)
    features = layer.getFeatures(request)
    resultList = list(features)
    return resultList

#通过空间查询获取中心点附近最近的指定数点的features
# spatialIndex: QgsSpatialIndex
# basePoint: QgsPoint
# returnNum: int
# returns array of feature IDs
def getFeaturesIdBynearestNeighbor(spatialIndex, basePoint, returnNum) :
    nearest = spatialIndex.nearestNeighbor(basePoint, returnNum)
    return nearest

# returns array of IDs of features which intersect the rectangle
# spatialIndex: QgsSpatialIndex
# baseRectangle: QgsRectangle
def getFeaturesIdByIntersects(spatialIndex, baseRectangle):
    intersect = spatialIndex.intersects(baseRectangle)
    return intersect

# 通过空间查询返回在指定区域内的feature列表
# area: QgsRectangle
def getFeaturesListByArea(layer, area):
    featuresList = []
    request = QgsFeatureRequest()
    request.setFilterRect(area)
    for feature in layer.getFeatures(request):
        featuresList.append(feature)
    return featuresList

# 判断是否已初始化工程
def judgeInitProject(iface):
    all_layerName = getAllLayerName(iface)
    if len(all_layerName) < 3:
        return False
    for layerName in [u"基站", u"小区", u"相邻小区"]:
        if layerName not in all_layerName:
            return False
    return True

# 获取图层所有的features，以list形式返回
def getFeaturesList(layer):
    featuresList = []
    allFeatures = layer.getFeatures()
    for feature in allFeatures:
        featuresList.append(feature)
    return featuresList

# 获取图层有所有features的值，以list形式返回
def getFeaturesDataBtLayer(layer):
    featuresData_list = []
    fieldNames = getLayerFieldNames(layer)
    allFeatures = layer.getFeatures()
    for feature in allFeatures:
        myAttr = []
        for fieldName in fieldNames:
            tmpval = feature[fieldName]
            if tmpval != None:
                myAttr.append(tmpval)
            else:
                myAttr.append("")
        featuresData_list.append(myAttr)
        del myAttr
    return featuresData_list

# 根据基站ID、RNC-BSC和运营商获取与其关联的小区列表
def getCellListBySite(iface, site_id, rnc_bsc, operator):
    cell_list = []
    cellLayer = getLayerByName(u"小区",iface)
    allcell = cellLayer.getFeatures()
    for cell in allcell:
        if (cell[u'基站ID'] == site_id) \
                and (cell[u'RNC-BSC'] == rnc_bsc) \
                and operator == cell[u'运营商']:
            cell_list.append(cell)
    return cell_list