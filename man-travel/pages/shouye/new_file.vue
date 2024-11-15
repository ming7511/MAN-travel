<template>
  <view class="container">
    <!-- 顶部标题和日期 -->
    <view class="header">
      <text class="title">福州三日游 | 在三坊七巷感受榕城秋日古韵</text>
      <text class="date">10.1 - 10.3   3天2晚</text>
    </view> 

    <!-- 标签栏 -->
    <view class="tab-bar">
      <view class="tab">行程</view>
      <view class="tab active">旅行账单</view>
      <view class="tab" @click="goToXingli">行李清单</view>
      <view class="settings-button" @click="showBudgetInputOverlay">
        <text class="settings-text">设置预算</text>
      </view>
    </view>

    <!-- 账单明细 -->
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

    <!-- 底部 Logo 和按钮 -->
    <view class="footer">
      <view class="footer-logo"></view>
      <text class="footer-text">旅行账单 轻松记录</text>
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
export default {
  data() {
    return {
      showBudgetInput: false, // 控制预算输入框显示
      budget: '', // 存储当前预算输入值
      keys: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'C', '←'] // 数字键盘按键
    };
  },
  methods: {
    goToXingli() {
      uni.navigateTo({
        url: '/pages/xingli/xingli'
      });
    },
    goToAddBill() {
      uni.navigateTo({
        url: '/pages/addBill/addBill'
      });
    },
    // 显示预算输入弹窗
    showBudgetInputOverlay() {
      this.showBudgetInput = true;
    },
    // 处理数字键盘按键点击
    handleKeyClick(key) {
      if (key === 'C') {
        this.budget = ''; // 清空输入
      } else if (key === '←') {
        this.budget = this.budget.slice(0, -1); // 删除最后一个字符
      } else {
        this.budget += key; // 添加数字
      }
    },
    // 确认预算并关闭输入框
    confirmBudget() {
      this.showBudgetInput = false;
      console.log('预算设置为:', this.budget);
    }
  }
};
</script>
<style scoped>
/* 整体容器 */
.container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  box-sizing: border-box;
}
/* 顶部标题和日期 */
.header {
  background-color: #e1f0ff;
  padding: 60rpx; /* 增大 padding */
  border-radius: 10rpx;
  margin-bottom: 12rpx; /* 增加下方间距 */
}

.title {
  font-size: 52rpx; /* 增大字体 */
  font-weight: bold;
  color: #333;
}

.date {
  font-size: 40rpx; /* 调整日期字体以与标题相配 */
  color: #666;
display: block; 
  margin-top: 6rpx; /* 增加一点间距 */
}

/* 标签栏 */
.tab-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20rpx;
  padding-bottom: 10rpx;
  border-bottom: 1px solid #e0e0e0;
}

.tab {
  font-size: 28rpx;
  color: #888;
}

.tab.active {
  color: #4c8cf5;
  font-weight: bold;
  border-bottom: 3rpx solid #4c8cf5;
}

.settings-button {
  font-size: 24rpx;
  color: #4c8cf5;
  display: flex;
  align-items: center;
}

.settings-text {
  margin-left: 5rpx;
}

/* 账单明细 */
.bill {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

/* 气泡框样式 */
.bill-item {
  padding: 15rpx 30rpx;
  border-radius: 20rpx;
  font-size: 40rpx;
  font-weight: bold;
  color: #333;
  width: 60%;
  position: relative; /* 为伪元素定位 */
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

/* 气泡框的箭头 */
.bill-item::after {
  content: "";
  position: absolute;
  bottom: -10rpx; /* 箭头位置 */
  left: 20rpx;
  width: 0;
  height: 0;
  border-left: 10rpx solid transparent;
  border-right: 10rpx solid transparent;
  border-top: 10rpx solid rgba(255, 255, 255, 0.8);
}

.food::after {
  border-top-color: #ffe6e6;
}

.stay::after {
  border-top-color: #fff5cc;
  left: 30rpx; /* 调整箭头位置 */
}

.transport::after {
  border-top-color: #e6ffe6;
}

/* 底部 Logo 和按钮 */
.footer {
  text-align: center;
  margin-top: auto;
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

.record-button {
  font-size: 28rpx;
  background-color: #4c8cf5;
  color: #fff;
  padding: 12rpx 30rpx;
  border-radius: 24rpx;
  text-align: center;
  width: 50%;
  margin: 0 auto;
}
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
