<template>
  <div class="about-page">
    <!-- 顶部返回按钮 -->
    <div class="header">
      <div class="back-button" @click="goBack">＜ 返回</div>
    </div>

    <!-- 应用信息 -->
    <div class="app-info">
      <image src="/static/logo.png" alt="Bottom Logo" class="logo-image" />
      <div class="app-name">Man游</div>
      <div class="app-version">Version 1.0.0</div>
    </div>

    <!-- 功能选项列表 -->
    <div class="options-list">
      <div class="option-item" @click="goToFunctionIntroduction">
        <span>功能介绍</span>
        <span class="arrow-symbol">></span>
      </div>
      <div class="option-item" @click="goToSuggestion">
        <span>投诉</span>
        <span class="arrow-symbol">></span>
      </div>
      <div class="option-item" @click="checkForUpdate">
        <span>检查新版本</span>
        <span class="arrow-symbol">></span>
      </div>
    </div>

    <!-- 版权信息 -->
    <div class="footer">
      <div>iman团队 版权所有</div>
      <div>All Rights Reserved</div>
    </div>
  </div>
</template>

<script setup>
// 跳转到上一个页面
const goBack = () => {
  uni.navigateBack({
    delta: 1
  });
};

// 跳转到功能介绍页面
const goToFunctionIntroduction = () => {
  uni.navigateTo({
    url: '/pages/function-introduction/function-introduction'
  });
};

// 跳转到投诉页面，直接跳转到 suggestion 页
const goToSuggestion = () => {
  uni.navigateTo({
    url: '/pages/suggestion/suggestion' // 更新跳转路径到 suggestion 页面
  });
};

// 检查新版本
const checkForUpdate = () => {
  uni.showToast({
    title: '当前已是最新版本',
    icon: 'none'
  });
};
</script>

<style scoped>
.about-page {
  padding: 20px;
  background-color: #f8f8f8;
  min-height: 100vh;
}

.header {
  display: flex;
  align-items: center;
  padding: 10px 0;
}

.back-button {
  font-size: 16px;
  cursor: pointer;
  color: #333;
}

.app-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
}

.logo-image {
  width: 100px;
  height: 100px;
  margin-bottom: 10px;
}

.app-name {
  font-size: 24px;
  font-weight: bold;
  color: #444;
  margin-bottom: 5px;
}

.app-version {
  font-size: 14px;
  color: #888;
}

.options-list {
  background-color: #ffffff;
  margin-top: 20px;
  border-radius: 10px;
  overflow: hidden;
}

.option-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px 20px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
}

.option-item:last-child {
  border-bottom: none;
}

.arrow-symbol {
  font-size: 20px;
  color: #999;
}

.footer {
  text-align: center;
  margin-top: 50px;
  color: #aaa;
  font-size: 12px;
}
</style>
