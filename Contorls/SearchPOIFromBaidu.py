# -*- coding: utf-8 -*-
'''
从百度地图中抓取地理信息
@author: Karwai Kwok
'''
import urllib, urllib2, json, threading, os, math, traceback
from PyQt4.QtCore import QVariant
from PyQt4.QtGui import QMessageBox
from qgis._core import QgsMapLayerRegistry, QgsVectorLayer, QgsVectorFileWriter, \
    QGis, QgsFields, QgsField, QgsPoint
from MyQGIS.gui.Progress import Progess
from MyQGIS.Contorls.FileControls import getProjectDir
from MyQGIS.Contorls.FeaturesControls import createABasicPointFeature, importFeaturesToLayer, \
    delFeatures

# 从百度地图中抓取地理信息执行主体类
class SearchPOIFromBaidu(object):
    mutex = threading.Condition()
    def __init__(self, iface, keywords=[], searchRange=tuple, searchType=0, selectedLayer=object, density=0.1, save_layer_name=u"",
                 ak=u"BtvVWRqGfnffNqdqAN7rusTlb2E020C8", parent=None):
        super(SearchPOIFromBaidu, self).__init__()
        self.iface = iface
        self.parent = parent
        self.ak = ak
        self.baseUrl = u"http://api.map.baidu.com/place/v2/search";

        self.keywords = keywords
        self.searchRange = searchRange
        self.density = density
        self.searchType = searchType
        self.selectedLayer = selectedLayer
        self.save_layer_name = save_layer_name

    def createURL(self, bottom_left_point, upper_right_point, page_size="20", page_num="0"):
        # 关键字
        url = self.baseUrl + u"?query="
        for (i, keyword) in enumerate(self.keywords):
            url += urllib.quote(keyword.encode('utf8'))
            if (len(self.keywords) > 1) and (i <= len(self.keywords) - 1):
                url += "$"
        # 检索结果详细程度
        url += "&scope=2"
        # 搜索区域
        url += "&bounds="
        if not bottom_left_point or not upper_right_point:
            bottom_left_point = self.searchRange[0]
            upper_right_point = self.searchRange[1]
        url += str(bottom_left_point[1]) + "," + str(bottom_left_point[0]) + "," + \
               str(upper_right_point[1]) + "," + str(upper_right_point[0])
        # 请求参数中坐标的类型
        url += "&coord_type=1"
        # 范围记录数量和分页页码
        url += "&page_size=" + str(page_size) + "&page_num=" + str(page_num)
        # 返回格式和ak码
        url += "&output=json&ak=" + self.ak
        return url

    # 根据数据生成结果图层
    def createLayer(self, datas):
        layerName = self.save_layer_name  # 图层名称
        layerType = QGis.WKBPoint  # 图层类型
        shapPath = os.path.join(getProjectDir(self.iface), layerName + u".shp")
        # 创建图层字段
        field_names = [u"名称", u"类别", u"地址", u"经度", u"纬度"]
        field_types = [QVariant.String, QVariant.String, QVariant.String, QVariant.Double, QVariant.Double]
        field_lengs = [50,50,100,20,20]
        field_precs = [0,0,0,7,7]
        fields = QgsFields()
        for (i, itm) in enumerate(field_names):
            cuType = field_types[i]
            if cuType == QVariant.Int:
                mtype = 'Integer'
            elif cuType == QVariant.Double:
                mtype = 'Real'
            else:
                mtype = 'String'
            field = QgsField(itm, cuType, mtype, field_lengs[i], field_precs[i])
            fields.append(field)
        # 创建出Shap文件
        # 数据源编码模式为GBK2312（否则中文字段会乱码）
        wr = QgsVectorFileWriter(shapPath, "GBK2312", fields, layerType, None, "ESRI Shapefile")
        # 如果保存的时候没有错误
        if wr.hasError() == QgsVectorFileWriter.NoError:
            pass
        else:
            print wr.hasError()
            raise Exception, wr.errorMessage()  # 发生错误，抛出异常交给外面的方法处理异常
        del wr  # 使添加的字段生效
        layer = QgsVectorLayer(shapPath, layerName, 'ogr') # 新生成的搜索结果图层
        QgsMapLayerRegistry.instance().addMapLayer(layer)
        # 更新图层
        self.iface.actionDraw().trigger()
        # 写入数据
        features_list = []
        selected_polygons = []
        for polygon in self.selectedLayer.selectedFeatures():
            selected_polygons.append(polygon)
        for data in datas:
            feature = createABasicPointFeature(QgsPoint(float(data[3]),float(data[4])), data)
            point_gemo = feature.geometry()
            if self.searchType == 0:
                for polygon in selected_polygons:
                    if point_gemo.intersects(polygon.geometry()):
                        features_list.append(feature)
                        break
            else:
                features_list.append(feature)
        # 把新建的features导入图层
        result = importFeaturesToLayer(layer, features_list)
        if result:
            # 更新图层
            self.iface.actionDraw().trigger()
            return layer
        else:
            return None

    # 百度坐标转GPS坐标
    def geoconv(self, coord_list=[]):
        result_coord_list = [] # 转换结果
        # 先将坐标分组，一组最多100个
        bd_coord_list = []
        for i in range(0,len(coord_list),100):
            bd_coord_list.append(coord_list[i:i+100])
        for bd_coord_group in bd_coord_list:
            url = u"http://api.map.baidu.com/geoconv/v1/?coords="
            for (i, coord) in enumerate(bd_coord_group):
                url += str(coord[0]) + "," + str(coord[1])
                if i != (len(bd_coord_group)-1):
                    url += ";"
            url += u"&from=1&to=5&ak=" + self.ak
            # 获取转换结果
            try:
                req = urllib2.Request(url)
                res_data = urllib2.urlopen(req)
                res = res_data.read()
                s = json.loads(res)
            except Exception, e:
                print e
                print url
                return False
            if s[u"status"] != 0:
                QMessageBox.critical(self.parent, u"坐标转换错误", unicode(str(s[u"message"])))
                print url
                return False
            if not s[u"result"]:
                print url
                return False
            for (i, coord) in enumerate(s[u"result"]):
                x2 = coord["x"]
                y2 = coord["y"]
                x1 = bd_coord_group[i][0]
                y1 = bd_coord_group[i][1]
                x = 2 * x1 - x2
                y = 2 * y1 - y2
                result_coord_list.append((x,y))
        return result_coord_list

    def deleteExtra(self, layer):
        extra_list = []
        polygon_layer = self.iface.activeLayer()
        selected_polygon = []
        for polygon in polygon_layer.selectedFeatures():
            selected_polygon.append(polygon)
        all_result = []
        for point in layer.getFeatures():
            all_result.append(point)
        for point in all_result:
            intersect_flag = False
            point_gemo = point.geometry()
            for polygon in selected_polygon:
                if point_gemo.intersects(polygon.geometry()):
                    intersect_flag = True
                    #print "had run"
                    break
            if intersect_flag == False:
                extra_list.append(point.id())
        # 删除多余features
        if delFeatures(layer, extra_list):
            return True
        else:
            return False

    def run(self):
        search = SearchPOIThread(self.keywords, self.searchRange, self.density, self.ak, self.parent)
        search.run()
        result = search.getResult()
        if not result:
            QMessageBox.information(self.parent, u"提示", u"查询不到结果!")
            return False

        # 坐标纠偏
        bd_coord_list = []
        for data in result:
            bd_coord_list.append((data[3], data[4]))
        gps_coords = self.geoconv(bd_coord_list)
        # 更新坐标
        if not gps_coords:
            QMessageBox.critical(self.parent, u"错误", u"坐标纠偏失败！")
            return False
        for i, data in enumerate(result):
            result[i][3] = float(gps_coords[i][0])
            result[i][4] = float(gps_coords[i][1])

        # 生成结果图层
        if self.createLayer(result):
            QMessageBox.information(self.parent, u"成功", u"抓取兴趣点成功，请查看!")
        else:
            QMessageBox.critical(self.parent, u"错误", u"生成结果图层失败！")

