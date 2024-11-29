<template>
  <view class="container">
    <!-- 叉号和链接框分为两行 -->
    <view class="row">
      <!-- 叉号 -->
      <view class="close-icon-container">
        <image src="/static/icons/close.png" class="close-icon" @click="closePage" />
      </view>
    </view>

    <!-- 链接框 -->
    <view class="link-container">
      <view class="link-box">
        <image :src="linkImage" class="link-image" />
        <text class="link-title">{{ linkTitle }}</text>
      </view>
    </view>
  </view>

  <!-- 警告提示 -->
  <view class="warning-box">
    <image src="/static/icons/warning.png" class="warning-icon" />
    <text class="warning-text">{{ warningMessage }}</text>
  </view>

  <!-- 行程和地点概览 -->
  <view class="overview">
    <!-- 行程部分 -->
    <text
      :class="['overview-text', { 'active-obview-text': activeTab === 'itinerary' }]"
      @click="toggleTab('itinerary')"
    >
      行程·{{ itineraryDays }}天
    </text>

    <!-- 地点部分 -->
    <text
      :class="['overview-text', { 'active-obview-text': activeTab === 'locations' }]"
      @click="toggleTab('locations')"
    >
      地点·{{ locationCount }}个
    </text>
  </view>

  <!-- 分割线 -->
  <view class="divider-line"></view>

  <!-- 根据选择显示不同的内容 -->
  <view class="tab-content">
    <!-- 行程内容 -->
    <view v-if="activeTab === 'itinerary'">
      <view class="itinerary-selection">
        <view
          class="itinerary-box"
          :class="{'active-itinerary-box': selectedDay === 'overview'}"
          @click="selectDay('overview')"
        >
          <text :class="{'active-tab-text': selectedDay === 'overview'}">
            总览
          </text>
        </view>

        <view
          v-for="i in itineraryDays"
          :key="i"
          class="itinerary-box"
          :class="{'active-itinerary-box': selectedDay === i}"
          @click="selectDay(i)"
        >
          <text :class="{'active-tab-text': selectedDay === i}">
            DAY{{ i }}
          </text>
        </view>
      </view>

      <!-- 总览 -->
      <view v-if="selectedDay === 'overview'">
        <view v-for="day in itineraryData" :key="day.day">
          <text class="day-heading">DAY{{ day.day }}</text>
          <view v-for="(location, index) in day.locations" :key="index" class="location-item">
            <view class="location-thumbnail">
              <image :src="location.photo" class="thumbnail" @error="(event) => event.target.src = '/static/link_image.png'" />
            </view>
            <view class="location-info">
              <text class="location-name">{{ location.name }}</text>
              <view class="location-details">
                <text class="location-type" :style="getLocationTypeColor(location.type)">
                  {{ location.type }}
                </text>
                <text class="location-separator"> | </text>
                <text class="location-description">{{ location.description }}</text>
              </view>
            </view>
            <!-- 选择框 -->
            <view class="select-icon-container" @click="toggleSelection(day.day - 1, index)">
              <image
                :src="location.isSelected ? '/static/icons/selected.png' : '/static/icons/select.png'"
                class="select-icon"
              />
            </view>
          </view>
        </view>
      </view>

      <!-- 显示特定DAY的地点 -->
      <view v-if="selectedDay !== 'overview'">
        <view class="day-heading">
          DAY{{ selectedDay }}
        </view>
        <view v-for="(location, index) in itineraryData[selectedDay - 1].locations" :key="index" class="location-item">
          <view class="location-thumbnail">
            <image :src="location.photo" class="thumbnail" @error="(event) => event.target.src = '/static/link_image.png'" />
          </view>
          <view class="location-info">
            <text class="location-name">{{ location.name }}</text>
            <view class="location-details">
              <text class="location-type" :style="getLocationTypeColor(location.type)">
                {{ location.type }}
              </text>
              <text class="location-separator"> | </text>
              <text class="location-description">{{ location.description }}</text>
            </view>
          </view>
          <view class="select-icon-container" @click="toggleSelection(selectedDay - 1, index)">
            <image :src="location.isSelected ? '/static/icons/selected.png' : '/static/icons/select.png'" class="select-icon" />
          </view>
        </view>
      </view>
    </view>

    <!-- 地点内容 -->
    <view v-if="activeTab === 'locations'">
      <view v-for="(day, dayIndex) in itineraryData" :key="dayIndex">
        <view v-for="(location, index) in day.locations" :key="index" class="location-item">
          <view class="location-thumbnail">
            <image :src="location.photo" class="thumbnail" @error="(event) => event.target.src = '/static/link_image.png'" />
          </view>
          <view class="location-info">
            <text class="location-name">{{ location.name }}</text>
            <view class="location-details">
              <text class="location-type" :style="getLocationTypeColor(location.type)">
                {{ location.type }}
              </text>
              <text class="location-separator"> | </text>
              <text class="location-description">{{ location.description }}</text>
            </view>
          </view>
          <!-- 选择框 -->
          <view class="select-icon-container" @click="toggleSelection(dayIndex, index)">
            <image
              :src="location.isSelected ? '/static/icons/selected.png' : '/static/icons/select.png'"
              class="select-icon"
            />
          </view>
        </view>
      </view>
    </view>
  </view>

  <!-- 行程确认框 -->
  <view v-if="showItineraryConfirm" class="confirm-box black-confirm" @click="createNewTrip">
    <text class="confirm-text white-text">创建为新的行程</text>
  </view>

  <!-- 地点确认框 -->
  <view v-if="showLocationConfirm" class="confirm-box white-confirm">
    <text class="confirm-text black-text">添加至行程</text>
  </view>
