# -*- coding:utf-8 -*-
'''
腾讯地图小区数据html模板
@author: Karwai Kwok
'''

# 腾讯地图小区数据html模板
class TencentCellTemplate(object):
    def __init__(self, key=u"G2TBZ-VWXR5-XKRIU-QOTEH-LWV4Z-R3FSW"):
        super(TencentCellTemplate, self).__init__()
        self.key = key

    def getHead(self):
        output = u"""
            <!DOCTYPE html>
            <html>
            <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            <title>腾讯地图小区显示</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no"/>
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
            </style>
            <script charset="utf-8" src="http://map.qq.com/api/js?v=2.exp&libraries=drawing,geometry&key=""" + self.key + \
            u""""></script>
            <script src="cell.js"></script>
            </head>
            <body>
            <div id="toolbar1">【查找基站名称】
                <input type='text' id='cellName' style='width:150px;' value=''/>
                <input type='button' class='wyq4' onClick="searchName()" value='Search'/>
                【查找基站ID】
                <input type='text' id='cellId' style='width:130px;' value=''/>
                <input type='button' class='wyq4' onClick="searchID()" value='Search'/>
                【搜索地址】
                <input type='text' id='address' style='width:350px;' value=''/>
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
                【测距】
                <input type='button' class='wyq4' onClick="DistanceOpen()" style="font-size:18px" value='On'/>
                <input type='button' class='wyq4' onClick="DistanceOff()" style="font-size:18px" value='Off'/>
                【显示小区名】
                <input type='button' class='wyq4' onClick="LabelOpen()" value='Open'/>
                <input type='button' class='wyq4' onClick="LabelClose()" value='Close'/>
            </div>
            <div id="map"></div>
            <script type="text/javascript">
                // 加载地图
                var map = new qq.maps.Map(document.getElementById("map"), {
                        center: new qq.maps.LatLng(23.13513,113.35747),      // 地图的中心地理坐标。
                        zoom:10                                                 // 地图的中心地理坐标。
                });
                var infoWin = new qq.maps.InfoWindow({
                    map: map
                });
                // 载入小区
                var labelArry = [] // 保存所有基站名label
                for (var i=0; i<cell.length; i++)
                {
                    (function(n){
                        var position = new qq.maps.LatLng(cell[n].qq_lat,cell[n].qq_lon); // 基站所在坐标
                        var path = []; // polygon 路径
                        for (var j=0; j<cell[n].Polygon.length; j=j+2)
                        {
                            path.push(new qq.maps.LatLng(cell[n].Polygon[j+1], cell[n].Polygon[j]));
                        }
                        if (path.length == 1)
                        {
                            var polygon=new qq.maps.Circle({
                                map:map,
                                center:position,
                                radius:60,
                                //fillColor:"#00f",
                                strokeWeight:2
                            });
                        }
                        else
                        {
                            var polygon = new qq.maps.Polygon({
                                path:path,
                                strokeWeight: 2,
                                map: map
                            });
                        }
                        var label = new qq.maps.Label ({
                            position : position,    // 指定文本标注所在的地理位置
                            map: map,
                            content: cell[n].SiteName,
                            visible: false // 默认标签不可见
                        });
                        labelArry.push(label);
                        qq.maps.event.addListener(polygon, 'click', function() {
                            infoWin.open();
                            infoWin.setContent("小区名称:"+cell[n].CellName+"<br/>小区ID:"+cell[n].CellId+"<br/>经纬度:"+cell[n].lon +","+cell[n].lat);
                            infoWin.setPosition(position);
                        });
                    })(i);
                }
                // 查找功能
                var markersArray = []; // 查找结果
                // 查找小区名称
                function searchName()
                {
                    var result = false;
                    var keyword = document.getElementById("cellName").value;
                    for (var i = 0; i < cell.length; i++){
                        if (keyword == (cell[i].CellName))
                        {
                            result = true;
                            if (markersArray.length != 0)
                            {
                                for (j in markersArray)
                                {
                                    markersArray[j].setMap(null);
                                }
                                markersArray.length = 0;
                            };
                            /*
                            var anchor = new qq.maps.Point(6, 6),
                                size = new qq.maps.Size(24, 24),
                                origin = new qq.maps.Point(0, 0),
                                icon = new qq.maps.MarkerImage('http://lbs.qq.com/doc/img/center.gif', size, origin, anchor);
                            */
                            var marker = new qq.maps.Marker({
                                //icon: icon,
                                position: new qq.maps.LatLng(cell[i].qq_lat,cell[i].qq_lon),
                                map: map
                            });
                            //marker.setIcon(icon);
                            infoWin.open();
                            infoWin.setContent("小区名称:"+cell[i].CellName+"<br/>小区ID:"+cell[i].CellId+"<br/>经纬度:"+cell[i].lon +","+cell[i].lat);
                            infoWin.setPosition(new qq.maps.LatLng(cell[i].qq_lat,cell[i].qq_lon));

                            markersArray.push(marker);
                            map.panTo(new qq.maps.LatLng(cell[i].qq_lat,cell[i].qq_lon));
                            map.zoomTo(18);
                        }
                    }
                    if (result == false)
                    {
                        alert("找不到结果");
                    }
                }
                // 查找基站ID
                function searchID()
                {
                    var result = false;
                    var keyword = document.getElementById("cellId").value;
                    for (var i = 0; i < cell.length; i++){
                        if (keyword == (cell[i].CellId))
                        {
                            result = true;
                            if (markersArray.length != 0)
                            {
                                for (j in markersArray)
                                {
                                    markersArray[j].setMap(null);
                                }
                                markersArray.length = 0;
                            };
                            //var anchor = new qq.maps.Point(6, 6),
                            //	size = new qq.maps.Size(24, 24),
                            //	origin = new qq.maps.Point(0, 0),
                            //	icon = new qq.maps.MarkerImage('http://lbs.qq.com/doc/img/center.gif', size, origin, anchor);
                            var marker = new qq.maps.Marker({
                                //icon: icon,
                                position: new qq.maps.LatLng(cell[i].qq_lat,cell[i].qq_lon),
                                map: map
                            });
                            //marker.setIcon(icon);
                            infoWin.open();
                            infoWin.setContent("小区名称:"+cell[i].CellName+"<br/>小区ID:"+cell[i].CellId+"<br/>经纬度:"+cell[i].lon +","+cell[i].lat);
                            infoWin.setPosition(new qq.maps.LatLng(cell[i].qq_lat,cell[i].qq_lon));

                            markersArray.push(marker);
                            map.panTo(new qq.maps.LatLng(cell[i].qq_lat,cell[i].qq_lon));
                            map.zoomTo(18);

                        }
                    }
                    if (result == false)
                    {
                        alert("找不到结果");
                    }
                }
                //  搜索地址
                //调用地址解析类
                var geocoder = new qq.maps.Geocoder({
                    complete : function(result){
                        if (markersArray.length != 0)
                        {
                            for (j in markersArray)
                            {
                                markersArray[j].setMap(null);
                            }
                            markersArray.length = 0;
                        };
                        map.setCenter(result.detail.location);
                        var marker = new qq.maps.Marker({
                            map:map,
                            position: result.detail.location
                        });
                        markersArray.push(marker);
                        map.zoomTo(18);
                    }
                });
                function searchLocal()
                {
                    var address = document.getElementById("address").value;
                    //通过getLocation();方法获取位置信息值
                    geocoder.getLocation(address);
                }

                // 拉框放大功能
                var startPoint={left:0,top:0},//选框的起点
                  endPoint={left:0,top:0},//选框的终点
                  cor,//遮罩层
                  flag=true,//是否允许创建遮罩层
                  area,//选区
                  fla=true,//是否允许创建选区
                  ele;//地图容器
                // 开启拉框放大
                function RectangleZoomOpen()
                {
                    // 创建一个遮罩层
                    ele=document.getElementById("map");
                    //设置元素的宽高
                    var wid=ele.offsetWidth,hei=ele.offsetHeight;
                    //创建遮罩层元素
                    cor=document.createElement("div");
                    //创建元素的宽与高 并且设置样式
                    cor.style.cssText="width:"+wid+"px;height:"+hei+
                    "px;background:#999;opacity:0.3;filter:alpha"+
                    "(opacity=30);position:absolute;top:0px;z-index:9998;";
                    //添加遮罩层到元素
                    ele.appendChild(cor);
                    //绑定鼠标事件  鼠标单击按下触发函数
                    cor.onmousedown=setStartPoint;
                }
                //设置起点的位置，并创建一个空的div
                function setStartPoint(e)
                {
                    //解决怪异模式
                    var e=e||window.event;
                    //获取鼠标起始点左侧边距
                    startPoint.left=e.clientX-ele.offsetLeft;
                    //获取鼠标起始点顶部边距
                    startPoint.top=e.clientY-ele.offsetTop;
                    if(fla==true){
                        fla=false;
                        area=document.createElement("div");         //创建div遮罩层
                        ele.appendChild(area);
                    }else{
                        fla=true;
                        area.parentNode.removeChild(area);
                    }
                    cor.onmousemove=createArea;
                    cor.onmouseup=resetMap;
                }
                //创建选区
                function createArea(e)
                {
                    var e=e||window.event;
                    endPoint.left=e.clientX-ele.offsetLeft;
                    endPoint.top=e.clientY-ele.offsetTop;
                    var wid=endPoint.left-startPoint.left,hei=endPoint.top-startPoint.top;
                    area.style.cssText="width:"+wid+"px;height:"+hei+
                        "px;position:absolute;left:"+startPoint.left+
                        "px;top:"+startPoint.top+
                        "px;border:2px solid #0f0;";
                    return false;
                }
                //重置地区的中心点和放大级别
                function resetMap()
                {
                    var SW={left:startPoint.left,top:endPoint.top},
                        NE={left:endPoint.left,top:startPoint.top};
                    var SWP=new qq.maps.Point(SW.left,SW.top),
                        NEP=new qq.maps.Point(NE.left,NE.top);
                    map.fitBounds(new qq.maps.LatLngBounds(
                        map.get('mapCanvasProjection').fromContainerPixelToLatLng(SWP),
                        map.get('mapCanvasProjection').fromContainerPixelToLatLng(NEP)
                    ));
                    //cor.parentNode.removeChild(cor);
                    area.parentNode.removeChild(area);
                    //flag=true;
                    fla=true;
                }
                // 开启拉框放大
                function RectangleZoomEnd()
                {
                    cor.parentNode.removeChild(cor);
                    fla=false;
                }
                // 鼠标点击获取经纬度
                var getLocation = null
                // 开启
                function getLocationOn()
                {
                    //如果未开启则添加监听事件
                    if (getLocation == null)
                    {
                        getLocation = qq.maps.event.addListener(map, 'click', function(e) {
                            var latLng = e.latLng,
                                lat = latLng.getLat().toFixed(5),
                                lng = latLng.getLng().toFixed(5);
                                alert(lng + "," + lat);
                        });
                    };
                }
                // 关闭
                function getLocationOff(){
                    if (getLocation != null)
                    {
                         qq.maps.event.removeListener(getLocation);
                         getLocation = null
                    };
                }
                // 添加地图绘制工具
                //实例化鼠标绘制工具
                var overlays = [];
                var drawingManager = new qq.maps.drawing.DrawingManager({
                    drawingMode: qq.maps.drawing.OverlayType.MARKER,
                    drawingControl: true,
                    drawingControlOptions: {
                        position: qq.maps.ControlPosition.TOP_RIGHT,
                        drawingModes: [
                            qq.maps.drawing.OverlayType.MARKER,
                            qq.maps.drawing.OverlayType.CIRCLE,
                            qq.maps.drawing.OverlayType.POLYGON,
                            qq.maps.drawing.OverlayType.POLYLINE,
                            qq.maps.drawing.OverlayType.RECTANGLE
                        ]
                    },
                    circleOptions: {
                        fillColor: new qq.maps.Color(255, 208, 70, 0.3),
                        strokeColor: new qq.maps.Color(88, 88, 88, 1),
                        strokeWeight: 3,
                        clickable: false
                    }
                });
                drawingManager.setMap(map);
                //设置overlaycomplete事件
                qq.maps.event.addListener(drawingManager, 'overlaycomplete', function(e) {
                    // 把绘制的图形添加到 overlays 中
                    overlays.push(e.overlay);
                });

                // 清除绘制
                function CleanDrawing()
                {
                    if (overlays.length != 0)
                    {
                        for (i in overlays)
                        {
                            overlays[i].setMap(null);
                        }
                        overlays.length = 0;
                    };
                }
                // 绘制的点可移动
                function MarkerDraggingOn()
                {
                    for (var i = 0; i < overlays.length; i++){
                        if ((overlays[i] instanceof qq.maps.Marker))
                        {
                            overlays[i].setDraggable(true);
                        };
                    }
                }
                // 绘制的点不可移动
                function MarkerDraggingOff()
                {
                    for (var i = 0; i < overlays.length; i++){
                        if ((overlays[i] instanceof qq.maps.Marker))
                        {
                            overlays[i].setDraggable(false);
                        };
                    }
                }
                // 绘制的线面可编辑
                function EditingOn()
                {
                    for (var i = 0; i < overlays.length; i++){
                        if ((overlays[i] instanceof qq.maps.Polyline) || (overlays[i] instanceof qq.maps.Polygon))
                        {
                            var Options = {editable: true}
                            overlays[i].setOptions(Options);
                        };
                    };
                }
                // 绘制的线面不可编辑
                function EditingOff()
                {
                    for (var i = 0; i < overlays.length; i++){
                        if ((overlays[i] instanceof qq.maps.Polyline) || (overlays[i] instanceof qq.maps.Polygon))
                        {
                            var Options = {editable: false}
                            overlays[i].setOptions(Options);
                        };
                    };
                }
                // 鼠标测距
                var distanceListener = null;
                function DistanceOpen()
                {
                    var path = null; // 路径
                    var start = null; //  起始点
                    var end = null; // 终止点
                    distanceListener = qq.maps.event.addListener(drawingManager, 'overlaycomplete', function(e) {
                        // 把绘制的图形添加到 overlays 中
                        if (e.overlay instanceof qq.maps.Polyline)
                        {
                            path = e.overlay.getPath();
                            start = path.getAt(0);
                            end = path.getAt(path.length-1);
                            alert("起始点间的距离为： " + qq.maps.geometry.spherical.computeDistanceBetween(start, end) + "米");
                        };
                    });
                }
                function DistanceOff()
                {
                    if (distanceListener != null)
                    {
                        qq.maps.event.removeListener(distanceListener);
                        distanceListener = null
                    };
                }
                // 小区名字标签
                function LabelOpen()
                {
                    if (labelArry.length > 0)
                    {
                        for (var i=0; i<labelArry.length; i++)
                        {
                            labelArry[i].setVisible(true);
                        }
                    };
                }
                function LabelClose()
                {
                    if (labelArry.length > 0)
                    {
                        for (var i=0; i<labelArry.length; i++)
                        {
                            labelArry[i].setVisible(false);
                        }
                    };
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
                <title>腾讯地图小区街景工具</title>
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
                <script charset="utf-8"    src="http://map.qq.com/api/js?v=2.exp&libraries=drawing,geometry,convertor&key=""" + self.key + \
            u""""></script>
                <script src="cell.js"></script>
            </head>
            <body>
                <div id="pano_holder1"></div>
                <div id="map"></div>
                <div id="panel">

                    <span style="width:5px;">&nbsp;&nbsp;&nbsp;</span><span id="angle"></span><br/>
                    <span style="width:5px;">&nbsp;&nbsp;&nbsp;</span><span id="distance"></span><br/>
                    <span style="width:5px;">&nbsp;&nbsp;&nbsp;</span><span id="pano_lon"></span><br/>
                    <span style="width:5px;">&nbsp;&nbsp;&nbsp;</span><span id="pano_lat"></span><br/>
                    <span>
                    <br/>
                    <span style="width:5px;">&nbsp;&nbsp;&nbsp;</span>请输入基站信息：
                    <br/>
                    <br/>
                    <span style="width:5px;">&nbsp;&nbsp;&nbsp;</span>经度:
                    <input type="text" id="lon" style="width: 100px;height:25px;font-size:15px" />
                    <span style="width:5px;">&nbsp;&nbsp;&nbsp;</span>纬度:
                    <input type="text" id="lat" style="width: 100px;height:25px;font-size:15px" />
                    <span style="width:5px;">&nbsp;&nbsp;&nbsp;</span>基站规划名：
                    <input type="text" id="SiteName" name="SiteName" style="width: 125px;height:25px;font-size:15px" />
                    <input type="button" class="button" value="显示街景" id="setMarker" onclick="setMarker()" style="width:75px;height:28px;font-size:16px"/>
                    <br/>
                    <br/>
                    <span style="width:5px;">&nbsp;&nbsp;&nbsp;</span>基站搜索：
                    <input type="radio" name="SearchType" id="SearchID" value="ID" checked>按基站ID
                    <input type="radio" name="SearchType" id="SearchName" value="Name">按基站名称
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
                // 加载地图
                var map = new qq.maps.Map(document.getElementById("map"), {
                        center: new qq.maps.LatLng(23.13513,113.35747),      // 地图的中心地理坐标。
                        zoom:16                                                 // 地图的中心地理坐标。
                });
                var infoWin = new qq.maps.InfoWindow({
                    map: map
                });
                //设置路网图层
                var pano_layer = new qq.maps.PanoramaLayer();
                pano_layer.setMap(map);
                // 载入小区
                var labelArry = [] // 保存所有基站名label
                for (var i=0; i<cell.length; i++)
                {
                    (function(n){
                        var position = new qq.maps.LatLng(cell[n].qq_lat,cell[n].qq_lon); // 基站所在坐标
                        var path = []; // polygon 路径
                        for (var j=0; j<cell[n].Polygon.length; j=j+2)
                        {
                            path.push(new qq.maps.LatLng(cell[n].Polygon[j+1], cell[n].Polygon[j]));
                        }
                        if (path.length == 1)
                        {
                            var polygon=new qq.maps.Circle({
                                map:map,
                                center:position,
                                radius:60,
                                //fillColor:"#00f",
                                strokeWeight:2
                            });
                        }
                        else
                        {
                            var polygon = new qq.maps.Polygon({
                                path:path,
                                strokeWeight: 2,
                                map: map
                            });
                        }
                        var label = new qq.maps.Label ({
                            position : position,    // 指定文本标注所在的地理位置
                            map: map,
                            content: cell[n].SiteName,
                            visible: true // 默认标签可见
                        });
                        labelArry.push(label);
                        qq.maps.event.addListener(polygon, 'click', function() {
                            infoWin.open();
                            infoWin.setContent("小区名称:"+cell[n].CellName+"<br/>小区ID:"+cell[n].CellId+"<br/>经纬度:"+cell[n].lon +","+cell[n].lat);
                            infoWin.setPosition(position);
                        });
                    })(i);
                }

                // 设置基站Marker
                var lon = null;
                var lat = null;
                var markersArray = [];
                var cell_point = null;
                function setMarker()
                {
                    lon = document.getElementById("lon").value;
                    lat = document.getElementById("lat").value;
                    cell_name = document.getElementById("SiteName").value;
                    if (lon != "" && lat != "")
                    {
                        lon = document.getElementById("lon").value;
                        lat = document.getElementById("lat").value;
                        if (markersArray.length != 0)
                        {
                            for (j in markersArray)
                            {
                                markersArray[j].setMap(null);
                            }
                            markersArray.length = 0;
                        };
                        var point = new qq.maps.LatLng(lat,lon);
                        qq.maps.convertor.translate(point, 1, function(res) {
                            latlng = res[0];
                            var marker = new qq.maps.Marker({
                                map: map,
                                position: latlng
                            });
                            cell_point = latlng;
                            markersArray.push(marker);
                            map.panTo(latlng);
                            map.zoomTo(18);
                            // 添加信息窗口
                            if (cell_name != "")
                            {
                                qq.maps.event.addListener(marker, 'click', function() {
                                    infoWin.open();
                                    infoWin.setContent(cell_name);
                                    infoWin.setPosition(latlng);
                                });
                            };
                            // 创建街景
                            var pano = new qq.maps.Panorama(document.getElementById('pano_holder'));
                            pano.setPov({
                                heading: -40,
                                pitch: 6
                            });
                            //创建街景类
                            pano_service = new qq.maps.PanoramaService();
                            var radius;
                            pano_service.getPano(point, radius, function (result){
                                pano.setPano(result.svid);
                            });
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
                                if (markersArray.length != 0)
                                {
                                    for (j in markersArray)
                                    {
                                        markersArray[j].setMap(null);
                                    }
                                    markersArray.length = 0;
                                };
                                var point = new qq.maps.LatLng(cell[i].qq_lat, cell[i].qq_lon);
                                var marker = new qq.maps.Marker({
                                    position: point,
                                    map: map
                                });
                                markersArray.push(marker);
                                map.panTo(point);
                                map.zoomTo(18);

                                cell_point = point;
                                // 创建街景
                                var pano = new qq.maps.Panorama(document.getElementById('pano_holder'));
                                pano.setPov({
                                    heading: -40,
                                    pitch: 6
                                });
                                //创建街景类
                                pano_service = new qq.maps.PanoramaService();
                                var radius;
                                pano_service.getPano(point, radius, function (result){
                                    pano.setPano(result.svid);
                                });
                            };
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
                                if (markersArray.length != 0)
                                {
                                    for (j in markersArray)
                                    {
                                        markersArray[j].setMap(null);
                                    }
                                    markersArray.length = 0;
                                };
                                var point = new qq.maps.LatLng(cell[i].qq_lat, cell[i].qq_lon);
                                var marker = new qq.maps.Marker({
                                    position: point,
                                    map: map
                                });
                                markersArray.push(marker);
                                map.panTo(point);
                                map.zoomTo(18);

                                cell_point = point;
                                // 创建街景
                                var pano = new qq.maps.Panorama(document.getElementById('pano_holder'));
                                pano.setPov({
                                    heading: -40,
                                    pitch: 6
                                });
                                //创建街景类
                                pano_service = new qq.maps.PanoramaService();
                                var radius;
                                pano_service.getPano(point, radius, function (result){
                                    pano.setPano(result.svid);
                                });

                            }
                        }
                        if (result == false)
                        {
                            alert("找不到结果");
                        }
                    }

                }
                // 监听地图添加要显示的街景
                var markersArray1 = []; // 街景Marker列表(包含polyline连线)
                var pano_point = null; // 街景Point
                //var polylineArray = []; // 保存polyline连线的数组
                var panorama1 = null; // 定义街景图层
                qq.maps.event.addListener(map,"click",function(e){
                    if ((markersArray.length != 0) && (cell_point != null))
                    {
                        if (markersArray1.length != 0)
                        {
                            for (j in markersArray1)
                            {
                                markersArray1[j].setMap(null); // 移除原有标注
                            }
                            markersArray1.length = 0;
                        };
                        var position = e.latLng;
                        var marker = new qq.maps.Marker({
                            position: position,
                            map: map
                        });
                        markersArray1.push(marker);
                        //map.zoomTo(18);
                        // 创建街景
                        var pano1 = new qq.maps.Panorama(document.getElementById('pano_holder1'));
                        pano1.setPov({
                            heading: -40,
                            pitch: 6
                        });
                        //创建街景类
                        pano_service1 = new qq.maps.PanoramaService();
                        var radius;
                        pano_service1.getPano(position, radius, function (result){
                            pano1.setPano(result.svid);
                        });

                        pano_point = position;

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
                        document.getElementById("distance").innerHTML ="街景位置与基站距离"+qq.maps.geometry.spherical.computeDistanceBetween(cell_point,pano_point).toFixed(2)+"米";
                        //添加连线
                        var line_path = [cell_point, pano_point];
                        var polyline = new qq.maps.Polyline({
                            path: line_path,
                            editable:false,
                            map: map
                        });
                        markersArray1.push(polyline);
                        // 显示街景经纬度
                        document.getElementById("pano_lon").innerHTML ="街景位置经度：" + pano_point.lng;
                        document.getElementById("pano_lat").innerHTML ="街景位置纬度：" + pano_point.lat;
                    };
                });

            </script>
            """

        return output

