# -*- coding:utf-8 -*-
'''
导出数据到百度地图操作函数
@author: Karwai Kwok
'''

from PyQt4.QtGui import QMessageBox
import codecs, os, traceback, urllib2, json
from MyQGIS.config.EnumType import BaiduType
from MyQGIS.gui.Progress import Progess
from MyQGIS.Template.BaiduSiteTemplate import BaiduSiteTemplate
from MyQGIS.Template.BaiduCellTemplate import BaiduCellTemplate

# 百度API密钥
myKey = u'BtvVWRqGfnffNqdqAN7rusTlb2E020C8'

# 导出数据到百度地图执行函数
def exportDataToBaidu(filedir='', key=u"",type=BaiduType.Site, datas=None, parent=None):
    result = False
    try:
        if type == BaiduType.Site:
            datafile = codecs.open(os.path.join(filedir, 'site.js'), 'w', 'utf-8')
        else:
            datafile = codecs.open(os.path.join(filedir, 'cell.js'), 'w', 'utf-8')
        outputs = BaiduForm(key, type, datas, parent)
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
            # 生成街景工具
            (panoResult, pano) = outputs.createPano()
            if indexResult == True:
                if type == BaiduType.Site:
                    panofile = codecs.open(os.path.join(filedir, 'Site Panorama.html'), 'w', 'utf-8')
                elif type == BaiduType.Cell:
                    panofile = codecs.open(os.path.join(filedir, 'Cell Panorama.html'), 'w', 'utf-8')
                else:
                    return result
                panofile.write(pano)
                panofile.close()
            result = True
        else:
            result = False

    except Exception, e:
        raise traceback.format_exc(e)

    finally:
        return result

