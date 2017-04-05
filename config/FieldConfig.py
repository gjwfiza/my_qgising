# -*- coding:utf-8 -*-
'''
字段信息保存
@author: Karwai Kwok

'''
from PyQt4.QtCore import QVariant

SiteType2 = [
    QVariant.String, QVariant.String, QVariant.String,
    QVariant.Double, QVariant.Double, QVariant.String,
    QVariant.String, QVariant.String, QVariant.String,
    QVariant.String, QVariant.String, QVariant.String,
    QVariant.String, QVariant.String, QVariant.String,
    QVariant.String, QVariant.Int, QVariant.Int,
    QVariant.String, QVariant.String
]

SiteLength = [
    20, 50, 10,
    20, 20, 10,
    20, 20, 16,
    20, 20, 50,
    100, 10, 10,
    50, 10, 10,
    50, 100
]

SitePrec = [0, 0, 0,
            7, 7, 0,
            0, 0, 0,
            0, 0, 0,
            0, 0, 0,
            0, 0, 0,
            0, 0]

SiteSymbol = {u'移动':('yellow', u'移动'), u'联通':('green', u'联通'), u'电信':('darkcyan', u'电信'),u'铁塔':('blue',u'铁塔')}



CellType2 = [
    QVariant.String, QVariant.String, QVariant.String, QVariant.String, QVariant.Int,
    QVariant.String, QVariant.String, QVariant.Int, QVariant.Double, QVariant.Double,
    QVariant.String, QVariant.String, QVariant.String, QVariant.Double, QVariant.Double,
    QVariant.Double, QVariant.Double, QVariant.String, QVariant.String, QVariant.String,
    QVariant.String, QVariant.String, QVariant.String, QVariant.String, QVariant.String,
    QVariant.String, QVariant.String, QVariant.Int, QVariant.Int, QVariant.Int,
    QVariant.Int, QVariant.String, QVariant.Int, QVariant.String, QVariant.String,
    QVariant.String, QVariant.Double, QVariant.Int, QVariant.Int, QVariant.Int, QVariant.String,
    QVariant.String, QVariant.String, QVariant.String, QVariant.String, QVariant.Double,
    QVariant.String, QVariant.String, QVariant.String, QVariant.String, QVariant.Int,
    QVariant.Int, QVariant.String, QVariant.String
]

CellLength = [
    20,50,16,20,10,
    10,10,3,10,10,
    20,20,16,20,20,
    20,20,20,20,20,
    20,16,16,16,10,
    16,16,3,3,3,
    3,16,3,16,20,
    20,20,5,5,5,16,
    16,3,6,60,20,
    3,20,10,10,20,
    20,20,100
]

CellPrec = [
    0,0,0,0,0,
    0,0,0,6,6,
    0,0,0,0,6,
    6,6,6,0,0,
    0,0,0,0,0,
    0,0,0,0,0,
    0,0,0,0,0,
    0,6,0,0,0,0,
    0,0,0,0,6,
    0,6,0,0,0,
    0,0,0
]

CellSymbol = {u'移动':('yellow', u'移动'), u'联通':('green', u'联通'), u'电信':('darkcyan', u'电信'),u'铁塔':('blue',u'铁塔')}

ServingCellType2 = [QVariant.String, QVariant.String, QVariant.String, \
                    QVariant.Int, QVariant.Int, QVariant.Double, QVariant.Double]

ServingCellLength = [32, 32, 16, 9, 9, 10, 10]

ServingCellPrec = [0, 0, 0, 0, 0, 4, 2]

ServingCellSymbol =  {u'移动':('blue', u'移动'), u'联通':('blue', u'联通'), u'电信':('blue', u'电信'),u'铁塔':('blue',u'铁塔')}


PLANNINGType2 = [QVariant.String, QVariant.Double, QVariant.Double, QVariant.String, QVariant.String, QVariant.Double, QVariant.Double,
                 QVariant.String, QVariant.Double, QVariant.Double, QVariant.Double,
                 QVariant.String, QVariant.Double, QVariant.Double, QVariant.Double,
                 QVariant.String, QVariant.Double, QVariant.Double, QVariant.Double,
                 QVariant.String, QVariant.Double, QVariant.Double, QVariant.Double,
                 QVariant.String, QVariant.Double, QVariant.Double, QVariant.Double,
                 QVariant.String, QVariant.Double, QVariant.Double, QVariant.Double]

PLANNINGLength = [50, 20, 20, 50, 50, 20, 20,
                  50, 20, 20, 20,
                  50, 20, 20, 20,
                  50, 20, 20, 20,
                  50, 20, 20, 20,
                  50, 20, 20, 20,
                  50, 20, 20, 20]

PLANNINGPrec = [0, 7, 7, 0, 0, 7, 7,
                 0, 7, 7, 7,
                 0, 7, 7, 7,
                 0, 7, 7, 7,
                 0, 7, 7, 7,
                 0, 7, 7, 7,
                 0, 7, 7, 7]