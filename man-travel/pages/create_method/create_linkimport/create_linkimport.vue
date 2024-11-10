<template>
  <view class="container" @click="handleClose">
    <!-- 输入框区域 -->
    <view
      class="input-box"
      @click.stop
      @touchstart="handleTouchStart"
      @touchmove="handleTouchMove"
      @touchend="handleTouchEnd"
    >
      <!-- 灰色横线 -->
      <view class="line"></view>
      
      <!-- 输入框 -->
      <view class="input-container">
        <textarea
          class="input"
          placeholder="粘贴小红书等笔记链接即可导入地点或行程。"
          v-model="inputText"
          maxlength="500"
        />
      </view>
      
      <!-- 确认按钮 -->
      <view class="confirm-box" @click="handleConfirm">
        <image src="/static/icons/link_white.png" class="icon" mode="aspectFit"></image>
        <text class="confirm-text">粘贴并识别</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue';

const inputText = ref('');
const startY = ref(0);
const isSliding = ref(false);

// 触摸事件处理
const handleTouchStart = (e) => {
  startY.value = e.touches[0].clientY;
  isSliding.value = false;
};

const handleTouchMove = (e) => {
  const moveY = e.touches[0].clientY;
  const deltaY = moveY - startY.value;

  // 如果下滑超过50px，设置滑动状态为true
  if (deltaY > 50) {
    isSliding.value = true;
  }
};

const handleTouchEnd = () => {
  if (isSliding.value) {
    closeInputBox();
  }
};

// 关闭输入框动画
const closeInputBox = () => {
  const inputBox = document.querySelector('.input-box');
  if (inputBox) {
    inputBox.style.animation = 'slideDown 0.4s ease-out forwards';
    setTimeout(() => {
      uni.navigateTo({
        url: '/pages/create_method/create_method' // 修改为正确的跳转路径
      });
    }, 400);
  }
};

// 确认按钮点击事件
const handleConfirm = () => {
  const link = inputText.value.trim();

  // 检查输入是否为空
  if (link === '') {
    uni.showToast({
      title: '请输入有效链接',
      icon: 'none',
    });
    return;
  }

  // 直接跳转到 import 页面进行用例测试
  uni.navigateTo({
    url: '/pages/create_method/import/import'  // 修改为正确的跳转路径
  });
};

// 关闭当前页面
const handleClose = () => {
  closeInputBox();
};
</script>

<style scoped>
/* 页面容器 */
.container {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: flex-end;
  align-items: flex-end;
  background-color: rgba(0, 0, 0, 0.3); /* 半透明蒙版 */
}

/* 输入框容器 */
.input-box {
  width: 95%;
  height: 40%;
  background-color: #ffffff;
  border-radius: 33px 33px 0 0;
  padding: 20rpx;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  box-shadow: 0 -4px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  animation: slideUp 0.4s ease-out;
}

/* 滑入动画 */
@keyframes slideUp {
  from {
    transform: translateY(100%);
  }
  to {
    transform: translateY(0);
  }
}

/* 滑出动画 */
@keyframes slideDown {
  from {
    transform: translateY(0);
  }
  to {
    transform: translateY(100%);
  }
}

/* 灰色横线 */
.line {
  width: 60px;
  height: 6px;
  background-color: #888888;
  margin: 10rpx auto;
  border-radius: 3px;
  cursor: pointer;
}

/* 输入框容器 */
.input-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  margin-top: 50rpx;  /* 缩小 margin-top 值，让输入框更靠上 */
  flex-grow: 1;  /* 使得容器可以占据剩余空间 */
}

/* 多行输入框样式 */
.input {
  width: 90%;
  height: 300rpx;  /* 增加高度以支持多行输入 */
  padding: 10rpx 20rpx;
  font-size: 28rpx;
  border: 1px solid #fff;
  border-radius: 10px;
  text-align: left; /* 左对齐 */
  vertical-align: top;  /* 顶部对齐 */
  line-height: 40rpx; /* 行高设置，以确保多行文本行距适中 */
  resize: none; /* 禁止用户改变大小 */
}

/* 确认按钮 */
.confirm-box {
  position: absolute;
  bottom: 15rpx;
  right: 30rpx;
  width: 250rpx;
  height: 80rpx;
  background-color: #000;
  border-radius: 33px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 20rpx auto;
}

.icon {
  width: 65rpx;
  height: 65rpx;
  margin-left: -10rpx;
  color: #fff;
}

.confirm-text {
  font-size: 30rpx;
  font-weight: bold;
  color: #fff;
}
</style>
