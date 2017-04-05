# -*- coding:utf-8 -*-
'''
表头设置
原名为Config
@author: Karwai Kwok

'''

# 基站Excel模板头
SiteHead = [
    u"基站ID", u"基站名", u"RNC-BSC",
    u"经度", u"纬度", u"网络制式",
    u"典型环境", u"区域", u"运营商",
    u"簇", u"基站英文名", u"基站类型",
    u"站点地址", u"MCC", u"MNC",
    u"基站ID2", u"话务量", u"投诉量",
    u"Polygon", u"其他"
]

SiteType = [
    str, str, str,
    float, float, str,
    str, str, str,
    str, str, str,
    str, str, str,
    str, int, int,
    str, str
]

# 小区Excel模板头
CellHead = [
    u"基站ID", u"基站名", u"小区ID", u"小区名", u"扇区ID",
    u"小区类型", u"RNC-BSC", u"方向角", u"经度", u"纬度",
    u"网络制式", u"典型环境", u"频段", u"总下倾", u"电子下倾",
    u"机械下倾", u"天线挂高", u"区域", u"运营商", u"簇",
    u"基站英文名", u"BTS类型", u"基站类型", u"设备厂家", u"MSC",
    u"LAC", u"登记区", u"PN", u"PSC", u"SCG",
    u"SC", u"RAC", u"PCI", u"LTE-ECI", u"LTE-ECGI",
    u"TAC", u"导频功率", u"RsPower", u"LTE-PA", u"LTE-PB", u"频宽",
    u"ARFCN", u"BCCH", u"BSIC", u"天线类型", u"天线增益",
    u"天线波瓣角", u"TxPow", u"MCC", u"MNC", u"话务量",
    u"投诉量", u"Polygon", u"其他"
]

CellType = [
    str, str, str, str, int,
    str, str, int, float, float,
    str, str, str, float, float,
    float, float, str, str, str,
    str, str, str, str, str,
    str, str, int, int, int,
    int, str, int, str, str,
    str, float, int, int, int, str,
    str, str, str, str, float,
    str, str, str, str, int,
    int, str, str
]

# 基站和小区Excel模板头
SiteANDCellHead = [u"基站ID", u"基站名", u"小区ID",
                   u"小区名", u"扇区ID", u"小区类型",
                   u"RNC-BSC", u"方向角", u"经度",
                   u"纬度", u"网络制式", u"典型环境",
                   u"频段", u"总下倾", u"电子下倾",
                   u"机械下倾", u"天线挂高", u"区域",
                   u"运营商", u"簇", u"基站英文名",
                   u"BTS类型", u"基站类型", u"设备厂家",
                   u"MSC", u"LAC", u"登记区",
                   u"PN", u"PSC", u"SCG",
                   u"SC", u"RAC", u"PCI",
                   u"LTE-ECI", u"LTE-ECGI", u"TAC",
                   u"导频功率", u"RsPower", u"LTE-PA", u"LTE-PB",
                   u"频宽", u"ARFCN", u"BCCH",
                   u"BSIC", u"天线类型", u"天线增益",
                   u"天线波瓣角", u"TxPow", u"站点地址",
                   u"MCC", u"MNC", u"基站ID2",
                   u"话务量", u"投诉量", u"Polygon",
                   u"其他"]

SiteANDCellType = [str, str, str,
                   str, int, int,
                   str, int, float,
                   float, str, str,
                   str, float, float,
                   float, str, str,
                   str, str, str,
                   str, str, str,
                   str, str, str,
                   int, int, int,
                   str, str, str,
                   str, str, str,
                   float, int, int, str,
                   str, str, str,
                   float, int, float,
                   int, float, str,
                   str, str, str,
                   int, int, str,
                   str]

# 相邻小区导入模板头
ServingCellHead = ('SCell', 'NCell', 'NType', 'HOAttempt', 'HOSucc', 'HOSuccRate', 'Distance')
ServingCellType = [str, str, str, int, int, float, float]

# 基站分析
AnalySiteHeade1 = [u'运营商', u'基站名称', u'经度', u'纬度', u'行政区', u'片区', u'区域类型',
                   u'最近站点名', u'最近站点所属运营商', u'最近距离(米)',
                   u'最近现有需求站点', u'距离(米)',
                   u'最近移动网点', u'经度', u'纬度', u'距离(米)',
                   u'最近联通网点', u'经度', u'纬度', u'距离(米)', u'最近电信网点', u'经度', u'纬度',
                   u'距离(米)', u'最近铁塔网点', u'经度', u'纬度', u'距离(米)',
                   u'合理性', u'建议']

AnalySiteHeade2 = [u'运营商', u'基站名称', u'经度', u'纬度', u'行政区', u'片区', u'区域类型']
AnalySiteType = [str, str, float, float, str, str, str]

# 基站合并
MergeSiteHead = [u"推送基站名称", u"经度", u"纬度", u"区域类型", u"最近基站名称", u"最近距离", u"平均距离",
                 u"基站名称1", u"距离1", u"经度1", u"纬度1",
                 u"基站名称2", u"距离2", u"经度2", u"纬度2",
                 u"基站名称3", u"距离3", u"经度3", u"纬度3",
                 u"基站名称4", u"距离4", u"经度4", u"纬度4",
                 u"基站名称5", u"距离5", u"经度5", u"纬度5",
                 u"基站名称6", u"距离6", u"经度6", u"纬度6"]

