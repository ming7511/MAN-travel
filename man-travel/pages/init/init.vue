<template>
  <view class="travel-plan-overview-page">
    <!-- 返回按钮容器 -->
    <view class="back-button-container">
      <image src="/static/icons/back-icon.png" class="back-button" @click="goBack" />
    </view>

    <!-- 行程名 -->
    <view class="header">
      <text class="trip-name">{{ tripTitle || '未命名行程' }}</text>
    </view>

    <!-- 旅行时间 -->
    <view class="travel-time">{{ travelDateRange || '日期待定' }} {{ tripDuration }}</view>

    <!-- 行程标题及横线 -->
    <view class="trip-section">
      <view class="button-group">
        <!-- 行程按钮 -->
        <button class="btn-title" @click="handleShowOverview">行程</button>
        <!-- 旅行账单按钮 -->
        <button class="btn-title" @click="handleShouyeClick">旅行账单</button>
        <!-- 行李清单按钮 -->
        <button class="btn-title" @click="handleXingliClick">行李清单</button>
      </view>
      <view class="horizontal-line"></view>
    </view>

    <!-- 白色矩形区域 -->
    <view class="white-rectangle">
      <!-- 行程天数按钮 -->
      <view class="day-buttons">
        <button v-for="(day, index) in days" :key="index" :class="['day-button', { active: currentDay === day }]"
          @click="handleDayClick(day)">{{ day }}</button>
      </view>
      <!-- 行程概览标题 -->
      <view class="overview-title">行程概览</view>
      <!-- 地图区域，使用 div 作为地图容器，添加 map-container 类名 -->
      <div id="map-container" class="map-container" v-if="hasPlaces"></div>
      <view v-else class="no-map-info">暂无地点信息</view>
      <!-- 每天行程信息 -->
      <view class="daily-trips">
        <view v-for="(dayTrip, index) in filteredDailyTrips" :key="index" class="daily-trip">
          <view class="day-label">{{ dayTrip.day }}</view>
          <view class="city-label">{{ dayTrip.city || '城市待定' }}</view>
          <view class="places-label">{{ dayTrip.places.length > 0 ? dayTrip.places.join(', ') : '地点待定' }}</view>
        </view>
        <!-- 待规划行程 -->
        <view v-if="filteredDailyTrips.length === 0" class="to-plan-trip">待规划</view>
      </view>
    </view>

    <!-- 天气预报标题 -->
    <view class="weather-title">天气预报</view>
    <!-- 天气预报区域 -->
    <view class="weather-info" v-if="weatherForecast && weatherForecast.length > 0">
      <view v-for="(weather, index) in weatherForecast" :key="index" class="weather-item">
        <view>{{ weather.city }}</view>
        <view>{{ weather.date }} {{ weather.weekday }} {{ weather.icon }} {{ weather.condition }}
          {{ weather.temperature }}</view>
      </view>
    </view>
    <!-- 如果没有天气信息，显示为空 -->
    <view v-else>
      <view>暂无天气信息</view>
    </view>
  </view>
</template>

<script>
import AMapLoader from '@amap/amap-jsapi-loader';
import { useRoute } from 'vue-router';
import { ref, onMounted, computed } from 'vue';

