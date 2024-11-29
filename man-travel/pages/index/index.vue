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
      <div 
        class="trip-card" 
        v-for="trip in upcomingTrips" 
        :key="trip.trip_id" 
        :style="{ backgroundColor: trip.bgColor }" 
        @click="goToOverview(trip)"
      >
        <div class="trip-title">{{ trip.title }}</div>
        <div class="trip-dates">{{ trip.dateRange }}</div>
        <div class="trip-duration">{{ trip.duration }} 天</div>
      </div>
    </div>

    <!-- 已结束部分 -->
    <div class="section">
      <div class="section-title">已结束</div>
      <div 
        class="trip-card" 
        v-for="trip in pastTrips" 
        :key="trip.trip_id" 
        :style="{ backgroundColor: trip.bgColor }" 
        @click="goToOverview(trip)"
      >
        <div class="trip-title">{{ trip.title }}</div>
        <div class="trip-dates">{{ trip.dateRange }}</div>
        <div class="trip-duration">{{ trip.duration }} 天</div>
      </div>
    </div>

    <!-- 底部导航栏 -->
    <BottomNav />
  </div>
</template>

<script setup>
import BottomNav from '/BottomNav.vue';
import { ref, onMounted } from 'vue';
import axios from 'axios';

// 待出发行程数据
const upcomingTrips = ref([]);

// 已结束行程数据
const pastTrips = ref([]);

// 生成浅色背景颜色的函数
const getLightColor = () => {
  const r = Math.floor(Math.random() * 128 + 127); // R值在127到255之间
  const g = Math.floor(Math.random() * 128 + 127); // G值在127到255之间
  const b = Math.floor(Math.random() * 128 + 127); // B值在127到255之间
  return `rgb(${r}, ${g}, ${b})`;
};

// 获取所有 trip_id
const getTripIds = async () => {
  try {
    const token = uni.getStorageSync('access_token');  // 从本地存储获取token
    const response = await axios.get('https://734dw56037em.vicp.fun/api/trip/tripuser', {
      headers: {
        Authorization: `Bearer ${token}`,  // 使用Bearer类型的token
        'Content-Type': 'application/json'
      }
    });
    if (response.data && response.data.trips) {
      return response.data.trips.map(trip => trip.trip_id);  // 返回所有的trip_id
    }
    console.error('获取trip_id失败', response.data);
    return [];
  } catch (error) {
    console.error('请求trip_id失败', error);
    return [];
  }
};

// 获取行程活动数据
const getTripActivities = async (trip_id) => {
  try {
    const response = await axios.get('https://734dw56037em.vicp.fun/api/trip/get_trip_activities/', {
      params: { trip_information_id: trip_id }
    });

    if (response.data && response.data.trip) {
      return response.data.trip[0];  // 返回第一个trip对象
    } else {
      console.error('获取行程活动失败', response.data);
      return null;
    }
  } catch (error) {
    console.error('请求行程活动数据失败', error);
    return null;
  }
};

// 获取所有行程并分类
const fetchTrips = async () => {
  const tripIds = await getTripIds();  // 动态获取trip_id
  const updatedTrips = await Promise.all(
    tripIds.map(async (trip_id) => {
      const tripInfo = await getTripActivities(trip_id);  // 获取行程的基本信息
      if (tripInfo) {
        const startDate = new Date(tripInfo.start_date);  // 获取行程的起始日期
        const endDate = new Date(tripInfo.end_date);  // 获取行程的结束日期
        const duration = Math.ceil((endDate - startDate) / (1000 * 3600 * 24));  // 计算行程天数

        // 构造行程数据，包含浅色背景颜色
        return {
          trip_id: tripInfo.trip_id,
          title: tripInfo.trip_name,  // 行程名称
          start_date: tripInfo.start_date,
          end_date: tripInfo.end_date,
          dateRange: `${tripInfo.start_date} 至 ${tripInfo.end_date}`,  // 日期范围
          duration,  // 持续天数
          bgColor: getLightColor()  // 生成浅色背景颜色
        };
      }
      return null;
    })
  );

  // 对行程进行日期分类
  const today = new Date();
  updatedTrips.forEach((trip) => {
    if (trip) {
      const startDate = new Date(trip.start_date);  // 获取行程的起始日期
      const endDate = new Date(trip.end_date);  // 获取行程的结束日期

      // 将行程根据日期分类
      if (endDate < today) {
        pastTrips.value.push(trip);  // 已结束的行程
      } else if (startDate > today) {
        upcomingTrips.value.push(trip);  // 待出发的行程
      }
    }
  });
};

// 页面加载时获取行程数据
onMounted(() => {
  fetchTrips();
});

// 跳转到行程详情页
const goToOverview = (trip) => {
  const token = uni.getStorageSync('access_token');
  console.log('Access Token:', token);

  if (trip.trip_id) {
    uni.navigateTo({
      url: `/pages/Overview/Overview?trip_id=${trip.trip_id}`
    });
  } else {
    console.error('行程中缺少 trip_id');
    uni.showToast({ title: '行程数据错误', icon: 'none' });
  }
};
</script>

<style scoped>
.home-page {
  padding: 20px;
  padding-top: 40px;
  padding-bottom: 80px;
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
