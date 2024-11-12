<template>
  <div class="intro-page">
    <!-- 顶部返回按钮 -->


    <!-- 应用名称和介绍信息 -->
    <div class="intro-content">
      <div class="app-name">Man游</div>
      <div class="app-description">
        Man游在旅游规划与行程管理的生态系统中，是一个重要的信息处理中枢。它不仅能够接收用户输入的旅游相关推文或链接，还能够智能地解析这些信息，并自动生成详细的旅游计划。这种自动化处理能力极大地提高了用户的旅游规划效率，使用户能够更加轻松、快捷地规划出符合自己需求的旅游行程。
      </div>
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
</script>

<style scoped>
.intro-page {
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

.intro-content {
  margin-top: 20px;
  text-align: center;
}

.app-name {
  font-size: 28px;
  font-weight: bold;
  color: #444;
  margin-bottom: 20px;
}

.app-description {
  font-size: 16px;
  color: #666;
  line-height: 1.5;
  padding: 0 20px;
}
</style>