</template>

<script setup>
import { ref, onMounted, toRaw, getCurrentInstance } from 'vue'
import { useRoute } from 'vue-router'; // 导入 useRoute 以获取路由信息

// 数据和变量
const pageTitle = ref('');
const warningMessage = ref('地点和行程可能会有出入，请仔细核对哦~');
const itineraryDays = ref(0); // 初始化为0，根据 tripData
const locationCount = ref(0); // 初始化为0，根据 tripData
const activeTab = ref('itinerary'); // 默认显示行程
const selectedDay = ref('overview'); // 默认选中“总览”

// 确认框的状态变量
const showItineraryConfirm = ref(false);
const showLocationConfirm = ref(false);

// 新增变量用于存储接收到的 title 和 photo
const linkTitle = ref('链接标题');
const linkImage = ref('/static/link_image.png');

// 定义 tripId 变量
const tripId = ref(null);

// 定义 itineraryData 变量 (grouped by day)
const itineraryData = ref([]);

// 定义 allLocations (flat list)
const allLocations = ref([]);

// 定义 tripsById 缓存（假设有本地缓存需求）
const tripsById = ref({});

// 获取地点类型对应的颜色
const getLocationTypeColor = (type) => {
  if (type === '交通') {
    return { color: 'blue' }; // 交通 - 蓝色
  } else if (type === '美食') {
    return { color: '#E99D42' }; // 吃喝 - 黄色
  } else if (type === '景点') {
    return { color: '#54BCBD' }; // 景点 - 绿色
  }
  return {}; // 默认情况
};

// 获取路由对象
const route = useRoute();