export default {
  setup() {
    const route = useRoute();
    const currentDay = ref('总览'); // 当前选择的行程天数
    const weatherForecast = ref([]); // 天气预报
    const tripTitle = ref(''); // 行程标题
    const travelDateRange = ref(''); // 旅行日期范围
    const tripDuration = ref(''); // 旅行时长
    const places = ref([]); // 旅行地点
    const map = ref(null); // 地图实例
    const days = ref(['总览']); // 存储行程天数（如：总览，DAY1, DAY2）
    const dailyTrips = ref([]); // 每日行程
    const hasPlaces = ref(false); // 标记是否有地点信息
	
	    // 格式化旅行日期
	        const formattedTravelDateRange = computed(() => {
	          if (!travelDateRange.value) return '日期待定';
	          const startDate = new Date(travelDateRange.value.split('至')[0].trim());
	          const endDate = new Date(travelDateRange.value.split('至')[1].trim());
	          const formatDate = (date) => {
	            return `${date.getMonth() + 1}.${date.getDate() < 10 ? '0' + date.getDate() : date.getDate()}`;
	          };
	          return `${formatDate(startDate)}至${formatDate(endDate)}`;
	        });
	    
	        // 解析从创建页面传来的数据
	        onMounted(() => {
	          console.log('Received trip data from previous page:', route.query);
	    
	          const tripData = {
	            tripId: route.query.tripId || '',
	            location: route.query.location ? decodeURIComponent(route.query.location) : '未命名行程',
	            startDate: route.query.startDate ? new Date(route.query.startDate) : null,
	            endDate: route.query.endDate ? new Date(route.query.endDate) : null,
	            duration: route.query.duration ? `${parseInt(route.query.duration, 10)}天${parseInt(route.query.duration, 10) > 1 ? parseInt(route.query.duration, 10) - 1 : 0}晚` : '0天0晚',
	            places: route.query.places ? JSON.parse(decodeURIComponent(route.query.places)) : [],
	            dailyTrips: route.query.dailyTrips ? JSON.parse(decodeURIComponent(route.query.dailyTrips)) : [],
	            weather: route.query.weather ? JSON.parse(decodeURIComponent(route.query.weather)) : []
	          };
	    
	          if (tripData) {
	            tripTitle.value = tripData.location;
	            travelDateRange.value = tripData.startDate && tripData.endDate
	              ? `${tripData.startDate.getMonth() + 1}.${tripData.startDate.getDate() < 10 ? '0' + tripData.startDate.getDate() : tripData.startDate.getDate()} 至 ${tripData.endDate.getMonth() + 1}.${tripData.endDate.getDate() < 10 ? '0' + tripData.endDate.getDate() : tripData.endDate.getDate()}`
	              : '日期待定';
	            tripDuration.value = tripData.duration;
	    
	            places.value = tripData.places || [];
	            hasPlaces.value = places.value.length > 0;
	            weatherForecast.value = tripData.weather || [];

	
	        // 打印行程信息
	        console.log('接收到的行程数据:', tripData);
	
	        // 根据 duration 动态生成天数按钮
	        const dayCount = tripData.duration || 0;
	        days.value = ['总览', ...Array.from({ length: dayCount }, (_, i) => `DAY${i + 1}`)];
	
	        // 填充每日行程数据（假设传入的 dailyTrips 数据）
	        dailyTrips.value = tripData.dailyTrips || [];
	
	        // 初始化地图，如果有地点
	        if (hasPlaces.value) {
	          initMap(tripData.places.map(place => place.coordinates));
	        }
	      }
	    });


    // 初始化地图的函数
    const initMap = (coordinates) => {
      if (!coordinates || coordinates.length === 0) {
        console.log('No coordinates available for map initialization.');
        return;
      }
      // 假设你已经有了地图的初始化逻辑
      map.value = new AMap.Map('map-container', {
        zoom: 10,
        center: coordinates[0], // 初始化中心点为第一个地点
      });

      // 在地图上标记地点
      coordinates.forEach((coordinate) => {
        new AMap.Marker({
          position: coordinate, // 每个地点的坐标
          map: map.value,
        });
      });
    };

    // 返回按钮方法
    const goBack = () => {
      uni.navigateTo({
        url: '/pages/index/index'
      });
    };

    // 处理行程天数按钮点击
    const handleDayClick = (day) => {
      currentDay.value = day;
    };

    // 跳转到其他功能页面的按钮点击方法
    const handleShouyeClick = () => {
      // 此处添加跳转逻辑
    };

    const handleXingliClick = () => {
      // 此处添加跳转逻辑
    };

    const filteredDailyTrips = computed(() => {
      if (currentDay.value === '总览') {
        return dailyTrips.value;
      } else {
        return dailyTrips.value.filter(trip => trip.day === currentDay.value);
      }
    });

    return {
      currentDay,
      weatherForecast,
      tripTitle,
      travelDateRange,
      tripDuration,
      places,
      days,
      dailyTrips,
      hasPlaces,
      filteredDailyTrips,
      goBack,
      handleDayClick,
      handleShouyeClick,
      handleXingliClick
    };
  }
};
</script>


