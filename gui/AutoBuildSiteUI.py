# -*- coding: utf-8 -*-
'''
自动规划基站交互界面
@author: Karwai Kwok
'''

import os, processing
from PyQt4.QtGui import QDialog, QIntValidator, QLabel, QLineEdit, QGridLayout, \
    QPushButton, QHBoxLayout, QVBoxLayout, QIcon, QColor, QTableWidgetItem, \
    QMessageBox, QTableWidget, QFileDialog, QAbstractItemView
from PyQt4.QtCore import Qt, SIGNAL, QVariant
from qgis._core import QGis, QgsMapLayerRegistry, QgsProject, QgsVectorFileWriter, \
    QgsVectorLayer, QgsFields, QgsPoint, QgsField, QgsSpatialIndex
from qgis._gui import QgsVertexMarker, QgsRubberBand,QgsMessageBar
from MyQGIS.config.HeadsConfig import PLANNINGHead
from MyQGIS.config.FieldConfig import PLANNINGType2, PLANNINGLength, PLANNINGPrec
from MyQGIS.Contorls.LayerControls import getLayerByName
from MyQGIS.Contorls.FileControls import getProjectDir, deleteShapefile
from MyQGIS.Contorls.FeaturesControls import delAllFeatures, importFeaturesToLayer, \
    createABasicPointFeature
from MyQGIS.Contorls.AutoBuildSite import AutoBuildSite
from MyQGIS.Contorls.OptimizateNewSite import OptimizateNewSite

# 自动规划基站参数设置窗口
class AutoBuildSiteSettingDlg(QDialog):
    def __init__(self, iface, parent=None):
        super(AutoBuildSiteSettingDlg, self).__init__()
        self.iface = iface
        self.parent = parent

        self.initUI()

    # 初始化界面
    def initUI(self):
        self.setGeometry(200,200,250,200)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle(u'自动规划基站')

        validator = QIntValidator(1, 10000, self)   #设置以下几行输入限制为整数
        title1 = QLabel(u'分区角度:')
        self.titleEdit1 = QLineEdit()
        self.titleEdit1.setPlaceholderText('60')
        self.titleEdit1.setValidator(validator)
        title2=QLabel(u'最大辐射范围:')
        self.titleEdit2 = QLineEdit()
        self.titleEdit2.setPlaceholderText('2000')
        self.titleEdit2.setValidator(validator)
        title3=QLabel(u'农村(最小站间距)')
        self.titleEdit3 = QLineEdit()
        self.titleEdit3.setPlaceholderText('800')
        self.titleEdit3.setValidator(validator)
        title4=QLabel(u'郊区乡镇(最小站间距)')
        self.titleEdit4 = QLineEdit()
        self.titleEdit4.setPlaceholderText('500')
        self.titleEdit4.setValidator(validator)
        title5=QLabel(u'普通市区(最小站间距)')
        self.titleEdit5 = QLineEdit()
        self.titleEdit5.setPlaceholderText('350')
        self.titleEdit5.setValidator(validator)
        title6=QLabel(u'密集市区(最小站间距)')
        self.titleEdit6 = QLineEdit()
        self.titleEdit6.setPlaceholderText('200')
        self.titleEdit6.setValidator(validator)

        grid1=QGridLayout()
        grid1.setSpacing(10)

        grid1.addWidget(title1,1,0)
        grid1.addWidget(self.titleEdit1,1,1)
        grid1.addWidget(title2,2,0)
        grid1.addWidget(self.titleEdit2,2,1)
        grid1.addWidget(title3,3,0)
        grid1.addWidget(self.titleEdit3,3,1)
        grid1.addWidget(title4,4,0)
        grid1.addWidget(self.titleEdit4,4,1)
        grid1.addWidget(title5,5,0)
        grid1.addWidget(self.titleEdit5,5,1)
        grid1.addWidget(title6,6,0)
        grid1.addWidget(self.titleEdit6,6,1)

        ok = QPushButton(u'确定')
        self.connect(ok, SIGNAL('clicked()'), self.settingtext)
        cancel= QPushButton(u'取消')
        self.connect(cancel, SIGNAL('clicked()'), self.accept)

        hbox = QHBoxLayout()
        hbox.setSpacing(15)
        hbox.addStretch(1)
        hbox.addWidget(ok)
        hbox.addWidget(cancel)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addLayout(grid1)
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.resize(300,270)

    def settingtext(self):
        #获取所有设置参数
        text1=self.titleEdit1.text().strip()
        text2=self.titleEdit2.text().strip()
        text3=self.titleEdit3.text().strip()
        text4=self.titleEdit4.text().strip()
        text5=self.titleEdit5.text().strip()
        text6=self.titleEdit6.text().strip()

        if text1=='':
            text1=60
        if type(text1) != int:
            text1=int(text1)
        if text2=='':
            text2=2000             #最大辐射范围默认值为2000米
        if type(text2) != int:
            text2=int(text2)
        if text3=='':
            text3= 800                  #农村最小辐射范围默认值为800米
        if type(text3) != int:
            text3 = int(text3)
        if text4=='':
            text4=500               #郊区乡镇辐射范围默认值为500米
        if type(text4) != int:
            text4 = int(text4)
        if text5=='':
            text5=350               #普通市区最小辐射范围默认值为350米
        if type(text5) != int:
            text5 = int(text5)
        if text6=='':
            text6=200               #密集市区最小辐射范围默认值为200米
        if type(text6) != int:
            text6 = int(text6)
        #传值给dialog
        self.tlist=[text1,text2,text3,text4,text5,text6] #定义存放所有参数的列表
        self.accept()
        d = NewSiteDialog(self.iface,self.tlist, self.parent)
        del self.tlist