# 从百度地图中抓取地理信息线程主体
class SearchPOIThread(threading.Thread):
    def __init__(self, keywords, searchRange, dentisy, ak, parent):
        super(SearchPOIThread, self).__init__()
        self.parent = parent
        self.ak = ak
        self.keywords = keywords
        self.searchRange = searchRange
        self.dentisy = dentisy
        self.done_flag = False
        self.result = [] # 保存返回的信息(名称，类别，地址，经度，纬度)
        self.page_size = 20  # 默认页面大小为20


    def createURL(self, bottom_left_point, upper_right_point, page_num=0):
        baseUrl = u"http://api.map.baidu.com/place/v2/search"
        page_size = u"20" # 页面大小默认为20
        # 关键字
        url = baseUrl + u"?query="
        for (i, keyword) in enumerate(self.keywords):
            url += urllib.quote(keyword.encode('utf8'))
            if (len(self.keywords) > 1) and (i <= len(self.keywords) - 1):
                url += "$"
        # 检索结果详细程度
        url += "&scope=2"
        # 搜索区域
        url += "&bounds="
        if not bottom_left_point or not upper_right_point:
            bottom_left_point = self.searchRange[0]
            upper_right_point = self.searchRange[1]
        url += str(bottom_left_point[1]) + "," + str(bottom_left_point[0]) + "," + \
               str(upper_right_point[1]) + "," + str(upper_right_point[0])
        # 请求参数中坐标的类型
        url += "&coord_type=1"
        # 范围记录数量和分页页码
        url += "&page_size=" + str(page_size) + "&page_num=" + str(page_num)
        # 返回格式和ak码
        url += "&output=json&ak=" + self.ak
        return url

    def getDatas(self, url):
        datas = []  # u"名称", u"类别", u"地址", u"经度", u"纬度"
        req = urllib2.Request(url)
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        s = json.loads(res)
        if s[u'status'] != 0:
            status = s[u'status']
            return (False, status)
        else:
            try:
                total = int(s["total"])

                for result in s["results"]:
                    name = result["name"]
                    tag = ""
                    if result.has_key("detail") and result.has_key("detail_info"):
                        if result["detail"] == 1:
                            if result["detail_info"].has_key("tag"):
                                tag = result["detail_info"]["tag"]
                    if result.has_key("address"):
                        address = result["address"]
                    else:
                        address = ""
                    if not result.has_key("location"):
                        continue
                    else:
                        if not result["location"].has_key("lng") \
                            or not result["location"].has_key("lat"):
                            continue
                    lon = float(result["location"]["lng"])
                    lat = float(result["location"]["lat"])
                    datas.append([name, tag, address, lon, lat])

            except Exception, e:
                print url
                raise traceback.format_exc()
            return (total, datas)

    def getDivDatas(self, searchRange, density=0.5, main_thread_flag=False):
        search_result = []
        # 根据搜索密度分块
        xmin = float(searchRange[0][0])
        xmax = float(searchRange[1][0])
        ymin = float(searchRange[0][1])
        ymax = float(searchRange[1][1])
        xNum = (xmax - xmin) * density
        yNum = (ymax - ymin) * density
        rows = int(1 / density)
        cols = int(1 / density)
        if main_thread_flag:
            progess_len = rows * cols
            progess = Progess(self.parent,progess_len)
            progess.show()
        for block_index in xrange(rows * cols):
            # 整理当前分块的搜索范围
            i = block_index / rows
            j = block_index % rows
            aa = ymin + j * yNum
            bb = xmin + i * xNum
            cc = aa + yNum
            dd = bb + xNum
            bottom_left_point = (bb, aa)
            upper_right_point = (dd, cc)
            # 获取该分块的第0页搜索结果
            url = self.createURL(bottom_left_point, upper_right_point)
            try:
                (total, datas) = self.getDatas(url)
                # 如果搜索结果大于400则将分块按0.5的搜索密度继续分块
                if total >=400:
                    datas = self.getDivDatas((bottom_left_point, upper_right_point), 0.5)
                    if datas:
                        search_result.extend(datas)
                # 小于400获取该分块所有结果
                else:
                    # 添加第0页搜索结果
                    search_result.extend(datas)
                    # 遍历并添加余下页搜索结果
                    page_num = int(math.ceil(total / (self.page_size * len(self.keywords))))
                    for current_page_num in range(1,page_num):
                        url = self.createURL(bottom_left_point, upper_right_point, current_page_num)
                        (datas_result, datas) = self.getDatas(url)
                        if datas_result != False:
                            search_result.extend(datas)
                        else:
                            print url
                            return False
            except Exception, e:
                print url
                raise traceback.format_exc()
            if ("progess" in locals().keys() ) and main_thread_flag:
                # 判断进度条是否存在
                progess.count()
        if ("progess" in locals().keys() ) and main_thread_flag:
            progess.kill()
        return search_result

    def run(self):
        # 第一次判断是否需要按0.1密度分块
        url = self.createURL(self.searchRange[0], self.searchRange[1])
        result = self.getDatas(url)
        if result[0] == False:
            QMessageBox.critical(self.parent, u"错误", u"错误代码为：" + unicode(str(result[1])))
            return False
        # 判断结果是否在小于400
        (total, datas) = result
        # 如果搜索结果小于400，则直接遍历该区域的搜索结果
        if total < 400:
            # 第0页结果已获取，添加到结果列表中
            self.result.extend(datas)
            page_num = int(math.ceil(total / (self.page_size * len(self.keywords))))
            for current_page_num in range(1, page_num):
                url = self.createURL(self.searchRange[0], self.searchRange[1], current_page_num)
                datas = self.getDatas(url)[1]
                if datas:
                    self.result.extend(datas)
        # 如果搜索结果等于400，则按照搜索密度分块
        else:
            datas = self.getDivDatas(self.searchRange, self.dentisy, True)
            if datas:
                self.result.extend(datas)
        self.done_flag = True

    def getResult(self):
        if self.done_flag:
            return self.result
        else:
            return False