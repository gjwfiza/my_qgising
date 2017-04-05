# -*- coding: utf-8 -*-
'''
导出数据信息窗口
@author: Karwai Kwok
'''
from PyQt4.QtGui import QInputDialog, QFileDialog, QMessageBox
from MyQGIS.Contorls.LayerControls import getAllLayerName, getLayerByName
from MyQGIS.Contorls.ExportData import ExportData

class ExportDataUI(object):
    def __init__(self, iface, parent=None):
        super(ExportDataUI, self).__init__()
        self.iface = iface
        self.parent = parent

    def show(self):
        allLayerNames = getAllLayerName(self.iface)
        (layerName, ok) = QInputDialog.getItem(self.parent, u'导出数据',
                            u'选择要导出的数据图层', allLayerNames)

        if ok and (layerName != None and layerName != ''):
            layer = getLayerByName(layerName, self.iface)
            saveFileName = QFileDialog.getSaveFileName(self.parent, u"导出数据",
                                '/', 'Excel File (*.xls)')
            if saveFileName.strip() != "":
                exportData = ExportData(self.iface, self.parent)
                if exportData.exportDataToExcel(layer, saveFileName):
                    QMessageBox.information(self.parent, u"导出数据", u"导出数据成功！")
                else:
                    QMessageBox.critical(self.parent, u"导出数据", u"导出数据失败！")
