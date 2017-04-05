# -*- coding: utf-8 -*-
'''
添加自动规划基站待选站点交互界面
@author: Karwai Kwok
'''

import math
from PyQt4.QtGui import QMessageBox
from qgis._core import QGis, QgsMapLayerRegistry, QgsProject, QgsVectorFileWriter, \
    QgsVectorLayer, QgsFields, QgsPoint, QgsField, QgsSpatialIndex, QgsDistanceArea
from MyQGIS.Contorls.LayerControls import getLayerByName, getFeaturesListByArea
from MyQGIS.Contorls.FeaturesControls import importFeaturesToLayer, createABasicPointFeature
from MyQGIS.Contorls.GeometryControls import createARectangleByCenterPoint



# 添加待选站点到规划基站结果中
class AddNewSites(object):
    def __init__(self, iface, tlist):
        super(AddNewSites, self).__init__()
        self.iface = iface
        self.tlist = tlist # 存放所有参数的列表
        # 判断是否选中正确图层
        self.layer = self.iface.activeLayer()
        if self.layer.name() != u"泰森结点":
            QMessageBox.critical(self.parent, u"错误", u"请选择泰森结点图层！")
            return False
        self.result_layer = getLayerByName(u"规划基站结果", self.iface)
        if not self.result_layer:
            QMessageBox.critical(self.parent, u"错误", u"找不到规划基站结果！")
            return False
        self.nsiteLayer = getLayerByName(u'规划基站结果', self.iface)
        self.siteLayer = getLayerByName(u"基站", self.iface)

    # 获取要添加的结点
    def getNewSites(self):
        selectedNodes = self.layer.selectedFeatures()
        NewSites_list = []
        NewSites_point_list = []
        for node in selectedNodes:
            node_point = node.geometry().asPoint()
            # 元祖化node_point
            node_point = (node_point[0], node_point[1])
            if node_point not in NewSites_point_list:
                NewSites_point_list.append(node_point)
                NewSites_list.append(node)
        return NewSites_list


    def getResultNodesNames(self):
        result_nodes = self.result_layer.getFeatures()
        name_list = []
        for result_node in result_nodes:
            name = result_node[u"推送基站名"]
            if type(name) != str:
                name = str(name)
            name_list.append(name)
        return name_list


    def run(self):

        d = QgsDistanceArea()
        self.jlist = self.getNewSites()
        maxDistance = self.tlist[1] # 最大搜索范围
        feature_list = []
        existed_name_list = self.getResultNodesNames()
        for (jindex, jsite) in enumerate(self.jlist):  # 遍历结点
            perList = []  # 临时列表，用于转化子字典
            jnaminDis1, jnaminDis2, jnaminDis3, jnaminDis4, jnaminDis5, jnaminDis6 = [self.tlist[1] for i in
                                                                                      range(6)]
            asite1, asite2, asite3, asite4, asite5, asite6 = [None for i in range(6)]
            if jsite[7] == u'农村':
                minDis = float(self.tlist[2])
            elif jsite[7] == u'郊区乡镇':
                minDis = float(self.tlist[3])
            elif jsite[7] == u'密集市区':
                minDis = float(self.tlist[5])
            else:  # 区域类型的结点的最小辐射范围
                # 默认jsite[7]==u'普通市区'
                minDis = float(self.tlist[4])
            jpoint = jsite.geometry().asPoint()
            # 先找到结点附近设置搜索范围内的所有基站
            area = createARectangleByCenterPoint(jpoint, maxDistance)
            siteFeatures_list = getFeaturesListByArea(self.siteLayer, area)
            for asite in siteFeatures_list:  # #遍历找到的基站
                jnaDis = d.convertMeasurement(d.measureLine(jpoint, \
                                    QgsPoint(asite[4], asite[5])), 2, 0, False)[0]

                jnaAngle = math.atan2(asite[5] - jpoint.y(), asite[4] - jpoint.x())
                jnaAngle = 90.0 - 180 / math.pi * jnaAngle  # 弧度转角度(90-方位角，可转为以正北为0度角)

                if jnaDis <= jnaminDis1 and 0 < jnaAngle <= 60:
                    jnaminDis1 = float('%0.4f' % jnaDis)  # 保留四位小数
                    asite1 = asite
                elif jnaDis <= jnaminDis2 and 60 < jnaAngle <= 120:
                    jnaminDis2 = float('%0.4f' % jnaDis)  # 保留四位小数
                    asite2 = asite
                elif jnaDis <= jnaminDis3 and 120 < jnaAngle <= 180:
                    jnaminDis3 = float('%0.4f' % jnaDis)  # 保留四位小数
                    asite3 = asite
                elif jnaDis <= jnaminDis4 and -180 < jnaAngle <= -120:
                    jnaminDis4 = float('%0.4f' % jnaDis)  # 保留四位小数
                    asite4 = asite
                elif jnaDis <= jnaminDis5 and -120 < jnaAngle <= -60:
                    jnaminDis5 = float('%0.4f' % jnaDis)  # 保留四位小数
                    asite5 = asite
                elif jnaDis <= jnaminDis6 and -60 < jnaAngle <= 0:
                    jnaminDis6 = float('%0.4f' % jnaDis)  # 保留四位小数
                    asite6 = asite

            if jnaminDis1 and asite1: perList.append([jnaminDis1, asite1])
            if jnaminDis2 and asite2: perList.append([jnaminDis2, asite2])
            if jnaminDis3 and asite3: perList.append([jnaminDis3, asite3])
            if jnaminDis4 and asite4: perList.append([jnaminDis4, asite4])
            if jnaminDis5 and asite5: perList.append([jnaminDis5, asite5])
            if jnaminDis6 and asite6: perList.append([jnaminDis6, asite6])
            # 判断是否至少找到一个符合的基站
            if len(perList) < 6:
                for i in range(6 - len(perList)):
                    perList.append(None)  # 若数量不足，给列表补None值

            NewSiteName = "0"
            while True:
                if NewSiteName in existed_name_list:
                    NewSiteName = str(int(NewSiteName) + 1)

                else:
                    existed_name_list.append(NewSiteName)
                    break
            tempList1 = [NewSiteName, str(jpoint.x()), str(jpoint.y()), jsite[7]]
            tempList2 = []
            tolDistance = 0
            suit_site_dict = {}  # 用于记录符合基站的基站名和距离 (key: SiteName, value: distance)
            for L in perList:
                if isinstance(L, list):  # 判断是否为列表类型
                    tolDistance = tolDistance + L[0]
                    psite = L[1]
                    tempList2.append(psite[2])  # 基站名
                    tempList2.append(str(L[0]))  # 距离
                    tempList2.append(str(psite[4]))  # 经度
                    tempList2.append(str(psite[5]))  # 纬度
                    suit_site_dict[psite[2]] = L[0]
                else:
                    tempList2.append('NULL')
                    tempList2.append('NULL')  # 没有基站，设为None值
                    tempList2.append('NULL')
                    tempList2.append('NULL')
            if ((tolDistance != 0) and (len(suit_site_dict) != 0)):
                avgDistance = ("%.4f" % (tolDistance / len(suit_site_dict)))
                # 将符合要求的站点按距离从小到大排序
                sorted_list = sorted(suit_site_dict.iteritems(), key=lambda d: d[1], reverse=False)
                # tempList1后追加最近基站名称，最近基站距离，平均距离
                tempList1.extend([sorted_list[0][0], str(sorted_list[0][1]), str(avgDistance)])
            else:
                # tempList1后追加最近基站名称，最近基站距离，平均距离
                tempList1.extend(["NULL", "NULL", "0"])
            NewSite_datas = (tempList1 + tempList2)

            feature_list.append(createABasicPointFeature(jpoint, NewSite_datas))

        if importFeaturesToLayer(self.nsiteLayer, feature_list):
            self.iface.actionDraw().trigger()
            return True
        else:
            return False