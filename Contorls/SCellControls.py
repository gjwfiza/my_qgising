# -*- coding: utf-8 -*-
'''
Created on 2016年01月04日

@author: Karwai Kwok
更新内容：
2016/07/13
修正删除双向相邻小区是时NType没有相应变更问题
'''
from qgis._core import QgsVectorDataProvider, QgsFeature, QgsGeometry, QgsDistanceArea, QgsPoint
from qgis._gui import QgsMessageBar, QgsRubberBand, QgsHighlight
from PyQt4.QtGui import QColor, QMessageBox
from uuid import uuid4
from MyQGIS.gui.SCellInfoUI import SCellInfoUI
from MyQGIS.Contorls.FeaturesControls import modifyFeatures, modifyFeaturesGeom
from MyQGIS.Contorls.LayerControls import getLayerByName

# 设置相邻小区中的主服务小区函数
# @ HL_SCell为高亮显示的主服务小区
def getSCell(iface, HL_SCell=None, parent=None):
    SCellList = []
    layer = iface.activeLayer() # 获取当前活动图层
    if not layer == None:
        # 检查活动图层是否是小区图层
        if layer.name() == u'小区':
            cellLayer = getLayerByName(u"小区", iface)  # 小区图层
            selection = cellLayer.selectedFeatures()
            if HL_SCell is not None:
                iface.mapCanvas().scene().removeItem(HL_SCell)
            for s in selection:
                scell_id = s[u'RNC-BSC'] + '_' + (s[u'基站ID']) + '_' + (s[u"小区ID"])
                SCellList.append(scell_id)
                HL_SCell = QgsHighlight(iface.mapCanvas(), s.geometry(), layer)
                HL_SCell.setFillColor(QColor('Red'))
            if len(SCellList) > 0:
                SCell = SCellList
                return SCellList, HL_SCell
        else:
            QMessageBox.critical(parent, u"错误", u"请选择小区图层！")
    else:
        QMessageBox.critical(parent, u"错误", u"请选择小区图层！")

# 添加单向相邻小区
def addOneWaySCell(iface, SCell_list):
    try:
        SCell = SCell_list[0]
        cellfeature = SCellControls(iface, SCell)
        '''判断是否选中小区图层'''
        if cellfeature.checkSelectLayer():
            result = cellfeature.addCellFeature1()
            '''判断是否选中要添加的小区'''
            if cellfeature.checkSelectFeature():
                if result == 0:
                    iface.messageBar().pushMessage(u'添加成功', u'已成功添加相邻小区', QgsMessageBar.SUCCESS, 1)
                elif result == 1:
                    iface.messageBar().pushMessage(u'错误', u'不能选择服务小区为其相邻小区', QgsMessageBar.CRITICAL, 3)
                elif result == 2:
                    iface.messageBar().pushMessage(u'添加失败', u'所选服务小区的相邻小区已满，请删除后再添加', QgsMessageBar.CRITICAL, 3)
            else:
                iface.messageBar().pushMessage(u'错误', u'请选择小区', QgsMessageBar.CRITICAL, 3)
        else:
            iface.messageBar().pushMessage(u'错误', u'请先选中小区图层', QgsMessageBar.CRITICAL, 3)

    except Exception, e:
        iface.messageBar().pushMessage(u'错误', u'请先设置服务小区', QgsMessageBar.CRITICAL, 3)
        print e

# 添加双向相邻小区
def addTwoWaySCell(iface, SCell_list):
    try:
        SCell = SCell_list[0]
        cellfeature = SCellControls(iface, SCell)
        '''判断是否选中小区图层'''
        if cellfeature.checkSelectLayer():
            result = cellfeature.addCellFeature2()
            '''判断是否选中要添加的小区'''
            if cellfeature.checkSelectFeature():
                if result == 0:
                    iface.messageBar().pushMessage(u'添加成功', u'已成功添加相邻小区', QgsMessageBar.SUCCESS, 1)
                elif result == 1:
                    iface.messageBar().pushMessage(u'错误', u'不能选择服务小区为其相邻小区', QgsMessageBar.CRITICAL, 3)
                elif result == 2:
                    iface.messageBar().pushMessage(u'添加失败', u'所选小区的相邻小区已满，请删除后再添加', QgsMessageBar.CRITICAL, 3)
                elif result == 3:
                    iface.messageBar().pushMessage(u'添加失败', u'要添加的小区的相邻小区已满，请删除后再添加', QgsMessageBar.CRITICAL, 3)
            else:
                iface.messageBar().pushMessage(u'错误', u'请选择小区', QgsMessageBar.CRITICAL, 3)
        else:
            iface.messageBar().pushMessage(u'错误', u'请先选中小区图层', QgsMessageBar.CRITICAL, 3)
    except Exception, e:
        iface.messageBar().pushMessage(u'错误', u'请先设置服务小区', QgsMessageBar.CRITICAL, 3)
        print e

