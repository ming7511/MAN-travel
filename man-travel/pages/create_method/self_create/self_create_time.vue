<template>
  <view class="container">
    <!-- 关闭按钮 -->
    <view class="close-icon-container">
      <image src="/static/icons/close.png" class="close-icon" @click="closePage" />
    </view>

    <!-- 标题：这趟旅行要去哪里？ -->
    <view class="title-container">
      <text class="title-text">这趟旅行要去哪里？</text>
    </view>

    <!-- 旅行目的地 -->
    <view class="location-container">
      <view class="location-circle">
        <text class="location-text">{{ locationInput }}</text>
      </view>
    </view>

    <!-- 新页面的标题：确定好日期了吗？ -->
    <view class="sub-title-container">
      <text class="sub-title-text">确定好日期了吗？</text>
    </view>

    <!-- 天数和日期的横向选择栏 -->
    <view class="selection-container">
      <view class="selection-item" :class="{'active': isDaySelected}" @click="toggleSelection('day')">
        <text class="selection-text">天数</text>
      </view>
      <view class="selection-item" :class="{'active': isDateSelected}" @click="toggleSelection('date')">
        <text class="selection-text">日期</text>
      </view>
    </view>

    <!-- 横线部分拆分为两部分：左边和右边 -->
    <view class="selection-line-container">
      <!-- 左边的横线 (天数部分) -->
      <view class="selection-line" :class="{'active': isDaySelected}" style="left: 0;"></view>
      <!-- 右边的横线 (日期部分) -->
      <view class="selection-line" :class="{'active': isDateSelected}" style="left: 50%;"></view>
    </view>

    <!-- 滚动容器，仅包裹天数和日期选择部分 -->
    <view class="scroll-container">
      <scroll-view class="scroll-content" scroll-y>
        <!-- 天数选择（竖列展示） -->
        <view v-if="showDayPicker" class="day-picker-container">
          <view v-for="day in 30" :key="day" class="day-picker-item" :class="{'day-selected': selectedDay === day}" @click="selectDay(day)">
            <text class="day-text">{{ day }}</text>
          </view>
        </view>

        <!-- 日期选择表格 -->
        <view v-if="showDatePicker" class="date-picker-container">
          <scroll-view class="calendar-scroll" scroll-y>
            <view v-for="(month, index) in twelveMonthsData" :key="index" class="month-container">
              <!-- 年月显示部分 -->
              <view class="month-year-container">
                <text class="month-year-text">{{ month.year }}年{{ month.month }}月</text>
              </view>

              <!-- 星期标题行 -->
              <view class="weekdays-container">
                <view v-for="day in weekDays" :key="day" class="weekday-item">
                  <text class="weekday-text">{{ day }}</text>
                </view>
              </view>

              <!-- 日历日期网格 -->
              <view class="calendar-grid">
                <view v-for="(date, index) in month.dates" :key="index" class="calendar-day-item"
                      :class="{'selected-range': isInSelectedRange(date, month.year, month.month)}"
                      @click="selectDate(date, month.year, month.month)">
                  <text class="calendar-day-text">{{ date ? date : '' }}</text>
                </view>
              </view>
            </view>
          </scroll-view>
        </view>
      </scroll-view>
    </view>

    <view class="start-planning-container">
      <view class="start-planning-button" @click="startPlanning" :class="{'disabled': isUploading}">
        <text class="start-planning-text">开始规划！</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { v4 as uuidv4 } from 'uuid'; // 导入用于生成唯一 ID 的库

// 星期数据
const weekDays = ['日', '一', '二', '三', '四', '五', '六'];

// 存储未来 12 个月的数据
const twelveMonthsData = ref([]);

// 计算未来 12 个月的数据
const calculateTwelveMonthsData = () => {
  const today = new Date();
  const monthsData = [];

  for (let i = 0; i < 12; i++) {
    const year = today.getFullYear();
    const month = today.getMonth() + i;

    // 计算正确的年月（支持跨年）
    const displayYear = year + Math.floor(month / 12);
    const displayMonth = (month % 12) + 1;

    const firstDay = new Date(displayYear, displayMonth - 1, 1).getDay();
    const daysInMonth = new Date(displayYear, displayMonth, 0).getDate();

    const dates = Array(firstDay).fill(null); // 填充空白部分
    for (let d = 1; d <= daysInMonth; d++) {
      dates.push(d);
    }

    monthsData.push({
      year: displayYear,
      month: displayMonth,
      dates: dates
    });
  }

  twelveMonthsData.value = monthsData;
};

