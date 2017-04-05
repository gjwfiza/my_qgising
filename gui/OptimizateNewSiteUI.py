# -*- coding: utf-8 -*-
'''
优化自动规划基站交互界面
@author: Karwai Kwok
'''

import os
from PyQt4.QtGui import QDialog, QIntValidator, QLabel, QLineEdit, QGridLayout, \
    QPushButton, QHBoxLayout, QVBoxLayout, QIcon, QColor, QTableWidgetItem, \
    QMessageBox, QTableWidget, QFileDialog, QAbstractItemView, QMenu, QAction
from PyQt4.QtCore import Qt, SIGNAL, QVariant
from qgis._core import QGis, QgsMapLayerRegistry, QgsProject, QgsVectorFileWriter, \
    QgsVectorLayer, QgsFields, QgsPoint, QgsField, QgsSpatialIndex
from MyQGIS.config.HeadsConfig import MergeSiteHead, PLANNINGHead
from MyQGIS.config.EnumType import ExcelType
from MyQGIS.config.FieldConfig import PLANNINGType2, PLANNINGLength, PLANNINGPrec
from MyQGIS.Contorls.LayerControls import getLayerByName
from MyQGIS.Contorls.FileControls import getProjectDir, deleteShapefile
from MyQGIS.Contorls.ImportData import GetDataFromExcel
from MyQGIS.Contorls.ExportData import ExportData
from MyQGIS.Contorls.FeaturesControls import delAllFeatures, importFeaturesToLayer, \
    createABasicPointFeature
from MyQGIS.Contorls.OptimizateNewSite import OptimizateNewSite

