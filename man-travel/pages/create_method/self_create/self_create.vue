<template>
  <view class="container">
    <!-- 关闭按钮 -->
    <view class="close-icon-container">
      <image src="/static/icons/close.png" class="close-icon" @click="closePage" />
    </view>

    <!-- 标题 -->
    <view class="title-container">
      <text class="title-text">这趟旅行要去哪里？</text>
    </view>

    <!-- 输入框 -->
    <view class="input-container">
      <input
        v-model="locationInput"
        class="input-box"
        placeholder="请输入"
        :placeholder-style="'color: #888; font-size: 36rpx;'"
      />
      <!-- 进入按钮（图标 >） -->
      <view class="enter-icon-container" @click="goToNextPage">
        <image src="/static/icons/enter-icon.png" class="enter-icon" />
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue';

const locationInput = ref(''); // 输入框的绑定数据

// 关闭页面方法
const closePage = () => {
  uni.navigateBack(); // 返回上一页或关闭页面
};

// 跳转到下一个页面
const goToNextPage = () => {
  if (locationInput.value.trim() !== '') {
    // 存储用户输入的城市
    uni.setStorageSync('selectedCity', locationInput.value);
    uni.navigateTo({
      url: '/pages/create_method/self_create/self_create_time' // 根据实际页面路径修改
    });
  }
};
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

/* 标题 */
.title-container {
  margin-top: -600rpx; /* 控制标题与顶部的间距 */
  display: flex;
}

.title-text {
  font-size: 54rpx;
  font-weight: bold;
  color: #000;
  font-family: 'TaipeiSansTCBeta', sans-serif; /* 只在标题中使用特殊字体 */
}

/* 输入框容器 */
.input-container {
  margin-top: 200rpx; /* 输入框与标题的间距 */
  display: flex;
  align-items: center;
  position: relative;
}

/* 输入框 */
.input-box {
  width: 100%;
  height: 100rpx;
  padding-left: 50rpx;
  font-size: 36rpx;
  background-color: #fff;
  border-radius: 50rpx;
  color: #000;
  font-family: sans-serif; /* 默认字体 */
}

/* 进入按钮图标（>） */
.enter-icon-container {
  position: absolute;
  right: 20rpx;
  cursor: pointer;
}

.enter-icon {
  width: 60rpx;
  height: 60rpx;
  margin-top: 10rpx;
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
</style>
