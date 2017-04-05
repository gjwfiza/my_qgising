# -*- coding:utf-8 -*-
'''
@author: Karwai Kwok
'''

# Sogo地图基站显示主页面
Head = u"""
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>搜狗地图基站显示</title>
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
<script charset="utf-8" src="http://api.go2map.com/maps/js/api_v2.5.1.js"></script>
<script src="site.js"></script>
</head>
<body>
<div id="toolbar1">【查找基站名称】
	<input type='text' id='siteName' style='width:150px;' value=''/>
	<input type='button' class='wyq4' onClick="searchName()" value='Search'/>
	【查找基站ID】
	<input type='text' id='siteId' style='width:130px;' value=''/>
	<input type='button' class='wyq4' onClick="searchID()" value='Search'/>
	【搜索地址】
	<input type='text' id='address' style='width:350px;' value=''/>
	<input type='button' class='wyq4' onClick="searchLocal()" value='Search'/>
</div>
<div id="toolbar2">
	【测距】
	<input type='button' class='wyq4' onClick="DistanceOpen()" style="font-size:18px" value='On'/>
	<input type='button' class='wyq4' onClick="DistanceOff()" style="font-size:18px" value='Off'/>
</div>
<div id="map"></div>
<script src="site.js"></script>
<script type="text/javascript">
	// 加载地图
    var map = new sogou.maps.Map(document.getElementById("map"),{});
	map.setCenter(new sogou.maps.Point(12614437,2631281),10); // 设置地图中心为广州

	var markers_Array  = []; // 存放marker的数组
	var label_Array = [];
	for (var i=0; i<site.length; i++)
	{
		var lon = site[i].lon;
		var lat = site[i].lat;
		var point = new sogou.maps.LatLng(lat,lon);
		var markerOptions={
			id: i,
			map: map,
			position: point,
			disableLabel:false,
			//label:{visible:true,align:"BOTTOM"},
			title: site[i].SiteName,
			//visible:true
		}
		var marker = new sogou.maps.Marker(markerOptions);
		markers_Array.push(marker);
		addInfoWin(marker, i);
	};
	// 添加信息窗口listener
	function addInfoWin(marker, index){
		var infowindow = new sogou.maps.InfoWindow(
		{
			content: "基站名称:"+site[index].SiteName+"<br/>基站ID:"+site[index].SiteId+"<br/>经纬度:"+site[index].lon +","+site[index].lat
		});
		sogou.maps.event.addListener(marker, 'click', function() {
			infowindow.open(map,marker);
		});
	};
	// 查找功能
	var resultArray = []; // 查找结果
	// 查找基站名称
	function searchName()
	{
		var result = false;
		var keyword = document.getElementById("siteName").value;
		for (var i = 0; i < site.length; i++){
			if (keyword == (site[i].SiteName))
			{
				result = true;
				if (resultArray.length != 0)
				{
					for (j in resultArray)
					{
						resultArray[j].setMap(null);
					}
					resultArray.length = 0;
				};
				var lat = site[i].lat;
				var lon = site[i].lon;
				var point = new sogou.maps.LatLng(lat, lon);
				var marker = markers_Array[i];
				var infowindow = new sogou.maps.InfoWindow(
				{
					content: "基站名称:"+site[i].SiteName+"<br/>基站ID:"+site[i].SiteId+"<br/>经纬度:"+site[i].lon +","+site[i].lat
				});
				infowindow.open(map,marker);
				resultArray.push(marker);
				map.setCenter(point, 18);
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
		var keyword = document.getElementById("siteId").value;
		for (var i = 0; i < site.length; i++){
			if (keyword == (site[i].SiteId))
			{
				result = true;
				if (resultArray.length != 0)
				{
					for (j in resultArray)
					{
						resultArray[j].setMap(null);
					}
					resultArray.length = 0;
				};
				var lat = site[i].lat;
				var lon = site[i].lon;
				var point = new sogou.maps.LatLng(lat, lon);
				var marker = markers_Array[i];
				var infowindow = new sogou.maps.InfoWindow(
				{
					content: "基站名称:"+site[i].SiteName+"<br/>基站ID:"+site[i].SiteId+"<br/>经纬度:"+site[i].lon +","+site[i].lat
				});
				infowindow.open(map,marker);
				resultArray.push(marker);
				map.setCenter(point, 18);
			}
		}
		if (result == false)
		{
			alert("找不到结果");
		}
	}
	// 地址搜索
	function searchLocal(){
		var keyword = document.getElementById("address").value;
		var request={
			  address:{
				   addr:keyword,
				   city:"全国"
				}
		}
		var geo = new sogou.maps.Geocoder();
		geo.geocode(request,function(a)
		{
			if (a.status == "ok")
			{
				var geometry=a.data[0];
				var local = geometry.location
				var marker = new sogou.maps.Marker({
					map:map,
					title: geometry.address,
					position: local,
					label:{visible:true}
				});
				map.setCenter(local, 18);
				resultArray.push(marker);
			}
			else
			{
				alert("您选择地址没有解析到结果!");
			};
		});
	};
	// 测距功能
	var distance_flag = false; // 测距功能开启标志
	var distance_start, mousemove_Listener, distance_end;
	function DistanceOpen()
	{
		//定义标记样式
		var markerStyle=new sogou.maps.MarkerImage('http://api.go2map.com/maps/images/v2.0/c31.png',
			  // 蓝点图标宽16像素，高14像素
			  new sogou.maps.Size(16, 14),
			  // 原点在图片的(34,88)
			  new sogou.maps.Point(34,88),
			  // 锚点在图标中心
			  new sogou.maps.Point(8,7),
			  // 合并图片的大小
			  new sogou.maps.Size(51, 156));
		//定义带箭头的样式
		var lineStyle =  {
			id:"L02",
			"v:stroke":{color: "#0cf",
				weight:"5",
				endcap:"Round",
				opacity:"75%",
				endArrow:"Classic",
				endarrowlength:"long",
				endarrowwidth:"wide"}
		};      
		var line = new sogou.maps.Polyline({
		    map:map,
		    style:lineStyle,
		    zIndex:2
		});
		var path=[], marker;
		if (distance_flag == false)
		{
			distance_start = sogou.maps.event.addListener(map,"click",function(evt)
			{
				//evt.point 搜狗地图坐标
				path.push(evt.point);
				//添加节点蓝点，计算路径距离
				marker=new sogou.maps.Marker({
					map:map,
					position:evt.point,
					icon:markerStyle,
					title:calcDistance(path)+"米",
					label:{visible:true}
				});

				if(path.length>0)
				{
					line = new sogou.maps.Polyline({
						map:map,
						styles:[lineStyle],
						zIndex:2
					});
					path=[];
					path.push(evt.point);
				}
			});
			mousemove_Listener = sogou.maps.event.addListener(map,"mousemove",function(evt)
			{
				//evt.point 搜狗地图坐标
				path.length>0 && line.setPath(path.concat([evt.point]));

			});
			//点击右键结束
			distance_end = sogou.maps.event.addListener(map,"rightclick",function(evt)
			{
				//evt.point 搜狗地图坐标
				line.remove();
				path=[];
			});
			distance_flag = true;
		}
		//计算距离
		var convertor = new sogou.maps.Convertor();
		function calcDistance(a)
		{
			var b=0,i;
			for(i=0;i<a.length;i++)
			{
				if(a[i+1]) b+=convertor.distance(a[i],a[i+1]);
			}
			return parseInt(b)
		}
	}
	function DistanceOff()
	{
		if (distance_flag == true)
		{
			sogou.maps.event.removeListener(distance_start);
			sogou.maps.event.removeListener(mousemove_Listener);
			sogou.maps.event.removeListener(distance_end);
			distance_flag = false
		}
	}

</script>
</body>
</html>

"""
