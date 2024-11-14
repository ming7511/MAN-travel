<template>
  <view class="container">
    <!-- 顶部导航栏 -->
    <view class="navbar">
      <text class="title">添加账单</text>
    </view>

    <!-- 分类图标区域 -->
    <view class="category-section">
      <view class="category-item" v-for="(item, index) in categories" :key="index" @click="selectCategory(index)">
        <view :class="['icon-wrapper', selectedCategory === index ? 'selected' : '']">
          <image :src="item.icon" class="icon" />
        </view>
        <text class="category-text">{{ item.name }}</text>
      </view>
    </view>

    <!-- 输入区域：日期选择、备注输入和金额显示 -->
    <view class="input-section">
      <!-- 日期选择按钮 -->
      <view class="date-button" @click="chooseDate">选择日期: {{ date || '未选择' }}</view>
      
      <!-- 备注输入框 -->
      <input class="remark-input" placeholder="在这里输入备注..." v-model="remark" />
      
      <!-- 显示金额 -->
      <view class="amount">
        ¥ {{ amount }}
      </view>
    </view>

    <!-- 自定义数字键盘 -->
    <view class="keyboard">
      <view class="key" v-for="(key, index) in keys" :key="index" @click="handleKeyPress(key)">
        {{ key }}
      </view>
    </view>

    <!-- 完成按钮 -->
    <button class="submit-button" type="primary" @click="submit">完成</button>
  </view>
</template>

<script>
export default {
  data() {
    return {
      categories: [
        { name: "交通", icon: "/static/transport.png" },
        { name: "住宿", icon: "/static/hotel.png" },
        { name: "美食", icon: "/static/food.png" },
        { name: "景点", icon: "/static/scenic.png" },
        { name: "购物", icon: "/static/shopping.png" },
        { name: "活动", icon: "/static/activity.png" },
        { name: "其它", icon: "/static/other.png" }
      ],
      selectedCategory: null,
      date: '',         // 存储选择的日期
      remark: '',       // 存储备注
      amount: "0.00",   // 存储金额
      keys: ["1", "2", "3", "✖️", "4", "5", "6", "+", "7", "8", "9", "-", ".", "0", "=", "完成"],
    };
  },
  methods: {
    // 选择分类
    selectCategory(index) {
      this.selectedCategory = index;
    },
    // 调用日期选择器
    chooseDate() {
      uni.showDatePicker({
        success: (res) => {
          this.date = res.date;  // 成功选择日期后，将日期存储在 data 中
        },
        fail: () => {
          uni.showToast({
            title: '未选择日期',
            icon: 'none'
          });
        }
      });
    },
    // 处理键盘按键事件
    handleKeyPress(key) {
      if (key === "✖️") {
        this.amount = "0.00";
      } else if (key === "+") {
        // 加号逻辑处理
      } else if (key === "-") {
        // 减号逻辑处理
      } else if (key === "=") {
        // 计算逻辑
      } else if (key === "完成") {
        this.submit();
      } else {
        // 数字输入逻辑
        if (this.amount === "0.00") {
          this.amount = key;
        } else {
          this.amount += key;
        }
      }
    },
    // 完成提交
    submit() {
      uni.showToast({
        title: '账单已添加',
        icon: 'success'
      });
    }
  }
};
</script>

<style>
/* 页面整体样式 */
.container {
  padding: 20px;
  background-color: #f4f7fa;
  min-height: 100vh;
}

/* 顶部导航栏样式 */
.navbar {
  text-align: center;
  margin-bottom: 20px;
}

.title {
  font-size: 20px;
  font-weight: bold;
  color: #333;
}

/* 分类图标区域样式 */
.category-section {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  margin-bottom: 20px;
}

.category-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 15px;
  cursor: pointer;
}

.icon-wrapper {
  width: 60px;
  height: 60px;
  background-color: #f0f0f0;
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-wrapper.selected {
  border: 2px solid #4a90e2;
  background-color: #e1f5fe;
}

.icon {
  width: 30px;
  height: 30px;
}

.category-text {
  font-size: 12px;
  color: #666;
  margin-top: 5px;
}

/* 输入区域样式 */
.input-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

.date-button {
  width: 100%;
  padding: 10px;
  background-color: #f0f0f0;
  border-radius: 5px;
  font-size: 14px;
  color: #333;
  margin-bottom: 10px;
  text-align: left;
}

.remark-input {
  width: 100%;
  padding: 10px;
  font-size: 14px;
  color: #333;
  background-color: #f9f9f9;
  border-radius: 5px;
  margin-bottom: 10px;
}

.amount {
  font-size: 24px;
  font-weight: bold;
  color: #4a90e2;
  margin-bottom: 20px;
}

/* 自定义数字键盘样式 */
.keyboard {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  padding: 10px;
}

.key {
  text-align: center;
  padding: 15px 0;
  font-size: 18px;
  background-color: #e1f0ff;
  border-radius: 5px;
  cursor: pointer;
}

.key:active {
  background-color: #b3d8f0;
}

/* 完成按钮样式 */
.submit-button {
  width: 100%;
  padding: 12px;
  background-color: #4a90e2;
  color: white;
  font-size: 16px;
  border-radius: 5px;
  text-align: center;
  margin-top: 20px;
}
</style>
