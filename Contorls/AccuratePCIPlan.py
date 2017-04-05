# -*-coding:utf-8 -*-
'''
基于蚂蚁算法的PCI规划
@author: Karwai Kwok
'''

import threading, time, random, traceback
import numpy as np
from fractions import Fraction
from qgis._core import QgsVectorDataProvider, QgsFeature, QgsGeometry, QgsDistanceArea, QgsPoint
from PyQt4.QtCore import QObject, QThread
from MyQGIS.gui.Progress import Progess
from MyQGIS.Contorls.LayerControls import getLayerByName
from MyQGIS.Contorls.FeaturesControls import modifyFeatures

# PCI范围
PCI_range = [i for i in xrange(504)]
# SSS范围
SSS_range = [i for i in xrange(168)]

d = QgsDistanceArea()

# 关联小区表与相邻小区表数据
def connectDatas(iface):
    cell_dict = {}
    ncell_set = set()
    cellLayer = getLayerByName(u"小区", iface)
    ncellLayer = getLayerByName(u"相邻小区", iface)
    cells = cellLayer.selectedFeatures()
    ncells = ncellLayer.getFeatures()
    for cell in cells:
        key = cell[u'RNC-BSC'] + '_' + cell[u'基站ID'] + '_' + cell[u'小区ID']
        cell_dict[key] = cell.id()
    for ncell in ncells:
        ncell0 = ncell["SCell"]
        ncell1 = ncell["NCell"]
        if cell_dict.has_key(ncell0) and cell_dict.has_key(ncell1):
            cell0 = cell_dict[ncell0]
            cell1 = cell_dict[ncell1]
            ncell_set.add((cell0, cell1))
    return ncell_set

# 评估PCI方案
def Evaluate(cell_list, cells_distance_dict, ncell_set, pci_plan):
    # N为小区总数
    # p0、p1、p2、p3 为评价参数的权重
    # u为小区间是否为邻区关系
    # s,b,h,r分别为小区间是否存在PCI冲突、PCI混淆、模三相等、小区m1/m2相等， 是为1，否为0
    # d 表示小区间距离是否在2km以内
    p0 = 2
    p1 = 2
    p2 = 1
    p3 = 1
    p4 = 2
    c = 0
    relation_dict = getCellsRelation(ncell_set, cell_list, cells_distance_dict, pci_plan)
    for cell_id0 in cell_list:
        for cell_id1 in cell_list:
            if cell_id0 == cell_id1:
                continue
            if not relation_dict.has_key((cell_id0,cell_id1)):
                continue
            cells_relationship = relation_dict[(cell_id0,cell_id1)]
            u = cells_relationship["u"]
            s = cells_relationship["s"]
            b = cells_relationship["b"]
            h = cells_relationship["h"]
            r = cells_relationship["r"]
            d = cells_relationship["d"]
            del cells_relationship
            c = c + u * (p0 * s + p1 * b + p2 * h + p3 * r) + (p4 * d)
    return c

# 根据PCI计算相关参数
def getPCIParm(pci):
    if type(pci) != int:
        pci = int(pci)
    pss = pci % 3
    sss = (pci - pss) / 3
    qd = int(sss / 30)
    q = int((sss + qd * (qd + 1) / 2) / 30)
    md = sss + q * (q + 1) / 2
    m0 = md % 31
    m1 = m0 + int(md / 31) + 1 % 31
    PCI_Parm = {}
    PCI_Parm["PSS"] = pss
    PCI_Parm["SSS"] = sss
    PCI_Parm["qd"] = qd
    PCI_Parm["q"] = q
    PCI_Parm["md"] = md
    PCI_Parm["m0"] = m0
    PCI_Parm["m1"] = m1
    return PCI_Parm

