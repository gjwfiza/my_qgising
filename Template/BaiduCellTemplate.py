# -*- coding:utf-8 -*-
'''
@author: Karwai Kwok
'''

class BaiduCellTemplate():
    def __init__(self, ak=u"BtvVWRqGfnffNqdqAN7rusTlb2E020C8"):
        super(BaiduCellTemplate, self).__init__()
        self.ak = ak

    def getHead(self):
        output = u"""
            <!DOCTYPE HTML>
            <html>
            <head>
              <title>百度地图小区显示</title>
              <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
              <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no">
              <style type="text/css">
                html,body{
                    margin:0;
                    width:100%;
                    height:100%;
                    background:#ffffff;
                }
                #toolbar1{
                    width:100%;
                    height:4%;
                }
                #toolbar2{
                    width:100%;
                    height:5%;
                }
                #map{
                    width:100%;
                    height:91%;
                }
                #panel {
                    position: absolute;
                    top:30px;
                    left:10px;
                    z-index: 999;
                    color: #fff;
                }
                #login{
                    position:absolute;
                    width:300px;
                    height:40px;
                    left:50%;
                    top:50%;
                    margin:-40px 0 0 -150px;
                }
                #login input[type=password]{
                    width:200px;
                    height:30px;
                    padding:3px;
                    line-height:30px;
                    border:1px solid #000;
                }
                #login input[type=submit]{
                    width:80px;
                    height:38px;
                    display:inline-block;
                    line-height:38px;
                }
              </style>
              <script type="text/javascript" src="http://api.map.baidu.com/api?v=2.0&ak=""" + self.ak + u"""
              "></script>
              <script type="text/javascript" src="http://api.map.baidu.com/library/DistanceTool/1.2/src/DistanceTool_min.js"></script>
              <script type="text/javascript" src="http://api.map.baidu.com/library/RectangleZoom/1.2/src/RectangleZoom_min.js"></script>
              <!--加载鼠标绘制工具-->
                <script type="text/javascript" src="http://api.map.baidu.com/library/DrawingManager/1.4/src/DrawingManager_min.js"></script>
                <link rel="stylesheet" href="http://api.map.baidu.com/library/DrawingManager/1.4/src/DrawingManager_min.css" />
                <!--加载检索信息窗口-->
                <script type="text/javascript" src="http://api.map.baidu.com/library/SearchInfoWindow/1.4/src/SearchInfoWindow_min.js"></script>
                <link rel="stylesheet" href="http://api.map.baidu.com/library/SearchInfoWindow/1.4/src/SearchInfoWindow_min.css" />
              <script src="cell.js"></script>
            </head>
            <body>

                <div id="toolbar1">【查找小区名称】
                <input type='text' id='cellName' style='width:150px;' value=''/>
                <input type='button' class='wyq4' onClick="searchName()" value='Search'/>
                【查找小区ID】
                <input type='text' id='cellId' style='width:130px;' value=''/>
                <input type='button' class='wyq4' onClick="searchID()" value='Search'/>
                【搜索地址】
                <input type='text' id='localsearch' style='width:350px;' value=''/>
                <input type='button' class='wyq4' onClick="searchLocal()" value='Search'/>
                </div>
                <div id="toolbar2">

                【拉框放大】
                <input type='button' class='wyq4' onClick="RectangleZoomOpen()" value='Start'/>
                <input type='button' class='wyq4' onClick="RectangleZoomEnd()" value='End'/>
                【清除绘制】
                <input type='button' class='wyq4' onClick="CleanDrawing()" value='Clean'/>
                【点击获取经纬度】
                <input type='button' class='wyq4' onClick="getLocationOn()" value='On'/>
                <input type='button' class='wyq4' onClick="getLocationOff()" value='Off'/>
                【标志拖拽】
                <input type='button' class='wyq4' onClick="MarkerDraggingOn()" value='On'/>
                <input type='button' class='wyq4' onClick="MarkerDraggingOff()" value='Off'/>
                【线面编辑】
                <input type='button' class='wyq4' onClick="EditingOn()" value='On'/>
                <input type='button' class='wyq4' onClick="EditingOff()" value='Off'/>
                【
                <input type='button' class='wyq4' onClick="DistanceOpen()" style="font-size:18px" value='测距'/>
                】【显示小区名】
                <input type='button' class='wyq4' onClick="LabelOpen()" value='Open'/>
                <input type='button' class='wyq4' onClick="LabelClose()" value='Close'/>
                </div>

                <div id="map"></div>
                <script type="text/javascript">
                var map = new BMap.Map("map", {});                        // 创建Map实例
                map.centerAndZoom(new BMap.Point(113.36399344396, 23.140918708809), 16);     // 初始化地图,设置中心点坐标和地图级别
                map.enableScrollWheelZoom();                        //启用滚轮放大缩小
                var top_left_control = new BMap.ScaleControl({anchor: BMAP_ANCHOR_TOP_LEFT});// 左上角，添加比例尺
                map.addControl(top_left_control);
                var top_left_navigation = new BMap.NavigationControl();  //左上角，添加默认缩放平移控件
                map.addControl(top_left_navigation);
                var mapType1 = new BMap.MapTypeControl({mapTypes: [BMAP_NORMAL_MAP,BMAP_HYBRID_MAP]});  // 2D图，卫星图
                map.addControl(mapType1);
                var mapType2 = new BMap.MapTypeControl({anchor: BMAP_ANCHOR_TOP_RIGHT});  //右上角，默认地图控件
                map.addControl(mapType2);
                map.setCurrentCity("北京");          // 设置地图显示的城市 此项是必须设置的
                /*
                // 覆盖区域图层测试
                map.addTileLayer(new BMap.PanoramaCoverageLayer());
                var stCtrl = new BMap.PanoramaControl(); //构造全景控件
                stCtrl.setOffset(new BMap.Size(130, 5));
                map.addControl(stCtrl);//添加全景控件
                */
                // 添加小区
                for (var i=0; i<cell.length; i++)
                {
                    var points_list = [];
                    for (var j=0; j<cell[i].Polygon.length; j = j + 2)
                    {
                        points_list.push(new BMap.Point(cell[i].Polygon[j], cell[i].Polygon[j+1]));
                    }
                    var polyline = new BMap.Polyline(points_list, {strokeColor:"blue", strokeWeight:6, strokeOpacity:0.5});
                    var info =  {
                        CellName: cell[i].CellName,
                        CellId: cell[i].CellId,
                        SiteName: cell[i].SiteName,
                        SiteId: cell[i].SiteId,
                        Addr: [cell[i].lon, cell[i].lat],
                        WCDMA_PSC: cell[i].WCDMA_PSC,
                        LTE_PCI: cell[i].LTE_PCI,
                        CDMA_PN: cell[i].CDMA_PN,
                        GSM_BCCH: cell[i].GSM_BCCH,
                        Azimuth: cell[i].Azimuth,
                        TILT: cell[i].TILT,
                        AntHeigth: cell[i].AntHeigth,
                        RNC_BSC: cell[i].RNC_BSC,

                    }
                    map.addOverlay(polyline);
                    addClickHandler(info,polyline);
                }
                // 打开文字标签
                LabelOpen();
                // 添加信息窗口
                function addClickHandler(info,polyline){
                    polyline.addEventListener("click",function(e){
                        openInfo(info,e)}
                    );
                }
                function openInfo(info,e){
                    // 信息窗口样式设置
                    var opts = {
                        width: 350, // 信息窗口宽度
                        //height: 300, // 信息窗口高度
                        title:"", // 信息窗口标题
                        enableMessage: false,//设置允许信息窗发送短息
                    };
                    var infowindow = new BMap.InfoWindow(("小区名称:"+info.CellName
                                                        +"<br/>小区ID:"+info.CellId
                                                        +"<br/>基站名称:"+info.SiteName
                                                        +"<br/>基站Id:"+info.SiteId
                                                        +"<br/>位置:"+info.Addr[0]+","+info.Addr[1]
                                                        +"<br/>WCDMA-PSC:"+info.WCDMA_PSC
                                                        +"<br/>LTE-PCI:"+info.LTE_PCI
                                                        +"<br/>CDMA-PN:"+info.CDMA_PN
                                                        +"<br/>GSM-BCCH:"+info.GSM_BCCH
                                                        +"<br/>Azimuth:"+info.Azimuth
                                                        +"<br/>TILT:"+info.TILT
                                                        +"<br/>AntHeigth:"+info.AntHeigth
                                                        +"<br/>RNC-BSC:"+info.RNC_BSC), opts);  // 创建信息窗口对象
                    map.openInfoWindow(infowindow,e.point); //开启信息窗口
                }

                // 按名字查找
                var marker = null
                function searchName(){
                    var result = false;
                    var keyword = document.getElementById("cellName").value;
                    for (var i = 0; i < cell.length; i++){
                        if (keyword == (cell[i].CellName))
                        {
                            result = true;
                            if (marker != null)
                            {
                                map.removeOverlay(marker)
                            };
                            var point = new BMap.Point(cell[i].bd_lon, cell[i].bd_lat);
                            /*
                            var convertor = new BMap.Convertor();
                            var pointArr = [];
                            pointArr.push(point);
                            convertor.translate(pointArr, 1, 5, function(data){
                                if(data.status === 0) {
                                    marker = new BMap.Marker(data.points[0]);
                                    map.addOverlay(marker);
                                    map.centerAndZoom(point,16);
                                }
                            });
                            */
                            marker = new BMap.Marker(point);
                            map.addOverlay(marker);
                            map.centerAndZoom(point,16);
                        }
                    }
                    if (result == false)
                    {
                        alert("找不到结果");
                    }
                }
                // 按ID查找
                function searchID(){
                    var result = false;
                    var keyword = document.getElementById("cellId").value;
                    for (var i = 0; i < cell.length; i++){
                        if (keyword == (cell[i].CellId))
                        {
                            result = true;
                            if (marker != null)
                            {
                                map.removeOverlay(marker);
                            };
                            var point = new BMap.Point(cell[i].bd_lon, cell[i].bd_lat);
                            /*
                            var convertor = new BMap.Convertor();
                            var pointArr = [];
                            pointArr.push(point);
                            convertor.translate(pointArr, 1, 5, function(data){
                                if(data.status === 0) {
                                    marker = new BMap.Marker(data.points[0]);
                                    map.addOverlay(marker);
                                    map.centerAndZoom(point,16);
                                }
                            });
                            */
                            marker = new BMap.Marker(point);
                            map.addOverlay(marker);
                            map.centerAndZoom(point,16);

                        }
                    }
                    if (result == false)
                    {
                        alert("找不到结果");
                    }
                }
                // 鼠标测距
                function DistanceOpen(){
                    var myDis = new BMapLib.DistanceTool(map);
                    myDis.open();  //开启鼠标测距
                }
                // 鼠标拉框放大
                var myDrag = new BMapLib.RectangleZoom(map, {followText: "拖拽鼠标进行操作"});
                function RectangleZoomOpen(){
                    myDrag.open();  //开启拉框放大
                }
                function RectangleZoomEnd(){
                    myDrag.close();  //开启拉框放大
                }
                //实例化鼠标绘制工具
                var overlays = [];
                var overlaycomplete = function(e){
                    overlays.push(e.overlay);
                };
                var styleOptions = {
                    strokeColor:"red",    //边线颜色。
                    fillColor:"red",      //填充颜色。当参数为空时，圆形将没有填充效果。
                    strokeWeight: 3,       //边线的宽度，以像素为单位。
                    strokeOpacity: 0.8,	   //边线透明度，取值范围0 - 1。
                    fillOpacity: 0.6,      //填充的透明度，取值范围0 - 1。
                    strokeStyle: 'solid' //边线的样式，solid或dashed。
                }
                var drawingManager = new BMapLib.DrawingManager(map, {
                    isOpen: false, //是否开启绘制模式
                    enableDrawingTool: true, //是否显示工具栏
                    drawingToolOptions: {
                        anchor: BMAP_ANCHOR_TOP_RIGHT, //位置
                        offset: new BMap.Size(135, 5), //偏离值
                        scale: 0.7, //工具栏的缩放比例,默认为1
                    },
                    circleOptions: styleOptions, //圆的样式
                    polylineOptions: styleOptions, //线的样式
                    polygonOptions: styleOptions, //多边形的样式
                    rectangleOptions: styleOptions //矩形的样式
                });
                 //添加鼠标绘制工具监听事件，用于获取绘制结果
                drawingManager.addEventListener('overlaycomplete', overlaycomplete);

                function CleanDrawing(){
                    for(var i = 0; i < overlays.length; i++){
                        map.removeOverlay(overlays[i]);
                    }
                    overlays.length = 0
                }
                // 鼠标点击获取坐标
                var getLocation = false
                function getPoint(e){
                            alert(e.point.lng + "," + e.point.lat);
                }
                function getLocationOn(){
                    if (getLocation == false)
                    {
                        map.addEventListener("click",getPoint);
                        getLocation = true
                    };
                }
                function getLocationOff(){
                    if (getLocation == true)
                    {
                        map.removeEventListener("click",getPoint);
                        getLocation = false
                    };
                }
                // 地址搜索
                function searchLocal(){
                    var keyword = document.getElementById("localsearch").value;
                    // 创建地址解析器实例
                    var myGeo = new BMap.Geocoder();
                    // 将地址解析结果显示在地图上,并调整地图视野
                    myGeo.getPoint(keyword, function(point){
                        if (point) {
                            map.centerAndZoom(point, 16);
                            if (marker != null)
                            {
                                map.removeOverlay(marker)
                            };
                            marker = new BMap.Marker(point);
                            map.addOverlay(marker);
                        }else{
                            alert("您选择地址没有解析到结果!");
                        }
                    }, "北京市");
                }
                // 点可移动
                function MarkerDraggingOn(){
                    for (var i = 0; i < overlays.length; i++){
                        if ((overlays[i] instanceof BMap.Marker))
                        {
                                if (overlays[i] != marker)
                            {
                                overlays[i].enableDragging();
                            };
                        };
                    }
                }
                function MarkerDraggingOff(){
                    for (var i = 0; i < overlays.length; i++){
                        if (overlays[i] instanceof BMap.Marker)
                        {
                                if (overlays[i] != marker)
                            {
                                overlays[i].disableDragging();
                            };
                        };
                    }
                }
                // 线面可编辑
                function EditingOn(){
                    for (var i = 0; i < overlays.length; i++){
                        if ((overlays[i] instanceof BMap.Polyline) || (overlays[i] instanceof BMap.Polygon))
                        {
                            overlays[i].enableEditing();
                        };
                    };
                }
                function EditingOff(){
                    for (var i = 0; i < overlays.length; i++){
                        if ((overlays[i] instanceof BMap.Polyline) || (overlays[i] instanceof BMap.Polygon))
                        {
                            overlays[i].disableEditing();
                        };
                    }
                }
                // 添加文字标签
                function LabelOpen(){
                    for (var i=0; i<cell.length; i++)
                    {
                        var point = new BMap.Point(cell[i].bd_lon, cell[i].bd_lat);
                        var label_opts = {
                            position : point,    // 指定文本标注所在的地理位置
                            offset   : new BMap.Size(0, 0)    //设置文本偏移量
                        };
                        var label = new BMap.Label(cell[i].SiteName, label_opts);  // 创建文本标注对象
                        map.addOverlay(label);

                    }
                }
                function LabelClose(){
                    var allOverlay = map.getOverlays();
                    for(var i = 0; i < allOverlay.length; i++){
                        if (allOverlay[i] instanceof BMap.Label)
                        {
                            map.removeOverlay(allOverlay[i]);
                        }
                    }

                }

              </script>
            </body>
            </html>
            """

        return output

    def getPano(self):
        output = u"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
                <title>百度地图街景工具</title>
                <style type="text/css">
                    * {
                        margin: 0px;
                        padding: 0px;
                    }
                    body,
                    button,
                    input,
                    select,
                    textarea {
                        font: 12px/16px Verdana, Helvetica, Arial, sans-serif;
                    }
                    p {
                        width: 600px;
                        padding-top: 3px;
                        overflow: hidden;
                    }
                    div#pano_holder1{height:300px;width:610px;float:left;}
                    div#map {height:300px;width:610px;float:left;}
                    div#pano_holder {height:300px;width:610px;float:left;}
                    div#panel {height:300px;width:610px;float:left;}
                </style>
                <script type="text/javascript" src="http://api.map.baidu.com/api?v=2.0&ak=""" + self.ak + u"""
              "></script>
                <script src="cell.js"></script>
            </head>
            <body>
                <div id="pano_holder1"></div>
                <div id="map"></div>
                <div id="panel">
                    <br/><br/>
                    <span style="width:5px;">&nbsp;&nbsp;&nbsp;</span><span id="angle"></span><br/>
                    <span style="width:5px;">&nbsp;&nbsp;&nbsp;</span><span id="distance"></span><br/>
                    <span style="width:5px;">&nbsp;&nbsp;&nbsp;</span><span id="pano_lon"></span><br/>
                    <span style="width:5px;">&nbsp;&nbsp;&nbsp;</span><span id="pano_lat"></span><br/>
                    <span>
                    <br/>
                    <span style="width:5px;">&nbsp;&nbsp;&nbsp;</span>请输入小区信息：
                    <br/>
                    <br/>
                    <span style="width:5px;">&nbsp;&nbsp;&nbsp;</span>经度:
                    <input type="text" id="lon" style="width: 100px;height:25px;font-size:15px" />
                    <span style="width:5px;">&nbsp;&nbsp;&nbsp;</span>纬度:
                    <input type="text" id="lat" style="width: 100px;height:25px;font-size:15px" />
                    <span style="width:5px;">&nbsp;&nbsp;&nbsp;</span>小区规划名：
                    <input type="text" id="CellName" name="CellName" style="width: 125px;height:25px;font-size:15px" />
                    <input type="button" class="button" value="显示街景" id="setMarker" onclick="setMarker()" style="width:75px;height:28px;font-size:16px"/>
                    <br/>
                    <br/>
                    <span style="width:5px;">&nbsp;&nbsp;&nbsp;</span>基站搜索：
                    <input type="radio" name="SearchType" id="SearchID" value="ID" checked>按小区ID
                    <input type="radio" name="SearchType" id="SearchName" value="Name">按小区名称
                    <br/><br/>
                    <span style="width:5px;">&nbsp;&nbsp;&nbsp;</span>
                    <input type="text" id="Search" name="Search" style="width:450px;height:25px;font-size:15px" />
                    <input type="button" class="button" value="搜索并显示街景" id="setMarker" onclick="search()" style="width:120px;height:28px;font-size:15px"/>
                    </span>
                </div>
                <div id="pano_holder"></div>

            </body>
            </html>
            <script type="text/javascript">
                // 百度地图初始化
                var map = new BMap.Map("map");    // 创建Map实例
                map.centerAndZoom(new BMap.Point(113.36399344396, 23.140918708809), 16);  // 初始化地图,设置中心点坐标和地图级别
                map.addControl(new BMap.MapTypeControl());   //添加地图类型控件
                map.setCurrentCity("北京");          // 设置地图显示的城市 此项是必须设置的
                map.enableScrollWheelZoom(true);     //开启鼠标滚轮缩放
                map.addTileLayer(new BMap.PanoramaCoverageLayer()); // 全景覆盖区域图层测试
                // 添加小区
                for (var i=0; i<cell.length; i++)
                {
                    var points_list = [];
                    for (var j=0; j<cell[i].Polygon.length; j = j + 2)
                    {
                        points_list.push(new BMap.Point(cell[i].Polygon[j], cell[i].Polygon[j+1]));
                    }
                    var polyline = new BMap.Polyline(points_list, {strokeColor:"blue", strokeWeight:6, strokeOpacity:0.5});
                    var info =  {
                        CellName: cell[i].CellName,
                        CellId: cell[i].CellId,
                        SiteName: cell[i].SiteName,
                        CellId: cell[i].CellId,
                        Addr: [cell[i].lon, cell[i].lat],
                        WCDMA_PSC: cell[i].WCDMA_PSC,
                        LTE_PCI: cell[i].LTE_PCI,
                        CDMA_PN: cell[i].CDMA_PN,
                        GSM_BCCH: cell[i].GSM_BCCH,
                        Azimuth: cell[i].Azimuth,
                        TILT: cell[i].TILT,
                        AntHeigth: cell[i].AntHeigth,
                        RNC_BSC: cell[i].RNC_BSC,

                    }
                    map.addOverlay(polyline);
                    addClickHandler(info,polyline);
                }
                // 打开文字标签
                LabelOpen();
                // 添加文字标签
                function LabelOpen(){
                    for (var i=0; i<cell.length; i++)
                    {
                        var point = new BMap.Point(cell[i].bd_lon, cell[i].bd_lat);
                        var label_opts = {
                            position : point,    // 指定文本标注所在的地理位置
                            offset   : new BMap.Size(0, 0)    //设置文本偏移量
                        };
                        var label = new BMap.Label(cell[i].SiteName, label_opts);  // 创建文本标注对象
                        map.addOverlay(label);

                    }
                }
                // 添加信息窗口
                function addClickHandler(info,polyline){
                    polyline.addEventListener("click",function(e){
                        openInfo(info,e)}
                    );
                }
                function openInfo(info,e){
                    // 信息窗口样式设置
                    var opts = {
                        width: 350, // 信息窗口宽度
                        //height: 300, // 信息窗口高度
                        title:"", // 信息窗口标题
                        enableMessage: false,//设置允许信息窗发送短息
                    };
                    var infowindow = new BMap.InfoWindow(("小区名称:"+info.CellName
                                                        +"<br/>小区ID:"+info.CellId
                                                        +"<br/>基站名称:"+info.SiteName
                                                        +"<br/>基站Id:"+info.CellId
                                                        +"<br/>位置:"+info.Addr[0]+","+info.Addr[1]
                                                        +"<br/>WCDMA-PSC:"+info.WCDMA_PSC
                                                        +"<br/>LTE-PCI:"+info.LTE_PCI
                                                        +"<br/>CDMA-PN:"+info.CDMA_PN
                                                        +"<br/>GSM-BCCH:"+info.GSM_BCCH
                                                        +"<br/>Azimuth:"+info.Azimuth
                                                        +"<br/>TILT:"+info.TILT
                                                        +"<br/>AntHeigth:"+info.AntHeigth
                                                        +"<br/>RNC-BSC:"+info.RNC_BSC), opts);  // 创建信息窗口对象
                    map.openInfoWindow(infowindow,e.point); //开启信息窗口
                }
                // 设置基站Marker
                var lon = null;
                var lat = null;
                var marker = null;
                var cell_point = null;
                function setMarker()
                {
                    lon = document.getElementById("lon").value;
                    lat = document.getElementById("lat").value;
                    cell_name = document.getElementById("CellName").value;
                    if (lon != "" && lat != "")
                    {
                        lon = document.getElementById("lon").value;
                        lat = document.getElementById("lat").value;
                        if (marker != null)
                        {
                            map.removeOverlay(marker);
                        };
                        var point = new BMap.Point(lon, lat);
                        var convertor = new BMap.Convertor();
                        var pointArr = [];
                        pointArr.push(point);
                        convertor.translate(pointArr, 1, 5, function(data){
                            if(data.status === 0)
                            {
                                marker = new BMap.Marker(data.points[0]);
                                cell_point = data.points[0];
                                map.addOverlay(marker);
                                map.centerAndZoom(data.points[0],16);
                                if (cell_name != "")
                                {
                                    var opts = {
                                      width : 220,     // 信息窗口宽度（0为自动调整,220 - 730）
                                      height: 60,     // 信息窗口高度（0为自动调整,60 - 650）
                                    }
                                    var infoWindow = new BMap.InfoWindow(cell_name, opts);  // 创建信息窗口对象
                                    map.openInfoWindow(infoWindow,data.points[0]); //开启信息窗口
                                    marker.addEventListener("click", function(){
                                        map.openInfoWindow(infoWindow,data.points[0]); //开启信息窗口
                                    });
                                };
                                var panorama = new BMap.Panorama('pano_holder');
                                panorama.setPov({heading: -40, pitch: 6});
                                panorama.setPosition(data.points[0]); //根据经纬度坐标展示全景图
                            }
                        });
                    }
                    else
                    {
                        alert("请输入经纬度信息");
                    };
                }
                // 从现有小区中搜索
                function search()
                {
                    if (document.getElementById("SearchName").checked == true) // 按基站名称搜索
                    {
                        var result = false;
                        var keyword = document.getElementById("Search").value;
                        for (var i = 0; i < cell.length; i++){
                            if (keyword == (cell[i].CellName))
                            {
                                result = true;
                                if (marker != null)
                                {
                                    map.removeOverlay(marker);
                                };
                                var point = new BMap.Point(cell[i].bd_lon, cell[i].bd_lat);
                                marker = new BMap.Marker(point);
                                cell_point = point;
                                map.addOverlay(marker);
                                map.centerAndZoom(point,18);
                                var panorama = new BMap.Panorama('pano_holder');
                                panorama.setOptions({ navigationControl: true }); // 显示导航控件
                                panorama.setPov({heading: -40, pitch: 6});
                                panorama.setPosition(point); //根据经纬度坐标展示全景图
                            }
                        }
                        if (result == false)
                        {
                            alert("找不到结果");
                        }
                    }
                    else // 按基站ID搜索
                    {
                        var result = false;
                        var keyword = document.getElementById("Search").value;
                        for (var i = 0; i < cell.length; i++){
                            if (keyword == (cell[i].CellId))
                            {
                                result = true;
                                if (marker != null)
                                {
                                    map.removeOverlay(marker)
                                };
                                var point = new BMap.Point(cell[i].bd_lon, cell[i].bd_lat);
                                marker = new BMap.Marker(point);
                                cell_point = point;
                                map.addOverlay(marker);
                                map.centerAndZoom(point,18);
                                var panorama = new BMap.Panorama('pano_holder');
                                panorama.setOptions({ navigationControl: true }); // 显示导航控件
                                panorama.setPov({heading: -40, pitch: 6});
                                panorama.setPosition(point); //根据经纬度坐标展示全景图

                            }
                        }
                        if (result == false)
                        {
                            alert("找不到结果");
                        }
                    }

                }
                // 监听地图添加要显示的街景
                var marker1 = null; // 街景Marker
                var pano_point = null; // 街景Point
                var polyline = null;
                var panorama1 = null; // 定义街景图层
                map.addEventListener("click",function(e){
                    if (marker != null)
                    {
                            if (marker1 != null)
                        {
                            map.removeOverlay(marker1); // 移除原有标注
                            map.removeOverlay(polyline);
                        };
                        marker1 = new BMap.Marker(e.point,{icon:new BMap.Icon("http://api.map.baidu.com/lbsapi/createmap/images/icon.png",new BMap.Size(20,25),{imageOffset: new BMap.Size(-23,3)})});
                        marker1.setOffset(new BMap.Size(0,-6));
                        map.addOverlay(marker1);
                        panorama1 = new BMap.Panorama('pano_holder1');
                        panorama1.setOptions({ navigationControl: true }); // 显示导航控件
                        panorama1.setPov({heading: -40, pitch: 6});
                        panorama1.setPosition(e.point); //根据经纬度坐标展示全景图
                        pano_point = panorama1.getPosition();

                        // 计算街景位置与基站夹角
                        if ((pano_point.lng>cell_point.lng)&&(pano_point.lat>cell_point.lat))
                        {
                            angle = Math.atan((pano_point.lng - cell_point.lng) / (pano_point.lat - cell_point.lat));
                            document.getElementById("angle").innerHTML ="街景位置与基站夹角"+Math.abs(angle)/Math.PI*180+"度";
                        }
                        else if ((pano_point.lng>cell_point.lng)&&(pano_point.lat<cell_point.lat))
                        {
                            angle = Math.atan(Math.abs(pano_point.lng - cell_point.lng) / Math.abs(pano_point.lat - cell_point.lat));
                            document.getElementById("angle").innerHTML ="街景位置与基站夹角"+(180-(Math.abs(angle)/Math.PI*180))+"度";
                        }
                        else if ((pano_point.lng<cell_point.lng)&&(pano_point.lat<cell_point.lat))
                        {
                            angle = Math.atan(Math.abs(pano_point.lng - cell_point.lng) / Math.abs(pano_point.lat - cell_point.lat));
                            document.getElementById("angle").innerHTML ="街景位置与基站夹角"+(-180+(Math.abs(angle)/Math.PI*180))+"度";
                        }
                        else if ((pano_point.lng<cell_point.lng)&&(pano_point.lat>cell_point.lat))
                        {
                            angle = Math.atan(Math.abs(pano_point.lng - cell_point.lng) / Math.abs(pano_point.lat - cell_point.lat));
                            document.getElementById("angle").innerHTML ="街景位置与基站夹角"+(-(Math.abs(angle)/Math.PI*180))+"度";
                        }
                        else if ((pano_point.lng=cell_point.lng)&&(pano_point.lat>cell_point.lat))
                        {
                            document.getElementById("angle").innerHTML ="街景位置与基站夹角"+"0度";
                        }
                        else if ((pano_point.lng>cell_point.lng)&&(pano_point.lat=cell_point.lat))
                        {
                            document.getElementById("angle").innerHTML ="街景位置与基站夹角"+"90度";
                        }
                        else if ((pano_point.lng<cell_point.lng)&&(pano_point.lat=cell_point.lat))
                        {
                            document.getElementById("angle").innerHTML ="街景位置与基站夹角"+"-90度";
                        }
                        else
                        {
                            document.getElementById("angle").innerHTML ="街景位置与基站夹角"+"180度";
                        };
                        // 计算街景位置与基站距离
                        document.getElementById("distance").innerHTML ="街景位置与基站距离"+map.getDistance(cell_point,pano_point).toFixed(2)+"米";
                        polyline = new BMap.Polyline([cell_point,pano_point], {strokeColor:"blue", strokeWeight:6, strokeOpacity:0.5});  //定义折线
                        map.addOverlay(polyline);     //添加折线到地图上
                        // 显示街景经纬度
                        document.getElementById("pano_lon").innerHTML ="街景位置经度：" + pano_point.lng;
                        document.getElementById("pano_lat").innerHTML ="街景位置纬度：" + pano_point.lat;
                    };
                });


            </script>
            """

        return output

