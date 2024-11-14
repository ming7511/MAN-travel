<template>
  <view class="container">
    <!-- 顶部导航栏 -->
    <view class="navbar">
      <text class="title">福州三日游 | 在三坊七巷感受榕城秋日古韵</text>
      <text class="sub-title">10.1-10.3 | 3天2晚</text>
      <view class="tabs">
        <text class="tab-item">行程</text>
        <text class="tab-item active">旅行账单</text>
        <text class="tab-item" @click="goToPackingList">行李清单</text>
      </view>
    </view>

    <!-- 页面内容 -->
    <view class="bill-section">
      <view class="total-amount">
        <text class="total-label">总花费</text>
        <text class="amount">¥ 888.00</text>
      </view>
      <view class="set-budget-background"></view>
      <view class="set-budget-text" @click="showBudgetOverlay">
        <text class="set-budget">设置预算</text>
      </view>
    </view>

    <view class="detail-section">
      <view class="date-wrapper">
        <view class="date">
          <text>2024.10.1</text>
          <text class="amount">¥ 888.00</text>
        </view>
      </view>
      <view class="item">
        <image src="/static/ttravel.png" class="icon"></image>
        <text class="item-title">交通</text>
        <text class="amount">¥ 888.00</text>
      </view>
    </view>

    <!-- 自定义数字键盘弹出层 -->
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
      <!-- 移除 overlay 的 @click 事件 -->
      <view class="overlay" @click="closeKeyboard"></view>
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
    goToPackingList() {
      uni.navigateTo({
        url: '/pages/xingli/xingli'  // 跳转路径
      });
    },
    // 显示预算输入弹窗
    showBudgetOverlay() {
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
      console.log("当前预算输入:", this.budget); // 调试输出
    },
    // 确认预算并关闭输入框
    confirmBudget() {
      this.showBudgetInput = false;
      uni.showToast({
        title: `预算已设置为 ¥${this.budget}`,
        icon: 'success',
        duration: 2000
      });
      console.log("预算设置为:", this.budget); // 调试输出
    },
    // 关闭键盘
    closeKeyboard() {
      this.showBudgetInput = false;
    }
  }
};
</script>



<style>
.budget-input-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999; /* 确保弹窗在最上层 */
}


.budget-input-container {
  background-color: #fff;
  padding: 30px;
  border-radius: 10px;
  width: 300px;
  text-align: center;
}

.budget-input-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.budget-display {
  font-size: 28px;
  font-weight: bold;
  color: #007acc;
  margin-bottom: 20px;
}

.number-keyboard {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-bottom: 20px;
}

.key {
  background-color: #e1f0ff;
  padding: 15px 0;
  border-radius: 10px;
  font-size: 20px;
  font-weight: bold;
  color: #333;
  text-align: center;
}

.confirm-button {
  background-color: #007acc;
  color: #fff;
  padding: 10px 0;
  border-radius: 10px;
  font-size: 16px;
  width: 100%;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: transparent;
}
/* 页面整体样式 */
.container {
  background-color: #f4f7fa;
  padding: 20px;
}

/* 顶部导航栏样式 */
.navbar {
  background-color: #e1f0ff;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
}

.title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.sub-title {
  font-size: 14px;
  color: #888;
  margin-top: 5px;
}

.tabs {
  display: flex;
  justify-content: space-around;
  margin-top: 15px;
}

.tab-item {
  font-size: 16px;
  color: #888;
}

.tab-item.active {
  color: #0066cc;
  font-weight: bold;
}

/* 账单总花费样式 */
.bill-section {
  background-color: #d6f4ff; /* 较深的浅蓝色背景 */
  padding: 20px;
  border-radius: 10px;
  margin-top: 20px;
  text-align: center;
  position: relative; /* 用于定位子元素 */
}

/* 总花费和金额显示 */
.total-amount {
  display: flex;
  flex-direction: column; /* 垂直布局 */
  align-items: center; /* 水平居中对齐 */
  margin-bottom: 10px;
  position: relative; /* 相对定位，避免被背景遮挡 */
  z-index: 2; /* 确保在背景之上显示 */
}
.total-label {
  font-size: 12px; /* 增大字体大小 */
  font-weight: bold;
  color: #333;
}

.amount {
  font-size: 36px; /* 增大字体大小，使金额更显眼 */
  font-weight: bold;
  color: #000;
  margin-top: 5px;
}

/* 浅蓝色背景，覆盖到整个下半部分，并扩大到更多区域 */
.set-budget-background {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 40%; /* 扩大高度，覆盖更多上半部分 */
  background-color: #e1f5fe; /* 浅蓝色背景 */
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
  z-index: 1; /* 放在主内容的下层 */
}

/* 设置预算文本样式 */
.set-budget-text {
  position: relative;
  z-index: 2; /* 确保文字在背景之上 */
  margin-top: 50px; /* 下移设置预算文本 */
}

.set-budget {
  font-size: 16px;
  color: #007acc; /* 蓝色字体 */
  text-align: center;
}

/* 明细信息样式 */
.detail-section {
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  margin-top: 20px;
}

/* 日期和金额部分样式，添加背景 */
.date-wrapper {
  background-color: #f0f0f0; /* 灰色背景 */
  padding: 8px 12px;
  border-radius: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.date {
  font-size: 16px;
  color: #333;
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.date text {
  margin-right: 20px; /* 增加日期和金额的距离 */
}

.item {
  display: flex;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #f1f1f1;
}

.icon {
  width: 24px;
  height: 24px;
  background-color: #e1f5fe; /* 浅蓝色背景 */
  padding: 5px;
  border-radius: 50%;
  margin-right: 10px;
}

.item-title {
  font-size: 16px;
  color: #333;
  flex: 1;
}

.amount {
  font-size: 16px;
  color: #333;
}
</style>