# 构建百度地图html文件主体类
class BaiduForm(object):
    # type 要导出的图层（0：基站， 1：小区， 2：基站+小区）
    def __init__(self, key=myKey, type=BaiduType.Site, datas=None, parent=None):
        super(BaiduForm, self).__init__()
        self.parent = parent
        self.key = key # 用户的百度地图API密钥
        self.type = type
        if self.type == BaiduType.Site:
            self.site_datas = datas[0]
            self.site_points = datas[1]
        elif self.type == BaiduType.Cell:
            self.cell_datas = datas[0]
            self.cell_points = datas[1]

    # 生成主页面
    def createForm(self):
        try:
            outputs = None
            if self.type == BaiduType.Site:
                baidusite = BaiduSiteTemplate(self.key)
                outputs = baidusite.getHead()
            elif self.type == BaiduType.Cell:
                baiducell = BaiduCellTemplate(self.key)
                outputs = baiducell.getHead()
            return (True, outputs)

        except Exception, e:
            raise traceback.format_exc(e)

    # 生成JS数据文件
    def createData(self):
        outputs = None
        datas = u''
        if self.type == BaiduType.Site:
            # 基站
            # 数据分组，每组最多99
            points = [] # 已经分组的需要转换的点
            bd_points = [] # 已经转换好的点
            total = 0 # 总记录数
            if (len(self.site_datas)%99) > 0:
                groupCount = len(self.site_datas) / 99 + 1
            else:
                groupCount = len(self.site_datas) / 99
            for i in range(groupCount):
                temp = []
                for j in range(99):
                    if total < len(self.site_datas):
                        temp.append(self.site_points[(i*99)+j])
                    total = total + 1
                points.append(temp)
                del temp
            # 生成进度条
            total = len(points) + len(self.site_datas)
            progess = Progess(self.parent, total)
            progess.show()
            # 数据点转换
            for groups in points:
                coords = u''
                for (x, point) in enumerate(groups):
                    coords = coords + str(point[0]) + u"," + str(point[1])
                    if x != len(groups)-1:
                        coords = coords + u";"
                url = u"https://api.map.baidu.com/geoconv/v1/?coords=" + coords \
                      + u"&from=1&to=5&ak=" + self.key
                req = urllib2.Request(url)
                res_data = urllib2.urlopen(req)
                res = res_data.read()
                s = json.loads(res)
                if s[u'status'] != 0:
                    status = s[u'status']
                    if status == 1:
                        print status
                        QMessageBox.critical(self.parent, u"错误", u"坐标转换出现内部错误")
                        return (False, outputs)
                    elif status == 21:
                        print status
                        QMessageBox.critical(self.parent, u"错误", u"坐标转换from非法")
                        return (False, outputs)
                    elif status == 22:
                        print status
                        QMessageBox.critical(self.parent, u"错误", u"坐标转换to非法")
                        return (False, outputs)
                    elif status == 24:
                        print status
                        QMessageBox.critical(self.parent, u"错误", u"坐标转换coords格式非法")
                        return (False, outputs)
                    elif status == 25:
                        print status
                        QMessageBox.critical(self.parent, u"错误", u"坐标转换coords个数非法")
                        return (False, outputs)
                progess.count()
                for i in range(len(groups)):
                     bd_points.append((s[u'result'][i][u'x'], s[u'result'][i][u'y']))

            for (i, data) in enumerate(self.site_datas):
                bd_lon = bd_points[i][0]
                bd_lat = bd_points[i][1]

                datas =  datas + u"{SiteName:'" + data[0] + u"',SiteId:'" + data[1] + \
                        u"',lon:" + str(self.site_points[i][0]) + u",lat:" + str(self.site_points[i][1]) + \
                        u",bd_lon:" + str(bd_lon) + u",bd_lat:" + \
                        str(bd_lat) + u"}\n"
                if i != len(self.site_datas)-1:
                    datas = datas + ","
                progess.count()
            outputs = u"var site = [ \n" + datas + u"\n" + u"]\n"

            if outputs != None:
                return (True, outputs)
            else:
                return (False, outputs)

        elif self.type == BaiduType.Cell:
            # 小区
            # 生成进度条
            total = len(self.cell_datas) + 1
            progess = Progess(self.parent, total)
            progess.show()
            for (i, data) in enumerate(self.cell_datas):
                # 先转换基站的经纬度
                coords = str(data[4]) + u"," + str(data[5]) + u";"

                for (j, point) in enumerate(self.cell_points[i]):
                    #print 8
                    # 数据点转换
                    coords = coords + str(point[0]) + u"," + str(point[1])
                    if j != len(self.cell_points[i])-1:
                        coords = coords + u";"
                url = u"https://api.map.baidu.com/geoconv/v1/?coords=" + coords \
                        + u"&from=1&to=5&ak=" + self.key
                req = urllib2.Request(url)
                res_data = urllib2.urlopen(req)
                res = res_data.read()
                s = json.loads(res) # s[u'result'] 第一个数据为基站经纬度
                if s[u'status'] != 0:
                    status = s[u'status']
                    if status == 1:
                        print u"坐标转换出现内部错误"
                        return (False, outputs)
                    elif status == 21:
                        print u"坐标转换from非法"
                        return (False, outputs)
                    elif status == 22:
                        print u"坐标转换to非法 "
                        return (False, outputs)
                    elif status == 24:
                        print u"坐标转换coords格式非法 "
                        return (False, outputs)
                    elif status == 25:
                        print u"坐标转换coords个数非法，超过限制 "
                        return (False, outputs)
                    else:
                        print status

                polygon = u"["
                bd_lon = u"" # 转换后的基站经度
                bd_lat = u"" # 转换后的基站纬度
                for (m, bd_point) in enumerate(s[u'result']):
                    if m == 0:
                        bd_lon = str(bd_point[u'x'])
                        bd_lat = str(bd_point[u'y'])
                    else:
                        polygon = polygon + str(bd_point[u'x']) + u"," + str(bd_point[u'y'])
                        if m != len(s[u'result'])-1:
                            polygon = polygon + u","
                polygon = polygon + u"]"

                datas =  datas + u"{CellName:'" + data[0] + u"',CellId:'" + data[1] + \
                        u"',SiteName:'" + data[2] + u"',SiteId:'" + data[3] + \
                        u"',lon:" + str(data[4]) + u",lat:" + str(data[5]) + \
                        u",bd_lon:" + bd_lon + u",bd_lat:" + bd_lat + \
                        u",WCDMA_PSC:'" + str(data[6]) + u"',LTE_PCI:'" + str(data[7]) + \
                        u"',CDMA_PN:'" + str(data[8]) + u"',GSM_BCCH:'" + str(data[9]) + \
                        u"',Azimuth:'" + str(data[10]) + u"',TILT:'" + str(data[11]) + \
                        u"',AntHeigth:'" + str(data[12]) + u"',RNC_BSC:'" + str(data[13]) + \
                        u"', Polygon:" + polygon + u"}\n"
                if i != len(self.cell_datas)-1:
                    datas = datas + u","
                progess.count()
            outputs = u"var cell = [ \n" + datas + u"\n" + u"]\n"
            progess.count()

            if outputs != None:
                return (True, outputs)
            else:
                return (False, outputs)

    def createPano(self):
        try:
            outputs = None
            if self.type == BaiduType.Site:
                baidusite = BaiduSiteTemplate(self.key)
                outputs = baidusite.getPano()
            elif self.type == BaiduType.Cell:
                baiducell = BaiduCellTemplate(self.key)
                outputs = baiducell.getPano()
            return (True, outputs)

        except Exception, e:
            raise traceback.format_exc()