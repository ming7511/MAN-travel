<template>
  <view class="travel-plan-overview-page">
    <!-- 返回按钮容器 -->
    <view class="back-button-container">
      <image src="/static/icons/back-icon.png" class="back-button" @click="goBack" />
    </view>
    <!-- 行程名 -->
    <view class="header">
      <text class="trip-name">{{ tripTitle }}</text>
    </view>
    <!-- 旅行时间 -->
    <view class="travel-time">{{ travelDateRange }} {{ tripDuration }}</view>
    <!-- 行程标题及横线 -->
    <view class="trip-section">
      <view class="button-group">
        <!-- 行程按钮 -->
        <button class="btn-title" @click="handleShowOverview">行程</button>
        <!-- 旅行账单按钮 -->
        <button class="btn-title" @click="handleShouyeClick">旅行账单</button>
        <!-- 行李清单按钮 -->
        <button class="btn-title" @click="handleXingliClick">旅行清单</button>
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
      <div id="map-container" class="map-container"></div>
      <!-- 每天行程信息 -->
      <view class="daily-trips">
        <view v-for="(dayTrip, index) in dailyTrips" :key="index" class="daily-trip" @click="handleDayClick(dayTrip.day)">
          <view class="day-label">{{ dayTrip.day }}</view>
          <view class="city-label">{{ dayTrip.city }}</view>
          <view class="places-label">{{ dayTrip.places }}</view>
        </view>
        <!-- 待规划行程 -->
        <view class="to-plan-trip">待规划</view>
      </view>
      <!-- 新增：地点添加输入框及添加按钮 -->
      <view class="add-place-section">
        <input v-model="newPlace" placeholder="输入要添加的地点" class="add-place-input" />
        <button class="add-place-button" @click="addPlace">添加地点</button>
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
import { useRoute, useRouter } from 'vue-router';
import { ref, reactive, onMounted, nextTick } from 'vue';

