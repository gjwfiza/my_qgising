# -*- coding: utf-8 -*-
'''
删除相邻小区确认窗口
@author: Karwai Kwok
'''
from PyQt4.QtGui import QDialog, QLabel, QMessageBox, \
        QHBoxLayout, QPushButton, QVBoxLayout
from PyQt4.QtCore import SIGNAL
from MyQGIS.Contorls.SCellControls import SCellControls, getSCellName

class DeleteNCellUI(QDialog):
    def __init__(self, iface, SCell_list, parnet=None):
        super(DeleteNCellUI, self).__init__()
        self.iface = iface
        self.parent = parnet

        self.SCell = SCell_list[0]
        self.SCell_Name = getSCellName(self.iface, SCell_list)
        self.initUI()

    # 初始化界面
    def initUI(self):
        self.setWindowTitle(u"删除相邻小区")

        delete_btn = QPushButton(u"删除")
        self.connect(delete_btn, SIGNAL('clicked()'), self.delete)
        cancel_btn = QPushButton(u"取消")
        self.connect(cancel_btn, SIGNAL('clicked()'), self.reject)
        hbox = QHBoxLayout()
        hbox.addStretch(2)
        hbox.addWidget(delete_btn)
        hbox.addStretch(1)
        hbox.addWidget(cancel_btn)
        hbox.addStretch(2)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        confirm_label = QLabel(u"是否要删除   <b>" + self.SCell_Name + u"</b>  与所选小区的切换关系？")
        vbox.addWidget(confirm_label)
        vbox.addStretch(2)
        vbox.addLayout(hbox)
        vbox.addStretch(1)
        self.setLayout(vbox)

    # 删除按钮绑定事件
    def delete(self):
        self.accept()
        scellControls = SCellControls(self.iface, self.SCell)
        '''判断是否选中小区图层'''
        if scellControls.checkSelectLayer():
            '''判断是否选中要删除的小区'''
            if scellControls.checkSelectFeature():
                '''删除选中的小区，并返回布尔值'''
                if scellControls.delCellFeature():
                    QMessageBox.information(self, u'删除成功', u'已删除所选的相邻小区')
                    return True
                else:
                    QMessageBox.critical(self, u'错误', u'删除相邻小区失败')
                    return False
            else:
                QMessageBox.critical(self, u'错误', u'请选中要删除的小区')
                return False
        else:
            QMessageBox.critical(self, u'错误', u'请选中小区图层')
            return False
