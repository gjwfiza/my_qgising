# -*- coding: utf-8 -*-
'''
@ author: Karwai Kwok
程序主函数
'''
import os
from PyQt4.QtCore import SIGNAL, QObject
from PyQt4.QtGui import QAction, QIcon, QMenu, QToolBar, QActionGroup, QColor, QMessageBox
from qgis.core import QgsMapLayerStyleManager

from gui.InitProjectDlg import InitProjectDlg
from gui.ImportDataDlg import ImportDataDlg
from Contorls.LayerControls import judgeInitProject, isSelectedASite, getLayerByName
from gui.ExportDataUI import ExportDataUI
from gui.CreateModelDlg import CreateModelDlg
from gui.AddSiteUI import AddSiteUI
from gui.AddCellUI import AddCellUI
from gui.MoveSiteUI import MoveSiteUI
from gui.DeleteSiteUI import DeleteSiteUI
from gui.ModifyAzimuthUI import ModifyAzimuthUI
from gui.SearchUI import SearchUI
from Contorls.SCellControls import getSCell, SCellControls, addOneWaySCell, addTwoWaySCell
from gui.DeleteNCellUI import DeleteNCellUI
from Contorls.LayerRenderControls import Mod3Render, setDeafaultRender, HeatRender
from gui.UpdatePolygonInfoUI import UpdatePolygonInfoUI
from gui.RangeByNoUI import RangeByNoSettingUI
from gui.RangeByStrUI import RangeByStrSettingUI
from gui.ExportDataToKMLUI import ExportDataToKMLUI
from gui.ExportDataToBaiduUI import ExportDataToBaiduUI
from gui.ExportDataToTencetUI import ExportDataToTencentUI
from gui.ExportDataToSogoUI import ExportDataToSogoUI
from gui.SearchPOIFromBaiduUI import SearchPOIFromBaiduUI
from gui.AutoBuildSiteUI import AutoBuildSiteSettingDlg
from gui.AddNSitesUI import AddNSitesUI
from gui.QuickPCIUI import QuickPCISettingDlg
from gui.AccuratePCISettingUI import AccuratePCISettingDlg

# 插件所在路径
strfilepath = os.path.realpath(__file__)
cmd_folder = "%s/" % (os.path.dirname(strfilepath),)