# 百度地图小区显示主页面
Head = u"""
<!DOCTYPE HTML>
<html>
<head>
  <title>百度地图小区显示</title>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no">
  <style type="text/css">
    html,body{
        margin:0;
        width:100%;
        height:100%;
        background:#ffffff;
    }
	#toolbar1{
        width:100%;
        height:4%;
    }
	#toolbar2{
        width:100%;
        height:5%;
    }
    #map{
        width:100%;
        height:91%;
    }
    #panel {
        position: absolute;
        top:30px;
        left:10px;
        z-index: 999;
        color: #fff;
    }
    #login{
        position:absolute;
        width:300px;
        height:40px;
        left:50%;
        top:50%;
        margin:-40px 0 0 -150px;
    }
    #login input[type=password]{
        width:200px;
        height:30px;
        padding:3px;
        line-height:30px;
        border:1px solid #000;
    }
    #login input[type=submit]{
        width:80px;
        height:38px;
        display:inline-block;
        line-height:38px;
    }
  </style>
  <script type="text/javascript" src="http://api.map.baidu.com/api?v=2.0&ak=BtvVWRqGfnffNqdqAN7rusTlb2E020C8"></script>
  <script type="text/javascript" src="http://api.map.baidu.com/library/DistanceTool/1.2/src/DistanceTool_min.js"></script>
  <script type="text/javascript" src="http://api.map.baidu.com/library/RectangleZoom/1.2/src/RectangleZoom_min.js"></script>
  <!--加载鼠标绘制工具-->
	<script type="text/javascript" src="http://api.map.baidu.com/library/DrawingManager/1.4/src/DrawingManager_min.js"></script>
	<link rel="stylesheet" href="http://api.map.baidu.com/library/DrawingManager/1.4/src/DrawingManager_min.css" />
	<!--加载检索信息窗口-->
	<script type="text/javascript" src="http://api.map.baidu.com/library/SearchInfoWindow/1.4/src/SearchInfoWindow_min.js"></script>
	<link rel="stylesheet" href="http://api.map.baidu.com/library/SearchInfoWindow/1.4/src/SearchInfoWindow_min.css" />
  <script src="cell.js"></script>
</head>
<body>

	<div id="toolbar1">【查找小区名称】
	<input type='text' id='cellName' style='width:150px;' value=''/>
	<input type='button' class='wyq4' onClick="searchName()" value='Search'/>
	【查找小区ID】
	<input type='text' id='cellId' style='width:130px;' value=''/>
	<input type='button' class='wyq4' onClick="searchID()" value='Search'/>
	【搜索地址】
	<input type='text' id='localsearch' style='width:350px;' value=''/>
	<input type='button' class='wyq4' onClick="searchLocal()" value='Search'/>
	</div>
	<div id="toolbar2">

	【拉框放大】
	<input type='button' class='wyq4' onClick="RectangleZoomOpen()" value='Start'/>
	<input type='button' class='wyq4' onClick="RectangleZoomEnd()" value='End'/>
	【清除绘制】
	<input type='button' class='wyq4' onClick="CleanDrawing()" value='Clean'/>
	【点击获取经纬度】
	<input type='button' class='wyq4' onClick="getLocationOn()" value='On'/>
	<input type='button' class='wyq4' onClick="getLocationOff()" value='Off'/>
	【标志拖拽】
	<input type='button' class='wyq4' onClick="MarkerDraggingOn()" value='On'/>
	<input type='button' class='wyq4' onClick="MarkerDraggingOff()" value='Off'/>
	【线面编辑】
	<input type='button' class='wyq4' onClick="EditingOn()" value='On'/>
	<input type='button' class='wyq4' onClick="EditingOff()" value='Off'/>
	【
	<input type='button' class='wyq4' onClick="DistanceOpen()" style="font-size:18px" value='测距'/>
	】【显示小区名】
	<input type='button' class='wyq4' onClick="LabelOpen()" value='Open'/>
	<input type='button' class='wyq4' onClick="LabelClose()" value='Close'/>
	</div>

    <div id="map"></div>
    <script type="text/javascript">
    var map = new BMap.Map("map", {});                        // 创建Map实例
    map.centerAndZoom(new BMap.Point(113.36399344396, 23.140918708809), 16);     // 初始化地图,设置中心点坐标和地图级别
    map.enableScrollWheelZoom();                        //启用滚轮放大缩小
	var top_left_control = new BMap.ScaleControl({anchor: BMAP_ANCHOR_TOP_LEFT});// 左上角，添加比例尺
	map.addControl(top_left_control);
	var top_left_navigation = new BMap.NavigationControl();  //左上角，添加默认缩放平移控件
	map.addControl(top_left_navigation);
	var mapType1 = new BMap.MapTypeControl({mapTypes: [BMAP_NORMAL_MAP,BMAP_HYBRID_MAP]});  // 2D图，卫星图
	map.addControl(mapType1);
	var mapType2 = new BMap.MapTypeControl({anchor: BMAP_ANCHOR_TOP_RIGHT});  //右上角，默认地图控件
	map.addControl(mapType2);
	map.setCurrentCity("北京");          // 设置地图显示的城市 此项是必须设置的
	/*
	// 覆盖区域图层测试
	map.addTileLayer(new BMap.PanoramaCoverageLayer());
	var stCtrl = new BMap.PanoramaControl(); //构造全景控件
	stCtrl.setOffset(new BMap.Size(130, 5));
	map.addControl(stCtrl);//添加全景控件
	*/
	// 添加小区
	for (var i=0; i<cell.length; i++)
	{
		var points_list = [];
		for (var j=0; j<cell[i].Polygon.length; j = j + 2)
		{
			points_list.push(new BMap.Point(cell[i].Polygon[j], cell[i].Polygon[j+1]));
		}
		var polyline = new BMap.Polyline(points_list, {strokeColor:"blue", strokeWeight:6, strokeOpacity:0.5});
		var info =  {
			CellName: cell[i].CellName,
			CellId: cell[i].CellId,
			SiteName: cell[i].SiteName,
			SiteId: cell[i].SiteId,
			Addr: [cell[i].lon, cell[i].lat],
			WCDMA_PSC: cell[i].WCDMA_PSC,
			LTE_PCI: cell[i].LTE_PCI,
			CDMA_PN: cell[i].CDMA_PN,
			GSM_BCCH: cell[i].GSM_BCCH,
			Azimuth: cell[i].Azimuth,
			TILT: cell[i].TILT,
			AntHeigth: cell[i].AntHeigth,
			RNC_BSC: cell[i].RNC_BSC,

		}
		map.addOverlay(polyline);
		addClickHandler(info,polyline);
	}
	// 打开文字标签
	LabelOpen();
	// 添加信息窗口
	function addClickHandler(info,polyline){
		polyline.addEventListener("click",function(e){
			openInfo(info,e)}
		);
	}
	function openInfo(info,e){
		// 信息窗口样式设置
		var opts = {
			width: 350, // 信息窗口宽度
			//height: 300, // 信息窗口高度
			title:"", // 信息窗口标题
			enableMessage: false,//设置允许信息窗发送短息
		};
		var infowindow = new BMap.InfoWindow(("小区名称:"+info.CellName
											+"<br/>小区ID:"+info.CellId
											+"<br/>基站名称:"+info.SiteName
											+"<br/>基站Id:"+info.SiteId
											+"<br/>位置:"+info.Addr[0]+","+info.Addr[1]
											+"<br/>WCDMA-PSC:"+info.WCDMA_PSC
											+"<br/>LTE-PCI:"+info.LTE_PCI
											+"<br/>CDMA-PN:"+info.CDMA_PN
											+"<br/>GSM-BCCH:"+info.GSM_BCCH
											+"<br/>Azimuth:"+info.Azimuth
											+"<br/>TILT:"+info.TILT
											+"<br/>AntHeigth:"+info.AntHeigth
											+"<br/>RNC-BSC:"+info.RNC_BSC), opts);  // 创建信息窗口对象
		map.openInfoWindow(infowindow,e.point); //开启信息窗口
	}

	// 按名字查找
	var marker = null
	function searchName(){
		var result = false;
		var keyword = document.getElementById("cellName").value;
		for (var i = 0; i < cell.length; i++){
			if (keyword == (cell[i].CellName))
			{
				result = true;
				if (marker != null)
				{
					map.removeOverlay(marker)
				};
				var point = new BMap.Point(cell[i].bd_lon, cell[i].bd_lat);
				/*
				var convertor = new BMap.Convertor();
				var pointArr = [];
				pointArr.push(point);
				convertor.translate(pointArr, 1, 5, function(data){
					if(data.status === 0) {
						marker = new BMap.Marker(data.points[0]);
						map.addOverlay(marker);
						map.centerAndZoom(point,16);
					}
				});
				*/
				marker = new BMap.Marker(point);
				map.addOverlay(marker);
				map.centerAndZoom(point,16);
			}
		}
		if (result == false)
		{
			alert("找不到结果");
		}
	}
	// 按ID查找
	function searchID(){
		var result = false;
		var keyword = document.getElementById("cellId").value;
		for (var i = 0; i < cell.length; i++){
			if (keyword == (cell[i].CellId))
			{
				result = true;
				if (marker != null)
				{
					map.removeOverlay(marker);
				};
				var point = new BMap.Point(cell[i].bd_lon, cell[i].bd_lat);
				/*
				var convertor = new BMap.Convertor();
				var pointArr = [];
				pointArr.push(point);
				convertor.translate(pointArr, 1, 5, function(data){
					if(data.status === 0) {
						marker = new BMap.Marker(data.points[0]);
						map.addOverlay(marker);
						map.centerAndZoom(point,16);
					}
				});
				*/
				marker = new BMap.Marker(point);
				map.addOverlay(marker);
				map.centerAndZoom(point,16);

			}
		}
		if (result == false)
		{
			alert("找不到结果");
		}
	}
	// 鼠标测距
	function DistanceOpen(){
		var myDis = new BMapLib.DistanceTool(map);
		myDis.open();  //开启鼠标测距
	}
	// 鼠标拉框放大
	var myDrag = new BMapLib.RectangleZoom(map, {followText: "拖拽鼠标进行操作"});
	function RectangleZoomOpen(){
		myDrag.open();  //开启拉框放大
	}
	function RectangleZoomEnd(){
		myDrag.close();  //开启拉框放大
	}
	//实例化鼠标绘制工具
	var overlays = [];
	var overlaycomplete = function(e){
        overlays.push(e.overlay);
	};
    var styleOptions = {
        strokeColor:"red",    //边线颜色。
        fillColor:"red",      //填充颜色。当参数为空时，圆形将没有填充效果。
        strokeWeight: 3,       //边线的宽度，以像素为单位。
        strokeOpacity: 0.8,	   //边线透明度，取值范围0 - 1。
        fillOpacity: 0.6,      //填充的透明度，取值范围0 - 1。
        strokeStyle: 'solid' //边线的样式，solid或dashed。
    }
    var drawingManager = new BMapLib.DrawingManager(map, {
        isOpen: false, //是否开启绘制模式
        enableDrawingTool: true, //是否显示工具栏
        drawingToolOptions: {
            anchor: BMAP_ANCHOR_TOP_RIGHT, //位置
            offset: new BMap.Size(135, 5), //偏离值
			scale: 0.7, //工具栏的缩放比例,默认为1
        },
        circleOptions: styleOptions, //圆的样式
        polylineOptions: styleOptions, //线的样式
        polygonOptions: styleOptions, //多边形的样式
        rectangleOptions: styleOptions //矩形的样式
    });
	 //添加鼠标绘制工具监听事件，用于获取绘制结果
    drawingManager.addEventListener('overlaycomplete', overlaycomplete);

	function CleanDrawing(){
		for(var i = 0; i < overlays.length; i++){
            map.removeOverlay(overlays[i]);
        }
        overlays.length = 0
	}
	// 鼠标点击获取坐标
	var getLocation = false
	function getPoint(e){
				alert(e.point.lng + "," + e.point.lat);
	}
	function getLocationOn(){
		if (getLocation == false)
		{
			map.addEventListener("click",getPoint);
			getLocation = true
		};
	}
	function getLocationOff(){
		if (getLocation == true)
		{
			map.removeEventListener("click",getPoint);
			getLocation = false
		};
	}
	// 地址搜索
	function searchLocal(){
		var keyword = document.getElementById("localsearch").value;
		// 创建地址解析器实例
		var myGeo = new BMap.Geocoder();
		// 将地址解析结果显示在地图上,并调整地图视野
		myGeo.getPoint(keyword, function(point){
			if (point) {
				map.centerAndZoom(point, 16);
				if (marker != null)
				{
					map.removeOverlay(marker)
				};
				marker = new BMap.Marker(point);
				map.addOverlay(marker);
			}else{
				alert("您选择地址没有解析到结果!");
			}
		}, "北京市");
	}
	// 点可移动
	function MarkerDraggingOn(){
		for (var i = 0; i < overlays.length; i++){
			if ((overlays[i] instanceof BMap.Marker))
			{
					if (overlays[i] != marker)
				{
					overlays[i].enableDragging();
				};
			};
		}
	}
	function MarkerDraggingOff(){
		for (var i = 0; i < overlays.length; i++){
			if (overlays[i] instanceof BMap.Marker)
			{
					if (overlays[i] != marker)
				{
					overlays[i].disableDragging();
				};
			};
		}
	}
	// 线面可编辑
	function EditingOn(){
		for (var i = 0; i < overlays.length; i++){
			if ((overlays[i] instanceof BMap.Polyline) || (overlays[i] instanceof BMap.Polygon))
			{
				overlays[i].enableEditing();
			};
		};
	}
	function EditingOff(){
		for (var i = 0; i < overlays.length; i++){
			if ((overlays[i] instanceof BMap.Polyline) || (overlays[i] instanceof BMap.Polygon))
			{
				overlays[i].disableEditing();
			};
		}
	}
	// 添加文字标签
	function LabelOpen(){
		for (var i=0; i<cell.length; i++)
		{
			var point = new BMap.Point(cell[i].bd_lon, cell[i].bd_lat);
			var label_opts = {
				position : point,    // 指定文本标注所在的地理位置
				offset   : new BMap.Size(0, 0)    //设置文本偏移量
			};
			var label = new BMap.Label(cell[i].SiteName, label_opts);  // 创建文本标注对象
			map.addOverlay(label);

		}
	}
	function LabelClose(){
		var allOverlay = map.getOverlays();
		for(var i = 0; i < allOverlay.length; i++){
			if (allOverlay[i] instanceof BMap.Label)
			{
				map.removeOverlay(allOverlay[i]);
			}
        }

	}

  </script>
</body>
</html>
"""

