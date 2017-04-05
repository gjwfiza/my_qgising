# —*- coding: utf-8 -*-

# -*- coding:utf-8 -*-
'''
所有枚举类型
@author:  Karwai Kwok
'''
from MyQGIS.config import HeadsConfig


# 图层类型
class LayerType:
    SITE = 0
    CELL = 1
    SERVINGCELL = 2
    PLANNINGRESULT = 3
    MERGERESULT = 4


# 导入Excel数据类型
class ImpDateType:
    SITEANDCELL = 0  # 基站小区
    SERVINGCELL = 1  # 相邻小区


# 运营商类型
class Operator:
    YD = u'移动'  # 移动
    LT = u'联通'  # 联通
    DX = u'电信'  # 电信
    TT = u'铁塔'  # 铁塔


# 导入Excel表的列数
class ImpColum:
    SITE_COLUM = len(HeadsConfig.SiteHead)
    CELL_COLUM = len(HeadsConfig.CellHead)
    SERVINGCELL_COLUM = len(HeadsConfig.ServingCellHead)
    ANALY_COLUM = len(HeadsConfig.AnalySiteHeade2)


# Excel模板表格的类型
class ExcelType:
    SITEANDCELL = 0  # 基站和小区
    SERVINGCELL = 1  # 相邻小区
    ANALYSITE = 2  # 基站分析
    PUSHSITE = 3  # 基站推送
    MERGESITE = 4  # 基站合并


# 导出数据类型
class ExportType:
    SITE = 0
    CELL = 1
    SERVINGCELL = 2
    ANALYSITE = 3  # 基站分析
    PUSHSITE = 4  # 基站推送
    MERGESITE = 5  # 基站合并
    PCIPLAN = 6  # PCI规划


# 导出KML文件类型
class KMLType:
    Site = 0  # 基站
    Cell = 1  # 小区
    SiteAndCell = 2  # 基站+小区


# 导出百度地图网页文件类型
class BaiduType:
    Site = 0  # 基站
    Cell = 1  # 小区


# 导出腾讯地图网页文件类型
class TencentType:
    Site = 0  # 基站
    Cell = 1  # 小区


# 导出搜狗地图网页文件类型
class SogoType:
    Site = 0  # 基站
    Cell = 1  # 小区
