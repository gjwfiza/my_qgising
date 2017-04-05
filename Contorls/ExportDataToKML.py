# -*- coding:utf-8 -*-
'''
导出数据到KML操作函数
@author: Karwai Kwok
'''
import traceback, codecs
from MyQGIS.config.EnumType import KMLType
from MyQGIS.config.HeadsConfig import KMLHead
from MyQGIS.gui.Progress import Progess

# 导出数据到KML执行函数
def exportDataToKML(filename='',type=KMLType.Site, fields=[], datas=None, parent=None):
    result = False
    try:
        file = codecs.open(filename, 'w', 'utf-8')
        KML = KMLForm(parent, filename, type, fields, datas)
        (result, outputs) = KML.create()
        file.write(outputs)
        file.close()
    except Exception as e:
        raise traceback.format_exc()
    finally:
        return result

# 构建KML文件主体类
class KMLForm(object):
    # type 要导出的图层（0：基站， 1：小区， 2：基站+小区）
    # filehead 传入数据的字段名称
    def __init__(self, parent, filename, type, fields, datas):
        self.parent = parent
        self.filename = filename
        self.type = type
        if self.type == KMLType.Site:
            self.site_names = datas[0]
            self.site_datas = datas[1]
            self.site_points = datas[2]
            self.site_fields = fields
        elif self.type == KMLType.Cell:
            self.cell_names = datas[0]
            self.cell_datas = datas[1]
            self.cell_points = datas[2]
            self.cell_infos = datas[3]
            self.cell_fields = fields
        elif self.type == KMLType.SiteAndCell:
            self.site_names = datas[0][0]
            self.site_datas = datas[0][1]
            self.site_points = datas[0][2]
            self.cell_names = datas[1][0]
            self.cell_datas = datas[1][1]
            self.cell_points = datas[1][2]
            self.cell_infos = datas[1][3]
            self.site_fields = fields[0]
            self.cell_fields = fields[1]
        self.fields = fields


    def create(self):
        try:
            outputs = None
            head = u'<?xml version="1.0" encoding="utf-8" ?>'
            Schema_label = KMLLabel('Schema')
            Schema_label.setAttribute(('name', self.filename))

            for (field, type) in KMLHead.items():
                SimpleField_label = KMLLabel('SimpleField')
                SimpleField_label.setAttribute(('name', field), ('type', type))
                SimpleField = SimpleField_label.create()
                Schema_label.addLabel(SimpleField)
            Schema = Schema_label.create()
            Document_label = KMLLabel('Document')
            Document_label.addLabel(Schema)

            # 基站
            if self.type == KMLType.Site:
                # 生成进度条
                total = len(self.site_datas) + 1
                progess = Progess(self.parent, total)
                progess.show()

                Folder_label = KMLLabel('Folder')
                name_label = KMLLabel('name')
                name_label.createTextNode(u"基站")
                name = name_label.create()
                Folder_label.addLabel(name)

                for (i, feature) in enumerate(self.site_datas):
                    Placemark_label = KMLLabel('Placemark')
                    ExtendedData_label = KMLLabel('ExtendedData')
                    SchemaData_label = KMLLabel('SchemaData')
                    SchemaData_label.setAttribute(('schemaUrl', u'#'+self.filename))
                    for (j, data) in enumerate(feature):
                        SimpleData_label = KMLLabel('SimpleData')
                        SimpleData_label.setAttribute(('name', self.site_fields[j]))
                        if data != None:
                            SimpleData_label.createTextNode(data)
                        else:
                            SimpleData_label.createTextNode('NULL')
                        SimpleData = SimpleData_label.create()
                        SchemaData_label.addLabel(SimpleData)
                    SchemaData = SchemaData_label.create()
                    ExtendedData_label.addLabel(SchemaData)
                    ExtendedData = ExtendedData_label.create()
                    Point_label = KMLLabel('Point')
                    coordinates_label = KMLLabel('coordinates')
                    coordinates_label.createTextNode(str(self.site_points[i][0]) + ',' + str(self.site_points[i][1]))
                    coordinates = coordinates_label.create()
                    Point_label.addLabel(coordinates)
                    Point = Point_label.create()
                    Sitename_label = KMLLabel('name')
                    Sitename_label.createTextNode(self.site_names[i])
                    sitename = Sitename_label.create()

                    Style_label = KMLLabel('Style')
                    labelScale_label = KMLLabel('labelScale')
                    labelScale_label.createTextNode('0.7')
                    labelScale = labelScale_label.create()
                    Style_label.addLabel(labelScale)
                    Style = Style_label.create()
                    Placemark_label.addLabel(Style)

                    Placemark_label.addLabel(sitename)
                    Placemark_label.addLabel(ExtendedData)
                    Placemark_label.addLabel(Point)
                    Placemark = Placemark_label.create()
                    Folder_label.addLabel(Placemark)
                    # 更新进度
                    progess.count()
                Folder = Folder_label.create()
                Document_label.addLabel(Folder)
                # 更新进度
                progess.count()

            #小区
            elif self.type == KMLType.Cell:
                # 生成进度条
                total = len(self.cell_infos) + 1 + len(self.cell_datas) + 2
                progess = Progess(self.parent, total)
                progess.show()

                Folder_label = KMLLabel('Folder')
                name_label = KMLLabel('name')
                name_label.createTextNode(u'小区')
                name = name_label.create()
                Folder_label.addLabel(name)

                # 小区信息
                Folder1_label = KMLLabel('Folder')
                name_label = KMLLabel('name')
                name_label.createTextNode(u'小区信息')
                name = name_label.create()
                Folder1_label.addLabel(name)
                for infos in self.cell_infos:
                    Placemark_label = KMLLabel('Placemark')
                    name_label = KMLLabel('name')
                    if infos[0] != None:
                        name_label.createTextNode(infos[0])
                    else:
                        name_label.createTextNode(u'无')
                    name = name_label.create()
                    Placemark_label.addLabel(name)
                    # 设置样式
                    Style_label = KMLLabel('Style')
                    # 设置IconStyle
                    IconStyle_label = KMLLabel('IconStyle')
                    # 把小区信息的图标设置为无图标模式
                    Icon_label = KMLLabel('Icon')
                    Icon = Icon_label.create()
                    IconStyle_label.addLabel(Icon)
                    IconStyle = IconStyle_label.create()
                    Style_label.addLabel(IconStyle)

                    # 设置LabelStyle
                    LabelStyle_label = KMLLabel('LabelStyle')
                    # 把label比例修改为0.7
                    labelScale_label = KMLLabel('labelScale')
                    labelScale_label.createTextNode('0.7')
                    labelScale = labelScale_label.create()
                    LabelStyle_label.addLabel(labelScale)
                    # 设置label颜色
                    color_label = KMLLabel('color')
                    color_label.createTextNode('ff7fffaa')
                    color = color_label.create()
                    LabelStyle_label.addLabel(color)
                    LabelStyle = LabelStyle_label.create()
                    # 设置LabelStyle到Style_label
                    Style_label.addLabel(LabelStyle)
                    Style = Style_label.create()
                    Placemark_label.addLabel(Style)

                    styleUrl_label = KMLLabel('styleUrl')
                    styleUrl_label.createTextNode('#onlytextname')
                    styleUrl = styleUrl_label.create()
                    Placemark_label.addLabel(styleUrl)
                    Point_label = KMLLabel('Point')
                    extrude_label = KMLLabel('extrude')
                    extrude_label.createTextNode(1)
                    extrude = extrude_label.create()
                    Point_label.addLabel(extrude)
                    altitudeMode_label = KMLLabel('altitudeMode')
                    altitudeMode_label.createTextNode('relativeToGround')
                    altitudeMode = altitudeMode_label.create()
                    Point_label.addLabel(altitudeMode)
                    coordinates_label = KMLLabel('coordinates')
                    coordinates_label.createTextNode(str(infos[1]) + ',' + str(infos[2]) + ',' + '0')
                    coordinates = coordinates_label.create()
                    Point_label.addLabel(coordinates)
                    Point = Point_label.create()
                    Placemark_label.addLabel(Point)
                    Placemark = Placemark_label.create()
                    Folder1 = Folder1_label.addLabel(Placemark)
                    # 更新进度
                    progess.count()
                Folder1 = Folder1_label.create()
                Folder_label.addLabel(Folder1)
                # 更新进度
                progess.count()

                # 小区图形
                Folder2_label = KMLLabel('Folder')
                name_label = KMLLabel('name')
                name_label.createTextNode(u'小区图形')
                name = name_label.create()
                Folder2_label.addLabel(name)
                for (i, feature) in enumerate(self.cell_datas):
                    Placemark_label = KMLLabel('Placemark')
                    ExtendedData_label = KMLLabel('ExtendedData')
                    SchemaData_label = KMLLabel('SchemaData')
                    SchemaData_label.setAttribute(('schemaUrl', u'#'+self.filename))
                    for (j, data) in enumerate(feature):
                        SimpleData_label = KMLLabel('SimpleData')
                        SimpleData_label.setAttribute(('name', self.cell_fields[j]))
                        if data != None:
                            SimpleData_label.createTextNode(data)
                        else:
                            SimpleData_label.createTextNode('NULL')
                        SimpleData = SimpleData_label.create()
                        SchemaData_label.addLabel(SimpleData)
                    SchemaData = SchemaData_label.create()
                    ExtendedData_label.addLabel(SchemaData)
                    ExtendedData = ExtendedData_label.create()
                    Polygon_label = KMLLabel('Polygon')
                    altitudeMode_label = KMLLabel('altitudeMode')
                    altitudeMode_label.createTextNode('relativeToGround')
                    altitudeMode = altitudeMode_label.create()
                    Polygon_label.addLabel(altitudeMode)
                    outerBoundaryIs_label = KMLLabel('outerBoundaryIs')
                    LinearRing_label = KMLLabel('LinearRing')
                    LinearRing_label.addLabel(altitudeMode)
                    coordinates_label = KMLLabel('coordinates')
                    for cell_points in self.cell_points[i]:
                        for cell_point in cell_points:
                            coordinates_label.createTextNode(str(cell_point[0]) + ',' + str(cell_point[1]) + ' ')
                    coordinates = coordinates_label.create()
                    LinearRing_label.addLabel(coordinates)
                    LinearRing = LinearRing_label.create()
                    outerBoundaryIs_label.addLabel(LinearRing)
                    outerBoundaryIs = outerBoundaryIs_label.create()
                    Polygon_label.addLabel(outerBoundaryIs)
                    Polygon = Polygon_label.create()
                    Cellname_label = KMLLabel('name')
                    Cellname_label.createTextNode(self.cell_names[i])
                    cellname = Cellname_label.create()
                    Placemark_label.addLabel(cellname)
                    Style_label = KMLLabel('Style')
                    LineStyle_label = KMLLabel('LineStyle')
                    color_label = KMLLabel('color')
                    color_label.createTextNode('ff0000ff')
                    color = color_label.create()
                    LineStyle_label.addLabel(color)
                    # 将线的宽度定义为2
                    width_label = KMLLabel('width')
                    width_label.createTextNode('2')
                    width = width_label.create()
                    LineStyle_label.addLabel(width)

                    LineStyle = LineStyle_label.create()
                    Style_label.addLabel(LineStyle)
                    PolyStyle_label = KMLLabel('PolyStyle')
                    fill_label = KMLLabel('fill')
                    fill_label.createTextNode('0')
                    fill = fill_label.create()
                    PolyStyle_label.addLabel(fill)
                    PolyStyle = PolyStyle_label.create()
                    Style_label.addLabel(PolyStyle)
                    Style = Style_label.create()
                    Placemark_label.addLabel(Style)
                    Placemark_label.addLabel(ExtendedData)
                    Placemark_label.addLabel(Polygon)
                    Placemark = Placemark_label.create()
                    Folder2_label.addLabel(Placemark)
                    # 更新进度
                    progess.count()
                Folder2 = Folder2_label.create()
                Folder_label.addLabel(Folder2)
                # 更新进度
                progess.count()

                Folder = Folder_label.create()
                Document_label.addLabel(Folder)
                # 更新进度
                progess.count()

            # 基站+小区
            else:
                # 生成进度条
                total = len(self.site_datas) + 1 + len(self.cell_infos) + 1 + len(self.cell_datas) + 2
                progess = Progess(self.parent, total)
                progess.show()
                # 基站
                Folder_label = KMLLabel('Folder')
                name_label = KMLLabel('name')
                name_label.createTextNode(u'基站')
                name = name_label.create()
                Folder_label.addLabel(name)

                for (i, feature) in enumerate(self.site_datas):
                    Placemark_label = KMLLabel('Placemark')
                    ExtendedData_label = KMLLabel('ExtendedData')
                    SchemaData_label = KMLLabel('SchemaData')
                    SchemaData_label.setAttribute(('schemaUrl', u'#'+self.filename))
                    for (j, data) in enumerate(feature):
                        SimpleData_label = KMLLabel('SimpleData')
                        SimpleData_label.setAttribute(('name', self.site_fields[j]))
                        if data != None:
                            SimpleData_label.createTextNode(data)
                        else:
                            SimpleData_label.createTextNode('NULL')
                        SimpleData = SimpleData_label.create()
                        SchemaData_label.addLabel(SimpleData)
                    SchemaData = SchemaData_label.create()
                    ExtendedData_label.addLabel(SchemaData)
                    ExtendedData = ExtendedData_label.create()
                    Point_label = KMLLabel('Point')
                    coordinates_label = KMLLabel('coordinates')
                    coordinates_label.createTextNode(str(self.site_points[i][0]) + ',' + str(self.site_points[i][1]))
                    coordinates = coordinates_label.create()
                    Point_label.addLabel(coordinates)
                    Point = Point_label.create()
                    Sitename_label = KMLLabel('name')
                    Sitename_label.createTextNode(self.site_names[i])
                    sitename = Sitename_label.create()
                    # 将名字显示比例设置为0.7
                    Style_label = KMLLabel('Style')
                    labelScale_label = KMLLabel('labelScale')
                    labelScale_label.createTextNode('0.7')
                    labelScale = labelScale_label.create()
                    Style_label.addLabel(labelScale)
                    Style = Style_label.create()
                    Placemark_label.addLabel(Style)

                    Placemark_label.addLabel(sitename)
                    Placemark_label.addLabel(ExtendedData)
                    Placemark_label.addLabel(Point)
                    Placemark = Placemark_label.create()
                    Folder_label.addLabel(Placemark)
                    # 更新进度
                    progess.count()
                Folder = Folder_label.create()
                Document_label.addLabel(Folder)
                # 更新进度
                progess.count()

                # 小区
                Folder_label = KMLLabel('Folder')
                name_label = KMLLabel('name')
                name_label.createTextNode(u'小区')
                name = name_label.create()
                Folder_label.addLabel(name)
                # 小区信息
                Folder1_label = KMLLabel('Folder')
                name_label = KMLLabel('name')
                name_label.createTextNode(u'小区信息')
                name = name_label.create()
                Folder1_label.addLabel(name)
                for infos in self.cell_infos:
                    Placemark_label = KMLLabel('Placemark')
                    name_label = KMLLabel('name')
                    if infos[0] != None:
                        name_label.createTextNode(infos[0])
                    else:
                        name_label.createTextNode(u'无')
                    name = name_label.create()

                    Style_label = KMLLabel('Style')

                    # 把小区信息的图标设置为无图标模式
                    IconStyle_label = KMLLabel('IconStyle')
                    Icon_label = KMLLabel('Icon')
                    Icon = Icon_label.create()
                    IconStyle_label.addLabel(Icon)
                    IconStyle = IconStyle_label.create()
                    Style_label.addLabel(IconStyle)

                    # 设置LabelStyle
                    LabelStyle_label = KMLLabel('LabelStyle')
                    # 把label比例修改为0.7
                    labelScale_label = KMLLabel('labelScale')
                    labelScale_label.createTextNode('0.7')
                    labelScale = labelScale_label.create()
                    LabelStyle_label.addLabel(labelScale)
                    # 设置label颜色
                    color_label = KMLLabel('color')
                    color_label.createTextNode('ff7fffaa')
                    color = color_label.create()
                    LabelStyle_label.addLabel(color)
                    LabelStyle = LabelStyle_label.create()
                    # 设置LabelStyle到Style_label
                    Style_label.addLabel(LabelStyle)

                    Style = Style_label.create()
                    Placemark_label.addLabel(Style)

                    Style = Style_label.create()
                    Placemark_label.addLabel(Style)

                    Placemark_label.addLabel(name)
                    styleUrl_label = KMLLabel('styleUrl')
                    styleUrl_label.createTextNode('#onlytextname')
                    styleUrl = styleUrl_label.create()
                    Placemark_label.addLabel(styleUrl)
                    Point_label = KMLLabel('Point')
                    extrude_label = KMLLabel('extrude')
                    extrude_label.createTextNode(1)
                    extrude = extrude_label.create()
                    Point_label.addLabel(extrude)
                    altitudeMode_label = KMLLabel('altitudeMode')
                    altitudeMode_label.createTextNode('relativeToGround')
                    altitudeMode = altitudeMode_label.create()
                    Point_label.addLabel(altitudeMode)
                    coordinates_label = KMLLabel('coordinates')
                    coordinates_label.createTextNode(str(infos[1]) + ',' + str(infos[2]) + ',' + '0')
                    coordinates = coordinates_label.create()
                    Point_label.addLabel(coordinates)
                    Point = Point_label.create()
                    Placemark_label.addLabel(Point)
                    Placemark = Placemark_label.create()
                    Folder1_label.addLabel(Placemark)
                    # 更新进度
                    progess.count()
                Folder1 = Folder1_label.create()
                Folder_label.addLabel(Folder1)
                # 更新进度
                progess.count()
                # 小区图形
                Folder2_label = KMLLabel('Folder')
                name_label = KMLLabel('name')
                name_label.createTextNode(u'小区图形')
                name = name_label.create()
                Folder2_label.addLabel(name)
                for (i, feature) in enumerate(self.cell_datas):
                    Placemark_label = KMLLabel('Placemark')
                    ExtendedData_label = KMLLabel('ExtendedData')
                    SchemaData_label = KMLLabel('SchemaData')
                    SchemaData_label.setAttribute(('schemaUrl', u'#'+self.filename))
                    for (j, data) in enumerate(feature):
                        SimpleData_label = KMLLabel('SimpleData')
                        SimpleData_label.setAttribute(('name', self.cell_fields[j]))
                        if data != None:
                            SimpleData_label.createTextNode(data)
                        else:
                            SimpleData_label.createTextNode('NULL')
                        SimpleData = SimpleData_label.create()
                        SchemaData_label.addLabel(SimpleData)
                    SchemaData = SchemaData_label.create()
                    ExtendedData_label.addLabel(SchemaData)
                    ExtendedData = ExtendedData_label.create()
                    Polygon_label = KMLLabel('Polygon')
                    altitudeMode_label = KMLLabel('altitudeMode')
                    altitudeMode_label.createTextNode('relativeToGround')
                    altitudeMode = altitudeMode_label.create()
                    Polygon_label.addLabel(altitudeMode)
                    outerBoundaryIs_label = KMLLabel('outerBoundaryIs')
                    LinearRing_label = KMLLabel('LinearRing')
                    LinearRing_label.addLabel(altitudeMode)
                    coordinates_label = KMLLabel('coordinates')
                    for cell_points in self.cell_points[i]:
                        for cell_point in cell_points:
                            coordinates_label.createTextNode(str(cell_point[0]) + ',' + str(cell_point[1]) + ' ')
                    coordinates = coordinates_label.create()
                    LinearRing_label.addLabel(coordinates)
                    LinearRing = LinearRing_label.create()
                    outerBoundaryIs_label.addLabel(LinearRing)
                    outerBoundaryIs = outerBoundaryIs_label.create()
                    Polygon_label.addLabel(outerBoundaryIs)
                    Polygon = Polygon_label.create()
                    Cellname_label = KMLLabel('name')
                    Cellname_label.createTextNode(self.cell_names[i])
                    cellname = Cellname_label.create()
                    Placemark_label.addLabel(cellname)
                    Style_label = KMLLabel('Style')
                    LineStyle_label = KMLLabel('LineStyle')
                    color_label = KMLLabel('color')
                    color_label.createTextNode('ff0000ff')
                    color = color_label.create()
                    LineStyle_label.addLabel(color)
                    # 将线的宽度定义为2
                    width_label = KMLLabel('width')
                    width_label.createTextNode('2')
                    width = width_label.create()
                    LineStyle_label.addLabel(width)

                    LineStyle = LineStyle_label.create()
                    Style_label.addLabel(LineStyle)
                    PolyStyle_label = KMLLabel('PolyStyle')
                    fill_label = KMLLabel('fill')
                    fill_label.createTextNode('0')
                    fill = fill_label.create()
                    PolyStyle_label.addLabel(fill)
                    PolyStyle = PolyStyle_label.create()
                    Style_label.addLabel(PolyStyle)
                    Style = Style_label.create()
                    Placemark_label.addLabel(Style)
                    Placemark_label.addLabel(ExtendedData)
                    Placemark_label.addLabel(Polygon)
                    Placemark = Placemark_label.create()
                    Folder2_label.addLabel(Placemark)
                    # 更新进度
                    progess.count()
                Folder2 = Folder2_label.create()
                Folder_label.addLabel(Folder2)
                # 更新进度
                progess.count()
                Folder = Folder_label.create()
                Document_label.addLabel(Folder)
                # 更新进度
                progess.count()

            Document_label.setAttribute(('id', 'root_doc'))
            Document = Document_label.create()
            kml_label = KMLLabel('kml')
            kml_label.setAttribute(('xmlns', 'http://www.opengis.net/kml/2.2'))
            kml_label.addLabel(Document)
            kml = kml_label.create()

            outputs = head + kml
            return  (True, outputs)

        except Exception as e:
            raise traceback.format_exc()

# KML标签类
class KMLLabel(object):
    def __init__(self, ElementName):
        super(KMLLabel, self).__init__()
        self.name = ElementName
        self.setting = ''
        self.text = ''
        self.kmllabel = ''

    def setAttribute(self, *Attribute):
        self.setting = u''
        for (key, value) in Attribute:
            self.setting = self.setting + u' ' + key + u'="' + value + u'"'

    def createTextNode(self, text=''):
        if type(text) == int:
            self.text = self.text + str(text)
        elif type(text) == float:
            self.text = self.text + str(text)
        elif type(text) == str:
            self.text = self.text + text
        elif type(text) == unicode:
            self.text = self.text + text
        else :
            pass

    def addLabel(self, kmllabel=''):

        self.kmllabel = self.kmllabel + kmllabel


    def create(self):
        label =  '<' + self.name + self.setting + '>' + self.text + self.kmllabel + '</' + self.name + '>'
        return label