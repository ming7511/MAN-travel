<template>
  <view class="travel-plan-overview-page">
	  
	<!-- 返回按钮容器 -->
	    <view class="back-button-container">
	      <image src="/static/icons/back-icon.png" class="back-button" @click="goBack" />
	    </view>
	
    <!-- 行程名 -->
    <view class="trip-name">{{ tripTitle }}</view>
    <!-- 旅行时间 -->
    <view class="travel-time">{{ travelDateRange }}  {{ tripDuration }}</view>
    <!-- 行程标题及横线 -->
    <view class="trip-section">
      <view class="button-group">
        <!-- 行程按钮 -->
        <button class="btn-title" @click="handleShowOverview">行程</button>
        <!-- 旅行账单按钮 -->
        <button class="btn-title active">旅行账单</button>
        <!-- 行李清单按钮 -->
        <button class="btn-title" @click="handleXingliClick">行李清单</button>
      </view>
      <view class="horizontal-line"></view>
    </view>

    <!-- 白色矩形区域 -->
    <view class="white-rectangle">
      <!-- 账单标题 -->
      <view class="overview-title">旅行账单</view>

      <!-- 设置预算按钮 -->
      <view class="settings-button" @click="showBudgetInputOverlay">
        <text class="settings-text">设置预算</text>
      </view>

      <!-- 账单明细区域 -->
      <view class="bill">
        <view class="bill-item food left">
          <text class="label">🍽️ 美食 ¥288</text>
        </view>
        <view class="bill-item stay right">
          <text class="label">🏠 住宿 ¥988</text>
        </view>
        <view class="bill-item transport left">
          <text class="label">🚌 交通 ¥1888</text>
        </view>
      </view>
	  
	  <!-- 底部 Logo 和介绍 -->
	  <view class="footer">
	    <view class="footer-logo"></view>
	    <text class="footer-text">旅行账单 轻松记录</text>
	  </view>
	  
      <!-- 记一笔按钮 -->
      <button class="record-button" @click="goToAddBill">记一笔</button>
    </view>

    <!-- 设置预算的数字键盘输入框 -->
    <view class="budget-input-overlay" v-if="showBudgetInput">
      <view class="budget-input-container">
        <text class="budget-input-title">设置预算</text>
        <text class="budget-display">¥ {{ budget }}</text>
        <view class="number-keyboard">
          <view v-for="key in keys" :key="key" class="key" @click="handleKeyClick(key)">
            {{ key }}
          </view>
        </view>
        <button class="confirm-button" @click="confirmBudget">完成</button>
      </view>
    </view>
  </view>
</template>

<script>
import { useRoute, useRouter } from 'vue-router';

export default {
  data() {
    return {
      tripTitle: '',
      travelDateRange: '',
      tripDuration: '',
      showBudgetInput: false,
      budget: '', // 预算输入值
      keys: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'C', '←'] // 数字键盘按键
    };
  },
  mounted() {
    const route = useRoute();
    const tripId = route.query.id; // 获取当前路由中的行程ID

    // 获取 tripTitle, travelDateRange, tripDuration 信息
    const tripsById = {
      1: {
        title: '【示例】福州三日游 | 在三坊七巷感受榕城秋日古韵',
        dateRange: '11.01至11.03',
        duration: '3天2晚'
      },
      2: {
        title: '【示例】泉州三日游 | 螃蟹游记',
        dateRange: '12.01至12.03',
        duration: '3天2晚'
      }
    };

    const trip = tripsById[tripId];
    if (trip) {
      this.tripTitle = trip.title;
      this.travelDateRange = trip.dateRange;
      this.tripDuration = trip.duration;
    }
  },
  methods: {
	goBack() {
	        // 返回到首页 index.vue
	        uni.navigateTo({
	          url: '/pages/index/index'
	        });
	      },
    handleShowOverview() {
      const tripId = this.$route.query.id;
      if (tripId) {
        this.$router.push({
          path: `/pages/Overview/Overview`,
          query: { id: tripId }
        });
      }
    },
    handleXingliClick() {
      const tripId = this.$route.query.id;
      if (tripId) {
        this.$router.push({
          path: `/pages/xingli/xingli`,
          query: { id: tripId }
        });
      }
    },
    goToAddBill() {
      const tripId = this.$route.query.id;
      if (tripId) {
        this.$router.push({
          path: `/pages/addBill/addBill`,
          query: { id: tripId }
        });
      }
    },
    showBudgetInputOverlay() {
      this.showBudgetInput = true;
    },
    handleKeyClick(key) {
      if (key === 'C') {
        this.budget = ''; // 清空输入
      } else if (key === '←') {
        this.budget = this.budget.slice(0, -1); // 删除最后一个字符
      } else {
        this.budget += key; // 添加数字
      }
    },
    confirmBudget() {
      this.showBudgetInput = false;
      console.log('预算设置为:', this.budget);
    }
  }
};
</script>

