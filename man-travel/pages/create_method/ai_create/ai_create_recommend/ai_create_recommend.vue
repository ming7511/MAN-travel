<template>
  <view class="container">
    <!-- 关闭按钮 -->
    <view class="close-icon-container">
      <image src="/static/icons/close.png" class="close-icon" @click="closePage" />
    </view>

    <!-- 标题：这趟旅行要去哪里？ -->
    <view class="title-container">
      <text class="title-text">这趟旅行要去哪里？</text>
    </view>

    <!-- 旅行目的地 -->
    <view class="location-container">
      <view class="location-circle">
        <text class="location-text">{{ locationInput }}</text>
      </view>
    </view>

    <!-- 标题：你希望这趟旅行？ -->
    <view class="travel-preference-title-container">
      <text class="travel-preference-title">你希望这趟旅行？</text>
    </view>

    <!-- 旅行关键词块 -->
    <view class="keywords-container">
      <view class="keyword-item" v-for="(keyword, index) in travelKeywords.slice(0, 9)" :key="index" :class="{'selected': selectedKeywords.includes(keyword)}" @click="selectKeyword(keyword)">
        <text class="keyword-text">{{ keyword }}</text>
      </view>
    </view>

    <!-- 标题：这些地点不容错过！ -->
    <view class="must-visit-title-container">
      <text class="must-visit-title">这些地点不容错过！</text>
    </view>

    <!-- 热门景点列表 -->
    <scroll-view class="locations-container" scroll-y="true">
      <view class="location-item" v-for="(location, index) in popularLocations" :key="index">
        <view class="location-thumbnail">
          <image :src="location.thumbnail" class="thumbnail" />
        </view>
        <view class="location-info">
		<text class="location-name">{{ location.name }}</text>
          <view class="location-details">
            <text class="location-type" :style="getLocationTypeColor(location.type)">{{ location.type }}</text>
            <text class="location-separator"> |  </text>
            <text class="location-recommendation">{{  location.recommendation }}</text>
          </view>
        </view>
        <!-- 选择框 -->
        <view class="select-icon-container" @click="toggleLocationSelection(index)">
          <image :src="location.isSelected ? '/static/icons/selected.png' : '/static/icons/select.png'" class="select-icon" />
        </view>
      </view>
    </scroll-view>

<!-- 开始规划按钮 -->
    <view class="start-planning-container">
      <view class="start-planning-button" @click="startPlanning">
        <!-- 魔法棒图标 -->
        <image src="/static/icons/magic-wand-green.png" class="magic-wand-icon" />
        <text class="start-planning-text">开始规划！</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue';

// 从缓存中获取用户选择的城市
const locationInput = ref('');

// 旅行关键词词库
const keywordPool = [
'乡村风情', '呼吸自然', '美食之旅', '小众地点', '海岛风光', '特种兵打卡',
  '慢时光', '名胜古迹', 'CityWalk', '自然风光',
   '自然风光', '主题公园', '动物园探访', '博物馆之旅',  '购物狂欢',
  '奢华度假', '温馨亲子', '生态观光', '田园牧歌', '宗教朝圣',
 '夜市美食',  '夜空观星', '乡野采摘', '地道手工', '自驾之旅', '动物观察', '山川峡谷',  '音乐节日',
  '建筑之美',  '摄影打卡', '露营体验', '手工艺品探店', '寺庙参观',  '经典建筑',
];

// 存储随机选择的9个关键词
const travelKeywords = ref([]);
const selectedKeywords = ref([]);

// 初始化随机关键词
const initializeKeywords = () => {
  travelKeywords.value = keywordPool.sort(() => Math.random() - 0.5).slice(0, 9);
};

// 关闭页面方法
const closePage = () => {
  uni.navigateBack(); // 返回上一页或关闭页面
};

