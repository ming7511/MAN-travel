<template>
  <div class="bottom-nav">
    <!-- 行程计划 -->
    <div class="nav-item" @click="navigateTo('plans')">
      <i class="icon">📋</i>
      <span>行程计划</span>
    </div>
    
    <!-- 添加行程 -->
    <div class="nav-item add-trip" @click="addNewTrip">
      <span class="add-icon">+</span>
    </div>
    
    <!-- 我的 -->
    <div class="nav-item" @click="navigateTo('profile')">
      <i class="icon">👤</i>
      <span>我的</span>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// 导航到指定页面
const navigateTo = (page) => {
  if (page === 'plans') {
    uni.redirectTo({
      url: '/pages/index/index'
    });
  } else if (page === 'profile') {
    uni.redirectTo({
      url: '/pages/user/user'
    });
  }
};

// 添加新行程
const addNewTrip = () => {
  uni.redirectTo({
    url: '/pages/create_method/create_method'
  });
};
</script>

<style scoped>
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 70px; /* 增加高度以更显著地显示中间的按钮 */
  display: flex;
  justify-content: space-around;
  align-items: center;
  background-color: #ffffff;
  box-shadow: 0 -1px 5px rgba(0, 0, 0, 0.1);
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #999;
  cursor: pointer;
  font-size: 12px;
}

.icon {
  font-size: 24px;
}

.add-trip {
  width: 80px;
  height: 80px;
  background-color: #333; /* 中央按钮的背景色为深色 */
  color: #ffffff;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  margin-top: -30px; /* 使按钮浮出部分高度，增强视觉效果 */
  cursor: pointer;
}

.add-icon {
  color: #ffffff; /* 确保添加图标的颜色为白色，以便和深色背景对比明显 */
  font-size: 60px; /* 更大的字体使加号更显眼和规整 */
  line-height: 1; /* 确保加号在按钮中完全居中 */
  font-weight: bold; /* 使用较粗的字体以使加号更加显眼 */
}
</style>