<style scoped>
/* 页面整体样式 */
.travel-plan-overview-page {
  background-color: #e1f0ff;
  padding: 20px;
}

/* 返回按钮容器样式 */
.back-button-container {
  margin-bottom: 10px;
}

/* 返回按钮图标样式 */
.back-button {
  width: 30px;
  height: 30px;
  cursor: pointer;
}

/* 行程名样式 */
.trip-name {
  font-size: 24px;
  font-weight: bold;
  text-align: left;
  margin-bottom: 10px;
}

/* 旅行时间样式 */
.travel-time {
  font-size: 16px;
  color: dimgray;
  text-align: left;
  margin-bottom: 10px;
}

/* 行程标题及按钮样式 */
.trip-section {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-align: left;
}

.button-group {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 40rpx;
  margin-left: 15rpx;
}

.btn-title {
  font-size: 20px;
  font-weight: bold;
  color: black;
  background: none;
  border: none;
  outline: none;
  padding: 0;
  cursor: pointer;
  text-decoration: none;
  transition: color 0.3s ease;
}

.btn-title.active {
  color: #4c8cf5;
  border-bottom: 3rpx solid #4c8cf5;
}

.btn-title:hover {
  color: gray;
}

/* 横线样式 */
.horizontal-line {
  width: 100%;
  height: 1px;
  background-color: gray;
  margin-top: 10px;
}

/* 白色矩形区域样式 */
.white-rectangle {
  background-color: white;
  border-radius: 20px;
  padding: 20px;
  margin-bottom: 20px;
}

/* 账单标题样式 */
.overview-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
}

/* 设置预算按钮样式 */
.settings-button {
  font-size: 24rpx;
  color: #4c8cf5;
  display: flex;
  align-items: center;
  margin-bottom: 20rpx;
}

.settings-text {
  margin-left: 5rpx;
}

/* 底部 Logo 和介绍 */
.footer {
  text-align: center;
  margin-bottom: 20rpx;
}

.footer-logo {
  width:  400rpx;
  height: 400rpx;
  background: url('/static/logo.png') no-repeat center;
  background-size: cover;
  margin: 0 auto 10rpx;
}

.footer-text {
  font-size: 26rpx;
  color: #888;
  margin-bottom: 20rpx;
}

/* 账单明细样式 */
.bill {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
  margin-bottom: 20rpx;
}

/* 气泡框样式 */
.bill-item {
  padding: 15rpx 30rpx;
  border-radius: 20rpx;
  font-size: 40rpx;
  font-weight: bold;
  color: #333;
  width: 60%;
  position: relative;
  box-shadow: 0 4rpx 8rpx rgba(0, 0, 0, 0.1);
  margin-bottom: 40rpx;
}

/* 不同颜色的背景 */
.food {
  background-color: #ffe6e6;
}

.stay {
  background-color: #fff5cc;
}

.transport {
  background-color: #e6ffe6;
}

/* 左右错落布局 */
.left {
  align-self: flex-start;
}

.right {
  align-self: flex-end;
}

/* 记一笔按钮样式 */
.record-button {
  font-size: 28rpx;
  background-color: #4c8cf5;
  color: #fff;
  padding: 12rpx 30rpx;
  border-radius: 24rpx;
  text-align: center;
  width: 50%;
  margin: 0 auto;
  display: block;
}

/* 设置预算输入框样式 */
.budget-input-overlay {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20rpx;
}

.budget-input-container {
  width: 90%;
  background-color: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  text-align: center;
}

.budget-input-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.budget-display {
  font-size: 36rpx;
  color: #4c8cf5;
  margin-bottom: 20rpx;
}

.number-keyboard {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 10rpx;
  margin-bottom: 20rpx;
}

.key {
  width: 30%;
  padding: 15rpx 0;
  background-color: #f0f0f0;
  font-size: 28rpx;
  color: #333;
  border-radius: 10rpx;
  text-align: center;
}

.confirm-button {
  width: 100%;
  padding: 15rpx;
  font-size: 28rpx;
  background-color: #4c8cf5;
  color: #fff;
  border-radius: 15rpx;
}
</style>
