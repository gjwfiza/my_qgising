# -*- coding:utf-8 -*-
'''
导出数据到腾讯地图操作函数
@author: Karwai Kwok
'''

import traceback, codecs, os, urllib2, time, json
from PyQt4.QtGui import QMessageBox
from MyQGIS.gui.Progress import Progess
from MyQGIS.config.EnumType import TencentType
from MyQGIS.Template.TencentSiteTemplate import TencentSiteTemplate
from MyQGIS.Template.TencentCellTemplate import TencentCellTemplate

# 腾讯API密钥
myKey = u'G2TBZ-VWXR5-XKRIU-QOTEH-LWV4Z-R3FSW'
myKey2 = u"4V3BZ-SOKHU-EVAVO-4XNJR-GNNFQ-MXF3M" # 备用key

def exportDataToTencent(filedir='', key=u"", type=TencentType.Site, datas=None, parent=None):
    result = False
    try:
        if type == TencentType.Site:
            datafile = codecs.open(os.path.join(filedir, 'site.js'), 'w', 'utf-8')
        else:
            datafile = codecs.open(os.path.join(filedir, 'cell.js'), 'w', 'utf-8')
        outputs = TencentForm(key, type, datas, parent)
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
                if type == TencentType.Site:
                    panofile = codecs.open(os.path.join(filedir, 'Site Panorama.html'), 'w', 'utf-8')
                elif type == TencentType.Cell:
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

