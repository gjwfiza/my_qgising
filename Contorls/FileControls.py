# -*- coding: utf-8 -*-
'''
文件操作函数
@author: Karwai Kwok

'''

import os, pickle, traceback, shutil
from MyQGIS.Contorls.LayerControls import getLayerByName
from MyQGIS.config.EnumType import ExcelType

# 该文件当前路径
strfilepath = os.path.realpath(__file__)
cmd_folder = "%s/" % (os.path.dirname(strfilepath),)

# 获取工程所在路径
def getProjectDir(iface, layer_name=u""):
    if iface:
        if layer_name == u"":
            # 如果没有指定图层名字
            layers = iface.mapCanvas().layers()
            project_dir = os.path.dirname(layers[0].source())
        else:
            layer = getLayerByName(layer_name, iface)
            if not layer:
                # 如果相应图层不存在,则返回None
                return None
            else:
                project_dir = os.path.dirname(layer.source())

        return project_dir

    else:
        return None

# 删除目录下相应文件名的Shape文件
def deleteShapefile(project_dir, name):
    if name == "" and os.path.isfile(project_dir):
        pth,nm = os.path.split(project_dir)
        bn,ext = os.path.split(nm)
    else:
        pth = project_dir
        bn = name
    Ext = [".shp",".shx",".dbf",".prj",".qpj"]
    for e in Ext:
        f = os.path.join(pth,bn+e)
        if os.path.isfile(f):
            os.remove(f)

# 获取小区图形参数设置
def getCellGraphicParam(iface):
    setting_dict = {}
    projectDir = getProjectDir(iface, u"小区")
    settingFile_path = os.path.join(projectDir, u'sectorsetting.txt')
    if os.path.exists(settingFile_path):
        # 如果存在参数设置文件
        try:
            f = open(settingFile_path, 'r')
            setting_dict = pickle.load(f)
            f.close()
        except Exception:
            raise Exception, traceback.format_exc()
        finally:
            return setting_dict
    else:
        # 参数文件不存在
        return setting_dict

# 生成模板文件
def createModelFile(fileType, saveName):
    try:
        if fileType == ExcelType.SITEANDCELL:
            model = os.path.join(cmd_folder, '../', u'Template', u'基站小区模板.xls')
        elif fileType == ExcelType.ANALYSITE:
            model = os.path.join(cmd_folder, '../', u'Template', u'基站分析模板.xls')
        elif fileType == ExcelType.SERVINGCELL:
            model = os.path.join(cmd_folder, '../', u'Template', u'相邻小区模板.xls')
        elif fileType == ExcelType.MERGESITE:
            model = os.path.join(cmd_folder, '../', u'Template', u'基站合并模板.xls')
        elif fileType == ExcelType.PUSHSITE:
            model = os.path.join(cmd_folder, '../', u'Template', u'基站推送模板.xls')
        if os.path.exists(model):
            shutil.copyfile(model, saveName)
            return True
        else:
            print u'请检查模板文件是否在插件目录中!'
            return False
    except Exception, e:
        raise Exception, traceback.format_exc()
