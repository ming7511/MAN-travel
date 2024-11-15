<template>
  <view class="travel-plan-overview-page">
     <!-- 返回按钮 -->
         <view class="back-button-container">
           <image src="/static/icons/back-icon.png" class="back-button" @click="goBack" />
         </view>
     
         <!-- 行程名 -->
         <view class="header">
           <text class="trip-name">{{ tripTitle }}</text>
         </view>
    <!-- 旅行时间 -->
    <view class="travel-time">{{ travelDateRange }}  {{ tripDuration }}</view>
    <!-- 行程标题及横线 -->
    <view class="trip-section">
      <view class="button-group">
        <!-- 行程按钮 -->
        <button class="btn-title" @click="handleShowOverview">行程</button>
        <!-- 旅行账单按钮 -->
        <button class="btn-title" @click="goToBillPage">旅行账单</button>
        <!-- 行李清单按钮 -->
        <button class="btn-title active">行李清单</button>
      </view>
      <view class="horizontal-line"></view>
    </view>

    <!-- 白色矩形区域 -->
    <view class="white-rectangle packing-list">
      <!-- 标签列表 -->
      <view class="tags">
        <view class="tag-row">
          <view class="tag">耳机</view>
        </view>
        <view class="tag-row">
          <view class="tag">充电宝</view>
          <view class="tag">洗漱用品</view>
        </view>
        <view class="tag-row">
          <view class="tag">身份证</view>
        </view>
      </view>

      <!-- 插图 -->
      <image src="/static/logo.png" class="illustration" mode="widthFix" />

      <!-- 提示文字 -->
      <text class="reminder-text">出行前记得对照清单\n检查一下物品是否都带啦</text>

      <!-- 开始添加按钮，添加点击事件 -->
      <button class="add-button" @click="goToAddPage">开始添加</button>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      tripTitle: '【示例】福州三日游 | 在三坊七巷感受榕城秋日古韵',
      travelDateRange: '11.01至11.03',
      tripDuration: '3天2晚',
      tripId: '1', // 假设当前页面的行程ID为1
    };
  },
  methods: {
	  goBack() {
	        // 返回到首页 index.vue
	        uni.navigateTo({
	          url: '/pages/index/index'
	        });
	      },
    handleShowOverview() {
      // 跳转到行程页面
      uni.navigateTo({
        url: `/pages/Overview/Overview?id=${this.tripId}`
      });
    },
    goToBillPage() {
      // 跳转到旅行账单页面，传递行程 ID
      uni.navigateTo({
        url: `/pages/shouye/shouye?id=${this.tripId}` // 确保路径正确，传递行程ID参数
      });
    },
    goToAddPage() {
      // 跳转到添加行李的页面
      uni.navigateTo({
        url: `/pages/tianjia/tianjia?id=${this.tripId}` // 传递行程ID以便后续操作
      });
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
  margin-bottom: 10px; /* 设置与下方内容的间距 */
}

/* 返回按钮图标样式 */
.back-button {
  width: 30px;
  height: 30px;
  cursor: pointer;
}

/* 行程名样式 */
.header {
  margin-top: 10px; /* 设置与返回按钮的间距 */
  margin-bottom: 10px; /* 设置与下方内容的间距 */
}

.trip-name {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

/* 旅行时间样式 */
.travel-time {
  font-size: 16px;
  color: dimgray;
  text-align: left;
  margin-bottom: 10px;
}

/* 行程标题及横线 */
.trip-section {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-align: left;
}

.button-group {
  display: flex;
  gap: 20px;
}

.btn-title {
  font-size: 20px;
  font-weight: bold;
  color: black;
  background: none;
  border: none;
  outline: none;
  cursor: pointer;
}

.btn-title.active {
  color: #0066cc;
}

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
  margin-top: 20px;
}

/* 行李清单内容样式 */
.packing-list {
  text-align: center;
}

/* 标签样式 */
.tags {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.tag-row {
  display: flex;
  gap: 10px;
  justify-content: center;
}

/* 标签样式 */
.tag {
  background-color: #e0f7fa;
  color: #333;
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 20px;
  display: inline-flex;
  align-items: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  animation: fadeIn 0.5s ease-in-out;
}

/* 插图样式 */
.illustration {
  width: 120px;
  height: auto;
  margin-top: 20px;
}

/* 提示文字样式 */
.reminder-text {
  font-size: 14px;
  color: #333;
  margin-top: 10px;
  line-height: 1.5;
  white-space: pre-line;
  margin-bottom: 20px;
}

/* 添加按钮样式 */
.add-button {
  background-color: #4a90e2;
  color: white;
  padding: 10px 20px;
  border-radius: 20px;
  font-size: 16px;
  margin-top: 20px;
}

/* 标签动画 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