# 获取小区间的关系
def getCellsRelation(ncell_set=set(), cell_list=[], cells_distance_dict={}, pci_plan={}):
    relation_dict = {}
    for cell_id0 in cell_list:
        for cell_id1 in cell_list:
            if cell_id0 == cell_id1:
                continue
            # u为小区间是否为邻区关系
            # s,b,h,r分别为小区间是否存在PCI冲突、PCI混淆、模三相等、小区m1/m2相等， 是为1，否为0
            # 默认所有参数都是0
            relation_dict[(cell_id0, cell_id1)] = {"u": 0, "s": 0, "b": 0, "h": 0, "r": 0, "d": 0}
            # 判断小区间距离是否在2km以内
            if cells_distance_dict.has_key((cell_id0, cell_id1)):
                if cells_distance_dict[(cell_id0, cell_id1)] < 2000:
                    relation_dict[(cell_id0, cell_id1)]["d"] = 1
            # 判断是否为邻区
            if (cell_id0, cell_id1) in ncell_set:
                relation_dict[(cell_id0, cell_id1)]["u"] = 1
            else:
                return relation_dict
            # 判断PCI相关关系
            if not pci_plan.has_key(cell_id0) or not pci_plan.has_key(cell_id1):
                return relation_dict
            else:
                pci0 = pci_plan[cell_id0]
                pci1 = pci_plan[cell_id1]
            # 判断PCI是否冲突
            if pci0 == pci1:
                relation_dict["s"] = 1
            # 判断模三是否相等
            if (pci0 % 3) == (pci1 % 3):
                relation_dict[(cell_id0, cell_id1)]["h"] = 1
            # 判断m1/m2是否相等
            pci_parm_0 = getPCIParm(pci0)
            pci_parm_1 = getPCIParm(pci1)
            if (pci_parm_0["m0"] / pci_parm_0["m1"]) == (pci_parm_1["m0"] / pci_parm_1["m1"]):
                relation_dict[(cell_id0, cell_id1)]["r"] = 1
            del pci_parm_0, pci_parm_1
            # 判断PCI是否混淆
            # 获取cell0和cell1的邻区
            ncell_set0 = set()
            ncell_set1 = set()
            for scell_id, ncell_id in ncell_set:
                if scell_id == cell_id0:
                    ncell_set0.add((ncell_id))
                elif scell_id == cell_id1:
                    ncell_set1.add(ncell_id)
            # 检查邻区的cell_id不同的情况下是否存在PCI相同
            not_coincide = (ncell_set0 | ncell_set1) - (ncell_set0 & ncell_set1)
            not_coincide_pci = set()
            for cell_id in not_coincide:
                pci = pci_plan[cell_id]
                if pci in not_coincide:
                    relation_dict[(cell_id0, cell_id1)]["b"] = 1
                    break
                else:
                    not_coincide_pci.add(pci)
            del not_coincide, not_coincide_pci
    return relation_dict

# 蚂蚁线程
class Ant(threading.Thread, QThread):
    def __init__(self, ant_index, start_index=0, site_id_list=[], site_dict={},
                 cells_list=[], cells_distance_dict={}, ncell_set=set(), probability_dict={}):
        # start_index 蚂蚁起始小区
        super(Ant, self).__init__()
        self.ant_index = ant_index
        self.start_index = start_index
        self.site_id_list = site_id_list # 基站遍历顺序 （[[cell0, cell1,cell2]]）小区顺序按方向角从小到大排列
        self.site_dict = site_dict
        self.cells_list = cells_list
        self.cells_distance_dict = cells_distance_dict
        self.probability_dict = probability_dict # 当前的概率字典
        self.done_flag = False # 线程是否完成标志
        self.ncell_set = ncell_set

    def run(self):
        super(Ant, self).run()
        self.sss_plan = {}  # 该蚂蚁的SSS分配方案
        self.pci_plan = {}  # 该蚂蚁的PCI分配方案
        try:
            # 按照遍历顺序和概率生成SSS分配方案
            for site_id in self.site_id_list[self.start_index:]:
                sss = self.getSSS(self.probability_dict[site_id])
                self.sss_plan[site_id] = sss
            for site_id in self.site_id_list[0:self.start_index]:
                sss = self.getSSS(self.probability_dict[site_id])
                self.sss_plan[site_id] = sss
            # 根据SSS分配方案生成PCI分配方案
            # 同基站的小区按方向角大小顺序分配PSS
            for (site_id, sss) in self.sss_plan.iteritems():
                for (pss,cell_id) in enumerate(self.site_dict[site_id]):
                    self.pci_plan[cell_id] = 3*sss + pss
            # 计算此分配方案的干扰函数值c_k
            self.c_k = Evaluate(self.cells_list,self.cells_distance_dict,self.ncell_set,self.pci_plan)
        except Exception,e:
            raise traceback.format_exc()
        finally:
            self.done_flag = True

    # 获取SSS分配结果(sss_dict)
    def returnSSSPlan(self):
        if self.done_flag:
            return self.sss_plan
        else:
            raise u"线程未执行完成"

    # 获取pci分配结果(pci_dict)
    def returnPCIPlan(self):
        if self.done_flag:
            return self.pci_plan
        else:
            raise u"线程未执行完成"

    # 返回此分配方案的干扰函数值(c_k)
    def return_c_k(self):
        if self.done_flag:
            return self.c_k
        else:
            raise u"线程未执行完成"

    # 返回蚂蚁标识
    def returnAntIndex(self):
        return self.ant_index

    # 根据概率列表随机生成一个SSS
    def getSSS(self, probability_array):
        x = random.uniform(0, 1)
        cumulative_probability = 0.0
        for SSS, P in zip(SSS_range, probability_array):
            cumulative_probability += P
            if x < cumulative_probability: break
        return SSS