class NewSiteDialog(object):
    def __init__(self, iface, tlist, parent=None):
        super(NewSiteDialog, self).__init__()
        self.iface=iface
        self.tlist=tlist # 参数设置列表
        self.parent = parent

        #初始化表格
        self.calculationList=[] #保存新建基站计算结果表格数据
        self.finishFList=[] #保存计算后每个结点周围的基站
        self.sphead=[]

        self.newSiteAnaly()  #启动计算

    # 生成泰森结点
    def createNodeLayer(self):
        project_dir = getProjectDir(self.iface, u"基站")
        if not project_dir:
            QMessageBox.critical(self, u"错误", u"基站图层不存在!")
            return False
        else:
            project = QgsProject.instance()
            VoronoiName = u"泰森多边形"
            NodesName = u"泰森结点"
            # 若已存在泰森多边形和泰森结点图层，则先移除图层再删除shape文件
            voronoi_layer = getLayerByName(VoronoiName, self.iface)
            if voronoi_layer:
                QgsMapLayerRegistry.instance().removeMapLayer(voronoi_layer)
            else:
                deleteShapefile(project_dir, VoronoiName)
            nodes_layer = getLayerByName(NodesName, self.iface)
            if nodes_layer:
                QgsMapLayerRegistry.instance().removeMapLayer(nodes_layer)
            else:
                deleteShapefile(project_dir, NodesName)

            if (voronoi_layer) or (nodes_layer):
                project.write()
                QMessageBox.critical(self, u"错误", u"相应文件已被占用，请重启QGIS软件！")
                return False

            site_layer = getLayerByName(u'基站', self.iface)
            # 生成泰森多边形
            VoronoiFile = os.path.join(project_dir, VoronoiName + u".shp")
            Vor = processing.runalg("qgis:voronoipolygons", site_layer, 0, VoronoiFile)
            Voronoi = processing.load(Vor['OUTPUT'], VoronoiName)
            # 生成泰森结点
            NodesFile = os.path.join(project_dir, NodesName + u".shp")
            Nod = processing.runalg("qgis:extractnodes", Voronoi, NodesFile)
            Nodes = processing.load(Nod['OUTPUT'], NodesName)

            return Nodes


    def newSiteAnaly(self):
        sitelayer = getLayerByName(u'基站', self.iface)  #sitelayer 基站图层
        nodelayer = self.createNodeLayer()
        if not nodelayer:
            return False
        self.jlist=[]    #定义存放结点
        namelist1=[]
        self.alist=[]   #定义存放所有基站

        jfeatures = nodelayer.getFeatures()
        for jf in jfeatures :
            namelist1.append(jf[2])
        namelist2 = list(set(namelist1))
        namelist2.sort(key=namelist1.index)
        jfeatures = nodelayer.getFeatures()
        for jf in jfeatures :
            if jf[2] in namelist2 :
                self.jlist.append(jf)
                namelist2.remove(jf[2])
        if len(self.jlist)== 0 :
            self.iface.messageBar().pushMessage(u'提示', u'未找到规划站点!' , QgsMessageBar.CRITICAL, 5)

        spt = AutoBuildSite(self.iface, self.jlist, self.tlist, self)
        spt.calculationResult.connect(self.calculationFinish)
        spt.run()

    def calculationFinish(self, suit_jlist, totalDict):
        #totalDict,记录推送运营商基站的计算结果，{0:[[pnfDis,fsite],[],[],……],1:[……],……}
        count = 0 # 记录循环执行次数
        for (i, jsite) in enumerate(self.jlist):                    #遍历所有结点
            if not suit_jlist.has_key(i):
                continue
            jpoint=jsite.geometry().asPoint()
            if not isinstance(jsite[7],basestring):
                # 如果区域类型值不是字符串类型， 则把其转换为空字符串
                jsite[7] = unicode(jsite[7])
            tempList1 = [str(count+1),str(jpoint.x()),str(jpoint.y()),jsite[7]]
            #tempList1,填入结点名,经度,纬度,区域类型，并转换str类型
            perList=totalDict.get(i)   #根据键i获取perList
            tempList2=[] #tempList2,保存基站的站名，经度，纬度
            self.finishFList.append([])  #增加空子列表
            tolDistance = 0 # 结点距离所有符合基站的距离之和
            suit_site_dict = {} # 用于记录符合基站的基站名和距离 (key: SiteName, value: distance)
            for L in perList:
                if isinstance(L, list) :  #判断是否为列表类型
                    tolDistance = tolDistance + L[0]
                    psite = L[1]
                    tempList2.append(psite[2])  #基站名
                    tempList2.append(str(L[0])) #距离
                    tempList2.append(str(psite[4]))  #经度
                    tempList2.append(str(psite[5]))  #纬度
                    self.finishFList[count].append(psite)    #保存每一行的基站(基站feature)
                    suit_site_dict[psite[2]] = L[0]
                else :
                    tempList2.append('NULL')
                    tempList2.append('NULL')           #没有基站，设为None值
                    tempList2.append('NULL')
                    tempList2.append('NULL')
            if ((tolDistance != 0) and (len(suit_site_dict) != 0)):
                avgDistance = ("%.4f" % (tolDistance / len(suit_site_dict)))
                # 将符合要求的站点按距离从小到大排序
                sorted_list = sorted(suit_site_dict.iteritems(), key=lambda d:d[1], reverse=False)
                # tempList1后追加最近基站名称，最近基站距离，平均距离
                tempList1.extend([sorted_list[0][0], str(sorted_list[0][1]), str(avgDistance)])
            else:
                # tempList1后追加最近基站名称，最近基站距离，平均距离
                tempList1.extend(["NULL", "NULL", "0"])

            self.calculationList.append(tempList1 + tempList2)  #填入每一子列表数据
            count = count + 1

        self.setResultLayer(self.calculationList)


    # 生成规划基站结果图层
    def setResultLayer(self, result_list):
        layerName = u'规划基站结果'
        layerType = QGis.WKBPoint
        project_dir = getProjectDir(self.iface)
        # 先判断是否已存在规划基站结果图层
        result_layer = getLayerByName(layerName, self.iface)
        if result_layer:
            #清空数据
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
            feature = createABasicPointFeature(QgsPoint(float(result[1]),float(result[2])), result)
            features_list.append(feature)
        importFeaturesToLayer(result_layer, features_list)
        # 合并站点
        mergeNSite = OptimizateNewSite(result_layer, self.parent)
        if mergeNSite.run():
            QMessageBox.information(self.parent, u"自动规划基站", u"自动规划基站成功！")
        else:
            QMessageBox.critical(self.parent, u"自动规划基站", u"自动规划基站失败！")


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