# 获取主服务小区的名字
def getSCellName(iface, SCell_list):
    if len(SCell_list) > 0:
        scell_name = None
        scell_id = SCell_list[0]
        cellLayer = getLayerByName(u"小区", iface)  # 小区图层
        allCells = cellLayer.getFeatures()
        for cell in allCells:
            if cell[u'RNC-BSC'] + '_' + (cell[u'基站ID']) + '_' + (cell[u'小区ID']) == scell_id:
                scell_name = cell[u'小区名']
                break
        return scell_name
    else:
        iface.messageBar().pushMessage(u'错误', u'请先设置服务小区', QgsMessageBar.CRITICAL, 3)
        return None


class SCellControls(object):
    __dataprovider = None
    def __init__(self, iface, SCell=u'', HL_NCell_O=[], HL_NCell_D=[]):
        super(SCellControls, self).__init__()
        self.iface = iface

        self.cellLayer = self.iface.activeLayer() # 小区图层
        self.scellLayer = self.getLayer(u'相邻小区') # 相邻小区图层
        self.sitelayer = self.getLayer(u'基站') # 基站图层
        self.SCell = SCell
        self.__dataprovider = self.scellLayer.dataProvider()

        self.selections = self.getLayer(u'小区').selectedFeatures()

        self.canvas = self.iface.mapCanvas()
        self.canvas.show()
        self.HL_NCell_O = HL_NCell_O
        self.HL_NCell_D = HL_NCell_D


    """
            检查是否选中了小区图层
    """
    def checkSelectLayer(self):
        if not self.cellLayer == None:
            if self.cellLayer.name() == u'小区':
                return True
            else:
                return False
        else:
            return False



    """
            检查是否选中了小区
    """
    def checkSelectFeature(self):
        if len(self.selections) > 0:
            return True
        else:
            return False



    """
            增加单向相邻小区
    """
    def addCellFeature1(self):
        if self.__dataprovider.capabilities() & QgsVectorDataProvider.AddFeatures:
            cellfeatures = []
            ncells = {}
            ncell_dict = self.getNCellList()
            allCells = self.cellLayer.getFeatures()
            update_dict = {} # 要更新的features dict
            updateGemo_dict = {} # 要更新的features gemotry dict


            '''获得该小区的相邻小区数'''
            count = {}
            count = self.countCell(self.SCell, count)

            '''获得服务小区的基站ID'''
            scell = self.getCell()
            scell_SiteId = (scell[u'基站ID'])
            scell_point  = QgsPoint(scell[u"经度"],scell[u"纬度"])


            '''添加小区到相邻小区表中'''
            for ncell in self.selections:
                ncell_id = ncell[u'RNC-BSC'] + '_' + (ncell[u'基站ID']) + '_' + (ncell[u'小区ID'])
                ncells[ncell_id] = str(ncell[u'基站ID'])
                '''若服务小区与选中的小区重叠，返回  1 '''
                if ncell_id == self.SCell:
                    return 1
                '''检查相邻小区表中是否已存在要添加的相邻小区信息，若否则添加'''
                if not ncell_dict.has_key((self.SCell, ncell_id)):
                    ncell_point = QgsPoint(ncell[u"经度"],ncell[u"纬度"])
                    if (scell_point is not None) and (ncell_point is not None):
                        d = QgsDistanceArea()
                        distance = d.convertMeasurement(d.measureLine(scell_point, ncell_point), 2, 0, False)[0]

                    cellfaeture = QgsFeature()
                    cellfaeture.initAttributes(8)
                    cellfaeture.setAttribute(0, str(uuid4()).replace('-', '')) # 生成唯一标识id
                    cellfaeture.setAttribute(1, self.SCell)
                    cellfaeture.setAttribute(2, ncell_id)
                    # 判断是否存在对称相邻小区
                    if ncell_dict.has_key((ncell_id, self.SCell)):
                        # 如果存在对称小区，则新添加的小区为双向邻区
                        cellfaeture.setAttribute(3, '2')
                        # 把要更新的对称小区的 NType 信息加入到 update_dict 中
                        update_data_id = ncell_dict[(ncell_id, self.SCell)]
                        update_data_value = {self.scellLayer.fieldNameIndex('NType'): 2}
                        update_dict[update_data_id] = update_data_value
                    else:
                        # 如是单向相邻小区 NType 置为 1
                        cellfaeture.setAttribute(3, '1')
                    if distance >= 0 and (distance is not None):
                        cellfaeture.setAttribute(7, distance)
                        cellfaeture.setGeometry(QgsGeometry.fromPolyline([scell_point, ncell_point]))
                    cellfeatures.append(cellfaeture)
                    '''再次计算服务小区的相邻小区数'''
                    if count.has_key(self.SCell):
                        count[self.SCell] = count[self.SCell] + 1
                    else:
                        count[self.SCell] = 1
                else:
                    # 若已存在则更新信息
                    update_data_id = ncell_dict[(self.SCell, ncell_id)]
                    update_data_value = {} # 需要更新的 features 的值得dict
                    # 计算距离
                    ncell_point = QgsPoint(ncell[u"经度"],ncell[u"纬度"])
                    if (scell_point is not None) and (ncell_point is not None):
                        d = QgsDistanceArea()
                        distance = d.convertMeasurement(d.measureLine(scell_point, ncell_point), 2, 0, False)[0]
                    update_data_value[self.scellLayer.fieldNameIndex('Distance')] = distance
                    # 判断是否存在对称相邻小区
                    if ncell_dict.has_key((ncell_id, self.SCell)):
                        # 若存在对称小区则 NType 设为 2
                        update_data_value[self.scellLayer.fieldNameIndex('NType')] = 2
                    else:
                        # 反之，NType 设为 1
                        update_data_value[self.scellLayer.fieldNameIndex('NType')] = 1
                    update_dict[update_data_id] = update_data_value
                    updateGemo_dict[update_data_id] = QgsGeometry.fromPolyline([scell_point, ncell_point])


                '''若服务小区的相邻小区数大于31则不添加，并返回 2 '''
                if count[self.SCell] > 31:
                    return 2
            '''添加'''
            self.__dataprovider.addFeatures(cellfeatures)
            # 更新相邻小区表内数据
            if len(update_dict) > 0:
                modifyFeatures(self.scellLayer, update_dict)
            if len(updateGemo_dict) > 0:
                modifyFeaturesGeom(self.scellLayer, updateGemo_dict)
            return 0

        else:
            # 图层不能够添加新的Feature，提示错误消息给用户
            self.iface.messageBar().pushMessage(u'错误', u'添加相邻小区失败' , QgsMessageBar.CRITICAL, 3)



    """
                增加双向相邻小区
    """
    def addCellFeature2(self):
        if self.__dataprovider.capabilities() & QgsVectorDataProvider.AddFeatures:
            cellfeatures = []
            ncells = {}
            ncell_dict = self.getNCellList()
            allCells = self.cellLayer.getFeatures()

            update_dict = {} # 要更新的features dict
            updateGemo_dict = {} # 要更新的features gemotry dict

            '''获得该小区的相邻小区数'''
            count = {}
            count = self.countCell(self.SCell, count)


            '''获得服务小区的SiteId'''
            scell = self.getCell()
            scell_SiteId = (scell[u"基站ID"])
            scell_point  = QgsPoint(scell[u'经度'],scell[u'纬度'])

            '''添加小区到相邻小区表中'''
            for ncell in self.selections:
                ncell_id = ncell[u'RNC-BSC'] + '_' + (ncell[u"基站ID"]) + '_' + (ncell[u"小区ID"])
                ncells[ncell_id] = str(ncell[u"基站ID"])
                '''计算ncell的相邻小区个数'''
                count = self.countCell(ncell_id, count)
                '''若服务小区与选中的小区重叠，返回  1 '''
                if ncell_id == self.SCell:
                    return 1

                if not ncell_dict.has_key((self.SCell, ncell_id)):
                    '''若相邻小区表中不存在要添加的相邻小区信息，则添加'''
                    ncell_point = QgsPoint(ncell[u'经度'],ncell[u'纬度'])

                    if (scell_point is not None) and (ncell_point is not None):
                        d = QgsDistanceArea()
                        distance = d.convertMeasurement(d.measureLine(scell_point, ncell_point), 2, 0, False)[0]

                    cellfaeture = QgsFeature()
                    cellfaeture.initAttributes(8)
                    cellfaeture.setAttribute(0, str(uuid4()).replace('-', '')) # 生成唯一标识id
                    cellfaeture.setAttribute(1, self.SCell)
                    cellfaeture.setAttribute(2, ncell_id)

                    # 把 NType 置为 2 (双向)
                    cellfaeture.setAttribute(3, '2')

                    if distance >= 0 and (distance is not None):
                        cellfaeture.setAttribute(7, distance)
                        cellfaeture.setGeometry(QgsGeometry.fromPolyline([scell_point, ncell_point]))
                    cellfeatures.append(cellfaeture)
                    if count.has_key(self.SCell):
                        count[self.SCell] = count[self.SCell] + 1
                    else:
                        count[self.SCell] = 1
                else:
                    # 若已存在则更新信息
                    update_data_id = ncell_dict[(self.SCell, ncell_id)]
                    update_data_value = {} # 需要更新的 features 的值得dict
                    # 计算距离
                    ncell_point = QgsPoint(ncell[u'经度'],ncell[u'纬度'])
                    if (scell_point is not None) and (ncell_point is not None):
                        d = QgsDistanceArea()
                        distance = d.convertMeasurement(d.measureLine(scell_point, ncell_point), 2, 0, False)[0]
                    update_data_value[self.scellLayer.fieldNameIndex('Distance')] = distance
                    #  NType 设为 2（双向）
                    update_data_value[self.scellLayer.fieldNameIndex('NType')] = 2
                    update_dict[update_data_id] = update_data_value
                    updateGemo_dict[update_data_id] = QgsGeometry.fromPolyline([scell_point, ncell_point])
                '''判断原先是否存在对称相邻小区'''
                if not ncell_dict.has_key((ncell_id, self.SCell)):
                    # 如果不存在则添加对称相邻小区信息
                    ncell_point = QgsPoint(ncell[u'经度'],ncell[u'纬度'])
                    if (scell_point is not None) and (ncell_point is not None):
                        d = QgsDistanceArea()
                        distance = d.convertMeasurement(d.measureLine(ncell_point, scell_point), 2, 0, False)[0]

                    cellfaeture = QgsFeature()
                    cellfaeture.initAttributes(8)
                    cellfaeture.setAttribute(0, str(uuid4()).replace('-', '')) # 生成唯一标识id
                    cellfaeture.setAttribute(1, ncell_id)
                    cellfaeture.setAttribute(2, self.SCell)
                    # NType 置为 2 （双向）
                    cellfaeture.setAttribute(3, '2')

                    if distance >= 0 and (distance is not None):
                        cellfaeture.setAttribute(7, distance)
                        cellfaeture.setGeometry(QgsGeometry.fromPolyline([ncell_point, scell_point]))
                    cellfeatures.append(cellfaeture)
                    '''再次计算服务小区的相邻小区数'''
                    if count.has_key(ncell_id):
                        count[ncell_id] = count[ncell_id] + 1
                    else:
                        count[ncell_id] = 1

                else:
                    # 若已存在则对称小区的更新信息
                    # 把要更新的对称小区的 NType 信息加入到 update_dict 中
                    update_data_id = ncell_dict[(ncell_id, self.SCell)]
                    update_data_value = {} # 需要更新的 features 的值得dict
                    # 计算距离
                    ncell_point = QgsPoint(ncell[u'经度'],ncell[u'纬度'])
                    if (scell_point is not None) and (ncell_point is not None):
                        d = QgsDistanceArea()
                        distance = d.convertMeasurement(d.measureLine(scell_point, ncell_point), 2, 0, False)[0]
                    update_data_value[self.scellLayer.fieldNameIndex('Distance')] = distance
                    #  NType 设为 2 （双向）
                    update_data_value[self.scellLayer.fieldNameIndex('NType')] = 2
                    update_dict[update_data_id] = update_data_value
                '''若服务小区的相邻小区数大于31则不添加，并返回 2 '''
                if count[self.SCell] > 31:
                    return 2
                if count[ncell_id] > 31:
                    return 3
            '''添加'''
            self.__dataprovider.addFeatures(cellfeatures)
            # 更新相邻小区表内数据
            if len(update_dict) > 0:
                modifyFeatures(self.scellLayer, update_dict)
            if len(updateGemo_dict) > 0:
                modifyFeaturesGeom(self.scellLayer, updateGemo_dict)
            return 0




    """
                    从相邻小区表中删除选中的相邻小区
    """
    def delCellFeature(self):
        if self.__dataprovider.capabilities() & QgsVectorDataProvider.DeleteFeatures:
            delNCells = []
            delFeatureIDs = []
            modifyNType_dict = {} # 保存要修改 NType 的相邻小区 dict
            for cell in self.selections:
                cellId = cell[u'RNC-BSC'] + '_' + (cell[u'基站ID']) + '_' + (cell[u'小区ID'])
                delNCells.append(cellId)
            allNCells = self.scellLayer.getFeatures()
            for ncell in allNCells:
                for i in range(len(delNCells)):
                    if ncell['SCell'] == self.SCell and ncell['NCell'] == delNCells[i]:
                        delFeatureIDs.append(ncell.id())
                    if ncell['SCell'] == delNCells[i] and ncell['NCell'] == self.SCell:
                        if not modifyNType_dict.has_key(ncell.id()):
                            temp_dict = {}
                            temp_dict[ncell.fieldNameIndex('NType')] = 1
                            modifyNType_dict[ncell.id()] = temp_dict
                            del temp_dict

            '''检查是否选中了要删除的小区'''
            if len(delFeatureIDs) == 0:
                self.iface.messageBar().pushMessage(u'错误', u'请选择要删除的小区' , QgsMessageBar.CRITICAL, 3)
            else:
                # 先修改NType
                modifyFeatures(self.scellLayer, modifyNType_dict)
                # 删除，并返回删除结果
                deleteResult = self.__dataprovider.deleteFeatures(delFeatureIDs)
                return deleteResult

        else:
            self.iface.messageBar().pushMessage(u'错误', u'删除相邻小区失败' , QgsMessageBar.CRITICAL, 3)


    '''
            显示所选小区的相邻小区
    '''
    def showCellFeature(self):
        # 清空元素选择
        self.cellLayer.selectAll()
        self.cellLayer.invertSelection()
        self.scellLayer.selectAll()
        self.scellLayer.invertSelection()
        ncell_dict = self.getNCellList() # 提取所有相邻小区数据
        '''变量声明'''
        showNCellList = []
        showNCellIdDict = {} # key 为 NCell, value 为 NType
        showCellList = []
        distanceList = {}
        t_switchTimes_list = []
        s_switchTime_list = []
        s_switchRate_list = []

        count1 = 0
        count2 = 0

        '''清空涂色'''
        if len(self.HL_NCell_O) > 0:
            for h in self.HL_NCell_O:
                self.iface.mapCanvas().scene().removeItem(h)
        if len(self.HL_NCell_D) > 0:
            for h in self.HL_NCell_D:
                self.iface.mapCanvas().scene().removeItem(h)

        '''补全所选中的服务小区的相邻小区信息'''
        update_dict = {} # 要更新的features dict
        updateGemo_dict = {} # 要更新的features gemotry dict
        #featureUtils = FeatureUtils(u'相邻小区', self.iface)
        allNCells = self.scellLayer.getFeatures()
        for NCell in allNCells:
            feature_id = None # 需要更新的相邻小区的features_id
            if NCell['SCell'] == self.SCell:
                if NCell.geometry() == None:
                    # 相邻小区的 geometry 不存在才更新信息
                    feature_id = NCell.id()
                    scell_point = None # 服务小区经纬度
                    scell_siteId = None # 服务小区所属基站
                    ncell_point = None # 相邻小区经纬度
                    ncell_siteId = None # 相邻小区所属基站
                    allCells = self.cellLayer.getFeatures()
                    for Cell in allCells:
                        if Cell['id'] == NCell['SCell']:
                            scell_point = QgsPoint(Cell[u"经度"], Cell[u"纬度"])
                        if Cell['id'] == NCell['NCell']:
                            ncell_point = QgsPoint(Cell[u"经度"], Cell[u"纬度"])
                        if scell_point != None and ncell_point != None:
                            break
                    # 更新相邻小区信息
                    if feature_id != None and scell_point != None and ncell_point != None:
                        features_value = {} # 需要更新的 features 的值得dict
                        # 判断相邻小区类型
                        if not ncell_dict.has_key((NCell['NCell'],NCell['SCell'])):
                            features_value[self.scellLayer.fieldNameIndex('NType')] = 1
                        else:
                            features_value[self.scellLayer.fieldNameIndex('NType')] = 2
                        # 计算距离
                        d = QgsDistanceArea()
                        distance = d.convertMeasurement(d.measureLine(scell_point, ncell_point), 2, 0, False)[0]
                        features_value[self.scellLayer.fieldNameIndex('Distance')] = distance
                        update_dict[feature_id] = features_value
                        updateGemo_dict[feature_id] = QgsGeometry.fromPolyline([scell_point, ncell_point])

        if len(update_dict) > 0 and len(updateGemo_dict) > 0:
            modifyFeatures(self.scellLayer, update_dict)
            modifyFeaturesGeom(self.scellLayer, updateGemo_dict)
        else:
            pass

        '''获得相邻小区表中服务小区的相邻小区id，计算各类型相邻小区的数量，并保存其距离到 distanceList 中'''
        allNCells = self.scellLayer.getFeatures()
        for NCell in allNCells:
            if NCell['SCell'] == self.SCell:
                # 在相邻小区表中找出 SCell 为所设置的服务小区的项
                showNCellIdDict[NCell['NCell']] = NCell['NType']
                showNCellList.append(NCell.id())
                if NCell['NType'] == '1':
                    count1 = count1 + 1
                if NCell['NType'] == '2':
                    count2 = count2 + 1
                distanceList[(NCell['SCell'], NCell['NCell'])] = NCell['Distance']
                t_switchTimes_list.append(str(NCell['HOAttempt']))
                s_switchTime_list.append(str(NCell['HOSucc']))
                s_switchRate_list.append(str(NCell['HOSuccRate']))
            else:
                pass
        '''在小区图层中选中相邻小区，并找到服务小区的名字'''
        allCells = self.cellLayer.getFeatures()
        for cell in allCells:
            for (NCell, NType) in showNCellIdDict.items():
                if cell[u'RNC-BSC'] + '_' + (cell[u'基站ID']) + '_' + (cell[u'小区ID']) == NCell:
                    showCellList.append(cell.id())
                    # 涂色
                    self.iface.actionZoomFullExtent().trigger() # 涂色前将画布缩放到全图显示
                    if NType == u"1":
                        # 单向小区涂粉色
                        h = QgsHighlight(self.iface.mapCanvas(), cell.geometry(), self.cellLayer)
                        h.setFillColor(QColor('Pink'))
                        self.HL_NCell_O.append(h)
                    else:
                        h = QgsHighlight(self.iface.mapCanvas(), cell.geometry(), self.cellLayer)
                        h.setFillColor(QColor('Blue'))
                        self.HL_NCell_D.append(h)
            if cell[u'RNC-BSC'] + '_' + (cell[u'基站ID']) + '_' + (cell[u'小区ID']) == self.SCell:
                scell_name = cell[u'小区名']
        '''获得相邻小区的名字，并显示服务小区与相邻小区的距离'''
        i = 0
        allCells = self.cellLayer.getFeatures()
        info_list = []
        for cell2 in allCells:
            for ncell, distance in distanceList.items():
                if ncell[1] == (cell2[u'RNC-BSC'] + '_' + (cell2[u'基站ID']) + '_' + (cell2[u'小区ID'])):
                    ncell_name = cell2[u"小区名"]
                    try:
                        # 显示服务小区与相邻小区的相关信息
                        info =  unicode(scell_name) + u' <----> ' + unicode(ncell_name) + u'之间的距离为： ' + unicode(str(distance)) + u'米'
                        info_list.append(info)
                        i = i + 1
                    except UnicodeEncodeError:
                        pass
        '''显示相邻小区'''
        if len(showCellList) == 0:
            return False
        else:

            self.cellLayer.setSelectedFeatures(showCellList)
            self.scellLayer.setSelectedFeatures(showNCellList)
            self.iface.actionZoomToSelected().trigger()

            self.scellwin = SCellInfoUI(info_list, scell_name, count1, count2)
            self.scellwin.show()
            self.scellwin.exec_()

            return (scell_name, count1, count2)


    '''根据图层名字返回相应图层'''
    def getLayer(self, name):
            layers = self.iface.mapCanvas().layers()
            for layer in layers:
                if layer.name() == name:
                    return layer

    '''从相邻小区表中获得所有相邻小区信息'''
    def getNCellList(self):
        iters = self.scellLayer.getFeatures()
        ncell_dict = {}
        for iter in iters:
            scell = iter['SCell']
            ncell = iter['NCell']
            ncell_dict[(scell, ncell)] = iter.id()
        return ncell_dict

    '''
                返回服务小区
    '''
    def getCell(self):
        allCells = self.cellLayer.getFeatures()
        hasCell = False
        for Cell in allCells:
            if (Cell[u'RNC-BSC'] + '_' + (Cell[u'基站ID']) + '_' + (Cell[u'小区ID'])) == self.SCell:
                hasCell = True
                return Cell
        if not hasCell:
            self.iface.messageBar().pushMessage(u'错误', u'请选择小区' , QgsMessageBar.CRITICAL, 3)



    '''
            检查相邻小区的重复性，并自动修正
    '''
    def checkRepeat(self):
        if self.__dataprovider.capabilities() & QgsVectorDataProvider.DeleteFeatures:
            ncell_dict = {}
            delNCell_list = []
            '''从相邻小区表中获得所有相邻小区，若重复则添加到 delNCell_list'''
            allNCells = self.scellLayer.getFeatures()
            for ncell in allNCells:
                if not ncell_dict.has_key((ncell['SCell'], ncell['NCell'])):
                    ncell_dict[(ncell['SCell'], ncell['NCell'])] = 1
                else:
                    delNCell_list.append(ncell.id())
            '''删除重复的相邻小区'''
            if len(delNCell_list) > 0:
                deleteResult = self.__dataprovider.deleteFeatures(delNCell_list)
                if deleteResult:
                    self.iface.messageBar().pushMessage(u'检查完成', u'已自动删除重复的相邻小区' , QgsMessageBar.SUCCESS, 1)
                else:
                    self.iface.messageBar().pushMessage(u'错误', u'无法删除重复的相邻小区!' , QgsMessageBar.CRITICAL, 3)
            else:
                self.iface.messageBar().pushMessage(u'检查完成', u'没有发现重复的相邻小区' , QgsMessageBar.SUCCESS, 1)


    '''
            检查相邻小区的对称性
    '''
    def checkSymmetry(self):

        ncell_dict = {}
        HasSym_Cell_list = []
        NoSym_Cell_list = []
        '''从相邻小区表中获得所有相邻小区，并记录在 ncell_dict中'''
        allNCells = self.scellLayer.getFeatures()
        for ncell in allNCells:
            ncell_dict[(ncell['SCell'], ncell['NCell'])] = False

        allNCells = self.scellLayer.getFeatures()
        for ncell in allNCells:
            if ncell_dict.has_key((ncell['SCell'], ncell['NCell'])) and ncell_dict.has_key((ncell['NCell'], ncell['SCell'])):
                HasSym_Cell_list.append(ncell.id())
                ncell_dict[(ncell['SCell'], ncell['NCell'])] = True
                ncell_dict[(ncell['NCell'], ncell['SCell'])] = True
        if len(HasSym_Cell_list) > 0:
            '''清空选择'''
            self.scellLayer.selectAll()
            self.scellLayer.invertSelection()
            '''选中有对称性的相邻小区'''
            self.scellLayer.setSelectedFeatures(HasSym_Cell_list)
            '''反选,获得不存在对称性的相邻小区id'''
            self.scellLayer.invertSelection()
            NoSym_Cells = self.scellLayer.selectedFeatures()
            for NoSym_Cell in NoSym_Cells:
                NoSym_Cell_list.append(NoSym_Cell.id())
            return NoSym_Cell_list
        else:
            return NoSym_Cell_list




    '''计算一个小区的相邻小区个数'''
    def countCell(self, cell_id, count):

        if cell_id != u'' and cell_id != None:
            NCells = self.scellLayer.getFeatures()
            for NCell in NCells:
                if NCell['SCell'] == cell_id:
                    if count.has_key(cell_id):
                        count[cell_id] = count[cell_id] + 1
                    else:
                        count[cell_id] = 1
            return count
        else:
            self.iface.messageBar().pushMessage(u'错误', u'无法计算相邻小区!' , QgsMessageBar.CRITICAL, 3)
            return count



























