# -*- coding:utf-8 -*-
'''
从Excel导入图层数据(原名为ImpDateThread)
@author: Karwai Kwok
'''

import xlrd, traceback, threading, os, pickle
from qgis._core import QgsPoint
from PyQt4.QtGui import QMessageBox
from MyQGIS.config.EnumType import ExcelType
from MyQGIS.config.HeadsConfig import SiteANDCellType, ServingCellType, \
    MergeSiteType, PCIType, AnalySiteType, AnalySiteHeade2, MergeSiteHead, \
    PCIHead1, ServingCellHead
from MyQGIS.Contorls.FileControls import getCellGraphicParam
from MyQGIS.Contorls.GeometryControls import createCircle, createSector
from MyQGIS.Contorls.FeaturesControls import createACellFeature, createASiteFeature, \
    importFeaturesToLayer, createASCellFeature
from MyQGIS.Contorls.LayerControls import getLayerByName
from MyQGIS.gui.Progress import Progess

# 从Excel中获取数据
class GetDataFromExcel(object):
    def __init__(self, fileName, mtype, heads=[]):
        super(GetDataFromExcel, self).__init__()
        self.fileName = fileName
        self.mtype = mtype
        self.heads = heads

    def getData(self):
        mlist = []
        try:
            data = xlrd.open_workbook(unicode(self.fileName))
            tab = data.sheets()[0]  # 仅仅获取表格1
            mrow = tab.nrows  # 获取当前sheet的行数
            mcol = tab.ncols  # 获取当前sheet的列数
            if mrow > 1:
                typelist = []
                if self.__validateHead(tab.row(0)) == False:
                    raise Exception, u'Excel表格式不正确，请新建项目！'

                if self.mtype == ExcelType.SITEANDCELL:
                    typelist = SiteANDCellType
                    # 补全typelist
                    if len(typelist) < len(self.heads):
                        for i in range(len(self.heads) - len(typelist)):
                            typelist.append(str)
                elif self.mtype == ExcelType.SERVINGCELL:
                    typelist = ServingCellType
                elif self.mtype == ExcelType.MERGESITE:
                    typelist = MergeSiteType
                elif self.mtype == ExcelType.PCIPLAN:
                    typelist = PCIType
                else:
                    typelist = AnalySiteType

                for i in range(1, mrow):
                    mrow = tab.row(i)
                    clist = []
                    for j in range(mcol):
                        if type(typelist[j]) == int:
                            typelist[j] = str

                        clist.append(self.__switchType(typelist[j], mrow[j].value))

                    mlist.append(clist)
                    del clist, mrow
            else:
                raise Exception, u'Excel表数据为空！'
        except Exception, e:
            # 发生异常，将异常以信号方式发送出去
            raise traceback.format_exc()

        finally:
            return mlist

    # 数据类型转换
    # @param curType 当前数据类型
    # @param curval 当前数据值
    def __switchType(self, curType, curval):
        val = None
        try:
            if curType == int:
                val = int(curval)
            elif curType == float:
                val = float(curval)
            elif curType == str:
                val = int(curval)
            else:
                val = unicode(curval)
        except Exception:
            val = curval

        return val

    # 判断表头是否与标准一致
    def __validateHead(self, rowHead):
        valihead = []
        isuccess = True
        if self.mtype == ExcelType.SITEANDCELL:
            valihead = self.heads
        elif self.mtype == ExcelType.ANALYSITE:
            valihead = AnalySiteHeade2
        elif self.mtype == ExcelType.MERGESITE:
            valihead = MergeSiteHead
        elif self.mtype == ExcelType.PCIPLAN:
            valihead = PCIHead1
        else:
            valihead = ServingCellHead

        # 如果两个列表的长度不一致，则有错误
        if len(rowHead) != len(valihead):
            print u"长度问题"
            return False

        for (i, mcol) in enumerate(rowHead):
            curhead = u''
            try:
                curhead = str(mcol.value)
            except Exception:
                curhead = mcol.value

            if curhead != valihead[i]:
                isuccess = False
                print curhead
                break
        return isuccess
    
