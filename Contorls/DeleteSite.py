# -*- coding: utf-8 -*-
'''
删除基站函数
@author: Karwai Kwok
'''

from MyQGIS.Contorls.LayerControls import getLayerByName
from MyQGIS.Contorls.FeaturesControls import delFeatures

def deleteSite(iface):
    # 若选中基站则联动把其所带的小区一并删除，若只选中小区则值删除小区
    delete_site = []  # 存放要删除的基站features id
    delete_cell = []  # 存放要删除的小区features id
    siteLayer = getLayerByName(u'基站', iface)
    cellLayer = getLayerByName(u'小区', iface)

    selected_site = siteLayer.selectedFeatures()
    selected_cell = cellLayer.selectedFeatures()
    for site in selected_site:
        site_id = site[u"基站ID"]
        site_rnc_bsc = site[u"RNC-BSC"]
        allcell = cellLayer.getFeatures()
        delete_site.append(site.id())
        for cell in allcell:
            if site_id == cell[u"基站ID"] and site_rnc_bsc == cell[u"RNC-BSC"]:
                delete_cell.append(cell.id())
    for cell in selected_cell:
        if cell.id() not in delete_cell:
            delete_cell.append(cell.id())

    delete_result = True  # 默认为True
    if len(delete_site) != 0:
        if not delFeatures(siteLayer, delete_site):
            delete_result = False
    if len(delete_cell) != 0:
        if not delFeatures(cellLayer, delete_cell):
            delete_result = False
    return delete_result