# 根据蚂蚁算法进行PCI配置
class AccuratePCIThread(QObject):
    def __init__(self, itermax, iface, parent=None):
        super(AccuratePCIThread, self).__init__()
        self.iface = iface
        self.parent = parent
        self.itermax = itermax # 最大循环次数
        (self.selectedCells_list, self.selectedCells_dict) = self.getSelectedCells() # 以cell.id（）为key
        (self.selectedSites_id_list, self.selectedSites_dict) = self.CellsSortBySite()
        self.cellsDistance_dict = self.getCellsDistance(self.selectedCells_dict)
        # 关联小区与邻区数据
        self.ncell_set = connectDatas(self.iface)
        self.num_cell = len(self.selectedCells_list)
        self.num_site = len(self.selectedSites_id_list)
        random.seed(self.num_site)
        #　参数
        self.alpha = 0.5
        self.rhp = 0.7
        self.Q = 1
        # 初始信息素字典
        self.pheromone_dict= {}
        self.delta_pheromone_dict = {}
        for site_id in self.selectedSites_id_list:
            self.pheromone_dict[site_id] = np.ones(168)
            self.delta_pheromone_dict[site_id] = np.zeros(168)

    # 返回选中的小区列表(key:cell.id())
    def getSelectedCells(self):
        cellLayer = getLayerByName(u"小区", self.iface)
        selectedCells_list = []
        selectedCells_dict = {}
        for cell in cellLayer.selectedFeatures():
            selectedCells_list.append(cell.id())
            selectedCells_dict[cell.id()] = cell
        return (selectedCells_list, selectedCells_dict)

    # 返回选中的小区所属基站id列表
    # 和已按方向角大小排序并以基站ID分类的小区字典

    def CellsSortBySite(self):
        cellLayer = getLayerByName(u"小区", self.iface)
        selectedSites_id_list = []
        selectedSites_dict = {}
        # 先将小区按基站ID分类
        for cell in cellLayer.selectedFeatures():
            site_id = cell[u"基站ID"]
            if not selectedSites_dict.has_key(site_id):
                temp_list = [cell]
                selectedSites_dict[site_id] = temp_list
                del temp_list
            else:
                temp_list = selectedSites_dict[site_id]
                temp_list.append(cell)
                selectedSites_dict[site_id] = temp_list
                del temp_list
        # 按方向角大小从小到大排序，并将字典列表化
        for (site_id, cells_list) in selectedSites_dict.iteritems():
            selectedSites_id_list.append(site_id)
            sorted_cells_list = sorted(cells_list, key=lambda f:f[u"方向角"], reverse=False)
            sorted_cell_id_list = []
            for cell in sorted_cells_list:
                sorted_cell_id_list.append(cell.id())
            selectedSites_dict[site_id] = sorted_cell_id_list
        return (selectedSites_id_list, selectedSites_dict)

    # 返回保存小区与小区间距离的dict (key: (cell0.id(), cell1.id()), value: distance)
    def getCellsDistance(self, cell_dict={}):
        cells_distance_dict = {}
        for (cell_id0, cell0) in cell_dict.iteritems():
            for (cell_id1, cell1) in cell_dict.iteritems():
                if cell_id0 == cell_id1:
                    continue
                cell_point0 = QgsPoint(cell0[u"经度"], cell0[u"纬度"])
                cell_point1 = QgsPoint(cell1[u"经度"], cell1[u"纬度"])
                distance = d.convertMeasurement(d.measureLine(cell_point0, cell_point1), 2, 0, False)[0]
                cells_distance_dict[(cell_id0, cell_id1)] = distance
        return cells_distance_dict

    # 返回当前的SSS概率字典(key: site_id, value: SSS概率numpy.array)
    def getProbabilityDict(self):
        probability_dict = {}
        for site_id in self.selectedSites_id_list:
            probability_list = []
            total_pheromone = sum(self.pheromone_dict[site_id])
            for sss in xrange(168):
                probability = Fraction(self.pheromone_dict[site_id][sss]) / Fraction(total_pheromone)
                probability_list.append(probability)
            probability_dict[site_id] = np.array(probability_list)
        return probability_dict

    def run(self):
        start_time = time.clock()
        #num_ant = len(self.selectedCells_list) # 蚂蚁数为选中的小区数只
        num_ant = self.num_site  # 蚂蚁数为选中的基站数只
        # 迭代itermax次
        best_plan = {} # 保存最佳的PCI分配方案
        progress_len = self.itermax
        progress = Progess(self.parent, progress_len)
        progress.show()
        for iter in xrange(self.itermax):
            ant_threads = [] # 保存蚂蚁线程
            sss_plan = {} # # 保存此次循环所有蚂蚁的SSS分配结果 (key: ant_index value: sss_plan)
            pci_plan = {} # 保存此次循环所有蚂蚁的PCI分配结果 (key: ant_index value: pci_plan)
            c_dict = {} # 保存此次循环所有蚂蚁的PCI分配方案的干扰函数值(key: ant_index, value: c_k)
            # 获取当前概率字典
            probability_dict = self.getProbabilityDict()
            # 创建num_ant只蚂蚁
            for k in xrange(num_ant):
                # 随机产生起始小区
                start_index = random.randint(0, self.num_site)
                ant = Ant(k, start_index, self.selectedSites_id_list, self.selectedSites_dict,
                          self.selectedCells_list, self.cellsDistance_dict, self.ncell_set, probability_dict)
                ant_threads.append(ant)
            # 开启线程
            for ant in ant_threads:
                ant.setDaemon(True)
                ant.start()
            # 等待线程完成
            for ant in ant_threads:
                ant.join()
                ant_index = ant.returnAntIndex()
                ant_pci_plan = ant.returnPCIPlan()
                ant_sss_plan = ant.returnSSSPlan()
                pci_plan[ant_index] = ant_pci_plan
                sss_plan[ant_index] = ant_sss_plan
                c_k =  ant.return_c_k()
                c_dict[ant_index] = c_k
            #print c_dict
            # 更新信息素
            # 此次循环信息素增量
            delta_pheromone_dict = self.delta_pheromone_dict.copy()
            for site_id in self.selectedSites_id_list:
                for k in xrange(num_ant):
                    sss = sss_plan[k][site_id]
                    if c_dict[k] == 0:
                        delta_pheromone_dict[site_id][sss] += 0
                    else:
                        delta_pheromone_dict[site_id][sss] += self.Q / c_dict[k]
                self.pheromone_dict[site_id] = self.pheromone_dict[site_id]*(1-self.rhp) + delta_pheromone_dict[site_id]
            (min_c_index, min_c) = sorted(c_dict.iteritems(), key=lambda d:d[1], reverse=False)[0]
            best_plan = pci_plan[min_c_index]
            # 更新进度
            progress.count()
        # 提交PCI方案
        cellLayer = getLayerByName(u"小区", self.iface)
        update_dict = {}
        pci_field_index = cellLayer.fieldNameIndex('PCI')
        for (cell_id, pci) in best_plan.iteritems():
            update_dict[cell_id] = {pci_field_index: pci}
        modifyFeatures(cellLayer, update_dict)
        end_time = time.clock()
        print "total time:" + str(end_time - start_time)
        return True

