# -*- coding: utf-8 -*-
'''
geometry操作函数
@author: Karwai Kwok
'''

import math
from qgis._core import QgsPoint, QgsRectangle

# 画出扇形（原名为draw）
# @param mpoint 基站的坐标
# @param mradius 小区的长度（圆的半径）
# @param iface
# @param mapunits 是否使用地图单位（默认使用）
# @param angle 表示小区的方向角度（未转化成弧度）
# @param szAngle 表示扇形的角度大小（未转化成弧度）
# @param segment 表示将扇形划分成多少等分
def createSector(mpoint, mradius, iface, mapunits=True, angle=0.0, szAngle=0.0, segment=24):
    if not mapunits:
        ctx = iface.mapCanvas().mapRenderer().rendererContext()
        mradius *= ctx.scaleFactor() * ctx.mapToPixel().mapUnitsPerPixel()
    if type(angle) != float:
        angle = math.pi / 180 * (90.0 - float(angle))
    szAngle = math.pi / 180 * szAngle
    pts = []
    pts.append(mpoint)
    for i in range(segment):
        theta = angle - szAngle / 2 + i * (szAngle / segment)
        p = QgsPoint(mpoint.x() + mradius * math.cos(theta), mpoint.y() + mradius * math.sin(theta))
        pts.append(p)
    pts.append(mpoint)
    return pts


# 画圆
# @param segment 将圆分成几份（默认64，最好为8的倍数）
def createCircle(mpoint, mradius, iface, mapunits=True, segment=64):
    if not mapunits:
        ctx = iface.mapCanvas().mapRenderer().rendererContext()
        mradius *= ctx.scaleFactor() * ctx.mapToPixel().mapUnitsPerPixel()
    pts = []
    for i in range(segment):
        theta = i * (2.0 * math.pi / segment)
        p = QgsPoint(mpoint.x() + mradius * math.cos(theta), mpoint.y() + mradius * math.sin(theta))
        pts.append(p)

    return pts

# 根据中心点和高宽生成一个矩形
# mradius：半径（米）
# 在经线上，纬度每差1度,实地距离大约为111千米
# 在纬线上，经度每差1度,实际距离为111×cosθ千米
def createARectangleByCenterPoint(centerPoint, mradius):
    x0 = centerPoint.x()
    y0 = centerPoint.y()
    delta_x = (1.0 / 111000.0 * mradius)
    delta_y = (1.0 / 111000.0 * mradius * math.cos(y0))
    x1 = x0 - delta_x
    y1 = y0 - delta_y
    point1 = QgsPoint(x1, y1)
    x2 = x0 + delta_x
    y2 = y0 + delta_y
    point2 = QgsPoint(x2, y2)
    rectangle = QgsRectangle(point1, point2)
    return rectangle
