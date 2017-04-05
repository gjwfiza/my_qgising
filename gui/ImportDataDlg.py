# -*- coding: utf-8 -*-
'''
导入数据信息窗口
@author: Karwai Kwok
'''

from PyQt4.QtCore import QObject, SIGNAL, Qt, QThread
from PyQt4.QtGui import QIcon, QTableWidget, QListWidget, QPushButton, \
    QVBoxLayout, QHBoxLayout, QStatusBar, QTableWidgetItem, QFileDialog, QDialog, \
    QAbstractItemView, QListWidgetItem, QToolBar, QAction, QComboBox, \
    QMessageBox, QMenu
from MyQGIS.config.EnumType import ImpDateType, LayerType
from MyQGIS.config import HeadsConfig
from MyQGIS.Contorls.LayerControls import getLayerByName
from MyQGIS.Contorls.ImportData import GetDataFromExcel, ImportDataToLayer
from MyQGIS.Contorls.DataValidation import checkDataByDataType

class ImportDataDlg(QDialog):
    __isJy = False  # 数据校验成功的标志
    __mlist = []  # 定义一个列表用于保存从excel表中取出的数据

    def __init__(self, iface, parent=None, impType=ImpDateType.SITEANDCELL):
        super(ImportDataDlg, self).__init__()
        self.iface = iface
        self.parent = parent
        self.impType = impType
        self.initView()



    def initView(self):
        if self.impType == ImpDateType.SERVINGCELL:
            self.setWindowTitle(u'相邻小区数据导入')
        else:
            self.setWindowTitle(u'基站和小区数据导入')
        self.setWindowIcon(QIcon('images/logo.png'))
        self.resize(620, 480)

        # 数据表格
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setRowCount(7)
        # 设置当前Table不能编辑
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 初始化表格上下文菜单
        self.initTableContextMenu()
        # 初始化表头
        self.initTableHeader()
        # 导入出错列表
        self.listWidget = QListWidget(self)
        # 按钮组
        impBtn = QPushButton(u"导入EXCEL表", self)
        yzBtn = QPushButton(u"数据检验", self)
        impdateBtn = QPushButton(u"导入数据", self)
        btnVBox = QVBoxLayout()
        btnVBox.addWidget(impBtn)
        btnVBox.addWidget(yzBtn)
        btnVBox.addWidget(impdateBtn)
        # 错误列表与按钮组
        hBox = QHBoxLayout()
        hBox.setMargin(20)
        hBox.addWidget(self.listWidget)
        hBox.addLayout(btnVBox)

        self.mbar = QStatusBar(self)
        self.mbar.showMessage(u'准备就绪...')

        self.maction = QToolBar(self)
        self.editAction = QAction(u'编辑', self.maction)
        self.editAction.setCheckable(True)

        self.combox = QComboBox(self)
        self.combox.addItems(HeadsConfig.ImpExcelName)

        self.maction.addWidget(self.combox)
        self.maction.addAction(self.editAction)

        vBox = QVBoxLayout()
        vBox.addWidget(self.maction)
        vBox.addWidget(self.tableWidget)
        vBox.addLayout(hBox)
        vBox.addWidget(self.mbar)

        vBox.setStretchFactor(self.tableWidget, 9)
        vBox.setStretchFactor(hBox, 5)
        vBox.setStretchFactor(self.mbar, 1)

        self.setLayout(vBox)

        QObject.connect(impBtn, SIGNAL('clicked()'), self.impClick)
        QObject.connect(yzBtn, SIGNAL('clicked()'), self.yzClick)
        QObject.connect(impdateBtn, SIGNAL('clicked()'), self.impdateClick)
        QObject.connect(self.editAction, SIGNAL('triggered()'), self.editClick)
        QObject.connect(self.combox, SIGNAL('currentIndexChanged(int)'), self.comboxChange)

        self.listWidget.doubleClicked.connect(self.mlistClicked)
        # self.connect(self.listWidget, SIGNAL("itemDoubleClicked (QListWidgetItem)"), self.mlistClicked)

    def initTableContextMenu(self):
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.popMenu = QMenu(self.tableWidget)
        delAction = QAction(u'删除', self)  # 删除
        self.popMenu.addAction(delAction)

    # 设置表格可以双击修改数据
    def setEditTriggers(self, isTrigger):
        if isTrigger:
            self.tableWidget.setEditTriggers(QAbstractItemView.DoubleClicked)
        else:
            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

    # 提供给外部修改状态栏消息
    def setStatusBarMsg(self, msg):
        self.mbar.showMessage(msg)

    # 选框改变时，清空当前表格的全部内容，包括表格头
    def updateType(self, mtype):
        self.impType = mtype
        self.tableWidget.clear()  # 清空表格所有内容
        self.initTableHeader()

    # 初始化表格的每个Item
    def initTable(self, mlist):
        self.tableWidget.setRowCount(len(mlist))
        for (i, v) in enumerate(mlist):
            for (j, item) in enumerate(v):
                if type(item) != str:
                    item = unicode(item)
                if item == None:
                    item = u""
                tabItem = QTableWidgetItem(item)
                tabItem.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(i, j, tabItem)

    # 初始化错误信息列表
    def initListView(self, mlist):

        for iv in mlist:
            lisItm = QListWidgetItem(self.listWidget)
            lisItm.setTextColor(Qt.red)
            lisItm.setData(Qt.UserRole, iv)
            if isinstance(iv, basestring):
                # 如果错误信息是一行字符串
                lisItm.setText(iv)
            else:
                lisItm.setText(
                    u'第' + unicode(str(iv['row'] + 1)) + u'行，第' + unicode(str(iv['col'] + 1)) + u'列：' + iv['msg'])

    # 初始化Table的头
    def initTableHeader(self):
        self.heads = []
        if self.impType == ImpDateType.SITEANDCELL:
            # 获取当前项目图层的字段名
            cell_layer = getLayerByName(u"小区", self.iface)
            for head in HeadsConfig.SiteANDCellHead:
                self.heads.append(head)
            if len(cell_layer.pendingFields()) > 55:
                for (index, field) in enumerate(cell_layer.pendingFields()):
                    if index > 54:
                        field_name = field.name().strip()
                        self.heads.append(field_name)

        else:
            self.heads = HeadsConfig.ServingCellHead

        self.tableWidget.setColumnCount(len(self.heads))  # 设置表格的列数
        for (i, h) in enumerate(self.heads):
            tabItem = QTableWidgetItem(h)
            self.tableWidget.setHorizontalHeaderItem(i, tabItem)

    # 自定义为Table添加Item
    def addTableItem(self, row, col, content):
        tabItem = QTableWidgetItem(content)
        self.tableWidget.setItem(row, col, tabItem)

    # 修改Item的内容
    def editTableItem(self, row, col, content):
        tabItem = self.tableWidget.item(row, col)
        tabItem.setText(content)
        self.tableWidget.setItem(row, col, tabItem)

    # 从Excel表读取数据（导入Excel表）
    def impClick(self):
        fileName = QFileDialog.getOpenFileName(self, u'基站小区数据导入', '/', 'Excel Files (*.xls *.xlsx)')
        if fileName.strip() != "":
            self.setStatusBarMsg(u'选择完毕：' + fileName)
            importData = GetDataFromExcel(fileName, self.impType, self.heads)
            self.__mlist = []
            self.__mlist.extend(importData.getData())
            self.tableWidget.clearContents()
            self.listWidget.clear()
            self.initTable(self.__mlist)
            self.setStatusBarMsg(u'数据导入完成...')
            self.__isJy = False  # 导入完数据后，说明需要重新验证数据的正确性

        else:
            QMessageBox.information(self.parent, u"错误", u"请选中文件")

    # 数据验证按钮点击事件处理
    def yzClick(self):
        if len(self.__mlist) > 0:
            self.erlist = []  # 定义一个列表用于保存数据验证错误的数据
            # 清楚全部的Item
            if self.listWidget.count() > 0:
                self.listWidget.clear()

            # 根据tableWidget更新self.__mlist
            for (r, items) in enumerate(self.__mlist):
                for (v, item) in enumerate(self.__mlist[r]):
                    if self.tableWidget.item(r, v).text() == u"":
                        continue
                    else:
                        # 跟据self.__mlist[r][v]数据类型进行比对
                        if type(self.__mlist[r][v]) == int:
                            if unicode(self.__mlist[r][v]) != (self.tableWidget.item(r, v).text()):
                                self.__mlist[r][v] = int(self.tableWidget.item(r, v).text())
                        elif type(self.__mlist[r][v]) == float:
                            if unicode(self.__mlist[r][v]) != (self.tableWidget.item(r, v).text()):
                                self.__mlist[r][v] = float(self.tableWidget.item(r, v).text())
                        elif type(self.__mlist[r][v]) == str:
                            if unicode(self.__mlist[r][v]) != self.tableWidget.item(r, v).text():
                                self.__mlist[r][v] = str(self.tableWidget.item(r, v).text())
                        elif type(self.__mlist[r][v]) == unicode:
                            if (self.__mlist[r][v]) != self.tableWidget.item(r, v).text():
                                self.__mlist[r][v] = self.tableWidget.item(r, v).text()
                        else:
                            print type(self.__mlist[r][v])
            # 执行数据校验函数
            self.erlist = checkDataByDataType(self.__mlist, self.impType)
            if len(self.erlist) > 0:
                self.initListView(self.erlist)
                QMessageBox.information(self.parent, u'数据校验', u'数据校验失败，请检查数据正确性后，再导入到地图中')
                self.__isJy = False
            else:
                QMessageBox.information(self.parent, u'数据校验', u'数据校验成功，没有错误数据')
                self.__isJy = True
        else:
            QMessageBox.warning(self.parent, u'数据校验', u'请先导入Excel数据后再操作！')

    # 导入数据到地图中
    def impdateClick(self):
        if self.__isJy:  # 如果数据校验成功
            if self.impType == ImpDateType.SITEANDCELL:
                # 导入基站小区
                importDataToLayer = ImportDataToLayer(self.iface, self.__mlist, self.parent)
                if importDataToLayer.importSiteAndCellData():
                    QMessageBox.information(self.parent, u"导入数据", u"导入数据成功！")
                else:
                    QMessageBox.critical(self.parent, u"导入数据", u"导入数据失败！")

            else:
                # 导入相邻小区
                importDataToLayer = ImportDataToLayer(self.iface, self.__mlist, self.parent)
                if importDataToLayer.importSCellData():
                    QMessageBox.information(self.parent, u"导入数据", u"导入数据成功！")
                else:
                    QMessageBox.critical(self.parent, u"导入数据", u"导入数据失败！")
        else:
            QMessageBox.warning(self.parent, u'数据导入', u'请确保校验数据成功后，再导入到地图中')

    # 编辑Action点击事件
    def editClick(self):
        self.setEditTriggers(self.editAction.isChecked())

    # 错误列表双击事件处理
    def mlistClicked(self, listItem):
        itemData = listItem.data(Qt.UserRole)
        self.tableWidget.setFocus()
        self.tableWidget.setCurrentCell(itemData['row'], itemData['col'])

    # 选框改变事件
    def comboxChange(self, index):
        self.updateType(index)

    # 字段验证是否为空
    def __validNull(self, name, col, row, itm, rowitm):
        if itm is None or itm == '':
            tmpMap = {}
            tmpMap['col'] = col
            tmpMap['row'] = row
            tmpMap['msg'] = unicode(name) + u'不能为空'
            tmpMap['item'] = rowitm
            return tmpMap
        else:
            return None

    # 导入数据线程开始信号  绑定函数
    def impStart(self):
        self.setStatusBarMsg(u'准备导入...')

    # 导入数据线程发生异常信号 绑定函数
    def impError(self, e, exception_string):
        self.setStatusBarMsg(u'发生错误：' + unicode(e))
        QMessageBox.warning(self.parent, u'Excel数据导入', u'发生错误：' + unicode(e))

    # 导入数据线程完成信号 绑定函数
    def impFinish(self, mylist):
        self.__mlist = []
        self.__mlist.extend(mylist)
        self.mthread.quit()
        self.mthread.wait()
        self.mthread.deleteLater()
        self.impDateThread.deleteLater()

        self.tableWidget.clearContents()
        self.listWidget.clear()
        self.initTable(self.__mlist)
        self.setStatusBarMsg(u'数据导入完成...')
        self.__isJy = False  # 导入完数据后，说明需要重新验证数据的正确性

    # 导入数据到地图线程发生异常信号 绑定函数
    def impError1(self, e, exception_string):
        self.setStatusBarMsg(u"导入数据发生错误");
        QMessageBox.critical(self, u'数据导入', u"发生错误：" + unicode(e))

    # 导入数据到地图线程完成信号 绑定函数
    def impFinish1(self, mylist):
        self.threadImp.quit()
        self.threadImp.wait()
        self.threadImp.deleteLater()
        self.impFeatureThread.deleteLater()
        remsg = u'数据导入完成！';
        layer = None
        if self.impType == LayerType.SITE:
            # remsg = u'基站' + remsg
            layer = getLayerByName(u'基站', self.iface)
        elif self.impType == LayerType.CELL:
            # remsg = u'小区' + remsg
            layer = getLayerByName(u'小区', self.iface)
        else:
            remsg = u'相邻小区' + remsg
            layer = getLayerByName(u'相邻小区', self.iface)
        self.setStatusBarMsg(remsg)
        layer.updateExtents()  # 更新地图数据
        self.iface.actionDraw().trigger()
        QMessageBox.information(self, u'数据导入', remsg)

        merlist = []
        for eritm in self.erlist:
            merlist.append(eritm['item'])
        self.tableWidget.clearContents()  # 先清楚表格的内容，再将错误的行显示到表格中
        self.initTable(merlist)