MergeSiteType = [str, float, float, str, str, float, float,
                 str, float, float, float,
                 str, float, float, float,
                 str, float, float, float,
                 str, float, float, float,
                 str, float, float, float,
                 str, float, float, float]

# PCI规划
PCIHead1 = [u'小区名称', u'经度', u'纬度', u'Azimuth']
PCIType = [str, float, float, float]
PCIHead2 = [u'小区名称', u'经度', u'纬度', u'Azimuth', u'LTE-PCI']
# 基站推送
# SitePushHead = [ u'推送运营商', u'基站名称', u'经度', u'纬度',u'区域类型',u'分析运营商',u'方差']
# SitePushType = [str, str, float, float, str, str, str, str]

# 模板表类型
SelecType = [u'基站小区', u'相邻小区']

# 导出数据Excel类型
ExpType = [u'基站', u'小区', u'相邻小区']

# 数据导入名称
ImpExcelName = [u'基站和小区', u'相邻小区']

# KML文件表头
KMLHead = {'SiteId': 'string', 'SiteName': 'string', 'System': 'string',
           'Lon': 'float', 'Lat': 'float', 'Operator': 'int',
           'SiteId2': 'string', 'ESiteName': 'string', 'SiteType': 'string',
           'Vendor': 'string', 'Cluster': 'string', 'Region': 'string',
           'Address': 'string', 'MCC': 'string', 'MNC': 'string',
           'CellId': 'string', 'SectorId': 'int', 'CellType': 'int',
           'Azimuth': 'int', 'Length': 'float', 'CellName': 'string',
           'BtStype': 'string', 'Msc': 'string', 'RNC-BSC': 'string',
           'LAC': 'string', 'CDMA-REG': 'sting', 'CDMA-PN': 'int',
           'WCDMA-PSC': 'string', 'LTE-ECI': 'string', 'LTE-ECGI': 'string',
           'LTE-TAC': 'string', 'LTE-PCI': 'int', 'LTE-RsPow': 'int',
           'LTE-PA': 'int', 'LTE-PB': 'int', 'FreBand': 'string',
           'BandWidth': 'string', 'ARFCN': 'string', 'GSM-BCCH': 'string',
           'GSM-BSIC': 'string', 'Antenna': 'string', 'AntGAIN': 'float',
           'AntHeight': 'float', 'Ant-Beam': 'int', 'TILT': 'float',
           'ETILT': 'float', 'MTILT': 'float', 'TxPow': 'float',
           'PcpochPowe': 'float', 'RAC': 'string', 'site_name': 'string'}

KML_SiteSetting = [u"基站ID", u'基站名', u"网络制式", u"经度", u'纬度', u'运营商',
                   u'基站ID2', u'基站类型', u'基站英文名', u'典型环境', u'站点地址']

KML_CellSetting = [u'小区ID', u'扇区ID', u'小区类型', u'方向角', u'经度', u'纬度',
                   u'基站ID', u'基站名', u'小区名', u'天线挂高', u'总下倾', u'电子下倾', u'机械下倾', u'RAC',
                   u'MSC', u'RNC-BSC', u'LAC', u'PN', u'PSC', u'TAC',
                   u'PCI', u'频段', u'LTE-PA', u'LTE-PB', u'BCCH', u'BSIC']

# 百度地图信息字段
Baidu_SiteFields = [u'基站名', u'基站ID']

Baidu_CellFields = [u'小区名', u'小区ID', u'基站名', u'基站ID', u'经度', u'纬度',
                    u'PSC', u'PCI', u'PN', u'BCCH',
                    u'方向角', u'总下倾', u'天线挂高', u'RNC-BSC']

# 腾讯地图信息字段
Tencent_SiteFields = [u'基站名', u'基站ID']

Tencent_CellFields = [u'小区名', u'小区ID', u'基站名', u'基站ID', u'经度', u'纬度',
                      u'PSC', u'PCI', u'PN', u'BCCH',
                      u'方向角', u'总下倾', u'天线挂高', u'RNC-BSC']

# 搜狗地图信息字段
Sogo_SiteFields = [u'基站名', u'基站ID']

Sogo_CellFields = [u'小区名', u'小区ID', u'基站名', u'基站ID', u'经度', u'纬度',
                   u'PSC', u'PCI', u'PN', u'BCCH',
                   u'方向角', u'总下倾', u'天线挂高', u'RNC-BSC']

# 规划基站字段
PLANNINGHead = [u"推送基站名称", u"经度", u"纬度", u"区域类型", u"最近基站名称", u"最近距离", u"平均距离",
                u"基站名称1", u"距离1", u"经度1", u"纬度1",
                u"基站名称2", u"距离2", u"经度2", u"纬度2",
                u"基站名称3", u"距离3", u"经度3", u"纬度3",
                u"基站名称4", u"距离4", u"经度4", u"纬度4",
                u"基站名称5", u"距离5", u"经度5", u"纬度5",
                u"基站名称6", u"距离6", u"经度6", u"纬度6"]

PLANNINGType = [str, float, float, str, str, float, float,
                str, float, float, float,
                str, float, float, float,
                str, float, float, float,
                str, float, float, float,
                str, float, float, float,
                str, float, float, float]