# 腾讯地图小区显示主页面
Head = u"""
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>腾讯地图小区显示</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no"/>
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
</style>
<script charset="utf-8" src="http://map.qq.com/api/js?v=2.exp&libraries=drawing,geometry&key=G2TBZ-VWXR5-XKRIU-QOTEH-LWV4Z-R3FSW"></script>
<script src="cell.js"></script>
</head>
<body>
<div id="toolbar1">【查找基站名称】
	<input type='text' id='cellName' style='width:150px;' value=''/>
	<input type='button' class='wyq4' onClick="searchName()" value='Search'/>
	【查找基站ID】
	<input type='text' id='cellId' style='width:130px;' value=''/>
	<input type='button' class='wyq4' onClick="searchID()" value='Search'/>
	【搜索地址】
	<input type='text' id='address' style='width:350px;' value=''/>
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
	【测距】
	<input type='button' class='wyq4' onClick="DistanceOpen()" style="font-size:18px" value='On'/>
	<input type='button' class='wyq4' onClick="DistanceOff()" style="font-size:18px" value='Off'/>
	【显示小区名】
	<input type='button' class='wyq4' onClick="LabelOpen()" value='Open'/>
	<input type='button' class='wyq4' onClick="LabelClose()" value='Close'/>
</div>
<div id="map"></div>
<script type="text/javascript">
	// 加载地图
	var map = new qq.maps.Map(document.getElementById("map"), {
            center: new qq.maps.LatLng(23.13513,113.35747),      // 地图的中心地理坐标。
            zoom:10                                                 // 地图的中心地理坐标。
    });
	var infoWin = new qq.maps.InfoWindow({
        map: map
    });
	// 载入小区
	var labelArry = [] // 保存所有基站名label
	for (var i=0; i<cell.length; i++)
	{
		(function(n){
			var position = new qq.maps.LatLng(cell[n].qq_lat,cell[n].qq_lon); // 基站所在坐标
            var path = []; // polygon 路径
            for (var j=0; j<cell[n].Polygon.length; j=j+2)
            {
				path.push(new qq.maps.LatLng(cell[n].Polygon[j+1], cell[n].Polygon[j]));
            }
			if (path.length == 1)
			{
				var polygon=new qq.maps.Circle({
					map:map,
					center:position,
					radius:60,
					//fillColor:"#00f",
					strokeWeight:2
				});
			}
			else
			{
				var polygon = new qq.maps.Polygon({
					path:path,
					strokeWeight: 2,
					map: map
				});
			}
			var label = new qq.maps.Label ({
				position : position,    // 指定文本标注所在的地理位置
				map: map,
				content: cell[n].SiteName,
				visible: false // 默认标签不可见
			});
			labelArry.push(label);
            qq.maps.event.addListener(polygon, 'click', function() {
                infoWin.open();
                infoWin.setContent("小区名称:"+cell[n].CellName+"<br/>小区ID:"+cell[n].CellId+"<br/>经纬度:"+cell[n].lon +","+cell[n].lat);
                infoWin.setPosition(position);
            });
        })(i);
	}
	// 查找功能
	var markersArray = []; // 查找结果
	// 查找小区名称
	function searchName()
	{
		var result = false;
		var keyword = document.getElementById("cellName").value;
		for (var i = 0; i < cell.length; i++){
			if (keyword == (cell[i].CellName))
			{
				result = true;
				if (markersArray.length != 0)
				{
					for (j in markersArray)
					{
						markersArray[j].setMap(null);
					}
					markersArray.length = 0;
				};
				/*
				var anchor = new qq.maps.Point(6, 6),
					size = new qq.maps.Size(24, 24),
					origin = new qq.maps.Point(0, 0),
					icon = new qq.maps.MarkerImage('http://lbs.qq.com/doc/img/center.gif', size, origin, anchor);
				*/
				var marker = new qq.maps.Marker({
					//icon: icon,
					position: new qq.maps.LatLng(cell[i].qq_lat,cell[i].qq_lon),
					map: map
				});
				//marker.setIcon(icon);
				infoWin.open();
                infoWin.setContent("小区名称:"+cell[i].CellName+"<br/>小区ID:"+cell[i].CellId+"<br/>经纬度:"+cell[i].lon +","+cell[i].lat);
                infoWin.setPosition(new qq.maps.LatLng(cell[i].qq_lat,cell[i].qq_lon));

				markersArray.push(marker);
				map.panTo(new qq.maps.LatLng(cell[i].qq_lat,cell[i].qq_lon));
				map.zoomTo(18);
			}
		}
		if (result == false)
		{
			alert("找不到结果");
		}
	}
	// 查找基站ID
	function searchID()
	{
		var result = false;
		var keyword = document.getElementById("cellId").value;
		for (var i = 0; i < cell.length; i++){
			if (keyword == (cell[i].CellId))
			{
				result = true;
				if (markersArray.length != 0)
				{
					for (j in markersArray)
					{
						markersArray[j].setMap(null);
					}
					markersArray.length = 0;
				};
				//var anchor = new qq.maps.Point(6, 6),
				//	size = new qq.maps.Size(24, 24),
				//	origin = new qq.maps.Point(0, 0),
				//	icon = new qq.maps.MarkerImage('http://lbs.qq.com/doc/img/center.gif', size, origin, anchor);
				var marker = new qq.maps.Marker({
					//icon: icon,
					position: new qq.maps.LatLng(cell[i].qq_lat,cell[i].qq_lon),
					map: map
				});
				//marker.setIcon(icon);
				infoWin.open();
                infoWin.setContent("小区名称:"+cell[i].CellName+"<br/>小区ID:"+cell[i].CellId+"<br/>经纬度:"+cell[i].lon +","+cell[i].lat);
                infoWin.setPosition(new qq.maps.LatLng(cell[i].qq_lat,cell[i].qq_lon));

				markersArray.push(marker);
				map.panTo(new qq.maps.LatLng(cell[i].qq_lat,cell[i].qq_lon));
				map.zoomTo(18);

			}
		}
		if (result == false)
		{
			alert("找不到结果");
		}
	}
	//  搜索地址
	//调用地址解析类
    var geocoder = new qq.maps.Geocoder({
        complete : function(result){
			if (markersArray.length != 0)
			{
				for (j in markersArray)
				{
					markersArray[j].setMap(null);
				}
				markersArray.length = 0;
			};
            map.setCenter(result.detail.location);
            var marker = new qq.maps.Marker({
                map:map,
                position: result.detail.location
            });
			markersArray.push(marker);
			map.zoomTo(18);
        }
    });
	function searchLocal()
	{
		var address = document.getElementById("address").value;
		//通过getLocation();方法获取位置信息值
		geocoder.getLocation(address);
	}

	// 拉框放大功能
	var startPoint={left:0,top:0},//选框的起点
      endPoint={left:0,top:0},//选框的终点
      cor,//遮罩层
      flag=true,//是否允许创建遮罩层
      area,//选区
      fla=true,//是否允许创建选区
      ele;//地图容器
	// 开启拉框放大
	function RectangleZoomOpen()
	{
		// 创建一个遮罩层
		ele=document.getElementById("map");
		//设置元素的宽高
		var wid=ele.offsetWidth,hei=ele.offsetHeight;
		//创建遮罩层元素
		cor=document.createElement("div");
		//创建元素的宽与高 并且设置样式
		cor.style.cssText="width:"+wid+"px;height:"+hei+
		"px;background:#999;opacity:0.3;filter:alpha"+
		"(opacity=30);position:absolute;top:0px;z-index:9998;";
		//添加遮罩层到元素
		ele.appendChild(cor);
		//绑定鼠标事件  鼠标单击按下触发函数
		cor.onmousedown=setStartPoint;
	}
	//设置起点的位置，并创建一个空的div
	function setStartPoint(e)
	{
		//解决怪异模式
		var e=e||window.event;
		//获取鼠标起始点左侧边距
		startPoint.left=e.clientX-ele.offsetLeft;
		//获取鼠标起始点顶部边距
		startPoint.top=e.clientY-ele.offsetTop;
		if(fla==true){
			fla=false;
			area=document.createElement("div");         //创建div遮罩层
			ele.appendChild(area);
		}else{
			fla=true;
			area.parentNode.removeChild(area);
		}
		cor.onmousemove=createArea;
		cor.onmouseup=resetMap;
	}
	//创建选区
	function createArea(e)
	{
		var e=e||window.event;
		endPoint.left=e.clientX-ele.offsetLeft;
		endPoint.top=e.clientY-ele.offsetTop;
		var wid=endPoint.left-startPoint.left,hei=endPoint.top-startPoint.top;
		area.style.cssText="width:"+wid+"px;height:"+hei+
			"px;position:absolute;left:"+startPoint.left+
			"px;top:"+startPoint.top+
			"px;border:2px solid #0f0;";
		return false;
	}
	//重置地区的中心点和放大级别
	function resetMap()
	{
		var SW={left:startPoint.left,top:endPoint.top},
			NE={left:endPoint.left,top:startPoint.top};
		var SWP=new qq.maps.Point(SW.left,SW.top),
			NEP=new qq.maps.Point(NE.left,NE.top);
		map.fitBounds(new qq.maps.LatLngBounds(
			map.get('mapCanvasProjection').fromContainerPixelToLatLng(SWP),
			map.get('mapCanvasProjection').fromContainerPixelToLatLng(NEP)
		));
		//cor.parentNode.removeChild(cor);
		area.parentNode.removeChild(area);
		//flag=true;
		fla=true;
	}
	// 开启拉框放大
	function RectangleZoomEnd()
	{
		cor.parentNode.removeChild(cor);
		fla=false;
	}
	// 鼠标点击获取经纬度
	var getLocation = null
	// 开启
	function getLocationOn()
	{
		//如果未开启则添加监听事件
		if (getLocation == null)
		{
			getLocation = qq.maps.event.addListener(map, 'click', function(e) {
				var latLng = e.latLng,
					lat = latLng.getLat().toFixed(5),
					lng = latLng.getLng().toFixed(5);
					alert(lng + "," + lat);
			});
		};
	}
	// 关闭
	function getLocationOff(){
		if (getLocation != null)
		{
			 qq.maps.event.removeListener(getLocation);
			 getLocation = null
		};
	}
	// 添加地图绘制工具
	//实例化鼠标绘制工具
	var overlays = [];
	var drawingManager = new qq.maps.drawing.DrawingManager({
        drawingMode: qq.maps.drawing.OverlayType.MARKER,
        drawingControl: true,
        drawingControlOptions: {
            position: qq.maps.ControlPosition.TOP_RIGHT,
            drawingModes: [
                qq.maps.drawing.OverlayType.MARKER,
                qq.maps.drawing.OverlayType.CIRCLE,
                qq.maps.drawing.OverlayType.POLYGON,
                qq.maps.drawing.OverlayType.POLYLINE,
                qq.maps.drawing.OverlayType.RECTANGLE
            ]
        },
        circleOptions: {
            fillColor: new qq.maps.Color(255, 208, 70, 0.3),
            strokeColor: new qq.maps.Color(88, 88, 88, 1),
            strokeWeight: 3,
            clickable: false
        }
    });
    drawingManager.setMap(map);
	//设置overlaycomplete事件
    qq.maps.event.addListener(drawingManager, 'overlaycomplete', function(e) {
        // 把绘制的图形添加到 overlays 中
		overlays.push(e.overlay);
    });

	// 清除绘制
	function CleanDrawing()
	{
		if (overlays.length != 0)
		{
			for (i in overlays)
			{
				overlays[i].setMap(null);
			}
			overlays.length = 0;
		};
	}
	// 绘制的点可移动
	function MarkerDraggingOn()
	{
		for (var i = 0; i < overlays.length; i++){
			if ((overlays[i] instanceof qq.maps.Marker))
			{
				overlays[i].setDraggable(true);
			};
		}
	}
	// 绘制的点不可移动
	function MarkerDraggingOff()
	{
		for (var i = 0; i < overlays.length; i++){
			if ((overlays[i] instanceof qq.maps.Marker))
			{
				overlays[i].setDraggable(false);
			};
		}
	}
	// 绘制的线面可编辑
	function EditingOn()
	{
		for (var i = 0; i < overlays.length; i++){
			if ((overlays[i] instanceof qq.maps.Polyline) || (overlays[i] instanceof qq.maps.Polygon))
			{
				var Options = {editable: true}
				overlays[i].setOptions(Options);
			};
		};
	}
	// 绘制的线面不可编辑
	function EditingOff()
	{
		for (var i = 0; i < overlays.length; i++){
			if ((overlays[i] instanceof qq.maps.Polyline) || (overlays[i] instanceof qq.maps.Polygon))
			{
				var Options = {editable: false}
				overlays[i].setOptions(Options);
			};
		};
	}
	// 鼠标测距
	var distanceListener = null;
	function DistanceOpen()
	{
		var path = null; // 路径
		var start = null; //  起始点
		var end = null; // 终止点
		distanceListener = qq.maps.event.addListener(drawingManager, 'overlaycomplete', function(e) {
			// 把绘制的图形添加到 overlays 中
			if (e.overlay instanceof qq.maps.Polyline)
			{
				path = e.overlay.getPath();
				start = path.getAt(0);
				end = path.getAt(path.length-1);
				alert("起始点间的距离为： " + qq.maps.geometry.spherical.computeDistanceBetween(start, end) + "米");
			};
		});
	}
	function DistanceOff()
	{
		if (distanceListener != null)
		{
			qq.maps.event.removeListener(distanceListener);
			distanceListener = null
		};
	}
	// 小区名字标签
	function LabelOpen()
	{
		if (labelArry.length > 0)
		{
			for (var i=0; i<labelArry.length; i++)
			{
				labelArry[i].setVisible(true);
			}
		};
	}
	function LabelClose()
	{
		if (labelArry.length > 0)
		{
			for (var i=0; i<labelArry.length; i++)
			{
				labelArry[i].setVisible(false);
			}
		};
	}
</script>
</body>
</html>
"""

