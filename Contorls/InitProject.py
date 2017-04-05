# -*- coding:utf-8 -*-
'''
新建项目主函数
@author: Karwai Kwok
'''

from PyQt4.QtGui import QColor, QMessageBox
from PyQt4.QtCore import QVariant, QFileInfo
import os
from qgis._core import QgsField, QgsSymbolV2, \
    QgsRendererCategoryV2, QgsCategorizedSymbolRendererV2, QgsVectorLayer, \
    QgsMapLayerRegistry, QgsVectorFileWriter, QgsProject, QGis, QgsFields, \
    QgsMapUnitScale, QgsMarkerSymbolV2, QgsFillSymbolV2, \
    QgsSimpleFillSymbolLayerV2, QgsFillSymbolLayerV2, QgsLineSymbolV2, \
    QgsRendererRangeV2, QgsSingleSymbolRendererV2
from MyQGIS.config.EnumType import Operator, LayerType
from MyQGIS.config.FieldConfig import SiteType2, SiteLength, SitePrec, CellType2, \
    CellLength, CellPrec, ServingCellType2, ServingCellLength, ServingCellPrec, \
    SiteSymbol, CellSymbol, ServingCellSymbol
from MyQGIS.Contorls.FileControls import deleteShapefile
from MyQGIS.config.HeadsConfig import SiteHead, CellHead, ServingCellHead
from MyQGIS.gui.SectorSetingDlg import SectorSetingDlg