# 百度地图小区显示街景功能
Pano = u"""
<!DOCTYPE html>
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
	<title>百度地图街景工具</title>
	<style type="text/css">
        * {
            margin: 0px;
            padding: 0px;
        }
        body,
        button,
        input,
        select,
        textarea {
            font: 12px/16px Verdana, Helvetica, Arial, sans-serif;
        }
        p {
            width: 600px;
            padding-top: 3px;
            overflow: hidden;
        }
		div#pano_holder1{height:300px;width:610px;float:left;}
        div#map {height:300px;width:610px;float:left;}
		div#pano_holder {height:300px;width:610px;float:left;}
		div#panel {height:300px;width:610px;float:left;}
    </style>
	<script type="text/javascript" src="http://api.map.baidu.com/api?v=2.0&ak=BtvVWRqGfnffNqdqAN7rusTlb2E020C8"></script>
	<script src="cell.js"></script>
</head>
<body>
	<div id="pano_holder1"></div>
	<div id="map"></div>
	<div id="panel">
		<br/><br/>
		<span style="width:5px;">&nbsp;&nbsp;&nbsp;</span><span id="angle"></span><br/>
		<span style="width:5px;">&nbsp;&nbsp;&nbsp;</span><span id="distance"></span><br/>
		<span style="width:5px;">&nbsp;&nbsp;&nbsp;</span><span id="pano_lon"></span><br/>
		<span style="width:5px;">&nbsp;&nbsp;&nbsp;</span><span id="pano_lat"></span><br/>
		<span>
		<br/>
		<span style="width:5px;">&nbsp;&nbsp;&nbsp;</span>请输入小区信息：
		<br/>
		<br/>
		<span style="width:5px;">&nbsp;&nbsp;&nbsp;</span>经度:
		<input type="text" id="lon" style="width: 100px;height:25px;font-size:15px" />
		<span style="width:5px;">&nbsp;&nbsp;&nbsp;</span>纬度:
		<input type="text" id="lat" style="width: 100px;height:25px;font-size:15px" />
		<span style="width:5px;">&nbsp;&nbsp;&nbsp;</span>小区规划名：
		<input type="text" id="CellName" name="CellName" style="width: 125px;height:25px;font-size:15px" />
		<input type="button" class="button" value="显示街景" id="setMarker" onclick="setMarker()" style="width:75px;height:28px;font-size:16px"/>
		<br/>
		<br/>
		<span style="width:5px;">&nbsp;&nbsp;&nbsp;</span>基站搜索：
		<input type="radio" name="SearchType" id="SearchID" value="ID" checked>按小区ID
		<input type="radio" name="SearchType" id="SearchName" value="Name">按小区名称
		<br/><br/>
		<span style="width:5px;">&nbsp;&nbsp;&nbsp;</span>
		<input type="text" id="Search" name="Search" style="width:450px;height:25px;font-size:15px" />
		<input type="button" class="button" value="搜索并显示街景" id="setMarker" onclick="search()" style="width:120px;height:28px;font-size:15px"/>
		</span>
	</div>
	<div id="pano_holder"></div>

</body>
</html>
<script type="text/javascript">
	// 百度地图初始化
	var map = new BMap.Map("map");    // 创建Map实例
	map.centerAndZoom(new BMap.Point(113.36399344396, 23.140918708809), 16);  // 初始化地图,设置中心点坐标和地图级别
	map.addControl(new BMap.MapTypeControl());   //添加地图类型控件
	map.setCurrentCity("北京");          // 设置地图显示的城市 此项是必须设置的
	map.enableScrollWheelZoom(true);     //开启鼠标滚轮缩放
	map.addTileLayer(new BMap.PanoramaCoverageLayer()); // 全景覆盖区域图层测试
	// 添加小区
	for (var i=0; i<cell.length; i++)
	{
		var points_list = [];
		for (var j=0; j<cell[i].Polygon.length; j = j + 2)
		{
			points_list.push(new BMap.Point(cell[i].Polygon[j], cell[i].Polygon[j+1]));
		}
		var polyline = new BMap.Polyline(points_list, {strokeColor:"blue", strokeWeight:6, strokeOpacity:0.5});
		var info =  {
			CellName: cell[i].CellName,
			CellId: cell[i].CellId,
			SiteName: cell[i].SiteName,
			CellId: cell[i].CellId,
			Addr: [cell[i].lon, cell[i].lat],
			WCDMA_PSC: cell[i].WCDMA_PSC,
			LTE_PCI: cell[i].LTE_PCI,
			CDMA_PN: cell[i].CDMA_PN,
			GSM_BCCH: cell[i].GSM_BCCH,
			Azimuth: cell[i].Azimuth,
			TILT: cell[i].TILT,
			AntHeigth: cell[i].AntHeigth,
			RNC_BSC: cell[i].RNC_BSC,

		}
		map.addOverlay(polyline);
		addClickHandler(info,polyline);
	}
	// 打开文字标签
	LabelOpen();
	// 添加文字标签
	function LabelOpen(){
		for (var i=0; i<cell.length; i++)
		{
			var point = new BMap.Point(cell[i].bd_lon, cell[i].bd_lat);
			var label_opts = {
				position : point,    // 指定文本标注所在的地理位置
				offset   : new BMap.Size(0, 0)    //设置文本偏移量
			};
			var label = new BMap.Label(cell[i].SiteName, label_opts);  // 创建文本标注对象
			map.addOverlay(label);

		}
	}
	// 添加信息窗口
	function addClickHandler(info,polyline){
		polyline.addEventListener("click",function(e){
			openInfo(info,e)}
		);
	}
	function openInfo(info,e){
		// 信息窗口样式设置
		var opts = {
			width: 350, // 信息窗口宽度
			//height: 300, // 信息窗口高度
			title:"", // 信息窗口标题
			enableMessage: false,//设置允许信息窗发送短息
		};
		var infowindow = new BMap.InfoWindow(("小区名称:"+info.CellName
											+"<br/>小区ID:"+info.CellId
											+"<br/>基站名称:"+info.SiteName
											+"<br/>基站Id:"+info.CellId
											+"<br/>位置:"+info.Addr[0]+","+info.Addr[1]
											+"<br/>WCDMA-PSC:"+info.WCDMA_PSC
											+"<br/>LTE-PCI:"+info.LTE_PCI
											+"<br/>CDMA-PN:"+info.CDMA_PN
											+"<br/>GSM-BCCH:"+info.GSM_BCCH
											+"<br/>Azimuth:"+info.Azimuth
											+"<br/>TILT:"+info.TILT
											+"<br/>AntHeigth:"+info.AntHeigth
											+"<br/>RNC-BSC:"+info.RNC_BSC), opts);  // 创建信息窗口对象
		map.openInfoWindow(infowindow,e.point); //开启信息窗口
	}
	// 设置基站Marker
	var lon = null;
	var lat = null;
	var marker = null;
	var cell_point = null;
	function setMarker()
	{
		lon = document.getElementById("lon").value;
		lat = document.getElementById("lat").value;
		cell_name = document.getElementById("CellName").value;
		if (lon != "" && lat != "")
		{
			lon = document.getElementById("lon").value;
			lat = document.getElementById("lat").value;
			if (marker != null)
			{
				map.removeOverlay(marker);
			};
			var point = new BMap.Point(lon, lat);
			var convertor = new BMap.Convertor();
			var pointArr = [];
			pointArr.push(point);
			convertor.translate(pointArr, 1, 5, function(data){
				if(data.status === 0)
				{
					marker = new BMap.Marker(data.points[0]);
					cell_point = data.points[0];
					map.addOverlay(marker);
					map.centerAndZoom(data.points[0],16);
					if (cell_name != "")
					{
						var opts = {
						  width : 220,     // 信息窗口宽度（0为自动调整,220 - 730）
						  height: 60,     // 信息窗口高度（0为自动调整,60 - 650）
						}
						var infoWindow = new BMap.InfoWindow(cell_name, opts);  // 创建信息窗口对象
						map.openInfoWindow(infoWindow,data.points[0]); //开启信息窗口
						marker.addEventListener("click", function(){
							map.openInfoWindow(infoWindow,data.points[0]); //开启信息窗口
						});
					};
					var panorama = new BMap.Panorama('pano_holder');
					panorama.setPov({heading: -40, pitch: 6});
					panorama.setPosition(data.points[0]); //根据经纬度坐标展示全景图
				}
			});
		}
		else
		{
			alert("请输入经纬度信息");
		};
	}
	// 从现有小区中搜索
	function search()
	{
		if (document.getElementById("SearchName").checked == true) // 按基站名称搜索
		{
			var result = false;
			var keyword = document.getElementById("Search").value;
			for (var i = 0; i < cell.length; i++){
				if (keyword == (cell[i].CellName))
				{
					result = true;
					if (marker != null)
					{
						map.removeOverlay(marker);
					};
					var point = new BMap.Point(cell[i].bd_lon, cell[i].bd_lat);
					marker = new BMap.Marker(point);
					cell_point = point;
					map.addOverlay(marker);
					map.centerAndZoom(point,18);
					var panorama = new BMap.Panorama('pano_holder');
					panorama.setOptions({ navigationControl: true }); // 显示导航控件
					panorama.setPov({heading: -40, pitch: 6});
					panorama.setPosition(point); //根据经纬度坐标展示全景图
				}
			}
			if (result == false)
			{
				alert("找不到结果");
			}
		}
		else // 按基站ID搜索
		{
			var result = false;
			var keyword = document.getElementById("Search").value;
			for (var i = 0; i < cell.length; i++){
				if (keyword == (cell[i].CellId))
				{
					result = true;
					if (marker != null)
					{
						map.removeOverlay(marker)
					};
					var point = new BMap.Point(cell[i].bd_lon, cell[i].bd_lat);
					marker = new BMap.Marker(point);
					cell_point = point;
					map.addOverlay(marker);
					map.centerAndZoom(point,18);
					var panorama = new BMap.Panorama('pano_holder');
					panorama.setOptions({ navigationControl: true }); // 显示导航控件
					panorama.setPov({heading: -40, pitch: 6});
					panorama.setPosition(point); //根据经纬度坐标展示全景图

				}
			}
			if (result == false)
			{
				alert("找不到结果");
			}
		}

	}
	// 监听地图添加要显示的街景
	var marker1 = null; // 街景Marker
	var pano_point = null; // 街景Point
	var polyline = null;
	var panorama1 = null; // 定义街景图层
	map.addEventListener("click",function(e){
		if (marker != null)
		{
				if (marker1 != null)
			{
				map.removeOverlay(marker1); // 移除原有标注
				map.removeOverlay(polyline);
			};
			marker1 = new BMap.Marker(e.point,{icon:new BMap.Icon("http://api.map.baidu.com/lbsapi/createmap/images/icon.png",new BMap.Size(20,25),{imageOffset: new BMap.Size(-23,3)})});
			marker1.setOffset(new BMap.Size(0,-6));
			map.addOverlay(marker1);
			panorama1 = new BMap.Panorama('pano_holder1');
			panorama1.setOptions({ navigationControl: true }); // 显示导航控件
			panorama1.setPov({heading: -40, pitch: 6});
			panorama1.setPosition(e.point); //根据经纬度坐标展示全景图
			pano_point = panorama1.getPosition();

			// 计算街景位置与基站夹角
			if ((pano_point.lng>cell_point.lng)&&(pano_point.lat>cell_point.lat))
			{
				angle = Math.atan((pano_point.lng - cell_point.lng) / (pano_point.lat - cell_point.lat));
				document.getElementById("angle").innerHTML ="街景位置与基站夹角"+Math.abs(angle)/Math.PI*180+"度";
			}
			else if ((pano_point.lng>cell_point.lng)&&(pano_point.lat<cell_point.lat))
			{
				angle = Math.atan(Math.abs(pano_point.lng - cell_point.lng) / Math.abs(pano_point.lat - cell_point.lat));
				document.getElementById("angle").innerHTML ="街景位置与基站夹角"+(180-(Math.abs(angle)/Math.PI*180))+"度";
			}
			else if ((pano_point.lng<cell_point.lng)&&(pano_point.lat<cell_point.lat))
			{
				angle = Math.atan(Math.abs(pano_point.lng - cell_point.lng) / Math.abs(pano_point.lat - cell_point.lat));
				document.getElementById("angle").innerHTML ="街景位置与基站夹角"+(-180+(Math.abs(angle)/Math.PI*180))+"度";
			}
			else if ((pano_point.lng<cell_point.lng)&&(pano_point.lat>cell_point.lat))
			{
				angle = Math.atan(Math.abs(pano_point.lng - cell_point.lng) / Math.abs(pano_point.lat - cell_point.lat));
				document.getElementById("angle").innerHTML ="街景位置与基站夹角"+(-(Math.abs(angle)/Math.PI*180))+"度";
			}
			else if ((pano_point.lng=cell_point.lng)&&(pano_point.lat>cell_point.lat))
			{
				document.getElementById("angle").innerHTML ="街景位置与基站夹角"+"0度";
			}
			else if ((pano_point.lng>cell_point.lng)&&(pano_point.lat=cell_point.lat))
			{
				document.getElementById("angle").innerHTML ="街景位置与基站夹角"+"90度";
			}
			else if ((pano_point.lng<cell_point.lng)&&(pano_point.lat=cell_point.lat))
			{
				document.getElementById("angle").innerHTML ="街景位置与基站夹角"+"-90度";
			}
			else
			{
				document.getElementById("angle").innerHTML ="街景位置与基站夹角"+"180度";
			};
			// 计算街景位置与基站距离
			document.getElementById("distance").innerHTML ="街景位置与基站距离"+map.getDistance(cell_point,pano_point).toFixed(2)+"米";
			polyline = new BMap.Polyline([cell_point,pano_point], {strokeColor:"blue", strokeWeight:6, strokeOpacity:0.5});  //定义折线
			map.addOverlay(polyline);     //添加折线到地图上
			// 显示街景经纬度
			document.getElementById("pano_lon").innerHTML ="街景位置经度：" + pano_point.lng;
			document.getElementById("pano_lat").innerHTML ="街景位置纬度：" + pano_point.lat;
		};
	});


</script>
"""