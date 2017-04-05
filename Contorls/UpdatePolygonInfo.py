# -*- coding: utf-8 -*-
'''
向基站和小区图层更新Polygon属性函数
@author: Karwai Kwok
'''
from MyQGIS.Contorls.LayerControls import getLayerByName
from MyQGIS.Contorls.FeaturesControls import modifyFeatures
from MyQGIS.gui.Progress import Progess

def updatePolygonInfo(iface, polygonLayer, polygon_id_field, content_field, parent=None):
    siteLayer = getLayerByName(u"基站", iface)
    cellLayer = getLayerByName(u"小区", iface)
    update_site_dict = {}  # 要更新了的基站dict (key: site.id(), value: {field: value})
    update_cell_dict = {}  # 要更新了的小区dict (key: cell.id(), value: {field: value})

    all_polygon = polygonLayer.getFeatures()
    # 生成进度条
    total = polygonLayer.featureCount()
    progess = Progess(parent, total)
    progess.show()  # 显示进度条
    for polygon in all_polygon:
        polygon_geom = polygon.geometry()
        polygon_id = polygon[polygon_id_field]
        if content_field != '':
            content = polygon[content_field]
        else:
            content = None

        all_site = siteLayer.getFeatures()
        for site in all_site:
            if not update_site_dict.has_key(site.id()):
                site_geom = site.geometry()
                # 判断是否相交
                if site_geom.intersects(polygon_geom):
                    temp_dict = {}
                    temp_dict[site.fieldNameIndex(u'Polygon')] = polygon_id
                    if content != None:
                        temp_dict[site.fieldNameIndex(u'其他')] = content
                    update_site_dict[site.id()] = temp_dict
                    del temp_dict

        all_cell = cellLayer.getFeatures()
        for cell in all_cell:
            if not update_cell_dict.has_key(cell.id()):
                cell_gemo = cell.geometry()
                # 判断是否相交
                if cell_gemo.intersects(polygon_geom):
                    temp_dict = {}
                    temp_dict[cell.fieldNameIndex(u'Polygon')] = polygon_id
                    if content != None:
                        temp_dict[cell.fieldNameIndex(u'其他')] = content
                    update_cell_dict[cell.id()] = temp_dict
                    del temp_dict
        progess.count()

    result1 = modifyFeatures(siteLayer, update_site_dict)
    result2 = modifyFeatures(cellLayer, update_cell_dict)
    progess.kill()
    if result1 and result2:
        return True
    else:
        return False