<style lang="scss">
.travel-plan-overview-page {
  background-color: #e1f0ff;
  padding: 20px;


/* 返回按钮容器样式 */
.back-button-container {
  margin-bottom: 10px; /* 设置与下方内容的间距 */
}

/* 返回按钮图标样式 */
.back-button {
  width: 30px;
  height: 30px;
  cursor: pointer;
}

/* 行程名样式 */
.header {
  margin-top: 10px; /* 设置与返回按钮的间距 */
  margin-bottom: 10px; /* 设置与下方内容的间距 */
}

  // 行程名样式
.trip-name {
    font-size: 24px;
    font-weight: bold;
    text-align: left;
    margin-bottom: 10px;
  }

  // 旅行时间样式
.travel-time {
    font-size: 16px;
    color: dimgray;
    text-align: left;
    margin-bottom: 10px;
  }

.trip-section {
  display: flex; 
  flex-direction: column; /* 使其内部子项垂直排列 */
  align-items: flex-start; /* 确保内容从左侧对齐 */
  text-align: left; /* 保证文本左对齐 */
  border: none; /* 移除任何边框 */
  padding: 0; /* 确保没有多余的内边距 */


 .button-group {
   display: flex; /* 使用 flex 布局让按钮并排 */
   align-items: center; /* 垂直居中对齐按钮文本 */
   justify-content: flex-start; /* 水平方向左对齐 */
   gap: 40rpx; /* 使用 rpx 确保按钮之间有合适的间距（适合小程序环境） */
   margin-left: 15rpx; /* 确保按钮组容器没有左侧内边距或外边距 */
   padding-left: 0; /* 确保没有额外的左侧填充 */
 }

 .btn-title {
   font-size: 20px; /* 字体大小 */
   font-weight: bold; /* 字体加粗 */
   color: black; /* 黑色字体 */
   background: none; /* 移除按钮的背景 */
   border: none; /* 移除按钮的边框 */
   outline: none; /* 去掉焦点时的边框 */
   padding: 0; /* 无额外内边距 */
   cursor: pointer; /* 鼠标悬浮显示手型 */
   text-decoration: none; /* 去掉默认的文本装饰，比如下划线 */
   transition: color 0.3s ease; /* 颜色渐变过渡效果 */
 }
 
 .btn-title:hover {
   color: gray; /* 悬停时字体颜色变灰 */
 }
 
 .btn-title:focus {
   outline: none; /* 点击时不显示边框 */
 }
 
   .horizontal-line {
     width: 100%;
     height: 1px;
     background-color: gray;
     margin-top: 10px; /* 保证横线和按钮之间有足够的间隔 */
   }
 }
  // 白色矩形区域样式
.white-rectangle {
    background-color: white;
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 20px;

    // 行程天数按钮样式
	.day-buttons {
      display: flex;
      justify-content: space-around;
      margin-bottom: 10px;

    .day-button {
        padding: 1px 8px;
        border: 1px solid #808080; // 未点击时边框深灰色
        border-radius: 20px;
        background-color: white;
        color: #808080; // 未点击时字体深灰色
        cursor: pointer;
        font-weight: normal; // 未点击时字体正常粗细
        transition: all 0.3s ease; // 添加过渡效果，使样式变化更平滑

        &.active {
          border: 2px solid black; // 点击后边框加粗且为黑色
          color: black; // 点击后字体变为黑色
          font-weight: bold; // 点击后字体加粗
        }
      }
    }
	



    // 行程概览标题样式
	.overview-title {
      font-size: 18px;
      font-weight: bold;
      margin-bottom: 10px;
    }

    // 地图容器样式
	.map-container {
      width: 100%;
      height: 200px; // 根据需求调整地图容器高度
      border-radius: 20px;
      margin-bottom: 20px;
    }

    // 每天行程信息样式
	.daily-trips {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;

    .daily-trip {
        width: 100%; // 修改为占满父容器宽度
        height: 80px; // 设置固定高度为80px
        background-color: white;
        box-shadow: 0 0 5px lightgray;
        padding: 10px;
        margin-bottom: 20px;
        border-radius: 10px;

    .day-label {
          font-size: 16px;
          font-weight: bold;
          margin-bottom: 5px;
        }

    .city-label {
          font-size: 14px;
          color: lightgray;
          margin-bottom: 5px;
        }

    .places-label {
          font-size: 14px;
        }
      }

    .to-plan-trip {
        width: 100%;
        background-color: white;
        box-shadow: 0 0 5px lightgray;
        padding: 10px;
        margin-bottom: 20px;
        border-radius: 10px;
        font-size: 16px;
        font-weight: bold;
        text-align: center;
      }
    }
  }

  // 天气预报标题样式
.weather-title {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 10px;
  }

  // 天气预报区域样式
.weather-info {
    background-color: white;
    box-shadow: 0 0 5px lightgray;
    padding: 10px;
    border-radius: 10px;

.weather-item {
      margin-bottom: 10px;
    }
  }
}
</style>