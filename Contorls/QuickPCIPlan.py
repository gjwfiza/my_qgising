# -*- coding: utf-8 -*-
'''
全网快速PCI规划类
@author: Karwai Kwok
'''

import random
from qgis._core import QGis, QgsMapLayerRegistry, QgsProject, QgsVectorFileWriter, \
    QgsVectorLayer, QgsFields, QgsPoint, QgsField, QgsSpatialIndex, QgsDistanceArea
from MyQGIS.gui.Progress import Progess
from MyQGIS.Contorls.LayerControls import getLayerByName, getFeaturesList, getFeaturesBySQL
from MyQGIS.Contorls.FeaturesControls import modifyFeatures

class QuickPCIPlan(object):
    def __init__(self, iface, parent=None):
        super(QuickPCIPlan, self).__init__()
        self.iface = iface
        self.parent = parent
        self.marco_range = None
        self.room_range = None
        self.drip_range = None
        self.coverage = None
        self.siteLayer = getLayerByName(u"基站", self.iface)
        self.cellLayer = getLayerByName(u"小区", self.iface)

    # 设置参数
    def setParameters(self, marco_range, room_range, drip_range, coverage):
        self.marco_range = marco_range
        self.room_range = room_range
        self.drip_range = drip_range
        self.coverage = coverage

    def run(self):
        allCellFeatures_list = getFeaturesList(self.cellLayer)
        d = QgsDistanceArea()

        marco_cells_dict = {}
        room_cells_dict = {}
        not_room_cells_list = []
        drip_cells_dict = {}
        PCI_dict = {} # key:cell.id() value:PCI

        # 先把室分小区筛选出来
        for cell in allCellFeatures_list:
            if cell[u"小区类型"] == u"室分":
                site_name = cell[u"基站名"]
                site_id = cell[u"基站ID"]
                site = (site_id, site_name)
                if not room_cells_dict.has_key(site):
                    temp_list = [cell]
                    room_cells_dict[site] = temp_list
                    del temp_list
                else:
                    temp_list = room_cells_dict[site]
                    temp_list.append(cell)
                    room_cells_dict[site] = temp_list
                    del temp_list
            else:
                not_room_cells_list.append(cell)
        # 将非室分的小区按基站来分类以筛选滴灌小区
        if not_room_cells_list:
            cells_dict = {}
            for cell in not_room_cells_list:
                site_name = cell[u"基站名"]
                site_id = cell[u"基站ID"]
                site = (site_id, site_name)
                if not cells_dict.has_key(site):
                    temp_list = [cell]
                    cells_dict[site] = temp_list
                    del temp_list
                else:
                    temp_list = cells_dict[site]
                    temp_list.append(cell)
                    cells_dict[site] = temp_list
                    del temp_list
            # 筛选宏站和滴灌小区
            for (site, cells_list) in cells_dict.iteritems():
                if len(cells_list) > 3:
                    drip_cells_dict[site] = cells_list
                else:
                    marco_cells_dict[site] = cells_list

        # 生成进度条
        progess_len = len(marco_cells_dict)+len(room_cells_dict)+len(drip_cells_dict)
        progess = Progess(self.parent, progess_len)
        progess.show()

        # 先为宏站分配PCI
        sss = self.marco_range[0]
        for (site0, cells_list0) in marco_cells_dict.iteritems():
            had_used_SSS_set = set()
            for (site1, cells_list1) in marco_cells_dict.iteritems():
                if site0 == site1:
                    continue
                lon0 = cells_list0[0][u"经度"]
                lat0 = cells_list0[0][u"纬度"]
                site_point0 = QgsPoint(lon0, lat0)
                lon1 = cells_list1[0][u"经度"]
                lat1 = cells_list1[0][u"纬度"]
                site_point1 = QgsPoint(lon1, lat1)
                distance = d.convertMeasurement(d.measureLine(site_point0, site_point1), 2, 0, False)[0]  # 单位（米）
                if distance > 5*self.coverage:
                    continue
                # 在5倍覆盖范围内
                if not PCI_dict.has_key(cells_list1[0].id()):
                    pci1 = cells_list1[0]["PCI"]
                else:
                    pci1 = PCI_dict[cells_list1[0].id()]
                if pci1:
                    sss1 = pci1 / 3
                    had_used_SSS_set.add(sss1)
            # 为同一基站下的小区分配PCI
            # 先确定可用SSS
            for i in range(self.marco_range[0], self.marco_range[1]+1):
                if sss in had_used_SSS_set:
                    sss = sss + 1
                    if sss > self.marco_range[1]:
                        sss = self.marco_range[0]
                else:
                    break
            cells_list0.sort(key=lambda x:x[u"方向角"])
            for index,cell in enumerate(cells_list0):
                pci = index + 3*sss
                PCI_dict[cell.id()] = pci

            progess.count()

        # 为室分站分配PCI
        pci_count = self.room_range[0]*3
        for (site, cells_list) in room_cells_dict.iteritems():
            for cell in cells_list:
                if pci_count > self.room_range[1]*3 + 2:
                    pci_count = self.room_range[0]*3
                PCI_dict[cell.id()] = pci_count
                pci_count = pci_count + 1
            progess.count()

        # 为滴灌站分配PCI
        pci_count = self.drip_range[0] * 3
        for (site, cells_list) in drip_cells_dict.iteritems():
            for cell in cells_list:
                if pci_count > self.drip_range[1]*3 + 2:
                    pci_count = self.drip_range[0]*3
                PCI_dict[cell.id()] = pci_count
                pci_count = pci_count + 1
            progess.count()

        # 修改图层数据
        if PCI_dict:
            update_dict = {}
            pci_field_index = self.cellLayer.fieldNameIndex('PCI')
            for (id, pci) in PCI_dict.iteritems():
                update_dict[id] = {pci_field_index:pci}
            modifyFeatures(self.cellLayer, update_dict)
            progess.count()
            return True
        else:
            return False
