# -*- coding: utf-8 -*-
'''
图层渲染操作
@author: Karwai Kwok
'''
from PyQt4.QtGui import QColor, QMessageBox
from qgis.core import QgsVectorLayer, QgsFeature, QgsPoint,\
    QgsGeometry,QgsMapLayer,QgsSymbolV2,QgsRuleBasedRendererV2,QgsMapLayerRegistry,\
    QgsHeatmapRenderer,QgsMapLayerStyleManager,QgsFeatureRequest,QgsField,\
    QgsRendererRangeV2,QgsGraduatedSymbolRendererV2,\
    QgsRendererCategoryV2,QgsCategorizedSymbolRendererV2, QgsVectorGradientColorRampV2, \
    QgsGradientStop, QGis
from MyQGIS.Contorls.LayerControls import getLayerByName
from MyQGIS.gui.Mod3Legend import Mod3Legend
from MyQGIS.gui.HeatRenderUI import HeatRenderUI

# 将对图层渲染设回默认
def setDeafaultRender(iface, styleManager):
    styleManager.setCurrentStyle(u"默认")  ##恢复上一级样式，即取消额外渲染
    iface.actionDraw().trigger()
    # 设置参数变回默认值
    sitestyle = False
    radius = u"10.000"  # 默认渲染半径
    quality = 2  # 默认渲染质量
    return (sitestyle, radius, quality)

# 模三渲染
def Mod3Render(iface, styleManager, parent=None):
    cellLayer = getLayerByName(u"小区", iface)
    # 模三规则
    rules = (('0', ' "PCI" % 3 = 0', 'red'),
             ('1', ' "PCI" % 3 = 1', 'yellow'),
             ('2', ' "PCI" % 3 = 2', '#47d54c'))
    sym_pci = QgsSymbolV2.defaultSymbol(cellLayer.geometryType())  # 小区feature重置默认样式
    rend_pci = QgsRuleBasedRendererV2(sym_pci)  # 设置为基于规则样式
    root_rule = rend_pci.rootRule()

    for label, exp, color, in rules:  # 根据规则渲染
        rule = root_rule.children()[0].clone()
        rule.setLabel(label)
        rule.setFilterExpression(exp)
        rule.symbol().setColor(QColor(color))
        root_rule.appendChild(rule)
        cellLayer.setRendererV2(rend_pci)

    iface.actionDraw().trigger()

    legend = Mod3Legend(iface, styleManager, parent)
    legend.show()
    legend.exec_()

# 热力图渲染
def HeatRender(iface, siteStyle, radius, quality, parent=None):
    # 判断当前图层类型是否为Point
    layer = iface.activeLayer()
    if not layer:
        QMessageBox.critical(parent, u"错误", u"请选中图层！")
        return (siteStyle, radius, quality)
    features = layer.getFeatures()
    if features:
        feature = features.next()
        if feature.geometry():
            layer_type = feature.geometry().type()
            if layer_type != QGis.Point:
                QMessageBox.critical(parent, u"错误", u"所选图层不支持该功能！")
                return (siteStyle, radius, quality)
        else:
            QMessageBox.critical(parent, u"错误", u"所选图层没有数据！")
            return (siteStyle, radius, quality)
    stylemanager = QgsMapLayerStyleManager(layer)
    stylemanager.addStyleFromLayer(u"默认")
    traffics = HeatRenderUI(iface, layer, stylemanager, parent)
    traffics.show()
    traffics.exec_()

    setting = traffics.getSetting()
    radius = setting["radius"]
    quality = setting["quality"]
    sitestyle = True
    return (sitestyle, radius, quality)