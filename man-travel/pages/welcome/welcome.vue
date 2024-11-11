<template>
  <view class="container">
    <!-- 中间 logo 图片 -->
    <view class="middle-logo">
      <image src="/static/logo.png" alt="Middle Logo" class="logo-image-large" />
    </view>
    <!-- 底部图片 -->
    <view class="bottom-image">
      <image src="/static/logo3.png" alt="Bottom Logo" class="logo-image" />
    </view>
  </view>
</template>
<script>
export default {
  name: "IndexPage",
  mounted() {
    // 页面挂载后执行延迟跳转
    setTimeout(() => {
      // 使用 uni.navigateTo 跳转到登录页面
      uni.navigateTo({
        url: '/pages/login/login'
      });
    }, 3000); // 延迟 3 秒
  }
};
</script>
<style scoped>
.container {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  height: 100vh;
  background-color: #fff;
}
.top-image,
.bottom-image {
  margin: 20px;
}
.middle-logo {
  flex-grow: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}
.logo-image {
  width: 180px; /* 根据需要调整大小 */
  height: 47px;
}
.logo-image-large {
  width: 150px; /* 根据需要调整大小 */
  height: 150px;
}
</style>
