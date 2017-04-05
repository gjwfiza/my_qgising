# -*- coding: utf-8 -*-
'''
删除基站交互界面
@author: Karwai Kwok
'''
from PyQt4.QtGui import QDialog, QMessageBox
from MyQGIS.Contorls.LayerControls import getLayerByName
from MyQGIS.Contorls.DeleteSite import deleteSite

class DeleteSiteUI(QDialog):
    def __init__(self, iface, parent=None):
        super(DeleteSiteUI, self).__init__()
        self.iface = iface
        self.parent = parent

        if self.checkIsSelectedFeatures():
            self.delete()
        else:
            QMessageBox.critical(self, u'错误', u'<b>请选择要删除的基站或小区!<\b>')
            self.accept()

    # 判断是否选中了要删除的基站或小区
    def checkIsSelectedFeatures(self):
        siteLayer = getLayerByName(u"基站", self.iface)  # 基站图层
        selected_site = siteLayer.selectedFeatures()
        cellLayer = getLayerByName(u"小区", self.iface)  # 小区图层
        selected_cell = cellLayer.selectedFeatures()
        if len(selected_site) == 0 and len(selected_cell) == 0:
            return False
        else:
            return True


    def delete(self):
        if deleteSite(self.iface):
            QMessageBox.information(self.parent, u"删除基站小区", u"删除基站小区成功！")
        else:
            QMessageBox.critical(self.parent, u"删除基站小区", u"删除基站小区失败！")
        self.accept()