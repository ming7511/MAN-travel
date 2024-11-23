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

const goToNextPage = () => {
  if (locationInput.value.trim() !== '') {
    const city = locationInput.value.trim();

    console.log('这是ai城市');

    // 从本地存储中获取 access_token
    const token = uni.getStorageSync('access_token'); // 确保获取的是 access_token

    // 打印 token 到控制台
    console.log('Access Token:', token); // 使用 access_token 打印

    if (!token) {
      uni.showToast({
        title: '请先登录',
        icon: 'none'
      });
      return;
    }

    // 存储用户输入的城市
    uni.setStorageSync('selectedCity', city);

    // 在发起请求之前先跳转到下一个页面
    uni.navigateTo({
      url: `/pages/create_method/ai_create/ai_create_time`, // 不需要传递数据
    });

    // 构建 GET 请求的 URL，传递城市参数
    const url = `https://734dw56037em.vicp.fun/api/trip/RecommendHotSpots/?city=${encodeURIComponent(city)}`;

    // 发送GET请求，将城市数据上传到服务器
    uni.request({
      url: url, // 将城市参数直接附加到 URL 中
      method: 'GET',
      header: {
        'Content-Type': 'application/json', // 请求头
        'Authorization': `Bearer ${token}`, // 将 token 放入 Authorization 头中
      },
      success: (res) => {
        console.log('服务器返回的数据:', res); // 打印完整的返回内容

        if (res.statusCode === 200) {
          // 假设返回的数据是一个数组，包含景点信息
          const popularLocationsData = res.data; // 获取热门景点数据

          // 将返回的热门景点数据存储到缓存中
          uni.setStorageSync('popularLocations', JSON.stringify(popularLocationsData));
        } else {
          // 如果服务器响应状态不是200，可以在这里处理错误
          uni.showToast({
            title: '城市上传失败，请稍后再试',
            icon: 'none'
          });
        }
      },
      fail: (err) => {
        // 请求失败处理
        uni.showToast({
          title: '网络请求失败，请检查网络连接',
          icon: 'none'
        });
      }
    });
  } else {
    // 提示用户输入城市
    uni.showToast({
      title: '请输入城市',
      icon: 'none'
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
