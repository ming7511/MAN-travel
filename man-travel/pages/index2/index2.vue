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
    <view class="travel-time">{{ travelDateRange }} {{ tripDuration }}</view>

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
      <!-- 分类展示区域 -->
      <view v-for="(category, index) in categorizedItems" :key="index" class="category">
        <text class="category-title">{{ category.title }} ({{ category.completedCount }})</text>
        <!-- 物品列表 -->
        <view class="item-list">
          <view class="item" v-for="item in category.items" :key="item.id">
            <text>{{ item.name }}</text>
            <view class="checkmark" v-if="item.completed">✔️</view>
          </view>
        </view>
      </view>

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
      tripId: '1',
      fetchedItems: [],
      categorizedItems: [],
      token: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoyMDQ3NjQ5MDI0LCJpYXQiOjE3MzIyODkwMjQsImp0aSI6ImJkYmYzMWRlMTAwNTQ4ZTE5ZmI4NWQ5MDhjMGUzODZhIiwidXNlcl9pZCI6M30.JgXdiNcV3wVC73KWKORyOERdyeElEIm4ER5uWuNU3B0', // 假设你有一个令牌用于认证
    };
  },
  methods: {
    goBack() {
      uni.navigateTo({
        url: '/pages/index/index'
      });
    },
    handleShowOverview() {
      uni.navigateTo({
        url: `/pages/Overview/Overview?id=${this.tripId}`
      });
    },
    goToBillPage() {
      uni.navigateTo({
        url: `/pages/shouye/shouye?id=${this.tripId}`
      });
    },
    goToAddPage() {
      uni.navigateTo({
        url: `/pages/tianjia/tianjia?id=${this.tripId}`
      });
    },
    categorizeItems() {
      const categorized = {};
      this.fetchedItems.forEach(item => {
        if (!categorized[item.note]) {
          categorized[item.note] = { title: item.note, items: [], completedCount: 0 };
        }
        categorized[item.note].items.push(item);
          categorized[item.note].completedCount++;
        
      });
      this.categorizedItems = Object.values(categorized);
    },
    fetchItems() {
      fetch('http://127.0.0.1:8000/api/memos/memos/',  { // 确保 URL 正确
        method: 'GET',
        headers: {
         'Authorization': `Bearer ${this.token}` // 如果需要认证的话
        },
      })
      .then(response => {
        if (response.ok) {
          return response.json();
        }
        throw new Error('Network response was not ok.');
      })
      .then(data => {
        this.fetchedItems = data; // 更新fetchedItems数组
        this.categorizeItems(); // 获取数据后进行分类
      })
      .catch((error) => {
        console.error('Error:', error);
      });
    }
  },
  created() {
    this.fetchItems(); // 在组件创建时获取物品数据
  },
  mounted() {
    setInterval(() => {
      this.fetchItems();
    }, 10000); // 每隔 10 秒获取一次数据
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