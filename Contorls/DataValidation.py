# -*- coding: utf-8 -*-
'''
数据验证函数
@author: Karwai Kwok
'''

from MyQGIS.config.EnumType import ImpDateType
from MyQGIS.config.HeadsConfig import SiteANDCellHead, ServingCellHead, ImpExcelName

# 数据校验
def checkDataByDataType(data_list=[], dataType=ImpDateType.SITEANDCELL):
    warnInfo_list = [] # 保存错误信息
    if dataType == ImpDateType.SITEANDCELL:
        check_dict = {}  # 用于检查数据是否重复 (key:(SiteID,小区ID,RNCBSC,方向角,经度), value:index)
        for (index, rowlist) in enumerate(data_list):
            # 先检查数据是否有重复
            site_id = rowlist[0]
            cell_id = rowlist[2]
            rnc_bsc = rowlist[6]
            azimuth = rowlist[7]
            lon = rowlist[8]
            check_flag = (site_id, cell_id, rnc_bsc, azimuth, lon)
            if not check_dict.has_key(check_flag):
                check_dict[check_flag] = index
            else:
                warn_info = {}
                warn_info['col'] = 0
                warn_info['row'] = index
                warn_info['msg'] = u"第" + str(index + 1) + u"行与第" \
                                   + str(check_dict[check_flag] + 1) + u"行数据重复！"
                warn_info['item'] = rowlist
                warnInfo_list.append(warn_info)
                del warn_info
                # 基站名（0）、基站ID（1）、RNC-BSC（6）、经度(8)、纬度(9)、网络制式(10)、
                # 典型环境(11)、运营商(18) 必填
            for j in [0, 1, 6, 8, 9, 10, 11, 18]:
                valres = checkIsNull(SiteANDCellHead[j], j, index, rowlist[j], rowlist)
                if valres != None:
                    # 如果出现空值
                    warnInfo_list.append(valres)
            # 检验经度填写是否正确（无“°”或者“o”）
            lon = rowlist[8]
            if not isinstance(lon, basestring):
                lon = str(lon)
            if (u"°" in lon) or (u"o" in lon):
                warn_info = {}
                warn_info['col'] = 8  # lon列
                warn_info['row'] = index
                # siteid_dict[SiteId]+1 是为了对齐表格行数
                warn_info['msg'] = u"第" + str(index + 1) + u"行经度填写格式不正确"
                warn_info['item'] = rowlist
                warnInfo_list.append(warn_info)
                del warn_info
            # 检查经度范围是否正确
            if (float(lon) < -180) or (float(lon) > 180):
                print float(lon)
                warn_info = {}
                warn_info['col'] = 8  # lon列
                warn_info['row'] = index
                # siteid_dict[SiteId]+1 是为了对齐表格行数
                warn_info['msg'] = u"第" + str(index + 1) + u"行经度超出范围"
                warn_info['item'] = rowlist
                warnInfo_list.append(warn_info)
                del warn_info
            # 检验纬度填写是否正确（无“°”或者“o”）
            lat = rowlist[9]
            if not isinstance(lat, basestring):
                lat = str(lat)
            if (u"°" in lat) or (u"o" in lat):
                warn_info = {}
                warn_info['col'] = 9  # lat列
                warn_info['row'] = index
                warn_info['msg'] = u"第" + str(index + 1) + u"行纬度填写格式不正确"
                warn_info['item'] = rowlist
                warnInfo_list.append(warn_info)
                del warn_info
            # 检查纬度范围是否正确
            if (-90 > float(lat)) or (float(lat) > 90):
                warn_info = {}
                warn_info['col'] = 9  # lat列
                warn_info['row'] = index
                warn_info['msg'] = u"第" + str(index + 1) + u"行纬度超出范围"
                warn_info['item'] = rowlist
                warnInfo_list.append(warn_info)
                del warn_info

            # 当小区ID或小区名存在判断是否小区关键字段非空
            # 小区ID(2)、小区名(3)、扇区ID(4)、小区类型(5)、方向角(7)、频段(12)
            cell_id = rowlist[2]
            cell_name = rowlist[3]
            if (not cell_id) and (not cell_name):
                continue
            else:
                for j in [2, 3, 4, 5, 7, 12]:
                    valres = checkIsNull(SiteANDCellHead[j], j, index, rowlist[j], rowlist)
                    if valres != None:
                        # 如果出现空值
                        warnInfo_list.append(valres)
                # 判断角度填写是否规范
                azimuth_range = [i for i in range(0, 361)]
                azimuth = rowlist[7]  # 角度
                if azimuth not in azimuth_range:
                    warn_info = {}
                    warn_info['col'] = 7  # azimuth 列
                    warn_info['row'] = index
                    warn_info['msg'] = u"Azimuth必须为整数0~360"
                    warn_info['item'] = rowlist
                    warnInfo_list.append(warn_info)
                    del warn_info

    # 相邻小区数据验证
    elif dataType == ImpDateType.SERVINGCELL:
        for (vi, vrowlist) in enumerate(data_list):
            for (vj, vcol) in enumerate(vrowlist):
                if vj < 2:  # 非空验证
                    vvalres = checkIsNull(ServingCellHead[vj], vj, vi, vcol, vrowlist)
                    if vvalres != None:
                        warnInfo_list.append(vvalres)

    return warnInfo_list

def checkIsNull(name, col, row, itm, rowitm):
    if itm is None or itm == '':
        tmpMap = {}
        tmpMap['col'] = col
        tmpMap['row'] = row
        tmpMap['msg'] = unicode(name) + u'不能为空'
        tmpMap['item'] = rowitm
        return tmpMap
    else:
        return None


