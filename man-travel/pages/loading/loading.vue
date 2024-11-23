<template>
  <view class="loading-container">
    <image class="logo" src="/static/logo.png" alt="Logo" />
    <text class="text-line">人生路漫漫</text>
    <text class="text-line">man游常相伴~</text>
  </view>
</template>

<script setup>
// 页面逻辑
</script>

<style scoped>
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  height: 100vh;
  text-align: center;
}

.logo {
  width: 180px; /* 根据需要调整logo的大小 */
  height: 180px;
  animation: shake 1s ease-in-out infinite; /* logo抖动动画 */
  margin-bottom: 20px; /* 调整logo与文字的间距 */
  margin-top: -100px; /* 调整logo向上移动的距离 */
}


.text-line {
  font-size: 28px;
  font-weight: bold;
  color: #333;
  margin: 15px 0;
  font-family: 'TaipeiSansTCBeta', sans-serif; /* 只在标题中使用特殊字体 */
}

/* 来回抖动的动画 */
@keyframes shake {
  0% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-10px);
  }
  50% {
    transform: translateX(10px);
  }
  75% {
    transform: translateX(-10px);
  }
  100% {
    transform: translateX(0);
  }
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
