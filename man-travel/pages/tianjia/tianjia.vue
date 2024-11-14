<template>
  <view class="container">
    <!-- 顶部导航栏 -->
    <view class="navbar">
      <view class="back-button" @click="goBack">＜</view>
      <text class="title">添加行李</text>
    </view>

    <!-- 搜索框 -->
    <view class="search-bar">
      <input class="search-input" placeholder="输入物品名称..." />
    </view>

    <!-- 常用物品分类 -->
    <view class="category-section">
      <text class="section-title">常用物品</text>
      <view class="category-tabs">
        <view class="tab active">个人证件</view>
        <view class="tab">数码产品</view>
        <view class="tab">药品</view>
        <view class="tab">生活用品</view>
      </view>
    </view>

    <!-- 物品列表 -->
    <view class="item-list">
      <view class="item" v-for="item in items" :key="item.id">
        <text>{{ item.name }}</text>
        <view class="add-icon">＋</view>
      </view>
    </view>

    <!-- 保存按钮 -->
    <button class="save-button">保存</button>
  </view>
</template>

<script>
export default {
  data() {
    return {
      items: [
        { id: 1, name: '身份证' },
        { id: 2, name: '学生证' },
        { id: 3, name: '户口本' },
        { id: 4, name: '护照' },
        { id: 5, name: '签证' },
        { id: 6, name: '港澳通行证' },
        { id: 7, name: '大陆居民往来通行证' },
        { id: 8, name: '驾照' }
      ]
    };
  },
  methods: {
    goBack() {
      uni.navigateBack();
    }
  }
};
</script>

<style>
/* 页面整体样式 */
.header {
  background-color: #b0d8ff;
  padding: 20rpx;
  border-radius: 10rpx;
  text-align: center;
}

.title {
  font-size: 36rpx; /* 增大字体 */
  font-weight: bold;
  color: #333;
  line-height: 1.4; /* 增加行高以增加行间距 */
}

.subtitle {
  font-size: 24rpx; /* 较小字体用于副标题 */
  color: #666;
  margin-top: 8rpx; /* 增加与标题的间距 */
}

.container {
  background-color: #f4f7fa;
  padding: 10px;
  min-height: 100vh;
}

/* 顶部导航栏 */
.navbar {
  display: flex;
  align-items: center;
  padding: 10px 0;
  background-color: #fff;
  border-bottom: 1px solid #ddd;
}

.back-button {
  font-size: 18px;
  margin-right: 10px;
  color: #333;
}

.title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

/* 搜索框 */
.search-bar {
  margin: 10px 0;
  padding: 10px;
  background-color: #fff;
  border-radius: 5px;
}

.search-input {
  width: 100%;
  font-size: 16px;
  border: none;
  outline: none;
}

/* 分类标题和选项卡 */
.category-section {
  margin-top: 10px;
}

.section-title {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.category-tabs {
   display: flex;
   margin-top: 10px;
   overflow-x: auto; /* 当标签过多时允许横向滚动 */
   white-space: nowrap; /* 防止换行 */
}

.tab {
  padding: 8px 12px;
  background-color: #f5f5f5;
  color: #007acc;
  border-radius: 15px;
  margin-right: 10px;
  white-space: nowrap; /* 防止文字在按钮内换行 */
}

.tab.active {
  background-color: #007acc;
  color: #fff;
}

/* 物品列表 */
.item-list {
  margin-top: 10px;
  background-color: #fff;
}

.item {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  border-bottom: 1px solid #ddd;
  align-items: center;
}

.add-icon {
  font-size: 18px;
  color: #007acc;
}

/* 保存按钮 */
.save-button {
  width: 100%;
  padding: 12px;
  background-color: #4a90e2;
  color: white;
  font-size: 16px;
  font-weight: bold;
  text-align: center;
  border-radius: 5px;
  margin-top: 20px;
}
</style>