# 腾讯地图小区显示街景功能
Pano = u"""
<!DOCTYPE html>
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
	<title>腾讯地图小区街景工具</title>
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
	<script charset="utf-8"    src="http://map.qq.com/api/js?v=2.exp&libraries=drawing,geometry,convertor&key=G2TBZ-VWXR5-XKRIU-QOTEH-LWV4Z-R3FSW"></script>
	<script src="cell.js"></script>
</head>
<body>
	<div id="pano_holder1"></div>
	<div id="map"></div>
	<div id="panel">

		<span style="width:5px;">&nbsp;&nbsp;&nbsp;</span><span id="angle"></span><br/>
		<span style="width:5px;">&nbsp;&nbsp;&nbsp;</span><span id="distance"></span><br/>
		<span style="width:5px;">&nbsp;&nbsp;&nbsp;</span><span id="pano_lon"></span><br/>
		<span style="width:5px;">&nbsp;&nbsp;&nbsp;</span><span id="pano_lat"></span><br/>
		<span>
		<br/>
		<span style="width:5px;">&nbsp;&nbsp;&nbsp;</span>请输入基站信息：
		<br/>
		<br/>
		<span style="width:5px;">&nbsp;&nbsp;&nbsp;</span>经度:
		<input type="text" id="lon" style="width: 100px;height:25px;font-size:15px" />
		<span style="width:5px;">&nbsp;&nbsp;&nbsp;</span>纬度:
		<input type="text" id="lat" style="width: 100px;height:25px;font-size:15px" />
		<span style="width:5px;">&nbsp;&nbsp;&nbsp;</span>基站规划名：
		<input type="text" id="SiteName" name="SiteName" style="width: 125px;height:25px;font-size:15px" />
		<input type="button" class="button" value="显示街景" id="setMarker" onclick="setMarker()" style="width:75px;height:28px;font-size:16px"/>
		<br/>
		<br/>
		<span style="width:5px;">&nbsp;&nbsp;&nbsp;</span>基站搜索：
		<input type="radio" name="SearchType" id="SearchID" value="ID" checked>按基站ID
		<input type="radio" name="SearchType" id="SearchName" value="Name">按基站名称
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
	// 加载地图
	var map = new qq.maps.Map(document.getElementById("map"), {
            center: new qq.maps.LatLng(23.13513,113.35747),      // 地图的中心地理坐标。
            zoom:16                                                 // 地图的中心地理坐标。
    });
	var infoWin = new qq.maps.InfoWindow({
        map: map
    });
	//设置路网图层
	var pano_layer = new qq.maps.PanoramaLayer();
	pano_layer.setMap(map);
	// 载入小区
	var labelArry = [] // 保存所有基站名label
	for (var i=0; i<cell.length; i++)
	{
		(function(n){
			var position = new qq.maps.LatLng(cell[n].qq_lat,cell[n].qq_lon); // 基站所在坐标
            var path = []; // polygon 路径
            for (var j=0; j<cell[n].Polygon.length; j=j+2)
            {
				path.push(new qq.maps.LatLng(cell[n].Polygon[j+1], cell[n].Polygon[j]));
            }
			if (path.length == 1)
			{
				var polygon=new qq.maps.Circle({
					map:map,
					center:position,
					radius:60,
					//fillColor:"#00f",
					strokeWeight:2
				});
			}
			else
			{
				var polygon = new qq.maps.Polygon({
					path:path,
					strokeWeight: 2,
					map: map
				});
			}
			var label = new qq.maps.Label ({
				position : position,    // 指定文本标注所在的地理位置
				map: map,
				content: cell[n].SiteName,
				visible: true // 默认标签可见
			});
			labelArry.push(label);
            qq.maps.event.addListener(polygon, 'click', function() {
                infoWin.open();
                infoWin.setContent("小区名称:"+cell[n].CellName+"<br/>小区ID:"+cell[n].CellId+"<br/>经纬度:"+cell[n].lon +","+cell[n].lat);
                infoWin.setPosition(position);
            });
        })(i);
	}

	// 设置基站Marker
	var lon = null;
	var lat = null;
	var markersArray = [];
	var cell_point = null;
	function setMarker()
	{
		lon = document.getElementById("lon").value;
		lat = document.getElementById("lat").value;
		cell_name = document.getElementById("SiteName").value;
		if (lon != "" && lat != "")
		{
			lon = document.getElementById("lon").value;
			lat = document.getElementById("lat").value;
			if (markersArray.length != 0)
			{
				for (j in markersArray)
				{
					markersArray[j].setMap(null);
				}
				markersArray.length = 0;
			};
			var point = new qq.maps.LatLng(lat,lon);
			qq.maps.convertor.translate(point, 1, function(res) {
				latlng = res[0];
				var marker = new qq.maps.Marker({
					map: map,
					position: latlng
				});
				markersArray.push(marker);
				map.panTo(latlng);
				map.zoomTo(18);
				// 添加信息窗口
				if (cell_name != "")
				{
					qq.maps.event.addListener(marker, 'click', function() {
						infoWin.open();
						infoWin.setContent(cell_name);
						infoWin.setPosition(latlng);
					});
				};
				// 创建街景
				var pano = new qq.maps.Panorama(document.getElementById('pano_holder'));
				pano.setPov({
					heading: -40,
					pitch: 6
				});
				//创建街景类
				pano_service = new qq.maps.PanoramaService();
				var radius;
				pano_service.getPano(point, radius, function (result){
					pano.setPano(result.svid);
				});
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
					if (markersArray.length != 0)
					{
						for (j in markersArray)
						{
							markersArray[j].setMap(null);
						}
						markersArray.length = 0;
					};
					var point = new qq.maps.LatLng(cell[i].qq_lat, cell[i].qq_lon);
					var marker = new qq.maps.Marker({
						position: point,
						map: map
					});
					markersArray.push(marker);
					map.panTo(point);
					map.zoomTo(18);

					cell_point = point;
					// 创建街景
					var pano = new qq.maps.Panorama(document.getElementById('pano_holder'));
					pano.setPov({
						heading: -40,
						pitch: 6
					});
					//创建街景类
					pano_service = new qq.maps.PanoramaService();
					var radius;
					pano_service.getPano(point, radius, function (result){
						pano.setPano(result.svid);
					});
				};
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
					if (markersArray.length != 0)
					{
						for (j in markersArray)
						{
							markersArray[j].setMap(null);
						}
						markersArray.length = 0;
					};
					var point = new qq.maps.LatLng(cell[i].qq_lat, cell[i].qq_lon);
					var marker = new qq.maps.Marker({
						position: point,
						map: map
					});
					markersArray.push(marker);
					map.panTo(point);
					map.zoomTo(18);

					cell_point = point;
					// 创建街景
					var pano = new qq.maps.Panorama(document.getElementById('pano_holder'));
					pano.setPov({
						heading: -40,
						pitch: 6
					});
					//创建街景类
					pano_service = new qq.maps.PanoramaService();
					var radius;
					pano_service.getPano(point, radius, function (result){
						pano.setPano(result.svid);
					});

				}
			}
			if (result == false)
			{
				alert("找不到结果");
			}
		}

	}
	// 监听地图添加要显示的街景
	var markersArray1 = []; // 街景Marker列表(包含polyline连线)
	var pano_point = null; // 街景Point
	//var polylineArray = []; // 保存polyline连线的数组
	var panorama1 = null; // 定义街景图层
	qq.maps.event.addListener(map,"click",function(e){
		if ((markersArray.length != 0) && (cell_point != null))
		{
			if (markersArray1.length != 0)
			{
				for (j in markersArray1)
				{
					markersArray1[j].setMap(null); // 移除原有标注
				}
				markersArray1.length = 0;
			};
			var position = e.latLng;
			var marker = new qq.maps.Marker({
				position: position,
				map: map
			});
			markersArray1.push(marker);
			//map.zoomTo(18);
			// 创建街景
			var pano1 = new qq.maps.Panorama(document.getElementById('pano_holder1'));
			pano1.setPov({
				heading: -40,
				pitch: 6
			});
			//创建街景类
			pano_service1 = new qq.maps.PanoramaService();
			var radius;
			pano_service1.getPano(position, radius, function (result){
				pano1.setPano(result.svid);
			});

			pano_point = position;

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
			document.getElementById("distance").innerHTML ="街景位置与基站距离"+qq.maps.geometry.spherical.computeDistanceBetween(cell_point,pano_point).toFixed(2)+"米";
			//添加连线
			var line_path = [cell_point, pano_point];
			var polyline = new qq.maps.Polyline({
				path: line_path,
				editable:false,
				map: map
			});
			markersArray1.push(polyline);
			// 显示街景经纬度
			document.getElementById("pano_lon").innerHTML ="街景位置经度：" + pano_point.lng;
			document.getElementById("pano_lat").innerHTML ="街景位置纬度：" + pano_point.lat;
		};
	});

</script>
"""