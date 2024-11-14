<template>
  <div class="home-page">
    <!-- 顶部Logo和标题 -->
    <div class="header">
      <image src="/static/logo.png" alt="Man游 Logo" class="logo" />
      <span class="title">man游</span>
    </div>

    <!-- 待出发部分 -->
    <div class="section">
      <div class="section-title">待出发</div>
      <div class="trip-card" v-for="trip in upcomingTrips" :key="trip.id" :style="{ backgroundColor: trip.bgColor }" @click="goToOverview(trip)">
        <div class="trip-title">{{ trip.title }}</div>
        <div class="trip-dates">{{ trip.dateRange }}</div>
        <div class="trip-duration">{{ trip.duration }}</div>
      </div>
    </div>

    <!-- 已结束部分 -->
    <div class="section">
      <div class="section-title">已结束</div>
      <div class="trip-card" v-for="trip in pastTrips" :key="trip.id" :style="{ backgroundColor: trip.bgColor }" @click="goToOverview(trip)">
        <div class="trip-title">{{ trip.title }}</div>
        <div class="trip-dates">{{ trip.dateRange }}</div>
        <div class="trip-duration">{{ trip.duration }}</div>
      </div>
    </div>

    <!-- 底部导航栏 -->
    <BottomNav />
  </div>
</template>

<script setup>
import BottomNav from '/BottomNav.vue'; // 导入底部导航栏组件
import { ref } from 'vue';
import { useRouter } from 'vue-router'; // 导入 useRouter

// 生成随机颜色的函数
const generateRandomColor = () => {
  const letters = '89ABCDEF'; // 为了保证颜色更亮一些，使用 '8' 到 'F'
  let color = '#';
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * letters.length)];
  }
  return color;
};

// 待出发行程数据
const upcomingTrips = ref([
  {
    id: 1,
    title: '【示例】福州三日游 | 在三坊七巷感受榕城秋日古韵',
    dateRange: '11.01至11.03',
    duration: '3天2晚',
    bgColor: generateRandomColor(),
    places: [
      '烟台山公园', '崔酱炸鸡', '上下杭', '三坊七巷', '后街捞化',
      '鼓山', '福道', '达明美食街', '森林公园', '温泉公园', '间江夜游'
    ]
  },
  {
    id: 2,
    title: '【示例】泉州三日游 | 螃蟹游记',
    dateRange: '12.01至12.03',
    duration: '3天2晚',
    bgColor: generateRandomColor(),
    places: [] // 该行程没有具体地点
  }
]);

// 已结束行程数据
const pastTrips = ref([
  {
    id: 3,
    title: '【示例】武汉三日游 | 遍吃逛吃武汉',
    dateRange: '10.01至10.03',
    duration: '3天2晚',
    bgColor: generateRandomColor(),
    places: [] // 该行程没有具体地点
  }
]);

const goToOverview = (trip) => {
  // 传递行程的 id 到 Overview 页面
  uni.navigateTo({
    url: `/pages/Overview/Overview?id=${trip.id}`
  });
};
</script>

<style scoped>
.home-page {
  padding: 20px;
  padding-top: 40px; /* 给顶部预留空间 */
  padding-bottom: 80px; /* 预留空间给底部导航栏，防止内容被遮挡 */
  background-color: #f8f8f8;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.logo {
  width: 50px;
  height: 50px;
}

.title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-left: 10px;
}

.section {
  margin-bottom: 30px;
}

.section-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
  color: #333;
}

.trip-card {
  padding: 15px;
  border-radius: 10px;
  margin-bottom: 10px;
  color: #333;
}

.trip-title {
  font-size: 16px;
  font-weight: bold;
}

.trip-dates,
.trip-duration {
  font-size: 14px;
  color: #666;
}
</style>