export default {
    setup() {
        // 使用reactive创建响应式的tripsById对象
        const tripsById = reactive({
            1: {
                title: '',
                dateRange: '',
                duration: '',
                places: [],
                weather: [],
                placeCoordinates: {},
                dailyTrips: []
            }
        });

        const currentDay = ref('总览');
        const weatherForecast = ref([]);
        const tripTitle = ref('');
        const travelDateRange = ref('');
        const tripDuration = ref('');
        const places = ref([]);
        const map = ref(null);
        const days = ref([]);
        const newPlace = ref('');
        const placeCoordinates = ref({});
        const selectedCity = ref('');
        const startDate = ref('');
        const endDate = ref('');
        const dayCount = ref(0);

        onMounted(() => {
            const route = useRoute();
            // 从路由参数获取行程数据（假设self_create_time.vue上传后传递过来的参数包含这些信息）
            const tripId = route.query.id;
            const tripData = route.query.tripData? JSON.parse(decodeURIComponent(route.query.tripData)) : {};
            const { trip_name: city, start_date: start, end_date: end, day_count: dayCountValue } = tripData;

            // 获取存储的行程信息，并进行赋值和初始化相关数据
            selectedCity.value = city || uni.getStorageSync('selectedCity') || '';
            startDate.value = start || uni.getStorageSync('startDate') || '';
            endDate.value = end || uni.getStorageSync('endDate') || '';
            dayCount.value = dayCountValue || uni.getStorageSync('dayCount') || 0;

            if (tripId) {
                const trip = tripsById[tripId];
                if (trip) {
                    // 依据获取的信息初始化行程相关数据
                    tripTitle.value = `${selectedCity.value}${dayCount.value}日游`;
                    travelDateRange.value = `${startDate.value}至${endDate.value}`;
                    tripDuration.value = `${dayCount.value}天`;
                    places.value = trip.places;
                    weatherForecast.value = trip.weather;

                    // 动态生成天数按钮
                    days.value = ['总览',...Array.from({ length: dayCount.value }, (_, i) => `DAY${i + 1}`)];

                    // 填充每日行程数据（确保从对应行程数据中正确获取数据，若为空则初始化简单结构）
                    if (trip.dailyTrips.length === 0 && dayCount.value > 0) {
                        trip.dailyTrips = Array.from({ length: dayCount.value }, (_, i) => ({
                            day: `DAY${i + 1}`,
                            city: selectedCity.value,
                            places: ''
                        }));
                    }

                    // 初始化地图，设置中心为第一天第一个地点的坐标（需确保坐标数据准确获取）
                    initMap(trip.placeCoordinates).then(() => {
                        // 使用nextTick确保地图初始化完成后（可能涉及异步操作）再更新视图，避免视图渲染时相关数据还没准备好
                        nextTick(() => {
                            // 这里可以添加一些额外的逻辑，比如触发一些依赖地图初始化完成后的业务逻辑等
                        });
                    });
                }
            }
        });

        // 辅助方法：从旅行时长字符串中提取天数（适配如 "5天4晚" 等不同格式），这里暂时可能用不到，可根据实际情况保留或调整
        const getDayCountFromDuration = (duration) => {
            return parseInt(duration.split('天')[0]);
        };

        // 定义获取单个地点坐标的函数，目前只是简单返回已有数据结构中的坐标，后续可扩展实现从接口等获取
        const getPlaceCoordinate = (place) => {
            return placeCoordinates.value[place] || null;
        };

        // 初始化地图，并加载行程坐标
        const initMap = (placeCoordinates) => {
            return AMapLoader.load({
                key: 'd702b20c1d0b7a34eaffae39500d2210', // 替换为你的高德地图 API 密钥
                version: '2.0',
                plugins: ['AMap.ToolBar']
            }).then((AMap) => {
                map.value = new AMap.Map('map-container', {
                    center: [119.306238, 26.075302], // 默认中心位置，可以改为从行程数据中获取第一天第一个地点坐标
                    zoom: 12
                });
                map.value.addControl(new AMap.ToolBar());

                const dayMarkers = [];
                const dayColors = {};
                for (let i = 1; i <= days.value.length - 1; i++) {
                    dayColors[`DAY${i}`] = getRandomColor();
                }

                // 遍历每天行程信息，添加标记和连线（适配任意天数行程，这里正确处理对应天数情况）
                trip.dailyTrips.forEach((dayTrip) => {
                    const places = dayTrip.places.split(' - ');
                    let prevMarker = null;
                    places.forEach((place) => {
                        const coordinates = getPlaceCoordinate(place);
                        if (coordinates) {
                            const marker = new AMap.Marker({
                                position: coordinates,
                                map: map.value,
                                title: place
                            });
                            if (prevMarker) {
                                const polyline = new AMap.Polyline({
                                    path: [prevMarker.getPosition(), marker.getPosition()],
                                    map: map.value,
                                    strokeColor: dayColors[dayTrip.day],
                                    strokeWeight: 6
                                });
                            }
                            prevMarker = marker;
                        }
                    });
                });

                // 设置地图中心为第一天第一个地点
                const firstDayTrip = trip.dailyTrips[0];
                if (firstDayTrip) {
                    const firstPlace = firstDayTrip.places.split(' - ')[0];
                    const coordinates = getPlaceCoordinate(firstPlace);
                    if (coordinates) {
                        map.value.setCenter(coordinates);
                        map.value.setZoom(12);
                    }
                }

                return map.value;
            });
        };

        // 辅助方法：生成随机颜色（用于不同天数行程的连线等颜色区分）
        const getRandomColor = () => {
            const letters = '0123456789ABCDEF';
            let color = '#';
            for (let i = 0; i < 6; i++) {
                color += letters[Math.floor(Math.random() * 16)];
            }
            return color;
        };

        const goBack = () => {
            // 返回到首页 index.vue
            uni.navigateTo({
                url: '/pages/index/index'
            });
        };

        const handleDayClick = (day) => {
            const tripId = route.query.id;
            const trip = tripsById[tripId];

            if (day!== '总览') {
                const selectedTrip = trip.dailyTrips.find((trip) => trip.day === day);
                if (selectedTrip) {
                    let places = selectedTrip.places;
                    const placesArray = Array.isArray(places)? places : places.split(' - ');
                    const placesEncoded = encodeURIComponent(placesArray.join(' - '));
                    const tripEncoded = encodeURIComponent(JSON.stringify(trip));

                    // 获取对应天行程地点的坐标信息，并进行编码传递（完善了坐标信息获取逻辑）
                    const coordinatesForDay = getCoordinatesByDay(day, trip.placeCoordinates);
                    const coordinatesEncoded = encodeURIComponent(JSON.stringify(coordinatesForDay));

                    uni.navigateTo({
                        url: `/pages/DayDetail/DayDetail?day=${day}&id=${tripId}&places=${placesEncoded}&title=${encodeURIComponent(trip.title)}&dateRange=${encodeURIComponent(trip.dateRange)}&duration=${encodeURIComponent(trip.duration)}&tripData=${tripEncoded}&coordinates=${coordinatesEncoded}`
                    });
                }
            } else {
                // 如果点击的是总览，保持在当前页面并更新视图
                setCurrentDay(day);
            }
        };

        const getCoordinatesByDay = (day, placeCoordinates) => {
            const selectedTrip = trip.dailyTrips.find((trip) => trip.day === day);
            const result = {};
            if (selectedTrip) {
                const places = selectedTrip.places.split(' - ');
                places.forEach((place) => {
                    const coordinate = getPlaceCoordinate(place);
                    if (coordinate) {
                        result[place] = coordinate;
                    } else {
                        console.log(`地点 ${place} 的坐标不存在，请检查数据。`);
                    }
                });
            }
            return result;
        };

        const handleShouyeClick = () => {
            const tripId = route.query.id;
            if (tripId) {
                useRouter().push({
                    path: `/pages/shouye/shouye`, // 目标页面的路径
                    query: { id: tripId } // 将行程 ID 作为查询参数传递
                });
            }
        };

        const handleXingliClick = () => {
            const tripId = route.query.id;
            if (tripId) {
                useRouter().push({
                    path: `/pages/xingli/xingli`, // 目标页面的路径
                    query: { id: tripId } // 将行程 ID 作为查询参数传递
                });
            }
        };

        const setCurrentDay = (day) => {
            currentDay.value = day;

            const tripId = route.query.id;
            const trip = tripsById[tripId];

            if (trip) {
                if (day!== '总览') {
                    const selectedTrip = trip.dailyTrips.find((trip) => trip.day === day);
                    if (selectedTrip) {
                        const firstPlace = selectedTrip.places.split(' - ')[0];
                        const coordinates = trip.placeCoordinates[firstPlace];
                        if (coordinates) {
                            map.value.setCenter(coordinates);
                            map.value.setZoom(14);
                        }
                    }
                } else {
                    const firstDayTrip = trip.dailyTrips[0];
                    const firstPlace = firstDayTrip.places.split(' - ')[0];
                    const coordinates = trip.placeCoordinates[firstPlace];
                    if (coordinates) {
                        map.value.setCenter(coordinates);
                        map.value.setZoom(12);
                    }
                }
            }
        };

        const addPlace = (newPlace) => {
            if (newPlace.value.trim()!== '') {
                // 假设后续实现了从地图服务 API 获取坐标的函数 fetchCoordinateFromAPI
                fetchCoordinateFromAPI(newPlace.value).then((coordinate) => {
                    if (coordinate) {
                        places.value.push(newPlace.value);
                        placeCoordinates.value[newPlace.value] = coordinate;
                        updateDailyTripsWithNewPlace(newPlace.value);
                        newPlace.value = '';
                    } else {
                        console.log(`获取地点 ${newPlace.value} 的坐标失败，请稍后再试。`);
                    }
                }).catch((error) => {
                    console.log(`获取坐标出现错误：${error}`);
                });
            }
        };

        const updateDailyTripsWithNewPlace = (newPlace) => {
            trip.dailyTrips.forEach((dayTrip) => {
                if (dayTrip.places === '') {
                    dayTrip.places = newPlace;
                } else {
                    const placesArray = dayTrip.places.split(' - ');
                    if (!placesArray.includes(newPlace)) {
                        dayTrip.places += ` - ${newPlace}`;
                    }
                }
            });
        };

        const handleShowOverview = () => {
            // 这里可以添加具体逻辑，比如切换行程展示视图为详细列表或者地图展示等模式
            console.log('执行了handleShowOverview方法，可在此添加切换视图逻辑');
        };

        return {
            currentDay,
            weatherForecast,
            tripTitle,
            travelDateRange,
            tripDuration,
            places,
            map,
            days,
            tripsById,
            newPlace,
            placeCoordinates,
            selectedCity,
            startDate,
            endDate,
            dayCount,
            getDayCountFromDuration,
            initMap,
            goBack,
            handleDayClick,
            getCoordinatesByDay,
            handleShouyeClick,
            handleXingliClick,
            setCurrentDay,
            addPlace,
            updateDailyTripsWithNewPlace,
            handleShowOverview
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
	  margin-top: 25px;
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
