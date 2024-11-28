<template>
  <view class="container" @click="handleClose">
    <!-- 输入框区域 -->
    <view
      class="input-box"
      @click.stop
      @touchstart="handleTouchStart"
      @touchmove="handleTouchMove"
      @touchend="handleTouchEnd"
    >
      <!-- 灰色横线 -->
      <view class="line"></view>
      
      <!-- 输入框 -->
      <view class="input-container">
        <textarea
          class="input"
          placeholder="粘贴小红书等笔记链接即可导入地点或行程。"
          v-model="inputText"
          maxlength="500"
        />
      </view>
      
      <!-- 确认按钮 -->
      <view class="confirm-box" @click="handleConfirm" :disabled="isLoading">
        <image src="/static/icons/link_white.png" class="icon" mode="aspectFit"></image>
        <text class="confirm-text">粘贴并识别</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, toRaw } from 'vue';
import { onLoad } from '@dcloudio/uni-app'; // 正确导入 onLoad

// 定义变量接收旅行数据
const inputText = ref('');
const travelData = ref({});
const isLoading = ref(false);  // 标志位，用于判断是否处于加载状态

const startY = ref(0);
const isSliding = ref(false);

// 触摸事件处理
const handleTouchStart = (e) => {
  startY.value = e.touches[0].clientY;
  isSliding.value = false;
};

const handleTouchMove = (e) => {
  const moveY = e.touches[0].clientY;
  const deltaY = moveY - startY.value;

  // 如果下滑超过50px，设置滑动状态为true
  if (deltaY > 50) {
    isSliding.value = true;
  }
};

const handleTouchEnd = () => {
  if (isSliding.value) {
    closeInputBox();
  }
};

// 关闭输入框动画
const closeInputBox = () => {
  const inputBox = document.querySelector('.input-box');
  if (inputBox) {
    inputBox.style.animation = 'slideDown 0.4s ease-out forwards';
    setTimeout(() => {
      uni.navigateTo({
        url: '/pages/create_method/create_method' // 修改为正确的跳转路径
      });
    }, 400);
  }
};

