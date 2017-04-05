# -*- coding: utf-8 -*-
'''
自动规划基站类
@author: Karwai Kwok
'''

import math
from PyQt4.QtCore import QObject, pyqtSignal, SIGNAL
from qgis._core import QgsDistanceArea, QgsPoint
from MyQGIS.gui.Progress import Progess
from MyQGIS.Contorls.LayerControls import getLayerByName, getFeaturesListByArea
from MyQGIS.Contorls.GeometryControls import createARectangleByCenterPoint

#  自动规划基站类
class AutoBuildSite(QObject):
    calculationResult = pyqtSignal(object, object)
    def __init__(self, iface, jlist, tlist ,parent=None):
        super(AutoBuildSite, self).__init__()
        self.iface = iface
        self.jlist = jlist  # 存放泰森多边形结点
        self.tlist = tlist  # tlist=[分区角度，辐射范围，农村，郊区，普通市区，密集市区]
        self.siteLayer = getLayerByName(u"基站", self.iface)
        self.parent = parent

    def run(self):
        totalDict = {}  # 用于保存所有基站的计算结果
        suit_jlist = {} # 保存符合条件的结点
        d = QgsDistanceArea()
        total = len(self.jlist)  #写进度条
        progess = Progess(self.parent,total, u"分析中...")
        progess.show()
        maxDistance = self.tlist[1]
        for (jindex, jsite) in enumerate(self.jlist):   #遍历结点
            perList = [] #临时列表，用于转化子字典
            SuitOrNot = True # 结点是否符合标准标志(默认为True符合)
            jnaDis = None     # 保存结点和基站之间的距离
            jnaAngle = None
            jnaminDis1,jnaminDis2,jnaminDis3,jnaminDis4,jnaminDis5,jnaminDis6=[self.tlist[1] for i in range(6)]
            asite1,asite2,asite3,asite4,asite5,asite6=[None for i in range(6)]
            if jsite[7]==u'农村':
                minDis=float(self.tlist[2])
            elif jsite[7]==u'郊区乡镇' :
                minDis=float(self.tlist[3])
            elif jsite[7]==u'密集市区' :
                minDis=float(self.tlist[5])
            else:       #区域类型的结点的最小辐射范围
                # 默认jsite[7]==u'普通市区'
                minDis=float(self.tlist[4])
            jpoint=jsite.geometry().asPoint()
            # 先找到结点附近设置搜索范围内的所有基站
            area = createARectangleByCenterPoint(jpoint, maxDistance)
            siteFeatures_list = getFeaturesListByArea(self.siteLayer, area)
            for asite in siteFeatures_list: #遍历找到的基站
                jnaDis = d.convertMeasurement(d.measureLine(jpoint,\
                            QgsPoint(asite[4], asite[5])), 2, 0, False)[0]
                if jnaDis < minDis:
                    # 如果存在一个基站与结点间距离小于所设定的范围，则忽略该结点
                    SuitOrNot = False
                    break
                jnaAngle = math.atan2(asite[5]-jpoint.y(), asite[4]-jpoint.x())
                jnaAngle =90.0 - 180 / math.pi * jnaAngle #弧度转角度(90-方位角，可转为以正北为0度角)

                if jnaDis <= jnaminDis1 and 0 < jnaAngle <= 60 :
                    jnaminDis1 = float('%0.4f' % jnaDis)  # 保留四位小数
                    asite1 = asite
                elif jnaDis <= jnaminDis2 and 60 < jnaAngle <= 120 :
                    jnaminDis2 = float('%0.4f' % jnaDis)  # 保留四位小数
                    asite2 = asite
                elif jnaDis <= jnaminDis3 and 120 < jnaAngle <= 180 :
                    jnaminDis3 = float('%0.4f' % jnaDis)  # 保留四位小数
                    asite3 = asite
                elif jnaDis <= jnaminDis4 and -180 < jnaAngle <= -120 :
                    jnaminDis4 = float('%0.4f' % jnaDis)  # 保留四位小数
                    asite4 = asite
                elif jnaDis <= jnaminDis5 and -120 < jnaAngle <= -60 :
                    jnaminDis5 = float('%0.4f' % jnaDis)  # 保留四位小数
                    asite5 = asite
                elif jnaDis <= jnaminDis6 and -60 < jnaAngle <= 0 :
                    jnaminDis6 = float('%0.4f' % jnaDis)  # 保留四位小数
                    asite6 = asite

            if jnaminDis1 and asite1 : perList.append([jnaminDis1,asite1])
            if jnaminDis2 and asite2 : perList.append([jnaminDis2,asite2])
            if jnaminDis3 and asite3 : perList.append([jnaminDis3,asite3])
            if jnaminDis4 and asite4 : perList.append([jnaminDis4,asite4])
            if jnaminDis5 and asite5 : perList.append([jnaminDis5,asite5])
            if jnaminDis6 and asite6 : perList.append([jnaminDis6,asite6])
            # 判断是否至少找到一个符合的基站
            if len(perList) == 0:
                # 如果一个符合的基站都没有，则判断该节点不符合，跳过此次循环
                SuitOrNot = False
            elif len(perList) < 6 :
                for i in range(6-len(perList)) :
                    perList.append(None)                            #若数量不足，给列表补None值
            if SuitOrNot == True:
                # 结点符合才添加
                totalDict[jindex] = perList  #记录新建基站的计算结果，{0:[[],[],[],……],1:[……],……}
                suit_jlist[jindex] = jsite
            progess.count() #进度条+1
        self.calculationResult.emit(suit_jlist, totalDict)


