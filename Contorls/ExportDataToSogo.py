# -*- coding:utf-8 -*-
'''
导出数据到搜狗地图操作函数
@author: Karwai Kwok
'''

import traceback, codecs, os
from PyQt4.QtGui import QMessageBox
from MyQGIS.gui.Progress import Progess
from MyQGIS.config.EnumType import SogoType
from MyQGIS.Template import SogoSiteTemplate, SogoCellTemplate

def exportDataToSogo(filedir='',type=SogoType.Site, datas=None, parent=None):
    result = False
    try:
        if type == SogoType.Site:
            datafile = codecs.open(os.path.join(filedir, 'site.js'), 'w', 'utf-8')
        else:
            datafile = codecs.open(os.path.join(filedir, 'cell.js'), 'w', 'utf-8')
        outputs = SogoForm(type, datas, parent)
        # 生成JS数据
        (DataRetult, datas) = outputs.createData()
        if DataRetult == True:
            datafile.write(datas)
            datafile.close()
            # 生成主页面
            (indexResult, index) = outputs.createForm()
            if indexResult == True:
                indexfile = codecs.open(os.path.join(filedir, 'index.html'), 'w', 'utf-8')
                indexfile.write(index)
                indexfile.close()
            else:
                return result
            result = True
        else:
            result = False
    except Exception, e:
        raise traceback.format_exc(e)
    finally:
        return result

# 构建搜狗地图html文件主体类
class SogoForm(object):
    # type 要导出的图层（0：基站， 1：小区， 2：基站+小区）
    def __init__(self, type=SogoType.Site, datas=None, parent=None):
        super(SogoForm, self).__init__()
        self.parent = parent
        self.type = type
        if self.type == SogoType.Site:
            self.site_datas = datas[0]
            self.site_points = datas[1]
        elif self.type == SogoType.Cell:
            self.cell_datas = datas[0]
            self.cell_polygons = datas[1]

    # 生成主页面
    def createForm(self):
        try:
            outputs = None
            if self.type == SogoType.Site:
                outputs = SogoSiteTemplate.Head
            elif self.type == SogoType.Cell:
                outputs = SogoCellTemplate.Head
            return (True, outputs)
        except Exception, e:
            QMessageBox.critical(self.parent, u"错误", e)
            return (False, e)

    # 生成JS数据文件
    def createData(self):
        outputs = None
        datas = u''
        if self.type == SogoType.Site:
            # 生成进度条
            total = len(self.site_datas)
            progess = Progess(self.parent, total)
            progess.show()

            for (i, data) in enumerate(self.site_datas):
                datas = datas + u"{SiteName:'" + data[0] + u"',SiteId:'" + data[1] + \
                        u"',lon:" + str(self.site_points[i][0]) + u",lat:" + str(self.site_points[i][1]) + \
                        u"}\n"
                if i != len(self.site_datas)-1:
                    datas = datas + ","
                progess.count()
            outputs = u"var site = [ \n" + datas + u"\n" + u"]\n"

            if outputs != None:
                # print datas
                return (True, outputs)
            else:
                return (False, outputs)

        elif self.type == SogoType.Cell:
            # 小区
            # 生成进度条
            total = len(self.cell_datas)+1
            progess = Progess(self.parent, total)
            progess.show()
            for (i, data) in enumerate(self.cell_datas):
                polygon = u"["
                for (j, point) in enumerate(self.cell_polygons[i]):
                    polygon = polygon + str(point[0]) + u"," + str(point[1])
                    if j != len(self.cell_polygons[i]) - 1:
                        polygon = polygon + u","
                polygon = polygon + u"]"
                datas = datas + u"{CellName:'" + data[0] + u"',CellId:'" + data[1] + \
                        u"',SiteName:'" + data[2] + u"',SiteId:'" + data[3] + \
                        u"',lon:" + str(data[4]) + u",lat:" + str(data[5]) + \
                        u",WCDMA_PSC:'" + str(data[6]) + u"',LTE_PCI:'" + str(data[7]) + \
                        u"',CDMA_PN:'" + str(data[8]) + u"',GSM_BCCH:'" + str(data[9]) + \
                        u"',Azimuth:'" + str(data[10]) + u"',TILT:'" + str(data[11]) + \
                        u"',AntHeigth:'" + str(data[12]) + u"',RNC_BSC:'" + str(data[13]) + \
                        u"', Polygon:" + polygon + u"}\n"
                if i != len(self.cell_datas) - 1:
                    datas = datas + u","
                progess.count()
            outputs = u"var cell = [ \n" + datas + u"\n" + u"]\n"
            progess.count()

            if outputs != None:
                return (True, outputs)
            else:
                return (False, outputs)