class OptimizateNewSiteUI(QDialog):
    def __init__(self, iface, parent=None):
        super(OptimizateNewSiteUI, self).__init__()
        self.iface = iface
        self.parent = parent

        self.initUI()

    # 初始化界面
    def initUI(self):
        self.setWindowTitle(u'自动规划基站优化')
        self.setWindowIcon(QIcon('images/logo.png'))
        self.resize(600, 300)
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint)
        self.initView()

    def initView(self):
        # 数据表格
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setRowCount(7)
        # 设置当前Table不能编辑
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 初始化表格上下文菜单
        self.initTableContextMenu()

        self.initTableHeader()
        # 定义按钮
        impBtn = QPushButton(u"导入EXCEL表", self)
        self.connect(impBtn, SIGNAL('clicked()'), self.impData)
        startBtn = QPushButton(u"开始合并", self)
        self.connect(startBtn, SIGNAL('clicked()'), self.mergeJSite)
        #布局
        hbox = QHBoxLayout()
        hbox.addWidget(impBtn)
        hbox.addWidget(startBtn)
        vbox = QVBoxLayout()
        vbox.addWidget(self.tableWidget)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        # 判断是否已有规划基站结果
        layer = getLayerByName(u'规划基站结果', self.iface)
        if layer:
            data_list = []
            for feature in layer.getFeatures():
                temp_list = []
                for value in feature.attributes():
                    temp_list.append(value)
                data_list.append(temp_list)
                del temp_list
            self.initTable(data_list)
            self.__mlist = data_list

    def initTableContextMenu(self):
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.popMenu = QMenu(self.tableWidget)
        delAction = QAction(u'删除', self)  # 删除
        self.popMenu.addAction(delAction)

    # 初始化Table的头
    def initTableHeader(self):
        self.heads = []
        self.heads = MergeSiteHead
        self.tableWidget.setColumnCount(len(self.heads))  # 设置表格的列数
        for (i, h) in enumerate(self.heads):
            tabItem = QTableWidgetItem(h)
            self.tableWidget.setHorizontalHeaderItem(i, tabItem)

    # 导入Excel表数据
    def impData(self):
        fileName = QFileDialog.getOpenFileName(self, u'数据导入', '/', 'Excel Files (*.xls *.xlsx)')
        if fileName != None and fileName != '':
            self.impType = ExcelType.MERGESITE
            getDataFromExcel = GetDataFromExcel(fileName, self.impType)
            datas_list = getDataFromExcel.getData()
            self.impFinish(datas_list)

    # 导入数据完成绑定函数
    def impFinish(self, mylist):
        self.__mlist = []
        self.__mlist.extend(mylist)
        self.tableWidget.clearContents()
        self.initTable(self.__mlist)

    # 初始化表格的每个Item
    def initTable(self, mlist):
        self.tableWidget.setRowCount(len(mlist))
        for (i, v) in enumerate(mlist):
            for (j, item) in enumerate(v):
                if type(item) != str:
                    item = unicode(item)
                if item == None:
                    item = ''
                tabItem = QTableWidgetItem(item)
                tabItem.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(i, j, tabItem)

    # 开始运行
    def mergeJSite(self):
        self.accept()
        merge = OptimizateNewSite(self.__mlist, self)
        merge.calculationResult.connect(self.calculationFinish)
        merge.run()

    def calculationFinish(self, merge_result):
        self.setResultLayer(merge_result)
        fileName = QFileDialog.getSaveFileName(self, u'合并结果导出到 ...', '/', 'Excel File(*.xls *.xlsx)')
        if fileName:
            self.sphead = [u'规划基站名称', u'经度', u'纬度', u'区域类型', u"平均距离"]
            for i in range(6):  # 根据输入的参数增加表头
                self.sphead.append(u'基站名称')
                self.sphead.append(u'距离')
                self.sphead.append(u'经度')
                self.sphead.append(u'纬度')

            layer = getLayerByName(u"基站合并结果", self.iface)
            if not layer:
                QMessageBox.critical(self, u"错误", u"找不到基站合并结果图层")
            exportData = ExportData(self.iface, self)
            if exportData.exportDataToExcel(layer, fileName):
                QMessageBox.information(self, u"成功", u"数据导出成功！")
            else:
                QMessageBox.critical(self, u"错误", u"数据导出失败！")

        else:
            self.close()

    # 生成规划基站结果图层
    def setResultLayer(self, result_list):
        layerName = u'规划基站优化结果'
        layerType = QGis.WKBPoint

        project_dir = getProjectDir(self.iface)
        # 先判断是否已存在规划基站结果图层
        result_layer = getLayerByName(layerName, self.iface)
        if result_layer:
            # 清空数据
            delAllFeatures(result_layer)
        else:
            # 删除原有图层文件
            deleteShapefile(project_dir, layerName)
            shapPath = os.path.join(project_dir, layerName + u".shp")
            # 生成图层
            fileds = self.createFields()
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

            result_layer = QgsVectorLayer(shapPath, layerName, 'ogr')
            QgsMapLayerRegistry.instance().addMapLayer(result_layer)

        # 添加数据
        features_list = []
        for result in result_list:
            feature = createABasicPointFeature(QgsPoint(float(result[1]), float(result[2])), result)
            features_list.append(feature)
        importFeaturesToLayer(result_layer, features_list)

    def createFields(self):
        names = PLANNINGHead
        types = PLANNINGType2
        lengs = PLANNINGLength
        precs = PLANNINGPrec

        fields = QgsFields()
        for (i, itm) in enumerate(names):
            cuType = types[i]
            mtype = 'String'
            if cuType == QVariant.Int:
                mtype = 'Integer'
            elif cuType == QVariant.Double:
                mtype = 'Real'
            field = QgsField(itm, cuType, mtype, lengs[i], precs[i])
            fields.append(field)
        return fields

    def exportFinish(self, result):
        QMessageBox.information(self, u'新建基站结果', u'数据导出到Excel表完成，请查看')

    def exportError(self, e, erStr):
        QMessageBox.information(self, u'新建结果', u'生成基站时，发生错误，请重试+' + erStr)