// 规范化描述函数
const cleanDescription = (desc) => {
  if (!desc) return '';
  
  // Step 1: 移除开头的引号
  let cleaned = desc.replace(/^[‘’"']+/, '');
  
  // Step 2: 移除结尾的引号
  cleaned = cleaned.replace(/[‘’"']+$/, '');

  // Step 3: 移除结尾的中文和英文逗号
  cleaned = cleaned.replace(/[，,]$/, '');

  // 去除首尾多余的空格
  return cleaned.trim();
};




// 页面加载时获取 trip_id 并获取行程数据
onMounted(() => {
  // 获取 eventChannel
  const instance = getCurrentInstance();
  const eventChannel = instance.proxy.getOpenerEventChannel && instance.proxy.getOpenerEventChannel();

  if (eventChannel) {
    eventChannel.on('acceptDataFromOpenerPage', (data) => {
      console.log('接收到的数据:', data);
      // data 包含 title 和 photo
      if (data.title) {
        linkTitle.value = data.title;
        pageTitle.value = data.title;
      }
      if (data.photo) {
        linkImage.value = data.photo; // 保持原始的 URL
      }
    });
  }


  // 从路由查询参数中获取 trip_id
  const queryTripId = route.query.trip_information_id || route.query.trip_id || route.query.id;

  if (queryTripId) {
    console.log('获取到的 tripId:', queryTripId);
    tripId.value = queryTripId; // 将 tripId 存储到响应式变量中

    // 判断是本地数据还是从服务器获取数据
    if (tripsById.value[queryTripId]) {
      // 使用本地的行程数据进行初始化
      console.log('使用本地行程数据');
      initTripData(tripsById.value[queryTripId]).then(() => {
        // 照片已在 initTripData 中获取
      });
    } else {
      // 使用服务器数据
      console.log('请求服务器获取行程数据');
      fetchTripActivities(queryTripId);
    }
  } else {
    console.error('未找到 trip_id 或 trip_information_id 参数');
    uni.showToast({
      title: '未找到行程ID，请重新进入页面',
      icon: 'none',
      duration: 3000
    });
  }
});

// 从服务器获取行程数据
const fetchTripActivities = async (tripIdParam) => {
  if (!tripIdParam) {
    uni.showToast({
      title: '缺少行程 ID',
      icon: 'none',
    });
    return;
  }

  // 获取本地存储中的 access_token
  const token = uni.getStorageSync('access_token');
  if (!token) {
    uni.showToast({
      title: '请先登录',
      icon: 'none',
    });
    return;
  }

  // 显示加载提示
  uni.showLoading({
    title: '加载中...',
  });

  // 构建请求 URL，添加查询参数，参数名为 trip_information_id
  const url = `https://734dw56037em.vicp.fun/api/trip/get_trip_activities/?trip_information_id=${tripIdParam}`;
  console.log('请求 URL:', url);

  // 发起 GET 请求
  uni.request({
    url: url,
    method: 'GET',
    header: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    success: async (res) => {
      console.log('响应数据:', res);
      if (res.statusCode === 200) {
        const tripData = res.data; // 假设响应包含 'activities' 和 'trip'

        if (!tripData || !tripData.activities || !tripData.trip) {
          console.error('未获取到有效的行程数据');
          uni.showToast({
            title: '未获取到有效的行程数据',
            icon: 'none',
          });
          return;
        }

        console.log('行程数据:', tripData);
        // 将获取到的行程数据存入本地缓存
        tripsById.value[tripIdParam] = tripData;
        // 初始化行程数据并获取照片
        await initTripData(tripData);
      } else {
        uni.showToast({
          title: res.data.error || '请求失败',
          icon: 'none',
        });
      }
    },
    fail: (err) => {
      console.error('请求失败:', err);
      uni.showToast({
        title: '网络请求失败，请稍后重试',
        icon: 'none',
      });
    },
    complete: () => {
      uni.hideLoading();
    },
  });
};

// 辅助函数，用于延迟指定的毫秒数
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// 获取单个活动的照片
const getActivityPhoto = (activityId) => {
  return new Promise((resolve, reject) => {
    const token = uni.getStorageSync('access_token');
    if (!token) {
      reject('未找到 access_token，请先登录');
      return;
    }

    const url = `https://734dw56037em.vicp.fun/api/trip/trip-photo/${activityId}/`;
    console.log(`请求 trip-photo URL: ${url}`);

    uni.request({
      url: url,
      method: 'GET',
      header: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      success: (res) => {
        if (res.statusCode === 200 && res.data.poi && res.data.poi.url) {
          // 获取 poi.url，并将 http 改为 https
          const photoUrl = res.data.poi.url; // 保持原始的 URL
          resolve(photoUrl);
        } else {
          console.warn(`未能获取活动 ID ${activityId} 的照片:`, res.data.error || '未知错误');
          resolve('/static/link_image.png'); // 使用默认图片
        }
      },
      fail: (err) => {
        console.error(`获取活动 ID ${activityId} 照片失败:`, err);
        resolve('/static/link_image.png'); // 使用默认图片
      },
    });
  });
};

// 获取所有活动的照片，限制每秒最多3个请求
const fetchAllPhotos = async () => {
  const batchSize = 3; // 每批请求数量
  const delayMs = 1000; // 每批请求之间的延迟时间（毫秒）

  // 过滤出需要获取照片的活动
  const locationsToFetch = allLocations.value.filter(location => !location.photo || location.photo === '/static/link_image.png');

  for (let i = 0; i < locationsToFetch.length; i += batchSize) {
    const batch = locationsToFetch.slice(i, i + batchSize);

    // 为当前批次的每个活动创建请求
    const batchPromises = batch.map(async (location) => {
      try {
        const photoUrl = await getActivityPhoto(location.id);
        location.photo = photoUrl;
      } catch (error) {
        console.warn(`获取活动 ID ${location.id} 照片时出错:`, error);
        location.photo = '/static/link_image.png'; // 使用默认图片
      }
    });

    // 等待当前批次的所有请求完成
    await Promise.all(batchPromises);
    console.log(`第 ${i / batchSize + 1} 批次的照片已更新`);

    // 如果还有下一批请求，等待一秒钟
    if (i + batchSize < locationsToFetch.length) {
      await delay(delayMs);
    }
  }

  console.log('所有活动的照片已更新:', toRaw(allLocations.value));
};

// 初始化行程数据
const initTripData = async (tripData) => {
  // ...（前面的代码保持不变）

  // 处理 activities
  const activities = tripData.activities || [];

  // 确定行程天数
  const daysSet = new Set();
  activities.forEach(activity => {
    if (activity.days) {
      daysSet.add(activity.days);
    }
  });
  itineraryDays.value = daysSet.size;

  // 更新地点总数
  locationCount.value = activities.length;

  // 使用一个映射来存储地点对象
  const locationMap = {};
  const groupedByDay = {};

  activities.forEach(activity => {
    const day = activity.days;

    // 创建或获取地点对象
    let location = locationMap[activity.id];
    if (!location) {
      location = {
        id: activity.id,
        name: activity.trip_destination,
        type: activity.tag,
        description: cleanDescription(activity.description),
        address: '',
        photo: activity.photo || '/static/link_image.png',
        reservation_method: activity.reservation_method,
        isSelected: true,
      };
      locationMap[activity.id] = location;
    }

    // 将地点对象添加到 groupedByDay 中
    if (!groupedByDay[day]) {
      groupedByDay[day] = [];
    }
    groupedByDay[day].push(location);
  });

  // 转换为 itineraryData 数组
  const itineraryArray = [];
  const sortedDays = Array.from(daysSet).sort((a, b) => a - b);
  sortedDays.forEach(dayNum => {
    itineraryArray.push({
      day: dayNum,
      locations: groupedByDay[dayNum],
    });
  });

  itineraryData.value = itineraryArray;

  // 创建所有地点的扁平化列表
  allLocations.value = Object.values(locationMap);

  // 更新行程天数和地点总数
  itineraryDays.value = sortedDays.length;
  locationCount.value = activities.length;

  // 输出调试信息
  console.log('itineraryData:', toRaw(itineraryData.value));
  console.log('allLocations:', toRaw(allLocations.value));

  // 获取所有活动的照片
  await fetchAllPhotos();
};

// 获取 day 对应的 dayIndex
const getDayIndex = (day) => {
  return itineraryData.value.findIndex(d => d.day === day);
};

// 获取特定 day 的地点列表
const getDayLocations = (day) => {
  const dayIndex = getDayIndex(day);
  if (dayIndex !== -1) {
    return itineraryData.value[dayIndex].locations;
  }
  return [];
};

// 切换选择状态
const toggleSelection = (locationId) => {
  if (activeTab.value === 'itinerary') {
    // 在行程标签下，通过 locationId 找到对应的地点并切换状态
    itineraryData.value.forEach(day => {
      day.locations.forEach(location => {
        if (location.id === locationId) {
          location.isSelected = !location.isSelected;
        }
      });
    });
  } else if (activeTab.value === 'locations') {
    // 在地点标签下，通过 locationId 找到对应的地点并切换状态
    allLocations.value.forEach(location => {
      if (location.id === locationId) {
        location.isSelected = !location.isSelected;
      }
    });
  }
};

// 切换行程和地点标签
const toggleTab = (tab) => {
  activeTab.value = tab;
  if (tab === 'itinerary') {
    showItineraryConfirm.value = true;
    showLocationConfirm.value = false;
  } else if (tab === 'locations') {
    showLocationConfirm.value = true;
    showItineraryConfirm.value = false;
  }
};

// 选择行程的天数
const selectDay = (day) => {
  selectedDay.value = day;
};

// 收集用户选择的行程和地点
const collectSelectedActivities = () => {
  const selectedItinerary = [];
  itineraryData.value.forEach(day => {
    const selectedLocations = day.locations.filter(location => location.isSelected);
    if (selectedLocations.length > 0) {
      selectedItinerary.push({
        day: day.day,
        locations: selectedLocations
      });
    }
  });

  const selectedLocations = allLocations.value.filter(location => location.isSelected);

  return {
    itinerary: selectedItinerary,
    locations: selectedLocations
  };
};

// 创建新行程并跳转到 Overview 页面
const createNewTrip = () => {
  const selectedActivities = collectSelectedActivities();

  // 将选中的活动传递给 Overview 页面
  uni.navigateTo({
    url: `/pages/Overview/Overview?trip_id=${tripId.value}`,
    success: (res) => {
      // 向目标页面传递数据
      res.eventChannel.emit('sendSelectedActivities', selectedActivities);
    },
    fail: (err) => {
      console.error('跳转到 Overview 页面失败:', err);
      uni.showToast({
        title: '跳转失败，请稍后重试',
        icon: 'none',
      });
    },
  });
};


// 跳转到 create_method 页面
const closePage = () => {
  uni.redirectTo({
    url: '/pages/create_method/create_method' // 根据你的实际路径修改
  });
};
</script>

<style scoped>
/* 页面整体布局 */
.container {
  display: flex;
  flex-direction: column;
  padding: 20rpx;
}

/* 叉号 */
.close-icon-container {
  display: flex;
  justify-content: flex-start;
  padding-bottom: 20rpx;
}

.close-icon {
  width: 30rpx;
  height: 30rpx;
  cursor: pointer;
}

/* 链接框 */
.link-container {
  width: 100%;
  display: flex;
  justify-content: center;
  margin-top: 20rpx;
}

.link-box {
  width: 100%;
  max-width: 700rpx;
  height: 150rpx;
  display: flex;
  align-items: center;
  background-color: #fff;
  border-radius: 50rpx;
  box-shadow: 4px 4px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.link-image {
  width: 90px;
  height: 100%;
  object-fit: cover;
  border-radius: 50rpx 0 0 50rpx;
}

.link-title {
  font-size: 18px;
  color: #333;
  flex-grow: 1;
  padding-left: 20rpx;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 警告提示 */
.warning-box {
  width: 100%;
  max-width: 900rpx;
  margin: 0 auto;
  margin-left: -20rpx;
  margin-top: 20rpx;
  margin-bottom: 20rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.warning-icon {
  width: 50rpx;
  height: 50rpx;
  margin-right: 15rpx;
}

.warning-text {
  font-size: 17px;
  font-style: italic;
  color: #ff6f00;
}

/* 行程和地点概览 */
.overview {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  padding-left: 30rpx;
  margin: 20rpx 0;
}

.overview-text {
  font-size: 45rpx;
  color: #888;
  cursor: pointer;
  margin-right: 30rpx;
  letter-spacing: 2rpx;
}

.active-obview-text {
  color: #000;
  font-weight: bold;
}

/* 分割线 */
.divider-line {
  width: 100%;
  height: 2rpx;
  background-color: #e0e0e0;
  margin: 10rpx 0;
}

/* 行程选择框 */
.itinerary-selection {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  margin-bottom: 20rpx;
}

.itinerary-box {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10rpx;
  margin-left: 5rpx;
  margin-right: 15rpx;
  background-color: #fff;
  border-radius: 60rpx;
  border: 1px solid #ccc;
  cursor: pointer;
  font-size: 26rpx;
  width: 80rpx;
}

.active-itinerary-box {
  background-color: #000;
  color: #fff;
  font-weight: bold;
}

.tab-content {
  display: flex;
  flex-direction: column;
  padding: 20rpx;
  padding-bottom: 130rpx;
  position: relative;
}

.tab-text {
  font-size: 28rpx;
  color: #333;
}

.day-heading {
  font-size: 55rpx;
  font-weight: bold;
  color: #333;
  padding-left: 10px;
}

/* 地点列表 */
.location-item {
  display: flex;
  align-items: flex-start;
  padding: 20rpx;
  margin-left: 0rpx;
}

.location-thumbnail {
  width: 120rpx;
  height: 120rpx;
  border-radius: 30rpx;
  margin-right: 25rpx;
}

.thumbnail {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 40rpx;
  margin-left: -5rpx;
  border: 1px solid #888;
}

.location-info {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.location-name {
  font-size: 23px;
  color: #000;
  margin-top: 10rpx;
  margin-bottom: 5rpx;
}

.location-type {
  font-size: 26rpx;
  color: #888;
  font-weight: bold;
  margin-top: 18rpx;
}

.location-description {
  color: #000;
  font-size: 24rpx;
}

/* 选择框样式 */
.select-icon-container {
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  margin-left: 20rpx;
  margin-top: 20rpx;
}

.select-icon {
  width: 60rpx;
  height: 60rpx;
}

.confirm-box {
  position: fixed;
  bottom: 50rpx;
  left: 50%;
  transform: translateX(-50%);
  padding: 20rpx 40rpx;
  border-radius: 50rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32rpx;
  font-weight: bold;
}

.black-confirm {
  background-color: #000;
}

.white-text {
  color: #fff;
}

.white-confirm {
  background-color: #fff;
  box-shadow: 0 4px 10px rgba(0, 0, 0.1, 0.2);
}

.black-text {
  color: #000;
}

/* 加载自定义字体 */
@font-face {
  font-family: 'TaipeiSansTCBeta';
  src: url('font/TaipeiSansTCBeta-Regular.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

body {
  font-family: sans-serif;
}
</style>
