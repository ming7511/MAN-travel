<template>
  <div class="profile-page">
    <!-- 顶部个人信息 -->
    <div class="profile-header">
      <image class="avatar" src="/static/logo.png" alt="avatar" />
      <div class="username">一个真正的man</div>
      <!-- 右上角编辑按钮，改为灰色字体的可点击文本 -->
      <div class="edit-link" @click="goToEditPage">编辑</div>
    </div>

    <!-- 旅行数据统计 -->
    <div class="travel-stats">
      <div class="stat-item">
        <div class="stat-value">211</div>
        <div class="stat-label">旅行次数</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">19</div>
        <div class="stat-label">旅行天数</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">630km</div>
        <div class="stat-label">总里程</div>
      </div>
    </div>

    <!-- 功能选项 -->
    <div class="options-list">
      <div class="option-item" @click="goToFeedback">
        <i class="icon feedback-icon">💬</i>
        <span>建议反馈</span>
        <span class="arrow-symbol">></span>
      </div>
      <div class="option-item" @click="goToAboutUs">
        <i class="icon about-icon">ℹ️</i>
        <span>关于我们</span>
        <span class="arrow-symbol">></span>
      </div>
    </div>
  </div>
</template>

<script setup>
// 跳转到编辑页面
const goToEditPage = () => {
  uni.navigateTo({
    url: '/pages/edit-profile/edit-profile' // 指定目标页面的路径
  });
};

// 跳转到建议反馈页面
const goToFeedback = () => {
  uni.navigateTo({
    url: '/pages/suggestion/suggestion'
  });
};

// 跳转到关于我们页面
const goToAboutUs = () => {
  uni.navigateTo({
    url: '/pages/about-us/about-us'
  });
};
</script>

<style scoped>
.profile-page {
  padding: 20px;
  background-color: #f8f8f8;
  height: 100vh;
}

.profile-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
  position: relative;
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background-color: #f0f0f0;
}

.username {
  margin-top: 10px;
  font-size: 18px;
  font-weight: bold;
}

.edit-link {
  position: absolute;
  top: 10px;
  right: 20px;
  font-size: 14px;
  color: #808080; /* 灰色字体 */
  cursor: pointer;
  text-decoration: underline; /* 可选：增加下划线以表明可点击 */
}

.travel-stats {
  display: flex;
  justify-content: space-around;
  background-color: #ffffff;
  padding: 15px;
  border-radius: 10px;
  margin-bottom: 20px;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 20px;
  font-weight: bold;
}

.stat-label {
  color: #666;
  font-size: 14px;
}

.options-list {
  background-color: #ffffff;
  border-radius: 10px;
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

.icon {
  font-size: 20px;
  color: #999;
}

.arrow-symbol {
  font-size: 20px;
  color: #999;
  margin-left: 10px;
}

.feedback-icon,
.about-icon {
  margin-right: 10px;
}
</style>