// 新增的选中状态变量
const selectedDay = ref(null); // 选中的天数
const startDate = ref(null); // 选中的起始日期
const endDate = ref(null); // 选中的终止日期

// 选择某一天的天数
const selectDay = (day) => {
  selectedDay.value = day;
  console.log('选中的天数：', day);
};

// 选择日期范围
const selectDate = (day, year, month) => {
  if (!day) return;

  const date = new Date(year, month - 1, day);

  if (!startDate.value || (startDate.value && endDate.value)) {
    startDate.value = date;
    endDate.value = null; // 重置结束日期
  } else {
    if (date < startDate.value) {
      endDate.value = startDate.value;
      startDate.value = date;
    } else {
      endDate.value = date;
    }
  }

  console.log(`选择的日期范围：起始日期 ${startDate.value}, 结束日期 ${endDate.value || "未选择"}`);
};

// 判断是否为选中范围内的日期
const isInSelectedRange = (day, year, month) => {
  if (!startDate.value || !day) return false;

  const date = new Date(year, month - 1, day);
  if (endDate.value) {
    return date >= startDate.value && date <= endDate.value;
  } else {
    return date.getTime() === startDate.value.getTime();
  }
};

// 初始化时计算 12 个月的数据
onMounted(() => {
  calculateTwelveMonthsData();
});

// 从缓存中获取用户选择的城市
const locationInput = ref(''); // 用户输入的城市
const showDayPicker = ref(true);
const showDatePicker = ref(false);
const isDaySelected = ref(true);
const isDateSelected = ref(false);

// 关闭页面方法
const closePage = () => {
  uni.navigateBack();
};

const isUploading = ref(false); // 标记上传状态，防止重复点击

