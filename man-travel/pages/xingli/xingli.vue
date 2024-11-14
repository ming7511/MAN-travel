<template>
  <view class="container">
    <!-- 顶部导航栏 -->
   <view class="header">
     <text class="title">福州三日游 | 在三坊七巷感受榕城秋日古韵</text>
     <text class="subtitle">10.1 - 10.3   3天2晚</text>
      <view class="tabs">
        <text class="tab-item">行程</text>
        <text class="tab-item" @click="goToBillPage">旅行账单</text>
        <text class="tab-item active">行李清单</text>
      </view>
    </view>

    <!-- 行李清单内容 -->
    <view class="packing-list">
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
  methods: {
    goToBillPage() {
      // 跳转到旅行账单页面
      uni.navigateTo({
        url: '/pages/index/index' // 确保路径正确
      });
    },
    goToAddPage() {
      // 跳转到添加行李的页面
      uni.navigateTo({
        url: '/pages/tianjia/tianjia' // 确保路径正确
      });
    }
  }
};
</script>

<style>
/* 页面整体样式 */
.container {
  background-color: #f4f7fa;
  padding: 20px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 顶部导航栏样式 */
.navbar {
  background-color: #e1f0ff;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
}

.header {
  background-color: #d8ecff;
  padding: 20rpx;
  border-radius: 10rpx;
  text-align: left;
}

.title {
  font-size: 36rpx; /* 设置标题字体大小 */
  font-weight: bold;
  color: #333;
  line-height: 1.4; /* 增加行高，使标题和日期有间距 */
}

.subtitle {
  font-size: 24rpx; /* 设置日期字体大小 */
  color: #666;
  margin-top: 8rpx; /* 增加与标题之间的间距 */
  display: block; /* 确保日期独占一行 */
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
  cursor: pointer;
}

.tab-item.active {
  color: #0066cc;
  font-weight: bold;
}

/* 行李清单内容样式 */
.packing-list {
  text-align: center;
  margin-top: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

/* 标签样式 */
.tags {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px; /* 标签组之间的间距 */
  margin-bottom: 20px;
}

.tag-row {
  display: flex;
  gap: 10px;
  justify-content: center;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.8); /* 缩放效果 */
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
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
    margin: 10px; /* 随机的 margin 值让每个标签错落有致 */

  animation: fadeIn 0.5s ease-in-out; /* 应用淡入动画 */
}
/* 选中状态的样式 */
.tag.checked {
  background-color: #a0d8ef; /* 选中时的背景色 */
  color: #007acc; /* 选中时的文字颜色 */
  border: 1px solid #007acc; /* 选中时的边框颜色 */
}
.checkmark {
  color: #007acc;
  font-size: 16px;
}

.tag-text {
  font-size: 14px;
  color: #007acc;
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
</style>
