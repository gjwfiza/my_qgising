# -*- coding:utf-8 -*-
'''
Features相关操作FeatureUtils)
@author: Karwai Kwok
'''

from qgis._core import QgsVectorDataProvider, QgsFeature, QgsGeometry, QgsPoint, \
    QgsDistanceArea, QgsRectangle
from uuid import uuid4

"""
为指定图层添加Features
#param features: feature列表
#return bool 添加是否成功
"""
def importFeaturesToLayer(targetLayer, features):
    dataProvider = targetLayer.dataProvider()
    if dataProvider.capabilities() & QgsVectorDataProvider.AddFeatures:
        return dataProvider.addFeatures(features)
    else:
        # 图层不能够添加新的Feature，提示错误消息给用户
        raise Exception, u'对不起，你的图层不支持添加新的'

"""
创建一个基站feature
param point: 当前Feature的坐标点
param attrs: 当前Feature的参数列表
"""
def createASiteFeature(point, attrs):
    feature = QgsFeature()
    feature.initAttributes(len(attrs) + 1)
    for (index, attr) in enumerate(attrs):
        feature.setAttribute(index + 1, attr)
    # 如果是小区要素，id为(RNC-BSC_SiteId_CellId)
    feature.setAttribute(0, str(uuid4()).replace('-', ''))
    geom = QgsGeometry.fromPoint(point)
    feature.setGeometry(geom)
    return feature

"""
创建一个小区feature
param point: 当前Feature的坐标点
param attrs: 当前Feature的参数列表
"""
def createACellFeature(point, attrs):
    feature = QgsFeature()
    feature.initAttributes(len(attrs) + 1)
    for (index, attr) in enumerate(attrs):
        feature.setAttribute(index + 1, attr)
    # 如果是小区要素，id为(RNC-BSC_SiteId_CellId)
    feature.setAttribute(0, str(attrs[6]) + '_' + str(attrs[0]) + '_' + str(attrs[2]))
    geom = QgsGeometry.fromPolygon([point])
    feature.setGeometry(geom)
    return feature

"""
创建一个相邻小区feature
param attrs: 当前Feature的参数列表
"""
def createASCellFeature(attrs):
    feature = QgsFeature()
    feature.initAttributes(len(attrs) + 1)
    feature.setAttribute(0, str(uuid4()).replace('-', ''))
    for (index, attr) in enumerate(attrs):
        feature.setAttribute(index + 1, attr)
    return feature

"""
创建一个普通的点feature
param attrs: 当前Feature的参数列表
"""
def createABasicPointFeature(point, attrs):
    feature = QgsFeature()
    feature.initAttributes(len(attrs))
    for (index, attr) in enumerate(attrs):
        feature.setAttribute(index, attr)
    geom = QgsGeometry.fromPoint(point)
    feature.setGeometry(geom)
    return feature



"""
                    修改指定的Feature参数
        #param attrs: 所要修改的参数dict，格式为：{index(参数的索引) : name(需要修改的值)}
        #param featureId: 所要修改的Feature的ID
        #param dicts  {featureid1:attrs1,featureid2:attrs2......}
    """
def modifyFeatures(targetLayer, dicts):
    dataProvider = targetLayer.dataProvider()
    if dataProvider.capabilities() & QgsVectorDataProvider.ChangeAttributeValues:
        dataProvider.changeAttributeValues(dicts)
        return True
    else:
        # 图层不支持修改，则提示用户信息
        raise Exception, u'对不起，你的图层不支持修改'
        return False

"""
修改指定的Feature Geometry
param featureId: 所要修改的Feature的ID
param dicts  {featureid1:geom1,featureid2:geom2......}
"""
def modifyFeaturesGeom(targetLayer, geometry_dicts):
    dataProvider = targetLayer.dataProvider()
    if dataProvider.capabilities() & QgsVectorDataProvider.ChangeGeometries:
        dataProvider.changeGeometryValues(geometry_dicts)
    else:
        # 图层不支持修改，则提示用户信息
        raise Exception, u'对不起，你的图层不支持修改'

"""
    删除featureIds列表指定的Feature的ID
    @param: targetLayer， 目标图层
    @param: featureIds: 需要删除的Feature的 Id列表
    return bool 删除是否成功
"""
def delFeatures(targetLayer, featureIds):
    dataProvider = targetLayer.dataProvider()
    if dataProvider.capabilities() & QgsVectorDataProvider.DeleteAttributes:
        return dataProvider.deleteFeatures(featureIds)

# 删除所有features
def delAllFeatures(targetLayer):
    dataProvider = targetLayer.dataProvider()
    if dataProvider.capabilities() & QgsVectorDataProvider.DeleteAttributes:
        featureIds = []
        for feature in targetLayer.getFeatures():
            featureIds.append(feature.id())
        return dataProvider.deleteFeatures(featureIds)


def addAttributes(targetLayer, Field):
    dataProvider = targetLayer.dataProvider()
    if dataProvider.capabilities() & QgsVectorDataProvider.AddAttributes:
        dataProvider.addAttributes(Field)
        targetLayer.updateFields()

def deleteAttributes(targetLayer, attributeIds):
    dataProvider = targetLayer.dataProvider()
    if dataProvider.capabilities() & QgsVectorDataProvider.DeleteAttributes:
        dataProvider.deleteAttributes(attributeIds)
        targetLayer.updateFields()