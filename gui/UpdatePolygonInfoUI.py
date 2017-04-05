# -*- coding: utf-8 -*-
'''
向基站和小区图层更新Polygon属性交互界面
@author: Karwai Kwok
'''

from PyQt4.QtGui import QDialog, QLabel, QComboBox, QHBoxLayout, QGridLayout, \
    QVBoxLayout, QPushButton, QMessageBox
from PyQt4.QtCore import SIGNAL
from MyQGIS.Contorls.UpdatePolygonInfo import updatePolygonInfo

# 向基站和小区图层更新Polygon属性交互界面
class UpdatePolygonInfoUI(QDialog):
    def __init__(self, iface, parent=None):
        super(UpdatePolygonInfoUI, self).__init__()
        self.iface = iface
        self.parent = parent
        self.polygon_layer = self.iface.activeLayer()

        self.initUI()

    # 初始化界面
    def initUI(self):
        self.setWindowTitle(u"Polygon")

        polygon_id_label = QLabel(u'"Polygon" 来源： ')
        self.polygon_id = QComboBox()
        content_label = QLabel(u'"其他" 来源： ')
        self.content = QComboBox()
        fields = []
        for field in self.polygon_layer.pendingFields():
            fields.append(field.name().strip())
        self.polygon_id.addItems(fields)
        fields.insert(0, u"")
        self.content.addItems(fields)

        button_hbox = QHBoxLayout()
        button_hbox.addStretch(1)
        ok = QPushButton(u"确定")
        self.connect(ok, SIGNAL("clicked()"), self.run)
        button_hbox.addWidget(ok)
        cancel = QPushButton(u"取消")
        self.connect(cancel, SIGNAL("clicked()"), self.accept)
        button_hbox.addWidget(cancel)
        button_hbox.addStretch(1)

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(polygon_id_label, 0, 1)
        grid.addWidget(self.polygon_id, 0, 2)
        grid.addWidget(content_label, 1, 1)
        grid.addWidget(self.content, 1, 2)

        vbox = QVBoxLayout()
        vbox.setSpacing(10)
        vbox.addLayout(grid)
        vbox.addStretch(1)
        vbox.addLayout(button_hbox)

        self.setLayout(vbox)
        self.resize(300, 120)

    # 确定按钮监听事件
    def run(self):
        polygon_id_field = self.polygon_id.currentText().strip()
        content_field = self.content.currentText().strip()
        result = updatePolygonInfo(self.iface, self.polygon_layer,
                                   polygon_id_field, content_field, self)
        if result:
            QMessageBox.information(self, u"更新Polygon属性", u"更新相关字段成功!")
        else:
            QMessageBox.critical(self, u"更新Polygon属性", u"更新相关字段失败!")
        self.accept()