class InitProject(object):
    def __init__(self, iface, file_path, color_dict, heads, parent=None):
        super(InitProject, self).__init__()
        self.iface = iface
        self.file_path = file_path
        self.ydcolor = color_dict[Operator.YD]
        self.ltcolor = color_dict[Operator.LT]
        self.dxcolor = color_dict[Operator.DX]
        self.ttcolor = color_dict[Operator.TT]
        self.heads = heads
        self.parent = parent

    # 初始化基站Symbol
    def initSymbol(self, landus, layer, mtype):
        renderder = None
        mapScale = QgsMapUnitScale()
        mapScale.maxScale = 500000.0

        if mtype == LayerType.SITE:
            categorys = []
            for terrain, (color, label) in landus.items():
                sym = None
                sym = QgsMarkerSymbolV2.createSimple({'name': 'circle'})
                sym.setOutputUnit(QgsSymbolV2.MapUnit)  # 设置为地图单位
                # sym.setMapUnitScale(QgsMapUnitScale(400000.0, 1500000.0))  # 设置最大最小比例尺
                sym.setScaleMethod(QgsSymbolV2.ScaleArea)  # 设置缩放方式
                sym.setSize(0.001)
                sym.setMapUnitScale(mapScale)
                sym.setColor(QColor(color))  # 设置颜色
                category = QgsRendererCategoryV2(terrain, sym, label)
                categorys.append(category)
            renderder = QgsCategorizedSymbolRendererV2(u'运营商', categorys)
        elif mtype == LayerType.CELL:
            categorys = []
            for terrain, (color, label) in landus.items():
                symLayer = QgsSimpleFillSymbolLayerV2()
                symLayer.setBorderWidth(0.0)
                symLayer.setOutputUnit(QgsSymbolV2.MapUnit)
                # symLayer.setMapUnitScale(mapScale)
                symLayer.setFillColor(QColor(color))

                sym = None
                sym = QgsFillSymbolV2.createSimple({})
                sym.changeSymbolLayer(0, symLayer)
                sym.setAlpha(0.3)  # 设置透明度
                category = QgsRendererCategoryV2(terrain, sym, label)
                categorys.append(category)
            renderder = QgsCategorizedSymbolRendererV2(u'运营商', categorys)

        elif mtype == LayerType.SERVINGCELL:
            sym = None
            sym = QgsLineSymbolV2.createSimple({})
            sym.setColor(QColor('blue'))  # 设置颜色
            sym.setAlpha(0)  # 设置透明度
            renderder = QgsSingleSymbolRendererV2(sym)

        layer.setRendererV2(renderder)

    # 根据类型ID，创建图层
    # @param attrbuts 该图层的全部字段列表
    # @param mtype 当前创建图层的类型
    # @param directory 项目保存路径
    def createLayer(self, mtype, directory=''):
        layerName = ''  # 图层名称
        layerType = ''  # 图层类型
        landus = []  # Symbol分类
        if mtype == LayerType.SITE:
            layerName = u'基站'
            layerType = QGis.WKBPoint
            landus = SiteSymbol
        elif mtype == LayerType.CELL:
            layerName = u'小区'
            layerType = QGis.WKBPolygon
            landus = CellSymbol

        else:
            layerName = u'相邻小区'
            layerType = QGis.WKBLineString
            landus = ServingCellSymbol

        # 删除原有图层文件
        deleteShapefile(directory, layerName)
        shapPath = os.path.join(directory, layerName + u".shp")
        fileds = self.createAttributesByType(mtype)

        # 创建出Shap文件
        # 数据源编码模式为GBK2312（否则中文字段会乱码）
        wr = QgsVectorFileWriter(shapPath, "GBK2312", fileds, layerType, None, "ESRI Shapefile")
        # 如果保存的时候没有错误
        if wr.hasError() == QgsVectorFileWriter.NoError:
            pass
        else:
            print wr.hasError()
            raise Exception, wr.errorMessage()  # 发生错误，抛出异常交给外面的方法处理异常
        del wr  # 使添加的字段生效

        layer = QgsVectorLayer(shapPath, layerName, 'ogr')

        # 只有当Symbol分类规则不为空时才设置
        if landus != None and len(landus) > 0:

            myLandus = {}
            for i, (color, lab) in landus.items():
                if i == u'移动':
                    myLandus[i] = (self.ydcolor, lab)
                elif i == u'联通':
                    myLandus[i] = (self.ltcolor, lab)
                elif i == u'电信':
                    myLandus[i] = (self.dxcolor, lab)
                else:
                    myLandus[i] = (self.ttcolor, lab)

            self.initSymbol(myLandus, layer, mtype)

        QgsMapLayerRegistry.instance().addMapLayer(layer)

    # 保存项目
    # @param 项目的名称
    def saveProject(self, path):
        p = QgsProject.instance()
        return (p.write(QFileInfo(path)), p.error())

    # 通过图层类型，创建出图层的字段
    def createAttributesByType(self, mtype):
        names = []
        types = []
        lengs = []
        precs = []
        if mtype == LayerType.SITE:
            names = SiteHead
            types = SiteType2
            lengs = SiteLength
            precs = SitePrec
            # 补充基站图层字段
            if len(self.heads) > 55:
                for name in self.heads[56:]:
                    names.append(name)
                    types.append(QVariant.String)
                    lengs.append(100)
                    precs.append(0)
        elif mtype == LayerType.CELL:
            names = CellHead
            types = CellType2
            lengs = CellLength
            precs = CellPrec
            # 补充小区图层字段
            if len(self.heads) > 55:
                for name in self.heads[56:]:
                    names.append(name)
                    types.append(QVariant.String)
                    lengs.append(100)
                    precs.append(0)
        else:
            names = ServingCellHead
            types = ServingCellType2
            lengs = ServingCellLength
            precs = ServingCellPrec

        fields = QgsFields()
        # 唯一ID
        fields.append(QgsField('id', QVariant.String, "String", 50, 0))
        for (i, itm) in enumerate(names):
            cuType = types[i]
            mtype = "String"
            if cuType == QVariant.Int:
                mtype = "Integer"
            elif cuType == QVariant.Double:
                mtype = "Real"
            field = QgsField(itm, cuType, mtype, lengs[i], precs[i])
            fields.append(field)
        return fields

    def initLayer(self):
        try:
            file_dir = os.path.split(self.file_path)[0]
            self.createLayer(LayerType.SITE, file_dir)
            self.createLayer(LayerType.CELL, file_dir)
            self.createLayer(LayerType.SERVINGCELL, file_dir)
            (result, eroStr) = self.saveProject(self.file_path)
            if result:
                # 导入基站和小区
                # 显示设置扇形相关参数对话框
                sectorSet = SectorSetingDlg(self.iface, file_dir, self.parent)
                sectorSet.show()
                sectorSet.exec_()

            else:
                QMessageBox.critical(self.parent, u'创建项目', u'创建项目发生了错误：' + eroStr)

        except Exception, e:
            QMessageBox.critical(self.parent, u'创建项目', unicode(e))
            raise e