// 开始规划旅行
const startPlanning = () => {
  const travelData = {};

  // 确保用户选择了旅行的目的地
  if (!locationInput.value || locationInput.value === '未选择城市') {
    uni.showToast({
      title: '请选择旅行目的地',
      icon: 'none'
    });
    return; // 提示用户选择目的地，并终止函数
  }

  // 启动导航到计划页面并传递数据
  uni.navigateTo({
    url: `/pages/create_method/ai_create/ai_create_recommend/ai_create_recommend?data=${JSON.stringify(travelData)}`,
  });
};

// 初始化地点信息，假设是从上一页传递过来的
onMounted(() => {
  locationInput.value = uni.getStorageSync('selectedCity') || '未选择城市'; // 从缓存中获取城市
  initializeKeywords(); // 初始化关键词
});

// 选择旅行关键词
const selectKeyword = (keyword) => {
  if (selectedKeywords.value.includes(keyword)) {
    // 如果已经选中，则取消选中
    selectedKeywords.value = selectedKeywords.value.filter(item => item !== keyword);
  } else {
    // 如果未选中，则添加到选中列表
    selectedKeywords.value.push(keyword);
  }
};


// 热门景点数据
const popularLocations = ref([
  {
    name: '三坊七巷',
    type: '景点',
    recommendation: '历史悠久的福州古城',
    thumbnail: '/static/images/sanfangqixiang.png',
    isSelected: false
  },
  {
    name: '鼓山',
    type: '景点',
    recommendation: '邂逅一场浪漫的登顶徒步',
    thumbnail: '/static/images/gushan.png',
    isSelected: false
  },
  {
    name: '达明美食街',
    type: '吃喝',
    recommendation: '品尝福州的特色美食',
    thumbnail: '/static/images/daming.png',
    isSelected: false
  },
  {
    name: '烟台山公园',
    type: '景点',
    recommendation: '徜徉着中西结合的历史古韵',
    thumbnail: '/static/images/yantaishan.png',
    isSelected: false
  },
  {
    name: '烟台山公园',
    type: '景点',
    recommendation: '徜徉着中西结合的历史古韵',
    thumbnail: '/static/images/yantaishan.png',
    isSelected: false
  },{
    name: '烟台山公园',
    type: '景点',
    recommendation: '徜徉着中西结合的历史古韵',
    thumbnail: '/static/images/yantaishan.png',
    isSelected: false
  }
]);

// 切换景点选择状态
const toggleLocationSelection = (index) => {
  popularLocations.value[index].isSelected = !popularLocations.value[index].isSelected;
};

// 获取地点类型颜色
const getLocationTypeColor = (type) => {
  if (type === '景点') {
    return 'color: #54BCBD;';
  } else if (type === '吃喝') {
    return 'color: #E99D42;';
  }
  return 'color: #000;';
};
</script>

<style scoped>
/* 页面整体布局 */
.container {
  background-color: rgba(180, 253, 255, 0.20); /* 设置背景色的透明度为15% */
  padding: 40rpx;
  display: flex;
  flex-direction: column;
  justify-content: flex-start; /* 保持顶部内容固定 */
  height: 100vh;
  position: relative;
  overflow: hidden;
}

/* 关闭按钮 */
.close-icon-container {
  position: absolute;
  top: 20rpx;
  left: 20rpx;
  z-index: 100;
}

.close-icon {
  width: 40rpx;
  height: 40rpx;
  cursor: pointer;
}

/* 标题：这趟旅行要去哪里？ */
.title-container {
  margin-top: 80rpx; /* 调整顶部间距 */
  display: flex;
  font-family: 'TaipeiSansTCBeta';
}

.title-text {
  font-size: 54rpx;
  font-weight: bold;
  color: #000;
}

/* 旅行目的地显示 */
.location-container {
  margin-top: 30rpx;
  display: flex;
  margin-left: 20rpx;
}
.location-circle {
  display: inline-flex; /* 使容器宽度自适应内容 */
  align-items: center;
  justify-content: center;
  padding: 0 20rpx; /* 给内容左右增加额外的空间，使宽度稍微大于内容 */
  height: 75rpx;
  border-radius: 35rpx;
  border: 1px solid rgba(128, 128, 128, 0.5);
  background-color: white;
}