# 构建腾讯地图html文件主体类
class TencentForm(object):
    # type 要导出的图层（0：基站， 1：小区， 2：基站+小区）
    def __init__(self, key=myKey2, type=TencentType.Site, datas=None, parent=None):
        super(TencentForm, self).__init__()
        self.parent = parent
        self.key = key # 用户的腾讯API密钥
        self.type = type
        if self.type == TencentType.Site:
            self.site_datas = datas[0]
            self.site_points = datas[1]
        elif self.type == TencentType.Cell:
            self.cell_datas = datas[0]
            self.cell_points = datas[1]

    # 生成主页面
    def createForm(self):
        try:
            outputs = None
            if self.type == TencentType.Site:
                tencentsite = TencentSiteTemplate(self.key)
                outputs = tencentsite.getHead()
            elif self.type == TencentType.Cell:
                tencentcell = TencentCellTemplate(self.key)
                outputs = tencentcell.getHead()
            return (True, outputs)

        except Exception, e:
            QMessageBox.critical(self.parent, u"错误", e)
            return (False, e)

    # 生成JS数据文件
    def createData(self):
        outputs = None
        datas = u''
        if self.type == TencentType.Site:
            # 基站
            # 数据分组，每组最多30
            points = [] # 已经分组的需要转换的点
            qq_points = [] # 已经转换好的点
            total = 0 # 总记录数
            if (len(self.site_datas)%30) > 0:
                groupCount = len(self.site_datas) / 30 + 1
            else:
                groupCount = len(self.site_datas) / 30
            for i in range(groupCount):
                temp = []
                for j in range(30):
                    if total < len(self.site_datas):
                        temp.append(self.site_points[(i*30)+j])
                    total = total + 1
                points.append(temp)
                del temp
            # 生成进度条
            total = len(points) + len(self.site_datas)
            progess = Progess(self.parent, total)
            progess.show()
            # 数据点转换
            for groups in points:
                locations = u''
                for (x, point) in enumerate(groups):
                    locations = locations + str(point[1]) + u"," + str(point[0]) # 纬度在前，经度在后
                    if x != len(groups)-1:
                        locations = locations + u";"
                url = u"http://apis.map.qq.com/ws/coord/v1/translate?locations=" + locations \
                      + u"&type=1&key=" + self.key
                req = urllib2.Request(url)
                time.sleep(0.4) # 0.4s发送一次请求
                res_data = urllib2.urlopen(req)
                res = res_data.read()
                s = json.loads(res)
                if s[u'status'] != 0:
                    message = s[u'message']
                    print s[u'status']
                    print message
                    QMessageBox(self.parent, u"错误", u"错误代码："+ str(s[u'status']) + u"\n" + s[u'message'])
                    progess.kill()
                    return (False, outputs)
                else:
                    progess.count()

                for i in range(len(groups)):
                     qq_points.append((s[u'locations'][i][u'lng'], s[u'locations'][i][u'lat']))

             # 数据转换（用自定义算法）
            total = len(self.site_datas)
            progess = Progess(self.parent, total)
            progess.show()

            for (i, data) in enumerate(self.site_datas):
                qq_lon = qq_points[i][0]
                qq_lat = qq_points[i][1]

                datas =  datas + u"{SiteName:'" + data[0] + u"',SiteId:'" + data[1] + \
                        u"',lon:" + str(self.site_points[i][0]) + u",lat:" + str(self.site_points[i][1]) + \
                        u",qq_lon:" + str(qq_lon) + u",qq_lat:" + \
                        str(qq_lat) + u"}\n"
                if i != len(self.site_datas) - 1:
                    datas = datas + ","
                progess.count()
            outputs = u"var site = [ \n" + datas + u"\n" + u"]\n"

            if outputs != None:
                #print datas
                return (True, outputs)
            else:
                return (False, outputs)

        elif self.type == TencentType.Cell:
            # 小区
            # 生成进度条
            total = len(self.cell_datas) + 1
            progess = Progess(self.parent, total)
            progess.show()
            for (i, data) in enumerate(self.cell_datas):
                # 先转换基站的经纬度(纬度在前，经度在后)
                locations = str(data[5]) + u"," + str(data[4]) + u";"
                for (j, point) in enumerate(self.cell_points[i]):
                    # 数据点转换(纬度在前，经度在后)
                    if len(self.cell_points[i]) > 40:
                        # 如果小区是圆形则只转换基站坐标
                        locations = locations + str(data[5]) + u"," + str(data[4])
                        break
                    else:
                        locations = locations + str(point[1]) + u"," + str(point[0])
                        if j != len(self.cell_points[i])-1:
                            locations = locations + u";"
                url = u"http://apis.map.qq.com/ws/coord/v1/translate?locations=" + locations \
                      + u"&type=1&key=" + self.key
                req = urllib2.Request(url)
                time.sleep(0.4) # 0.4s发送一次请求
                res_data = urllib2.urlopen(req)
                res = res_data.read()
                s = json.loads(res) # s[u'locations'] 第一个数据为基站经纬度
                if s[u'status'] != 0:
                    print s[u'status']
                    message = s[u'message']
                    print message
                    QMessageBox(self.parent, u"错误", u"错误代码：" + str(s[u'status']) + u"\n" + s[u'message'])
                    progess.kill()
                    return (False, outputs)
                else:
                    polygon = u"["
                    qq_lon = u"" # 转换后的基站经度
                    qq_lat = u"" # 转换后的基站纬度
                    for (m, qq_point) in enumerate(s[u'locations']):
                        if m == 0:
                            qq_lon = str(qq_point[u'lng'])
                            qq_lat = str(qq_point[u'lat'])
                        else:
                            polygon = polygon + str(qq_point[u'lng']) + u"," + str(qq_point[u'lat'])
                            if m != len(s[u'locations'])-1:
                                polygon = polygon + u","
                    polygon = polygon + u"]"

                    datas =  datas + u"{CellName:'" + data[0] + u"',CellId:'" + data[1] + \
                            u"',SiteName:'" + data[2] + u"',SiteId:'" + data[3] + \
                            u"',lon:" + str(data[4]) + u",lat:" + str(data[5]) + \
                            u",qq_lon:" + qq_lon + u",qq_lat:" + qq_lat + \
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
                #print datas
                return (True, outputs)
            else:
                return (False, outputs)

    def createPano(self):
        try:
            outputs = None
            if self.type == TencentType.Site:
                tencentsite = TencentSiteTemplate(self.key)
                outputs = tencentsite.getPano()
            elif self.type == TencentType.Cell:
                tencentcell = TencentCellTemplate(self.key)
                outputs = tencentcell.getPano()
            return (True, outputs)

        except Exception, e:
            raise traceback.format_exc()