// 确认按钮点击事件
const handleConfirm = () => {
  const input = inputText.value.trim();

  // 检查输入是否为空
  if (input === '') {
    uni.showToast({
      title: '请输入有效链接',
      icon: 'none',
    });
    return;
  }

  // 提取链接
  const extractUrl = (text) => {
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    const urls = text.match(urlRegex);
    return urls ? urls[0] : '';
  };

  const link = extractUrl(input);

  if (link === '') {
    uni.showToast({
      title: '未能从输入中提取到有效链接',
      icon: 'none',
    });
    return;
  }

  // 如果获取到旅行数据，准备上传
  const { city, startDate, endDate, dayCount } = travelData.value || {};
  console.log('旅行数据：', travelData.value);

  // 获取本地存储中的 access_token
  const token = uni.getStorageSync('access_token');
  if (!token) {
    uni.showToast({
      title: '请先登录',
      icon: 'none',
    });
    return;
  }

  // 禁用按钮，避免多次点击
  isLoading.value = true;
  
  // 跳转至 loading 页面
  uni.navigateTo({
    url: '/pages/loading/loading', // 跳转到 loading 页面
  });
  
  // 格式化日期为 YYYY-MM-DD
  const formatDate = (date) => {
    if (!date) return '';
    const d = new Date(date);
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0'); // 保证两位数
    const day = String(d.getDate()).padStart(2, '0'); // 保证两位数
    return `${year}-${month}-${day}`;
  };

  // 格式化 startDate 和 endDate
  const formattedStartDate = formatDate(startDate);
  const formattedEndDate = formatDate(endDate);

  // 计算行程天数 day_count
  const calculateDayCount = (start, end) => {
    if (!start || !end) return 0;
    const startTime = new Date(start).getTime();
    const endTime = new Date(end).getTime();
    const diffTime = endTime - startTime;
    const diffDays = Math.ceil(diffTime / (1000 * 3600 * 24)) + 1; // 加1包括开始和结束日期
    return diffDays;
  };

  const day_count = calculateDayCount(startDate, endDate);

  // 打印准备上传的数据
  const dataToUpload = {
    url: link, // 用户提供的链接
    trip_name: city, // 用户提供的目的地
    start_date: formattedStartDate, // 格式化后的开始日期
    end_date: formattedEndDate, // 格式化后的结束日期
    day_counts: day_count, // 行程总共的天数
  };

  console.log('准备上传的数据:', dataToUpload);

  // 发送 POST 请求，将城市和日期等数据上传到服务器
  uni.request({
    url: 'https://734dw56037em.vicp.fun/api/trip/AiCreateUrls/', // 替换为实际的后端接口 URL
    method: 'POST',
    data: dataToUpload, // 上传的数据
    header: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`, // 将 token 放入 Authorization 头中
    },
    success: (res) => {
      console.log('服务器响应:', res); // 打印完整的响应数据
      if (res.statusCode === 201) {
        // 显示成功提示
        uni.showToast({
          title: '数据上传成功',
          icon: 'success',
        });
  
        // 提取服务器返回的 trip_id
        const { trip_id } = res.data;
        
        // 构建包含 trip_id 的 URL
        const importPageUrl = `/pages/create_method/import/import?trip_id=${trip_id}`;
  
        // 跳转到 import 页面
        uni.navigateTo({
          url: importPageUrl, // 包含 trip_id 的 URL
        });
      } else {
        // 服务器返回非成功状态码
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
      // 请求完成后，重置加载状态（如果有定义 isLoading）
      if (typeof isLoading !== 'undefined') {
        isLoading.value = false;
      }
    },
  });
};

// 使用 onLoad 生命周期获取页面参数
onLoad((options) => {
  console.log('页面启动参数:', options);  // 输出启动时的参数，检查 `options` 是否存在 `data`。

  if (options.data) {
    const data = options.data;  // 获取 URL 查询参数中的 "data"
    console.log('URL参数 data:', data);  // 调试：输出 URL 中的参数 data

    try {
      const decodedData = decodeURIComponent(data);  // 解码
      console.log('解码后的数据:', decodedData);  // 调试：输出解码后的数据

      try {
        let parsedData = JSON.parse(decodedData); // 解析 JSON
        console.log('解析后的数据:', parsedData);  // 调试：输出解析后的数据

        // 确保日期转换正常
        if (parsedData.startDate) {
          parsedData.startDate = new Date(parsedData.startDate);
        }
        if (parsedData.endDate) {
          parsedData.endDate = new Date(parsedData.endDate);
        }

        // 将解析的数据存储到 `travelData` 中
        travelData.value = parsedData;

        // 输出解开的数据
        console.log('接收到的旅行数据:', toRaw(travelData.value)); // 使用 toRaw() 获取实际的对象
      } catch (error) {
        console.error('解析失败:', error); // 如果解析失败，输出错误信息
      }
    } catch (error) {
      console.error('解码失败:', error); // 处理解码失败的情况
    }
  } else {
    console.log('没有接收到旅行数据');
  }
});
</script>


<style scoped>
/* 页面容器 */
.container {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: flex-end;
  align-items: flex-end;
  background-color: rgba(0, 0, 0, 0.3); /* 半透明蒙版 */
}

/* 输入框容器 */
.input-box {
  width: 95%;
  height: 40%;
  background-color: #ffffff;
  border-radius: 33px 33px 0 0;
  padding: 20rpx;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  box-shadow: 0 -4px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  animation: slideUp 0.4s ease-out;
}

/* 滑入动画 */
@keyframes slideUp {
  from {
    transform: translateY(100%);
  }
  to {
    transform: translateY(0);
  }
}

/* 滑出动画 */
@keyframes slideDown {
  from {
    transform: translateY(0);
  }
  to {
    transform: translateY(100%);
  }
}

/* 灰色横线 */
.line {
  width: 60px;
  height: 6px;
  background-color: #888888;
  margin: 10rpx auto;
  border-radius: 3px;
  cursor: pointer;
}

/* 输入框容器 */
.input-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  margin-top: 50rpx;  /* 缩小 margin-top 值，让输入框更靠上 */
  flex-grow: 1;  /* 使得容器可以占据剩余空间 */
}

/* 多行输入框样式 */
.input {
  width: 90%;
  height: 300rpx;  /* 增加高度以支持多行输入 */
  padding: 10rpx 20rpx;
  font-size: 28rpx;
  border: 1px solid #fff;
  border-radius: 10px;
  text-align: left; /* 左对齐 */
  vertical-align: top;  /* 顶部对齐 */
  line-height: 40rpx; /* 行高设置，以确保多行文本行距适中 */
  resize: none; /* 禁止用户改变大小 */
}

/* 确认按钮 */
.confirm-box {
  position: absolute;
  bottom: 15rpx;
  right: 30rpx;
  width: 250rpx;
  height: 80rpx;
  background-color: #000;
  border-radius: 33px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 20rpx auto;
}

.icon {
  width: 65rpx;
  height: 65rpx;
  margin-left: -10rpx;
  color: #fff;
}

.confirm-text {
  font-size: 30rpx;
  font-weight: bold;
  color: #fff;
}
</style>