class Main(object):
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        self.siteStyle = False # 用于判断是否对小区图层进行额外渲染
        self.cellStyle = False # 用于判断是否对小区图层进行额外渲染
        self.cellStyleManager = None # 小区样式管理器
        self._styleManager = None # 任意图层样式管理器
        self.radius = "10.000" # 默认渲染半径
        self.quality = 2  # 默认渲染质量
        self.mainWindow = self.iface.mainWindow()

        self.myMenu = QMenu(u'&移动通信规划功能', self.mainWindow)

        '''新建工程按钮'''
        initPorjectAction = QAction(QIcon(os.path.join(cmd_folder, u'images', u'imp.png')), u'新建工程', self.mainWindow)
        QObject.connect(initPorjectAction, SIGNAL('triggered()'), self.initProjectFunc)


        '''数据导入菜单'''
        DataMenu = QMenu(u'&数据处理', self.mainWindow)
        importAction = QAction(QIcon(os.path.join(cmd_folder, u'images', u'imp.png')), u'数据导入', self.mainWindow)
        QObject.connect(importAction, SIGNAL('triggered()'), self.importFunc)
        exportActoin = QAction(QIcon(os.path.join(cmd_folder, u'images', u'export.jpg')), u'数据导出', self.mainWindow)
        QObject.connect(exportActoin, SIGNAL('triggered()'), self.exportFunc)
        createModelAction = QAction(QIcon(os.path.join(cmd_folder, u'images', u'create.png')), u'生成Excel模板', self.mainWindow)
        QObject.connect(createModelAction, SIGNAL('triggered()'), self.createModelFunc)
        # 从子菜单中添加功能按钮
        DataMenu.addAction(importAction)
        DataMenu.addAction(exportActoin)
        DataMenu.addAction(createModelAction)

        '''基站布点'''
        SiteMenu = QMenu(u'&基站布点', self.mainWindow)

        addSiteAction = QAction(QIcon(os.path.join(cmd_folder, u'images', u'add.png')),
                                 u'添加基站  ', self.mainWindow)
        addSiteAction.triggered.connect(self.addSiteFunc)
        addCellAction = QAction(QIcon(os.path.join(cmd_folder, u'images', u'addcell.png')),
                                 u'添加小区  ', self.mainWindow)
        addCellAction.triggered.connect(self.addCellFunc)
        moveSiteAction = QAction(QIcon(os.path.join(cmd_folder, u'images', u'move.png')),
                                 u'移动基站  ', self.mainWindow)
        moveSiteAction.triggered.connect(self.moveSiteFunc)
        delSiteAction = QAction(QIcon(os.path.join(cmd_folder, u'images', u'remove.png')),
                                 u'删除基站小区  ', self.mainWindow)
        delSiteAction.triggered.connect(self.delSiteFunc)
        modifyAzimuthAction = QAction(u'修改小区方向角 ', self.mainWindow)
        QObject.connect(modifyAzimuthAction, SIGNAL('triggered()'), self.modifyAzimuthFunc)
        searchSiteAction = QAction(QIcon(os.path.join(cmd_folder, u'images', u'find.png')),
                                 u'查找基站小区  ', self.mainWindow)
        searchSiteAction.triggered.connect(self.searchFunc)

        SiteMenu.addAction(addSiteAction)
        SiteMenu.addAction(addCellAction)
        SiteMenu.addAction(moveSiteAction)
        SiteMenu.addAction(delSiteAction)
        SiteMenu.addAction(modifyAzimuthAction)
        SiteMenu.addAction(searchSiteAction)

        '''相邻小区'''
        NCellMenu = QMenu(u'&相邻小区', self.mainWindow)

        showNCellAction = QAction(QIcon(os.path.join(cmd_folder, u'images', u'设置相邻小区.png')),
                                   u'设置服务小区并显示其相邻小区  ', self.mainWindow)
        QObject.connect(showNCellAction, SIGNAL('triggered()'), self.showNCellFunc)
        addNCell1Action = QAction(QIcon(os.path.join(cmd_folder, u'images', u'增加单向邻区.png')),
                                   u'增加单向相邻小区  ', self.mainWindow)
        QObject.connect(addNCell1Action, SIGNAL('triggered()'), self.addOneWayNCellFunc)
        addNCell2Action = QAction(QIcon(os.path.join(cmd_folder, u'images', u'增加双向邻区.png')),
                                   u'增加双向相邻小区  ', self.mainWindow)
        QObject.connect(addNCell2Action, SIGNAL('triggered()'), self.addTwoWayNCellFunc)
        delNCellAction = QAction(QIcon(os.path.join(cmd_folder, u'images', u'删除邻区.jpg')),
                                   u'删除相邻小区  ', self.mainWindow)
        QObject.connect(delNCellAction, SIGNAL('triggered()'), self.delNCellFunc)
        checkRepeatAction = QAction(u'检查相邻小区的重复性，并自动修正  ', self.mainWindow)
        QObject.connect(checkRepeatAction, SIGNAL('triggered()'), self.checkRepeatFunc)
        #保存选中的服务小区（列表中存string）
        self.SCell_list = []
        self.HL_SCell = None # 当前的高亮显示的主服务小区
        self.HL_NCell_O = [] # 高亮显示的单向邻区list
        self.HL_NCell_D = [] # 高亮显示的双向邻区list

        NCellMenu.addAction(showNCellAction)
        NCellMenu.addSeparator()
        NCellMenu.addAction(addNCell1Action)
        NCellMenu.addAction(addNCell2Action)
        NCellMenu.addAction(delNCellAction)
        NCellMenu.addAction(checkRepeatAction)



        '''网优分析'''
        NetAnalysisMenu = QMenu(u'&网优分析', self.mainWindow)

        mod3Action = QAction(u'模三分析 ', self.mainWindow)
        QObject.connect(mod3Action, SIGNAL('triggered()'), self.mod3Func)
        createRenderAction = QAction(u'生成渲染图 ', self.mainWindow)
        QObject.connect(createRenderAction, SIGNAL('triggered()'), self.createRenderFunc)
        updatePolygonAction = QAction(u'更新区域信息 ', self.mainWindow)
        QObject.connect(updatePolygonAction, SIGNAL('triggered()'), self.updatePolygonInfoFunc)
        rangeByNoAction = QAction(u'按范围分类显示(针对数字)', self.mainWindow)
        QObject.connect(rangeByNoAction, SIGNAL('triggered()'), self.rangeByNoFunc)
        rangeByStrAction = QAction(u'按类别分类显示(针对字符)', self.mainWindow)
        QObject.connect(rangeByStrAction, SIGNAL('triggered()'), self.rangeByStrFunc)

        NetAnalysisMenu.addAction(mod3Action)
        NetAnalysisMenu.addAction(createRenderAction)
        NetAnalysisMenu.addAction(updatePolygonAction)
        NetAnalysisMenu.addAction(rangeByNoAction)
        NetAnalysisMenu.addAction(rangeByStrAction)

        '''基站规划分析'''
        SiteAnalysisMenu = QMenu(u'&基站规划分析', self.mainWindow)

        AutoBuildSiteAction = QAction(u'自动规划基站', self.mainWindow)
        QObject.connect(AutoBuildSiteAction, SIGNAL('triggered()'), self.AutoBuildSiteFunc)
        addCandidateSiteAction = QAction(u'添加待选站点', self.mainWindow)
        QObject.connect(addCandidateSiteAction, SIGNAL('triggered()'), self.addCandidateSiteFunc)
        quickPCIAction = QAction(u'快速PCI规划', self.mainWindow)
        QObject.connect(quickPCIAction, SIGNAL('triggered()'), self.quickPCIFunc)
        accuratePCIAction = QAction(u'精确PCI规划', self.mainWindow)
        QObject.connect(accuratePCIAction, SIGNAL('triggered()'), self.accuratePCIFunc)

        SiteAnalysisMenu.addAction(AutoBuildSiteAction)
        SiteAnalysisMenu.addAction(addCandidateSiteAction)
        # SiteAnalysisMenu.addAction(quickPCIAction)
        # SiteAnalysisMenu.addAction(accuratePCIAction)

        '''网络地图'''
        OnlineMapMenu = QMenu(u"网络地图", self.mainWindow)

        createKMLAction = QAction(QIcon(os.path.join(cmd_folder, u'images', u'kml_file.ico')), u'生成KML图层 ',
                                  self.mainWindow)
        QObject.connect(createKMLAction, SIGNAL('triggered()'), self.createKMLFunc)
        # 生成百度html
        createBaiduMapAction = QAction(QIcon(os.path.join(cmd_folder, u'images', u'Baidu.png')), u'导出到百度地图 ',
                                       self.mainWindow)
        QObject.connect(createBaiduMapAction, SIGNAL('triggered()'), self.createBaiduMapFunc)
        # 生成腾讯html
        createTencentMapAction = QAction(QIcon(os.path.join(cmd_folder, u'images', u'Tencent.png')), u'导出到腾讯地图 ',
                                         self.mainWindow)
        QObject.connect(createTencentMapAction, SIGNAL('triggered()'), self.createTencentMapFunc)
        # 生成搜狗html
        createSogotMapAction = QAction(QIcon(os.path.join(cmd_folder, u'images', u'Sogo.png')), u'导出到搜狗地图 ',
                                       self.mainWindow)
        QObject.connect(createSogotMapAction, SIGNAL('triggered()'), self.createSogotMapFunc)
        # 从百度地图抓取相关热点
        searchPOIAction = QAction(u'从百度地图抓取相关热点', self.mainWindow)
        QObject.connect(searchPOIAction, SIGNAL('triggered()'), self.searchPOIFunc)

        OnlineMapMenu.addAction(createKMLAction)
        OnlineMapMenu.addAction(createBaiduMapAction)
        OnlineMapMenu.addAction(createTencentMapAction)
        OnlineMapMenu.addAction(createSogotMapAction)
        OnlineMapMenu.addAction(searchPOIAction)

        '''帮助功能'''
        HelpAction = QAction(u'帮助', self.mainWindow)
        QObject.connect(HelpAction, SIGNAL('triggered()'), self.HelpFunc)

        # 整合功能菜单
        self.myMenu.addAction(initPorjectAction)
        self.myMenu.addMenu(DataMenu)
        self.myMenu.addMenu(SiteMenu)
        self.myMenu.addMenu(NCellMenu)
        self.myMenu.addMenu(NetAnalysisMenu)
        self.myMenu.addMenu(SiteAnalysisMenu)
        self.myMenu.addMenu(OnlineMapMenu)
        self.myMenu.addAction(HelpAction)

        #pluginM = self.iface.pluginMenu()
        #pluginM.addMenu(self.myMenu)

        # 向菜单栏中添加插件菜单
        menuBar = self.mainWindow.menuBar()
        self.m = menuBar.addMenu(u'&移动通信规划功能')
        self.m.addAction(initPorjectAction)
        self.m.addMenu(DataMenu)
        self.m.addMenu(SiteMenu)
        self.m.addMenu(NCellMenu)
        self.m.addMenu(NetAnalysisMenu)
        self.m.addMenu(SiteAnalysisMenu)
        self.m.addMenu(OnlineMapMenu)
        self.m.addAction(HelpAction)

    # remove the plugin menu item and icon
    def unload(self):
        self.myMenu.deleteLater()
        self.m.deleteLater()

    #新建工程
    def initProjectFunc(self):
        dlg = InitProjectDlg(self.iface, self.mainWindow)
        dlg.show()
        dlg.exec_()

    #导入数据
    def importFunc(self):
        # 判断是否已初始化工程
        if not judgeInitProject(self.iface):
            QMessageBox.critical(self.mainWindow, u"错误", u"请先初始化工程！")
            return
        else:
            dlg = ImportDataDlg(self.iface, self.mainWindow)
            dlg.show()
            dlg.exec_()

    #导出数据
    def exportFunc(self):
        dlg = ExportDataUI(self.iface, self.mainWindow)
        dlg.show()

    #生成模板文件
    def createModelFunc(self):
        dlg = CreateModelDlg(self.iface, self.mainWindow)
        dlg.show()

    # 向基站图层中添加基站
    def addSiteFunc(self):
        ui = AddSiteUI(self.iface, self.mainWindow)
        ui.show()
        ui.exec_()

    #选中基站后在小区图层中向其添加捆绑小区
    def addCellFunc(self):
        # 先判断有没有只选中1个基站
        if isSelectedASite(self.iface):
            ui = AddCellUI(self.iface, self.mainWindow)
            ui.show()
            ui.exec_()
        else:
            QMessageBox.critical(self.mainWindow, u"提示", u"请在基站图层上选中1个要添加小区的基站")

    # 移动基站
    def moveSiteFunc(self):
        # 判断是否只选中了一个基站
        if isSelectedASite(self.iface):
            ui = MoveSiteUI(self.iface, self.mainWindow)
            ui.show()
            ui.exec_()
        else:
            QMessageBox.critical(self.mainWindow, u"提示", u"请在基站图层上选中1个要添加小区的基站")

    # 删除基站和小区
    def delSiteFunc(self):
        ui = DeleteSiteUI(self.iface, self.mainWindow)

    # 修改小区方向
    def modifyAzimuthFunc(self):
        ui = ModifyAzimuthUI(self.iface, self.mainWindow)
        ui.show()
        ui.exec_()

    # 查找基站小区
    def searchFunc(self):
        ui = SearchUI(self.iface, self.mainWindow)
        ui.show()
        ui.exec_()

    # 设置服务小区并显示其相邻小区
    def showNCellFunc(self):
        self.SCell_list, self.HL_SCell = getSCell(self.iface, self.HL_SCell, self.mainWindow)
        # 判断选中的服务小区是否唯一
        if len(self.SCell_list) == 0:
            QMessageBox.critical(self.mainWindow, u"错误", u"请先设置服务小区！")
            return
        elif len(self.SCell_list) > 1:
            QMessageBox.critical(self.mainWindow, u"错误", u"只能选择一个小区作为服务小区！")
            return
        else:
            showSCell = SCellControls(self.iface, self.SCell_list[0], self.HL_NCell_O, self.HL_NCell_D)
            showSCell.showCellFeature()

    # 增加单向相邻小区
    def addOneWayNCellFunc(self):
        addOneWaySCell(self.iface, self.SCell_list)

    # 增加双向相邻小区
    def addTwoWayNCellFunc(self):
        addTwoWaySCell(self.iface, self.SCell_list)

    # 删除选中的相邻小区
    def delNCellFunc(self):
        ui = DeleteNCellUI(self.iface, self.SCell_list, self.mainWindow)
        ui.show()
        ui.exec_()

    # 检查相邻小区的重复性，并自动修正
    def checkRepeatFunc(self):
        controls = SCellControls(self.iface)
        controls.checkRepeat()

    # 模三分析
    def mod3Func(self):
        if not self.cellStyle:
            # 如果没有对小区图层进行额外渲染
            cellLayer = getLayerByName(u"小区", self.iface)
            # 判断是否存在cellLayer
            if not cellLayer:
                QMessageBox.critical(self.mainWindow, u"错误", u"找不到小区图层， 请检查是否已初始化工程！")
                return
            self.cellStyleManager = QgsMapLayerStyleManager(cellLayer)
            self.cellStyleManager.addStyleFromLayer(u'默认')
        Mod3Render(self.iface, self.cellStyleManager, self.mainWindow)

    # 生成热力渲染图
    def createRenderFunc(self):
        # 判断是否对基站图层进行过额外渲染
        # if self.siteStyle:
        #     self.siteStyle, self.radius, self.quality = setDeafaultRender(self.iface, self._styleManager)
        self.siteStyle, self.radius, self.quality  = HeatRender(self.iface, self.siteStyle, self.radius, self.quality, self.mainWindow)

    # 向基站和进小区图层的相应字段添加选中Polygon属性
    def updatePolygonInfoFunc(self):
        layer = self.iface.activeLayer()
        if not layer:
            QMessageBox.critical(self.mainWindow, u'错误', u'<b>请选择要添加的Polygon图层<\b>')
        elif (layer.name() in [u"基站", u"小区", u"相邻小区"]):
            QMessageBox.critical(self.mainWindow, u'错误', u'<b>请选择要添加的Polygon图层<\b>')
        else:
            polygon = UpdatePolygonInfoUI(self.iface, self.mainWindow)
            polygon.show()
            polygon.exec_()

    # 按范围分类显示(针对数字)
    def rangeByNoFunc(self):
        ui = RangeByNoSettingUI(self.iface, self.mainWindow)
        ui.show()
        ui.exec_()

    # 按类别分类显示(针对字符)
    def rangeByStrFunc(self):
        ui = RangeByStrSettingUI(self.iface, self.mainWindow)
        ui.show()
        ui.exec_()

    # 自动规划基站
    def AutoBuildSiteFunc(self):
        dlg = AutoBuildSiteSettingDlg(self.iface, self.mainWindow)
        dlg.show()
        dlg.exec_()

    # 添加待选站点
    def addCandidateSiteFunc(self):
        add = AddNSitesUI(self.iface, self.mainWindow)
        add.show()
        add.exec_()

    # 快速PCI规划
    def quickPCIFunc(self):
        dlg = QuickPCISettingDlg(self.iface, self.mainWindow)
        dlg.show()
        dlg.exec_()

    # 精确PCI规划
    def accuratePCIFunc(self):
        dlg = AccuratePCISettingDlg(self.iface, self.mainWindow)
        dlg.show()
        dlg.exec_()

    # 生成KML图层
    def createKMLFunc(self):
        expKML = ExportDataToKMLUI(self.iface, self.mainWindow)
        expKML.show()
        expKML.exec_()

    # 导出站点到百度地图
    def createBaiduMapFunc(self):
        expBaidu = ExportDataToBaiduUI(self.iface, self.mainWindow)
        expBaidu.show()
        expBaidu.exec_()

    # 导出站点到腾讯地图
    def createTencentMapFunc(self):
        expTencent = ExportDataToTencentUI(self.iface, self.mainWindow)
        expTencent.show()
        expTencent.exec_()

    # 导出站点到搜狗地图
    def createSogotMapFunc(self):
        expSogo = ExportDataToSogoUI(self.iface, self.mainWindow)
        expSogo.show()
        expSogo.exec_()

    # 从百度地图中抓取地理信息
    def searchPOIFunc(self):
        ui = SearchPOIFromBaiduUI(self.iface, self.mainWindow)
        ui.show()
        ui.exec_()

    # 弹出帮助文档
    def HelpFunc(self):
        doc_path = os.path.join(cmd_folder, u"移动通信网络规划功能帮助文档.pdf")
        if os.path.exists(doc_path):
            os.startfile(doc_path)
        else:
            QMessageBox.critical(self.mainWindow, u"错误", u"帮助文档不存在，请联系管理员!")