const startPlanning = () => {
  // 如果正在上传数据，则禁止再次点击
  if (isUploading.value) {
    return;
  }

  // 设置为正在上传状态
  isUploading.value = true;

  const travelData = {};

  // 确保用户选择了旅行的目的地
  if (!locationInput.value || locationInput.value === '未选择城市') {
    uni.showToast({
      title: '请选择旅行目的地',
      icon: 'none'
    });
    isUploading.value = false; // 上传结束，恢复点击
    return; // 提示用户选择目的地，并终止函数
  }

  // 输出用户选择的城市
  travelData.city = locationInput.value;

  // 输出选择的天数或日期
  if (startDate.value) {
    const dayCount = endDate.value
      ? (endDate.value - startDate.value) / (1000 * 60 * 60 * 24) + 1 // 计算日期之间的天数
      : 1;

    travelData.startDate = startDate.value;
    travelData.endDate = endDate.value || startDate.value;
    travelData.dayCount = dayCount;

    // 输出选择的日期范围和天数
    console.log('选择的日期和天数: ', {
      startDate: travelData.startDate,
      endDate: travelData.endDate,
      dayCount: travelData.dayCount,
    });
  } else if (selectedDay.value) {
    // 如果用户只选择了天数（没有选择日期）
    travelData.dayCount = selectedDay.value;

    // 输出选择的天数
    console.log('选择的天数: ', {
      dayCount: travelData.dayCount,
    });
  } else {
    // 如果没有选择天数和日期，则提示用户进行选择
    uni.showToast({
      title: '请选择行程天数或日期',
      icon: 'none'
    });
    isUploading.value = false; // 上传结束，恢复点击
    return; // 提示用户选择天数或日期，并终止函数
  }
  
  // 格式化日期为 YYYY-MM-DD
  const formatDate = (date) => {
    if (!date) return '';
    const d = new Date(date);
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0'); // 保证两位数
    const day = String(d.getDate()).padStart(2, '0'); // 保证两位数
    return `${year}-${month}-${day}`;
  };

  // 输出所有选择的信息（城市、日期、天数等）
  console.log('完整的旅行数据:', travelData);

  // 将旅行数据转换为 JSON 字符串，并进行 URL 编码
  const travelDataStr = JSON.stringify({
    trip_name: travelData.city,  // 行程名称（城市）
    start_date: formatDate(travelData.startDate),  // 格式化后的开始日期
    end_date: formatDate(travelData.endDate)  // 格式化后的结束日期
  });

  const encodedData = encodeURIComponent(travelDataStr); // 确保数据编码

  // 执行上传数据的操作
  const token = uni.getStorageSync('access_token');
  if (!token) {
    uni.showToast({
      title: '请先登录',
      icon: 'none',
    });
    isUploading.value = false; // 上传结束，恢复点击
    return;
  }

  // 准备上传的数据
  const dataToUpload = {
    trip_name: travelData.city,  // 行程名称（城市）
    start_date: formatDate(travelData.startDate),  // 格式化后的开始日期
    end_date: formatDate(travelData.endDate)  // 格式化后的结束日期
  };
  
  console.log('准备上传的数据:', dataToUpload);

  // 发送 POST 请求，将城市和日期等数据上传到服务器
  uni.request({
    url: 'https://734dw56037em.vicp.fun/api/trip/create_trip/', // 替换为实际的后端接口 URL 
    method: 'POST',
    data: dataToUpload, // 上传的数据
    header: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`, // 将 token 放入 Authorization 头中
    },
    success: (res) => {
      console.log('服务器响应:', res);  // 打印完整的响应数据
      if (res.statusCode === 201) {
        // 如果响应状态码是201，跳转至 overview 页面
        uni.showToast({
          title: '数据上传成功',
          icon: 'success',
        });
        uni.navigateTo({
          url: '/pages/Overview/Overview'  
        });
      } else {
        // 如果服务器返回的是非成功状态码
        uni.showToast({
          title: '数据上传失败，请稍后再试',
          icon: 'none',
        });
      }
    },

    fail: (err) => {
      // 请求失败处理
      uni.showToast({
        title: '网络请求失败，请检查网络连接',
        icon: 'none',
      });
    },
    complete: () => {
      // 上传完成后，重置上传状态
      isUploading.value = false;
    },
  });
};


// 切换选择天数或日期
const toggleSelection = (selection) => {
  if (selection === 'day') {
    showDayPicker.value = true;
    showDatePicker.value = false;
    isDaySelected.value = true;
    isDateSelected.value = false;
  } else if (selection === 'date') {
    showDayPicker.value = false;
    showDatePicker.value = true;
    isDaySelected.value = false;
    isDateSelected.value = true;
  }
};

// 初始化地点信息，假设是从上一页传递过来的
onMounted(() => {
  locationInput.value = uni.getStorageSync('selectedCity') || '未选择城市';
});
</script>



<style scoped>
/* 页面整体布局 */
.container {
  background-color: rgba(180, 253, 255, 0.20); /* 设置背景色的透明度为15% */
  padding: 40rpx;
  display: flex;
  flex-direction: column;
  justify-content: flex-start; /* 保持顶部内容固定 */
  height: 100vh;
  position: relative;
  overflow: hidden;
}

/* 关闭按钮 */
.close-icon-container {
  position: absolute;
  top: 20rpx;
  left: 20rpx;
  z-index: 100;
}

.close-icon {
  width: 40rpx;
  height: 40rpx;
  cursor: pointer;
}

/* 标题：这趟旅行要去哪里？ */
.title-container {
  margin-top: 100rpx; /* 调整顶部间距 */
  display: flex;
  font-family: 'TaipeiSansTCBeta';
}

.title-text {
  font-size: 54rpx;
  font-weight: bold;
  color: #000;
}

/* 旅行目的地显示 */
.location-container {
  margin-top: 30rpx;
  display: flex;
  margin-left: 20rpx;
}
.location-circle {
  display: inline-flex; /* 使容器宽度自适应内容 */
  align-items: center;
  justify-content: center;
  padding: 0 20rpx; /* 给内容左右增加额外的空间，使宽度稍微大于内容 */
  height: 75rpx;
  border-radius: 35rpx;
  border: 1px solid rgba(128, 128, 128, 0.5);
  background-color: white;
}


.location-text {
  font-size: 36rpx;
  color: #000;
  font-weight: 550;
}

/* 新页面的标题：确定好日期了吗？ */
.sub-title-container {
  margin-top: 40rpx;
  display: flex;
  justify-content: flex-start; /* 左对齐 */
  font-family: 'TaipeiSansTCBeta';
}

.sub-title-text {
  font-size: 54rpx;
  font-weight: bold;
  color: #000;
}
/* 天数和日期选择栏 */
.selection-container {
  display: flex;
  margin-top: 20rpx;
  justify-content: space-between; /* 左右分布以覆盖整行 */
  position: relative; /* 为了能够定位选择横线 */
  width: 100%; /* 占满整个宽度 */
  border-bottom: 2rpx solid #ccc; /* 为了视觉对比加一个底线 */
}

.selection-item {
  flex: 1; /* 每个项目平分容器 */
  text-align: center; /* 居中对齐 */
  padding: 20rpx;
  cursor: pointer;
  font-size: 36rpx;
}

.selection-item.active {
  font-weight: bold;
  color: #000; /* 选中项加深颜色 */
}

/* 横线容器，用于包含两部分的横线 */
.selection-line-container {
  position: relative;
  width: 100%;
  height: 3rpx; /* 横线的厚度 */
  margin-top: -5rpx; /* 可以根据需要调整和选择栏的距离 */
}

/* 两部分横线的基础样式 */
.selection-line {
  position: absolute;
  width: 50%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.1); /* 默认是浅色（未选中时） */
  transition: background-color 0.3s ease; /* 平滑过渡颜色变化 */
}

/* 选中状态的横线 */
.selection-line.active {
  background-color: #000; /* 选中后变为黑色 */
}


/* 滚动容器 */
.scroll-container {
  flex: 1; /* 使滚动区域占据剩余空间 */
  overflow-y: auto; /* 启用垂直滚动 */
  margin-top: 20rpx; /* 保证与上面内容有适当间距 */
  max-height: 50vh; /* 限制最大高度 */
}

/* 天数选择竖列 */
.day-picker-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.day-picker-item {
  font-size: 60rpx;
  padding: 10rpx;
  cursor: pointer;
}

/* 天数选择的样式 */
.day-picker-item.day-selected {
  font-size: 80rpx; /* 增大字体 */
  font-weight: bold; /* 加粗字体 */
}

/* 日历日期网格 */
.calendar-day-item.selected-range {
  background-color: rgba(0, 123, 255, 0.2); /* 在选中范围内的日期显示淡蓝色背景 */
  border-radius: 50%;
}

.calendar-day-item.start-date,
.calendar-day-item.end-date {
  background-color: #007bff; /* 起始和终止日期的颜色 */
  color: white; /* 文字颜色改为白色以便突出显示 */
  border-radius: 50%;
}

.day-text {
  color: #000;
}

/* 年月显示部分 */
.month-year-container {
  margin-top: 20rpx;
  display: flex;
  justify-content: center;
}

.month-year-text {
  font-size: 46rpx;
  font-weight: bold;
  color: #000;
}

/* 星期标题行 */
.weekdays-container {
  margin-top: 20rpx;
  display: flex;
  justify-content: space-around;
}

.weekday-item {
  flex: 1;
  text-align: center;
}

.weekday-text {
  font-size: 32rpx;
  color: #666;
}

/* 日历日期网格 */
.calendar-grid {
  margin-top: 20rpx;
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 10rpx;
  padding: 10rpx;
}

.calendar-day-item {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 80rpx;
}

.calendar-day-item.today {
  background-color: rgba(0, 123, 255, 0.1); /* 给今天一个淡蓝色背景 */
  border-radius: 50%;
}

.calendar-day-text {
  font-size: 36rpx;
  color: #000;
}


/* 开始规划按钮 */
.start-planning-container {
  margin-top: 25rpx;
  display: flex;
  justify-content: center;
}

.start-planning-button {
  width: 270rpx;
  height: 90rpx;
  border-radius: 50rpx;
  background-color: black;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
    box-shadow: 0 10rpx 20rpx rgba(0, 0, 0, 0.25); /* 添加阴影效果 */
  
}

.start-planning-text {
  color: white;
  font-size: 40rpx;
  font-weight: bold;
  margin-left: 26rpx;
  margin-bottom: 4rpx;
  letter-spacing: 2rpx; /* 设定字间距 */
}

.start-planning-button.disabled {
  background-color: #ccc; /* 禁用时的背景颜色 */
  cursor: not-allowed; /* 禁用时的光标样式 */
}
 
  
/* 加载自定义字体 */
@font-face {
  font-family: 'TaipeiSansTCBeta';
  src: url('font/TaipeiSansTCBeta-Regular.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

body {
  font-family: sans-serif; /* 默认字体 */
}

</style>
