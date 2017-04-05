# -*- coding: utf-8 -*-
'''
导出数据函数
@author: Karwai Kwok
'''

import xlwt, traceback
from PyQt4.QtGui import QMessageBox
from MyQGIS.Contorls.LayerControls import getLayerFieldNames, getFeaturesDataBtLayer
from MyQGIS.gui.Progress import Progess

class ExportData(object):
    def __init__(self, iface, parent=None):
        super(ExportData, self).__init__()
        self.iface = iface
        self.parent = parent

    # 设置表格样式
    def set_style(self, height, bold=False, ishead=False, pattern_color_no=None):
        style = xlwt.XFStyle()

        font = xlwt.Font()
        font.bold = bold
        font.height = height
        bord = xlwt.Borders()
        if ishead:
            bord.left = 2
            bord.right = 2
            bord.top = 2
            bord.bottom = 2
            font.colour_index = 4
        else:
            bord.left = 1
            bord.right = 1
            bord.top = 1
            bord.bottom = 1

        align = xlwt.Alignment()
        align.vert = align.VERT_CENTER
        align.horz = align.HORZ_CENTER

        style.font = font
        style.borders = bord
        style.alignment = align

        # 设置单元格填充颜色
        if pattern_color_no != None:
            if type(pattern_color_no) == int:
                pattern_color = xlwt.Pattern()
                pattern_color.pattern = xlwt.Pattern.SOLID_PATTERN
                pattern_color.pattern_fore_colour = pattern_color_no
                style.pattern = pattern_color

        return style

    def exportDataToExcel(self, layer, saveFilePath):
        fieldsName_list = getLayerFieldNames(layer)
        datas = getFeaturesDataBtLayer(layer)
        if len(datas) >= 65500:
            QMessageBox.critical(self.parent, u"错误", u"该功能不支持导出超过65500条数据")
            return False
        progress = Progess(self.parent, len(datas), u"导出数据中")
        progress.show()
        try:
            wbk = xlwt.Workbook(style_compression=2)
            sheet = wbk.add_sheet(unicode(layer.name()), True)
            # 先写入表头
            for (i, itm)  in enumerate(fieldsName_list):
                sheet.write(0, i, itm, self.set_style(220, True, True))
            progress.count()
            # 写入数据
            if datas != None and len(datas) > 0:
                for (a, aitm) in enumerate(datas):
                    for (b, bitm) in enumerate(aitm):
                        sheet.write(a + 1, b, bitm, self.set_style(220, False, False))
                progress.count()
            wbk.save(saveFilePath)
            return True
        except Exception:
            raise Exception, traceback.format_exc()
        finally:
            progress.kill()