.location-text {
  font-size: 36rpx;
  color: #000;
  font-weight: 550;
}

/* 标题：你希望这趟旅行？ */
.travel-preference-title-container {
  margin-top: 40rpx;
  display: flex;
  justify-content: flex-start; /* 左对齐 */
  font-family: 'TaipeiSansTCBeta';
}

.travel-preference-title {
  font-size: 54rpx;
  font-weight: bold;
  color: #000;
}

/* 旅行关键词块 */
.keywords-container {
  margin-top: 40rpx;
  display: flex;
  flex-wrap: wrap;
  gap: 20rpx;
  margin-left: 20rpx;
}

.keyword-item {
  display: inline-flex; /* 使容器宽度自适应内容 */
  align-items: center;
  justify-content: center;
  padding: 0 20rpx; /* 给内容左右增加额外的空间，使宽度稍微大于内容 */
  height: 75rpx;
  border-radius: 35rpx;
  border: 1px solid rgba(128, 128, 128, 0.5);
  background-color: #fff;
  cursor: pointer;
  transition: all 0.3s ease;
}

.keyword-item.selected {
  background-color: #000;
  color: #fff;
  font-weight: bold;
}

.keyword-text {
  font-size: 32rpx;
  color: #000;
  font-weight: 500;
}

.keyword-item.selected .keyword-text {
  color: #fff;
}

/* 开始规划按钮 */
.start-planning-container {
  position: fixed;
  bottom: 55rpx;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: center;
}

.start-planning-button {
  height: 105rpx;
  border-radius: 30rpx;
  border: 2px solid #05AD8E;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  box-shadow: 0 5rpx 7rpx rgba(0, 0, 0, 0.25); /* 添加阴影效果 */
}

.magic-wand-icon {
  margin-left: 22rpx;
  width: 75rpx;
  height: 75rpx;
  margin-right: 10rpx; /* 给魔法棒图标和文本之间添加间距 */
}

.start-planning-text {
  color: #05AD8E;
  font-size: 50rpx;
  font-weight: bold;
  letter-spacing: 1rpx; /* 设定字间距 */
}

/* 加载自定义字体 */
@font-face {
  font-family: 'TaipeiSansTCBeta';
  src: url('font/TaipeiSansTCBeta-Regular.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

body {
  font-family: sans-serif; /* 默认字体 */
}

/* 标题：这些地点不容错过！ */
.must-visit-title-container {
  margin-top: 40rpx;
  display: flex;
  justify-content: flex-start;
  font-family: 'TaipeiSansTCBeta';
}

.must-visit-title {
  font-size: 54rpx;
  font-weight: bold;
  color: #000;
}

/* 热门景点列表 */
.locations-container {
  margin-top: 30rpx;
  max-height: 550rpx;
  overflow-y: scroll;
  padding-right: 20rpx;
}

.location-item {
  display: flex;
  align-items: center;
  padding: 20rpx;
  border-radius: 20rpx;
  box-shadow: 0 5rpx 15rpx rgba(0, 0, 0, 0.01);
}

.location-thumbnail {
  width: 120rpx;
  height: 120rpx;
  border-radius: 20rpx;
  overflow: hidden;
  margin-right: 20rpx;
}

.thumbnail {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.location-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.location-name {
  font-size: 36rpx;
  color: #000;
  margin-bottom: 10rpx;
}

.location-details {
  display: flex;
  align-items: center;
}

.location-type {
  font-size: 28rpx;
  font-weight: bold;
  margin-right: 10rpx;
}

.location-recommendation {
  font-size: 28rpx;
  color: #666;
  margin-left: 8rpx;
}

.select-icon-container {
  width: 60rpx;
  height: 60rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.select-icon {
  width: 100%;
  height: 100%;
}
</style>
