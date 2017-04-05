# -*- coding: utf-8 -*-
'''
创建模板信息窗口
@author: Karwai Kwok
'''
from PyQt4.QtGui import QInputDialog, QMessageBox, QFileDialog
from MyQGIS.config.HeadsConfig import SelecType
from MyQGIS.config.EnumType import ExcelType
from MyQGIS.Contorls.FileControls import createModelFile

class CreateModelDlg(object):
    def __init__(self, iface, parent=None):
        super(CreateModelDlg, self).__init__()
        self.iface = iface
        self.parent = parent

    def show(self):
        (seType, ok) = QInputDialog.getItem(self.parent, u'创建模板',
                            u'需要创建的Excel文件模板', SelecType)
        if ok and (seType != None and seType.strip() != ''):
            if seType == SelecType[0]:
                mtype = ExcelType.SITEANDCELL
            elif seType == SelecType[1]:
                mtype = ExcelType.SERVINGCELL
            # elif seType == SelecType[2]:
            #     mtype = ExcelType.ANALYSITE
            # elif seType == SelecType[3]:
            #     mtype = ExcelType.PUSHSITE
            # elif seType == SelecType[4]:
            #     mtype = ExcelType.MERGESITE
            else:
                QMessageBox.critical(self.parent, u"错误", u"请重新选择要生成的模板!")
                return
            fileName = QFileDialog.getSaveFileName(self.parent, SelecType[mtype], SelecType[mtype]+u"数据.xls", 'Excel File (*.xls)')
            if fileName != None and fileName.strip() != '':
                if createModelFile(mtype, fileName):
                    QMessageBox.information(self.parent, u"生成模板文件", u"生成模板文件成功！")
                else:
                    QMessageBox.critical(self.parent, u"生成模板文件", u"生成模板文件失败！")

