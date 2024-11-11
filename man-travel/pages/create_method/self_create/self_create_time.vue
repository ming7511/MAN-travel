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

    <!-- 新页面的标题：确定好日期了吗？ -->
    <view class="sub-title-container">
      <text class="sub-title-text">确定好日期了吗？</text>
    </view>

    <!-- 天数选择表格 -->
    <view class="table-container">
      <view class="table-header">
        <text class="table-header-text">天数</text>
        <text class="table-header-text">日期</text>
      </view>

      <view class="table-body">
        <view v-for="day in 30" :key="day" class="table-row">
          <text class="table-cell">{{ day }}</text>
          <input v-model="dates[day - 1]" class="table-cell-input" type="date" />
        </view>
      </view>
    </view>

    <!-- 开始规划按钮 -->
    <view class="start-planning-container">
      <view class="start-planning-button" @click="startPlanning">
        <text class="start-planning-text">开始规划！</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue';

// 从上一页传递过来的城市信息
const locationInput = ref(''); // 假设通过某种方式传递过来

// 存储每一天的日期选择
const dates = ref(Array(30).fill(''));

// 关闭页面方法
const closePage = () => {
  uni.navigateBack(); // 返回上一页或关闭页面
};

// 开始规划旅行
const startPlanning = () => {
  uni.navigateTo({
    url: '/pages/planPage/planPage' // 假设这是下一步的页面路径
  });
};

// 初始化地点信息，假设是从上一页传递过来的
onMounted(() => {
  locationInput.value = uni.getStorageSync('selectedCity') || '未选择城市'; // 这里从缓存或者其他地方取值
});
</script>

<style scoped>
/* 页面整体布局 */
.container {
  background-color: rgba(180, 253, 255, 0.20); /* 设置背景色的透明度为15% */
  padding: 40rpx;
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100vh;
  position: relative;
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
  margin-top: -600rpx; /* 控制标题与顶部的间距 */
  display: flex;
}

.title-text {
  font-size: 54rpx;
  font-weight: bold;
  color: #000;
}

/* 旅行目的地显示 */
.location-container {
  margin-top: 50rpx;
  display: flex;
  justify-content: center;
}

.location-circle {
  width: 120rpx;
  height: 120rpx;
  border-radius: 50%;
  border: 2px solid gray;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: white;
}

.location-text {
  font-size: 36rpx;
  color: #000;
}

/* 新页面的标题：确定好日期了吗？ */
.sub-title-container {
  margin-top: 80rpx;
  display: flex;
  justify-content: center;
}

.sub-title-text {
  font-size: 54rpx;
  font-weight: bold;
  color: #000;
}

/* 天数选择表格 */
.table-container {
  margin-top: 60rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.table-header {
  display: flex;
  justify-content: space-between;
  width: 100%;
  margin-bottom: 20rpx;
}

.table-header-text {
  font-size: 36rpx;
  font-weight: bold;
  color: #000;
  width: 50%;
  text-align: center;
}

.table-body {
  width: 100%;
}

.table-row {
  display: flex;
  justify-content: space-between;
  width: 100%;
  margin-bottom: 10rpx;
}

.table-cell, .table-cell-input {
  width: 48%;
  text-align: center;
  font-size: 32rpx;
}

.table-cell-input {
  border: 1px solid #ccc;
  padding: 5rpx;
  border-radius: 10rpx;
}

/* 开始规划按钮 */
.start-planning-container {
  margin-top: 100rpx;
  display: flex;
  justify-content: center;
}

.start-planning-button {
  width: 150rpx;
  height: 150rpx;
  border-radius: 50%;
  background-color: black;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}

.start-planning-text {
  color: white;
  font-size: 36rpx;
  font-weight: bold;
}

</style>
