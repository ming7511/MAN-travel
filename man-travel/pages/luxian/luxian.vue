<template>
  <view class="container">
    <!-- 导航栏：切换天数和总览 -->
    <view class="tab-bar">
      <button :class="{ active: currentDay === -1 }" @click="showOverview">总览</button>
      <button :class="{ active: currentDay === 0 }" @click="changeDay(0)">DAY1</button>
      <button :class="{ active: currentDay === 1 }" @click="changeDay(1)">DAY2</button>
      <button :class="{ active: currentDay === 2 }" @click="changeDay(2)">DAY3</button>
    </view>

    <!-- 地图容器 -->
    <map id="map" :latitude="center.lat" :longitude="center.lng" style="width: 100%; height: 100%;"></map>
  </view>
</template>
<script>
export default {
  data() {
    return {
      currentDay: 0, // 当前选中的天数
      center: { lat: 26.0751, lng: 119.2956 }, // 地图初始中心坐标，根据需要调整
      daysData: {
        DAY1: [
          { lat: 26.082128, lng: 119.29642, day: 1, name: "三坊七巷" },
          { lat: 26.074385, lng: 119.295521, day: 1, name: "乌山" },
          { lat: 26.092037, lng: 119.289152, day: 1, name: "西湖公园" },
        ],
        DAY2: [
          { lat: 26.044964, lng: 119.315527, day: 2, name: "烟台山公园" },
          { lat: 26.052435, lng: 119.304399, day: 2, name: "上下杭历史文化街" },
        ],
        DAY3: [
          { lat: 26.076251, lng: 119.303745, day: 3, name: "南门兜" },
        ]
      },
      map: null
    };
  },
  methods: {
    loadMap() {
      // 动态加载高德地图API
      const script = document.createElement('script');
      script.src = `https://webapi.amap.com/maps?v=1.4.15&key=51c85c7d66041b827819349a61afdb49`;   
      document.body.appendChild(script);
      script.onload = () => {
        this.initMap();
      };
    },
    initMap() {
      // 初始化地图
      this.map = new AMap.Map('map', {
        center: [this.center.lng, this.center.lat],
        zoom: 14
      });
      this.renderMap();
    },
 renderMap() {
   // 清除旧的标记和路线
   this.map.clearMap();
 
   // 根据当前选中的天数或总览来决定显示哪些标记点和路线
   let dayData = [];
   if (this.currentDay === -1) {
     // 总览模式，显示所有标记点
     dayData = this.getAllPoints();
   } else {
     dayData = this.daysData['DAY' + (this.currentDay + 1)];
   }
 
   // 绘制标记点
   dayData.forEach(point => {
     const marker = new AMap.Marker({
       position: [point.lng, point.lat],
       title: `${point.name} - 第${point.day}天的游玩`,
       label: {
         content: `<div style="background-color: white; border: 1px solid #ccc; padding: 2px 5px; border-radius: 4px; font-weight: bold;">第${point.day}天 ${point.name}</div>`,
         offset: new AMap.Pixel(0, -5), // 调整偏移，可能需要根据实际情况微调
         direction: 'top' // 显示在标记的上方
       }
     });
     marker.setMap(this.map);
 
     // 为每个标记点设置信息窗口
     const infoWindow = new AMap.InfoWindow({
       content: `
         <div style="text-align: center; font-size: 16px; font-weight: bold; color: #333;">
           ${point.name}<br/>
           <span style="color: #666;">第${point.day}天的游玩</span>
         </div>`,
       offset: new AMap.Pixel(0, -30)
     });
 
     // 点击标记时打开信息窗口
     marker.on('click', () => {
       infoWindow.open(this.map, marker.getPosition());
     });
   });
 
   // 绘制路线
   if (this.currentDay !== -1 && dayData.length > 1) {
     this.getDrivingRoute(dayData);
   }
 
   // 计算平均坐标并更新地图中心
   if (dayData.length > 0) {
     const avgLat = dayData.reduce((acc, cur) => acc + cur.lat, 0) / dayData.length;
     const avgLng = dayData.reduce((acc, cur) => acc + cur.lng, 0) / dayData.length;
     this.center = { lat: avgLat, lng: avgLng };
     this.map.setCenter([this.center.lng, this.center.lat]);
   }
 },
getDrivingRoute(dayData) {
  // 如果只有一个点或没有点，则不绘制路线
  if (dayData.length < 2) return;

  // 初始化起点
  let origin = [dayData[0].lng, dayData[0].lat];
  let destinations = dayData.slice(1).map(point => [point.lng, point.lat]);

  // 连续调用驾车路线规划API
  this.drawRoute(origin, destinations);
},

drawRoute(origin, destinations) {
  if (destinations.length === 0) return; // 如果没有目的地，结束绘制

  let destination = destinations.shift(); // 获取下一个目的地
  let url = `https://restapi.amap.com/v3/direction/driving?origin=${origin.join(',')}&destination=${destination.join(',')}&key=e44f0883153e1002c6a9e6a99c86bf58`; 

  fetch(url)
    .then(response => response.json())
    .then(data => {
      if (data.status === "1" && data.info === "OK" && data.route) {
        // 获取路线规划结果
        const route = data.route.paths[0];
        const polylinePath = route.steps.map(step => {
          return step.polyline.split(';').map(coord => {
            const [lng, lat] = coord.split(',');
            return [parseFloat(lng), parseFloat(lat)];
          });
        }).flat();

        // 绘制路线
        new AMap.Polyline({
          path: polylinePath,
          strokeColor: "#FF3FF", // 路线颜色
          strokeWeight: 5, // 路线宽度
          strokeOpacity: 0.5, // 路线透明度
          map: this.map // 添加到地图
        });

        // 更新起点为当前目的地，继续绘制下一段路线
        this.drawRoute(destination, destinations);
      }
    })
    .catch(error => console.error('Error fetching driving route:', error));
},

    changeDay(day) {
      this.currentDay = day;
      this.renderMap();
    },
    showOverview() {
       this.currentDay = -1; // 设置为-1表示显示总览
       this.calculateAverageCenter(); // 计算所有标记点的平均坐标
       this.map.setCenter([this.center.lng, this.center.lat]); // 更新地图中心
       if (this.currentDay === -1) {
         this.map.setZoom(13.1); // 只在总览模式下设置更高的缩放级别
       } else {
         this.map.setZoom(14); // 其他天数保持原来的缩放级别
       }
       this.renderMap(); // 重新渲染地图
     },
     calculateAverageCenter() {
       // 获取所有标记点
       const allPoints = this.getAllPoints();
       if (allPoints.length > 0) {
         const totalLat = allPoints.reduce((acc, cur) => acc + cur.lat, 0);
         const totalLng = allPoints.reduce((acc, cur) => acc + cur.lng, 0);
         const avgLat = totalLat / allPoints.length;
         const avgLng = totalLng / allPoints.length;
         this.center = { lat: avgLat, lng: avgLng };
       }
     },
    getAllPoints() {
      // 将所有天数的标记点合并到一个数组中
      return this.daysData.DAY1.concat(this.daysData.DAY2, this.daysData.DAY3);
    }
  },
  mounted() {
    this.loadMap();
  }
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  margin: 0;
  padding: 0;
  overflow: hidden;
}

.tab-bar {
  display: flex;
  justify-content: center; /* 居中对齐 */
  align-items: center; /* 垂直居中 */
  padding: 10px;
  background-color: #e6f2ff; /* 天蓝色背景 */
  box-sizing: border-box;
  z-index: 1;
  border-bottom: 1px solid #ccc; /* 添加底部边框 */
}

.tab-bar button {
  margin: 0 10px; /* 按钮之间的间距 */
  padding: 5px 10px; /* 按钮内边距 */
  background-color: #fff; /* 白色背景 */
  border: 1px solid #ccc; /* 边框 */
  border-radius: 20px; /* 圆角 */
  color: #333; /* 字体颜色 */
  font-size: 16px; /* 字体大小 */
  cursor: pointer; /* 鼠标悬停时显示指针 */
}

.tab-bar button.active {
  background-color: #add8e6; /* 天蓝色背景 */
  color: #000; /* 黑色字体 */
}

#map {
  flex: 1;
  width: 100%;
  height: calc(100vh - 70px); /* 假设导航栏高度为70px */
}
</style>