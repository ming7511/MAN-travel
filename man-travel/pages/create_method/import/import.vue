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
        <image src="/static/link_image.png" class="link-image" />
        <text class="link-title">链接标题</text>
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
              <image :src="location.thumbnail" class="thumbnail" />
            </view>
            <view class="location-info">
              <text class="location-name">{{ location.name }}</text>
              <view class="location-details">
                <text class="location-type" :style="getLocationTypeColor(location.type)">
                  {{ location.type }}
                </text>
                <text class="location-separator"> | </text>
                <text class="location-address">{{ location.address }}</text>
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
            <image :src="location.thumbnail" class="thumbnail" />
          </view>
          <view class="location-info">
            <text class="location-name">{{ location.name }}</text>
            <view class="location-details">
              <text class="location-type" :style="getLocationTypeColor(location.type)">
                {{ location.type }}
              </text>
              <text class="location-separator"> | </text>
              <text class="location-address">{{ location.address }}</text>
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
            <image :src="location.thumbnail" class="thumbnail" />
          </view>
          <view class="location-info">
            <text class="location-name">{{ location.name }}</text>
            <view class="location-details">
              <text class="location-type" :style="getLocationTypeColor(location.type)">
                {{ location.type }}
              </text>
              <text class="location-separator"> | </text>
              <text class="location-address">{{ location.address }}</text>
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
  <view v-if="showItineraryConfirm" class="confirm-box black-confirm">
    <text class="confirm-text white-text">创建为新的行程</text>
  </view>

  <!-- 地点确认框 -->
  <view v-if="showLocationConfirm" class="confirm-box white-confirm">
    <text class="confirm-text black-text">添加至行程</text>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue';

// 数据和变量
const pageTitle = ref('福州三天两夜旅游攻略来喽~');
const warningMessage = ref('地点和行程可能会有出入，请仔细核对哦~');
const itineraryDays = ref(3); // 默认3天
const locationCount = ref(12); // 默认12个地点
const locations = ref([]); // 地点数据
const activeTab = ref('itinerary'); // 默认显示行程
const selectedDay = ref('overview'); // 默认选中“总览”

// 确认框的状态变量
const showItineraryConfirm = ref(false);
const showLocationConfirm = ref(false);

const getLocationTypeColor = (type) => {
  if (type === '交通') {
    return { color: '' }; // 交通 - 蓝色
  } else if (type === '吃喝') {
    return { color: '#E99D42' }; // 吃喝 - 黄色
  } else if (type === '景点') {
    return { color: '#54BCBD' }; // 景点 - 绿色
  }
  return {}; // 默认情况
};

// 页面加载时从数据库获取地点信息
onMounted(() => {
  locationData();
});
const itineraryData = ref([
  {
    day: 1,
    locations: [
      { 
        name: '福州站', 
        type: '交通', 
        address: '福州市晋安区华林路602号', 
        thumbnail: '/static/link_image.png', 
        isSelected: true // 确保添加 isSelected 属性
      },
      {
        name: '三坊七巷',
        type: '景点',
        address: '福州市鼓楼区文儒坊6号',
        thumbnail: '/static/link_image.png',
        isSelected: true
      },
      {
        name: '鼓山',
        type: '景点',
        address: '福州市晋安区鼓山路',
        thumbnail: '/static/link_image.png',
        isSelected: true
      },
      {
        name: '达明美食街',
        type: '吃喝',
        address: '福州市鼓楼区达明路186号',
        thumbnail: '/static/link_image.png',
        isSelected: true
      }
    ]
  },
  {
    day: 2,
    locations: [
      { 
        name: '同利肉燕（道山路店)', 
        type: '吃喝', 
        address: '福州市鼓楼区道山路157号', 
        thumbnail: '/static/link_image.png', 
        isSelected: true
      },
      {
        name: '上下杭历史文化街区',
        type: '景点',
        address: '福建省福州市台江区上下杭牌坊',
        thumbnail: '/static/link_image.png',
        isSelected: true
      },
      {
        name: '唐沫茶兮（达明路）',
        type: '吃喝',
        address: '福州市鼓楼区杨桥东路26号',
        thumbnail: '/static/link_image.png',
        isSelected: true
      },
      {
        name: '西禅古寺',
        type: '景点',
        address: '福州市鼓楼区洪山镇工业路455号',
        thumbnail: '/static/link_image.png',
        isSelected: true
      },
      {
        name: '公园路甜汤',
        type: '吃喝',
        address: '福州市鼓楼区公园路',
        thumbnail: '/static/link_image.png',
        isSelected: true
      }
    ]
  },
]);

// 模拟从数据库或API获取地点数据
const locationData = () => {
  locations.value = [
    {
      name: '福州站',
      type: '交通',
      address: '福州市晋安区华林路502号',
      thumbnail: '/static/logo.png',
      isSelected: false, // 添加 isSelected 属性
    },
    {
      name: '三坊七巷',
      type: '景点',
      address: '福州市鼓楼区三坊七巷',
      thumbnail: '/static/logo.png',
      isSelected: false, // 添加 isSelected 属性
    },
  ];
};

const toggleSelection = (dayIndex, locationIndex) => {
  const day = itineraryData.value[dayIndex];
  const location = day.locations[locationIndex];
  if (location) {
    location.isSelected = !location.isSelected; // 切换选中状态
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

.location-address {
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