# 导入数据到Layer中
class ImportDataToLayer(object):
    def __init__(self, iface, data_list=[], parent=None):
        super(ImportDataToLayer, self).__init__()
        self.iface = iface
        self.data_list = data_list
        self.parent = parent

    # 导入基站和小区数据到图层中
    def importSiteAndCellData(self):
        cell_features = []
        site_features = []
        site_dict = {}
        try:
            # 先生成小区feature再生成基站feature
            for itm in self.data_list:
                # 创建小区feature
                # 当有小区ID和小区名时才导入信息
                cell_id = itm[2]
                cell_name = itm[3]
                if cell_id and cell_name:
                    cell = []
                    for (index, i) in enumerate(itm):
                        # 小区表中没有站点地址（48）和基站ID2（51）
                        if index not in [48, 51]:
                            cell.append(i)
                    # 获取小区图形设置\
                    setting = self.getCellGraphicParam()
                    if not setting:
                        return
                    # 处理小区图形参数
                    if setting["type"] == 0:
                        # 按运营商
                        operator = itm[18]
                        if operator == u'移动':
                            angle = setting[u"移动"][0]
                            length = setting[u"移动"][1]
                        elif operator == u'联通':
                            angle = setting[u"联通"][0]
                            length = setting[u"联通"][1]
                        elif operator == u'电信':
                            angle = setting[u"电信"][0]
                            length = setting[u"电信"][1]
                        else:
                            angle = setting[u"铁塔"][0]
                            length = setting[u"铁塔"][1]
                    else:
                        # 自定义
                        system = itm[10]
                        frequency = itm[12]
                        # 获取默认设置
                        angle = self.setting[u"默认"][0]
                        length = self.setting[u"默认"][1]
                        # 获取分类
                        case_list = self.setting["case_list"]
                        for (c_system, c_frequency, c_angle, c_length) in case_list:
                            if c_system and (not c_frequency):
                                if system == c_system:
                                    angle = c_angle
                                    length = c_length
                            elif (not c_system) and c_frequency:
                                if frequency == c_frequency:
                                    angle = c_angle
                                    length = c_length
                            elif c_system and c_frequency:
                                if (system == c_system) and (frequency == c_frequency):
                                    angle = c_angle
                                    length = c_length
                    # 根据小区类型生成相应的geometry
                    if itm[5] == u"室分":
                        circle = createCircle(QgsPoint(float(itm[8]), float(itm[9])), length / 2,
                                            self.iface, True, 64)

                        cell_feat = createACellFeature(circle, cell)
                        cell_features.append(cell_feat)
                    else:
                        sector = createSector(QgsPoint(float(itm[8]), float(itm[9])), length, self.iface, True,
                                      itm[7], angle)

                        cell_feat = createACellFeature(sector, cell)
                        cell_features.append(cell_feat)
                # 创建基站feature
                site = [
                    itm[0],  # 基站ID
                    itm[1],  # 基站名
                    itm[6],  # RNC-BSC
                    itm[8],  # 经度
                    itm[9],  # 纬度
                    itm[10],  # 网络制式
                    itm[11],  # 典型环境
                    itm[17],  # 区域
                    itm[18],  # 运营商
                    itm[19],  # 簇
                    itm[20],  # 基站英文名
                    itm[22],  # 基站类型
                    itm[48],  # 站点地址
                    itm[49],  # MCC
                    itm[50],  # MNC
                    itm[51],  # 基站ID2
                    itm[52],  # 话务量
                    itm[53],  # 投诉量
                    itm[54],  # Polygon
                    itm[55]  # 其他
                ]
                site_id = itm[0]
                site_name = itm[1]
                rnc_bsc = itm[6]
                lon = itm[8]
                lat = itm[9]
                site_key = (site_id, site_name, rnc_bsc, lon, lat)
                if site_dict.has_key(site_key):
                    continue
                else:
                    site_dict[site_key] = True
                site_feat = createASiteFeature(QgsPoint(float(itm[8]), float(itm[9])), site)
                site_features.append(site_feat)

            # 导入数据
            siteLayer = getLayerByName(u"基站",self.iface)
            site_result = importFeaturesToLayer(siteLayer, site_features)
            cellLayer = getLayerByName(u"小区", self.iface)
            cell_result = importFeaturesToLayer(cellLayer, cell_features)
            if (site_result is False) or (cell_result is False):
                siteLayer.destroyEditCommand()
                cellLayer.destroyEditCommand()
                return False
            else:
                siteLayer.endEditCommand()
                cellLayer.endEditCommand()
                return True
        except Exception:
            raise Exception, traceback.format_exc()

    # 导入相邻小区数据到图层中
    def importSCellData(self):
        try:
            # 导入相邻小区数据
            features = []
            total = len(self.data_list)
            progess = Progess(self.parent, total, u"数据导入中")
            progess.show()
            for itm in self.data_list:
                feat = createASCellFeature(itm)
                if feat == False:
                    progess.kill()
                    break
                else:
                    features.append(feat)
                    progess.count()
            scellLayer = getLayerByName(u"相邻小区", self.iface)
            res = importFeaturesToLayer(scellLayer, features)
            if res is False:
                scellLayer.destroyEditCommand()
                return False
            else:
                scellLayer.endEditCommand()  # 事务提交
                return True
        except Exception:
            raise Exception, traceback.format_exc()

    # 设置小区图形参数
    def getCellGraphicParam(self):
        # 从项目路径中获取图形参数
        setting_dict = getCellGraphicParam(self.iface)
        if not setting_dict:
            # 若图形参数为空
            QMessageBox.critical(self.parent, u"错误", u"项目路径中找不到参数设置")
            return None
        else:
            return setting_dict