<template>
  <view class="travel-plan-overview-page">
    <!-- 返回按钮容器 -->
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
        <button class="btn-title" @click="handleShouyeClick">旅行账单</button>
        <!-- 行李清单按钮 -->
        <button class="btn-title" @click="handleXingliClick">行李清单</button>
      </view>
      <view class="horizontal-line"></view>
    </view>
    <!-- 白色矩形区域 -->
    <view class="white-rectangle">
      <!-- 行程天数按钮 -->
      <view class="day-buttons">
        <button v-for="(day, index) in days" :key="index"
                :class="['day-button', { active: currentDay === day }]"
                @click="handleDayClick(day)">{{ day }}</button>
      </view>
      <!-- DAY 行程标题 -->
      <view v-if="currentDay!== '总览'" class="day-header">
        <view class="day-label">{{ currentDay }}</view>
      </view>
      <!-- 行程地点信息 -->
      <view v-if="currentDay!== '总览'" v-for="(place, pIndex) in places" :key="pIndex" class="place-item">
        <image class="place-image" :src="getPlaceImage(place)" :alt="place" mode="aspectFill" />
        <view class="place-info">
          <view class="place-type">{{ getPlaceType(place) }}</view>
          <view class="place-name">{{ place }}</view>
        </view>
        <button class="delete-place-btn" @click="deletePlace(currentDay, pIndex)">
          <image class="delete-icon" :src="getDeleteIconPath" />
        </button>
      </view>
      <!-- 添加地点行 -->
      <view class="add-place-row" v-if="!showAddPlaceInput">
        <image class="add-place-image" src="/static/add_icon.png" />
        <view class="add-place-text" @click="showAddPlaceInput = true">添加地点</view>
      </view>
      <view v-if="showAddPlaceInput" class="add-place-input-row">
        <input class="add-place-input" v-model="newPlaceName" placeholder="请输入地点名称" />
        <button class="add-place-confirm-btn" @click="addPlace(currentDay)">确认添加</button>
      </view>
    </view>
  </view>
</template>

<script>
import axios from 'axios';
import { ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { nextTick } from 'vue';

export default {
  props: {
    day: {
      type: String,
      default: '总览'
    },
    id: {
      type: String,
      required: true
    },
    places: {
      type: String,
      default: ''
    },
    title: {
      type: String,
      default: '未命名行程'
    },
    dateRange: {
      type: String,
      default: '未知日期'
    },
    duration: {
      type: String,
      default: '未知时长'
    },
    dailyTrips: {
      type: String,
      default: '[]'
    },
    // 此处移除了overviewTripId相关的props定义，因为不再使用它了
    // overviewTripId: {
    //   type: String,
    //   required: true
    // },
    overviewDays: {
      type: String,
      default: ''
    },
    tripId: {
      type: [String, Number], // 根据实际情况确定类型，这里假设需要数字类型的tripId，要和父组件传递的值类型匹配
      required: true // 根据业务需求确定是否必填
    }
  },
  
  setup(props, { emit }) {
	console.log('接收到的props中的tripId参数值:', props.tripId, '类型:', typeof props.tripId);
    // 统一使用id作为行程ID，确保获取到有效值并转换为合适类型（这里假设为数字类型，可根据实际调整）
    let tripId = props.id;
    console.log('接收到的原始id参数值:', props.id, '类型:', typeof props.id);
    if (typeof tripId === 'string') {
        tripId = parseInt(tripId);
        console.log('转换后的tripId值:', tripId, '类型:', typeof tripId);
        if (isNaN(tripId)) {
            console.error('接收到的行程ID参数无法转换为有效数字，请检查参数传递');
            tripId = 0; // 设置一个默认值，可根据业务需求调整处理方式
        }
    }
    const tripIdRef = ref(tripId);

    // 用于存储天数的ref，接收并解析Overview传递过来的天数参数
    const days = ref(props.overviewDays? decodeURIComponent(props.overviewDays).split(' - ') : []);
    const currentDay = ref(props.day);
    const places = ref(props.places? decodeURIComponent(props.places).split(' - ') : []);
    const tripTitle = ref(decodeURIComponent(props.title));
    const travelDateRange = ref(decodeURIComponent(props.dateRange));
    const tripDuration = ref(decodeURIComponent(props.duration));
    const dailyTrips = ref([]);
    const userInputDestination = ref('');

    // 新增，接收并解析传递过来的天数参数
    const receivedDays = props.days? decodeURIComponent(props.days).split(' - ') : [];
    days.value = receivedDays;

    // 用于存储添加地点时输入的临时地点名称
    const newPlaceName = ref('');
    // 用于标识是否显示添加地点的输入框
    const showAddPlaceInput = ref(false);

    const router = useRouter();
    const route = useRoute();
    const tripDataEncoded = route.query.tripData;
    if (tripDataEncoded) {
        const tripData = JSON.parse(decodeURIComponent(tripDataEncoded));
        // 直接更新原有的places和dailyTrips
        places.value = tripData.places;
        dailyTrips.value = tripData.dailyTrips;
    }

    // 更新当前显示地点数据的方法（之前提到的updatePlacesForDay方法，根据实际情况完善具体逻辑）
    const updatePlacesForDay = (day) => {
      const formattedDay = day.trim().toUpperCase();
      const selectedTrip = dailyTrips.value.find((trip) => trip.day.trim().toUpperCase() === formattedDay);
      if (selectedTrip) {
        places.value = selectedTrip.places.split(' - ');
      } else {
        console.log('未找到对应天数的行程数据');
        // 可以添加一些兜底逻辑，比如显示默认提示信息等，例如：
        places.value = []; // 当没找到对应数据时，将地点列表置为空数组，避免后续操作报错
      }
    };

    // 在页面加载时，设置行程天数按钮
    onMounted(() => {
        const tripId = tripIdRef.value;
        if (!tripId) {
            console.error('未获取到有效的行程ID值，无法进行页面初始化，请检查参数传递');
            return;
        }
        try {
            // 使用传递下来的duration来动态设置天数按钮
            const durationMatch = /(\d+)天/.exec(tripDuration.value);
            const numberOfDays = durationMatch? parseInt(durationMatch[1]) : 3;
            days.value = ['总览',...Array.from({ length: numberOfDays }, (_, i) => `DAY${i + 1}`)];
    
            // 从路由获取参数，确保页面加载时正确获取places和dailyTrips
            if (route.query.places) {
                places.value = decodeURIComponent(route.query.places).split(' - ');
            }
    
            if (route.query.dailyTrips) {
                const rawDailyTrips = decodeURIComponent(route.query.dailyTrips);
                try {
                    const parsedDailyTrips = JSON.parse(rawDailyTrips);
    
                    // 新增：检查元素唯一性
                    const uniqueDays = new Set();
                    const hasDuplicates = parsedDailyTrips.some((trip) => {
                        if (uniqueDays.has(trip.day)) {
                            return true;
                        }
                        uniqueDays.add(trip.day);
                        return false;
                    });
                    if (hasDuplicates) {
                        console.error('dailyTrips数组中存在重复的天数元素，请检查数据来源和处理逻辑');
                        // 可以考虑在这里进行去重等处理，或者提示用户修改数据
                        const uniqueDailyTrips = Array.from(uniqueDays).map(day => {
                            return parsedDailyTrips.find(trip => trip.day === day);
                        });
                        dailyTrips.value = uniqueDailyTrips;
                    }
    
                    // 验证解析后的数据结构完整性，参考Overview.vue里的预期结构
                    if (!Array.isArray(parsedDailyTrips)) {
                        console.error('解析后的dailyTrips不是数组类型，不符合预期，尝试修复');
                        parsedDailyTrips = [];
                    } else {
                        parsedDailyTrips.forEach((trip) => {
                            if (!('day' in trip) ||!('places' in trip)) {
                                console.error('行程元素中缺少必要属性（day或places），不符合预期，尝试修复');
                                // 可以根据实际情况进行属性补全或者报错处理等
                                trip.day = '未知天数';
                                trip.places = '未知地点';
                            }
                        });
                    }
    
                    dailyTrips.value = parsedDailyTrips;
                } catch (error) {
                    console.error('解析dailyTrips数据出错:', error);
                }
            }
        } catch (error) {
            console.error('页面加载时初始化数据出错：', error);
        }
    });

    // 监听路由参数变化，更新数据
    watch(
        () => route.query,
        (newQuery) => {
            try {
                if (newQuery.places) {
                    places.value = decodeURIComponent(newQuery.places).split(' - ');
                }
    
                if (newQuery.dailyTrips) {
                    const updatedDailyTrips = JSON.parse(decodeURIComponent(newQuery.dailyTrips));
                    dailyTrips.value = updatedDailyTrips;
                }
    
                if (newQuery.day) {
                    currentDay.value = newQuery.day;
                    updatePlacesForDay(newQuery.day);
                }
            } catch (error) {
                console.error('处理路由参数变化时出错：', error);
            }
        },
        { immediate: true }
    );

    // 获取地点图片的方法
    const getPlaceImage = (place) => {
      return "/static/logo.png";
    };

    // 获取地点类型的方法
    const getPlaceType = (place) => {
      if (place.includes("公园") || place.includes("景点") || place.includes("山") || place.includes("杭") || place.includes("江") || place.includes("巷")) {
        return "景点 🏔";
      } else if (place.includes("炸鸡") || place.includes("捞化") || place.includes("美食街")) {
        return "吃喝 🍴";
      } else if (place.includes("站") || place.includes("机场")) {
        return "交通 🚗";
      } else {
        return "其他 💬";
      }
    };

    // 展开地点详情的方法（空实现，因为已移除相关显示元素）
    const expandPlace = () => {};

    // 添加备注的方法
    const addNote = (day) => {
      console.log(`添加${day}备注`);
    };

    // 添加地点的方法（修改此处逻辑以确保添加后能正确显示在行程中）
    const addPlace = (day) => {
      if (newPlaceName.value) {
        const formattedDay = day.trim().toUpperCase();
        // 先获取对应天数在整个行程中的数字表示（这里假设days数组已经正确初始化和赋值，你可以根据实际情况调整逻辑）
        const dayIndex = days.value.findIndex((d) => d.trim().toUpperCase() === formattedDay);
        if (dayIndex === -1) {
          console.error(`无法确定添加地点对应的行程天数，找不到匹配的天数（${formattedDay}）`);
          return;
        }
        const tripDay = dayIndex + 1; // 因为数组索引从0开始，所以天数要加1，符合后端要求的天数表示方式

        if (typeof tripId.value!== 'number' && isNaN(parseInt(tripId.value))) {
          console.error('tripId的值类型错误或无法转换为有效数字，请检查数据来源');
          return;
        }
        // 构造要发送到后端的请求数据，确保每个参数符合要求
        const requestData = {
          trip_information_id: parseInt(tripId.value), // 此处使用tripId代替原本可能用到overviewTripId的地方，确保是合法数字表示，否则可能得NaN，可加更多校验逻辑
          days: tripDay,
          trip_destination: userInputDestination.value || '默认地点', // 如果用户未输入目的地名称，设置一个默认值（根据业务需求调整），避免传递空值给后端
          description: '探索行程地点' // 根据业务需求填写合适的默认描述内容，避免传递空字符串（可根据实际修改）
        };

        // 设置请求头
        const headers = {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoyMDQ3MDM5NTM4LCJpYXQiOjE3MzE2Nzk1MzgsImp0aSI6ImQ5ODM5NDIxNTgwMTQ2NTQ5Yzk1ZDVmOTQwMTU3NjBkIiwidXNlcl9pZCI6M30.6lJwP0434Dh3KcG2A8SmJ6xAn65azoY6k4NKxaw99vM'
        };

        // 恢复原始的请求地址，去掉添加tripId的拼接逻辑
        const apiUrl = 'http://localhost:8000/api/trip/add-place-activity/';

        // 发送POST请求到后端接口
        axios.post(apiUrl, requestData, { headers })
        .then((response) => {
            if (response.status === 201) {
              console.log(response.data.message);
              updatePlacesForDay(day);
              newPlaceName.value = '';
              showAddPlaceInput.value = false;
              nextTick(() => {
                console.log('尝试触发更新后，places:', places.value);
                console.log('尝试触发更新后，dailyTrips:', dailyTrips.value);
              });
            }
          })
        .catch((error) => {
            // 根据不同的错误状态码处理错误情况
            if (error.response) {
              const statusCode = error.response.status;
              if (statusCode === 400) {
                console.error('添加地点出错：', error.response.data.error);
              } else if (statusCode === 403) {
                console.error('无权限添加地点：', error.response.data.error);
              } else if (statusCode === 500) {
                console.error('后端添加地点出现异常：', error.response.data.error);
              }
            } else {
              console.error('发送添加地点请求出错：', error);
            }
          });
      }
    };

    const getPlaceId = (place) => {
      // 假设地点对象是一个包含id属性的对象，这里将其解析并返回id值，实际情况你可能需要从数据库查询等其他方式获取
      return place.id;
    };

    // 删除地点的方法
    const deletePlace = (day, placeIndex) => {
      const formattedDay = day.trim().toUpperCase();
      // 先判断dailyTrips.value是否有效，避免空数组等情况导致查找问题
      if (Array.isArray(dailyTrips.value) && dailyTrips.value.length > 0) {
        const selectedTripIndex = dailyTrips.value.findIndex((trip) => trip.day.trim().toUpperCase() === formattedDay);
        if (selectedTripIndex!== -1) {
          const placesList = dailyTrips.value[selectedTripIndex].places.split(' - ');
          if (placeIndex >= 0 && placeIndex < placesList.length) {
            const place = placesList[placeIndex];
            // 获取地点对应的ID（这里假设地点对象有个id属性，实际中你需要根据真实的数据结构获取准确的活动/地点ID，比如从地点对象里提取等方式）
            const placeId = getPlaceId(place);
            // 构造要发送到后端的请求数据，包含要删除的地点对应的ID
            const requestData = {
              "activity_id": placeId
            };
            // 设置请求头
            const headers = {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoyMDQ3MDM5NTM4LCJpYXQiOjE3MzE2Nzk1MzgsImp0aSI6ImQ5ODM5NDIxNTgwMTQ2NTQ5Yzk1ZDVmOTQwMTU3NjBkIiwidXNlcl9pZCI6M30.6lJwP0434Dh3KcG2A8SmJ6xAn65azoY6k4NKxaw99vM'
            };
            // 发送POST请求到后端接口
            axios.post('https://734dw56037em.vicp.fun/api/trip/delete_activity/', requestData, { headers })
            .then((response) => {
                if (response.status === 200) {
                  console.log(response.data.message);  // 打印后端返回的成功提示信息
                  placesList.splice(placeIndex, 1);
                  dailyTrips.value[selectedTripIndex].places = placesList.join(' - ');
                  updatePlacesForDay(day);
                  // 手动触发更新检查
                  nextTick(() => {
                    console.log('删除地点后，places:', places.value);
                    console.log('删除地点后，dailyTrips:', dailyTrips.value);
                  });
                }
              })
            .catch((error) => {
                // 根据不同的错误状态码处理错误情况
                if (error.response) {
                  const statusCode = error.response.status;
                  if (statusCode === 400) {
                    console.error('删除地点出错：', error.response.data.error);
                  } else if (statusCode === 404) {
                    console.error('要删除的地点不存在：', error.response.data.error);
                  } else if (statusCode === 500) {
                    console.error('后端删除地点出现异常：', error.response.data.error);
                  }
                } else {
                  console.error('发送删除地点请求出错：', error);
                }
              });
          } else {
            console.log(`要删除地点的索引（${placeIndex}）超出范围，无法删除地点`);
          }
        } else {
          console.log(`未找到对应天数（${formattedDay}）的行程数据，无法删除地点`);
        }
      } else {
        console.log('dailyTrips数据结构异常，无法删除地点，请检查数据来源和格式');
      }
    };

    // 处理点击天数按钮的方法
    const handleDayClick = (day) => {
      currentDay.value = day;

      if (day === '总览') {
        // 如果点击了“总览”按钮，则返回到Overview页面
        backToOverview();
      } else {
        // 更新当前显示的地点数据
        updatePlacesForDay(day);
      }
    };

    // 返回总览的方法
    const backToOverview = () => {
      router.push({
        path: '/pages/Overview/Overview',
        query: {
          id: tripId.value,
          title: encodeURIComponent(tripTitle.value),
          dateRange: encodeURIComponent(travelDateRange.value),
          duration: encodeURIComponent(tripDuration.value),
          places: encodeURIComponent(places.value.join(' - ')),
          dailyTrips: encodeURIComponent(JSON.stringify(dailyTrips.value)),
          days: encodeURIComponent(days.value.join(' - '))
        }
      });
    };

    // 返回跳转
    const goBack = () => {
      // 返回到首页 index.vue
      uni.navigateTo({
        url: '/pages/index/index'
      });
    };

    const handleShowOverview = () => {
      // 获取当前行程 ID 等必要参数（假设通过 tripId 获取，你可以根据实际情况调整）
      const tripId = tripId.value;
      if (tripId) {
        router.push({
          path: `/pages/your-overview-page`, // 替换成实际的行程展示页面路径
          query: { id: tripId }
        });
      }
    };

    // 处理点击旅行账单按钮的方法（参考Overview文件中的逻辑，根据实际调整路径等）
    const handleShouyeClick = () => {
      const tripId = tripId.value;
      if (tripId) {
        router.push({
          path: `/pages/shouye/shouye`,
          query: { id: tripId }
        });
      }
    };

    // 处理点击行李清单按钮的方法（参考Overview文件中的逻辑，根据实际调整路径等）
    const handleXingliClick = () => {
      const tripId = tripId.value;
      if (tripId) {
        router.push({
          path: `/pages/xingli/xingli`,
          query: { id: tripId }
        });
      }
    };

    // 获取删除图标路径的方法
    const getDeleteIconPath = ref("/static/icons/delete.png");

    return {
        currentDay,
        places,
        dailyTrips,
        updatePlacesForDay,
        tripId: tripIdRef,
        tripTitle,
        travelDateRange,
        tripDuration,
        days,
        getPlaceImage,
        getPlaceType,
        expandPlace,
        addNote,
        handleDayClick,
        handleShowOverview,
        backToOverview,
        handleShouyeClick,
        handleXingliClick,
        newPlaceName,
        showAddPlaceInput,
        getDeleteIconPath,
        addPlace,
        deletePlace,
        goBack
    };
  }
};
</script>

<style lang="scss">
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

// 行程名样式
.trip-name {
  font-size: 24px;
  font-weight: bold;
  text-align: left;
  margin-bottom: 10px;
}

// 旅行时间样式
.travel-time {
  font-size: 16px;
  color: dimgray;
  text-align: left;
  margin-bottom: 10px;
}

.trip-section {
  display: flex;
  flex-direction: column; /* 使其内部子项垂直排列 */
  align-items: flex-start; /* 确保内容从左侧对齐 */
  text-align: left; /* 保证文本左对齐 */
  border: none; /* 移除任何边框 */
  padding: 0; /* 确保没有多余的内边距 */
}

.button-group {
  display: flex; /* 使用 flex 布局让按钮并排 */
  align-items: center; /* 垂直居中对齐按钮文本 */
  justify-content: flex-start; /* 水平方向左对齐 */
  gap: 40rpx; /* 使用 rpx 确保按钮之间有合适的间距（适合小程序环境） */
  margin-left: 15rpx; /* 确保按钮组容器没有左侧内边距或外边距 */
  padding-left: 0; /* 确保没有额外的左侧填充 */
}

.btn-title {
  font-size: 20px; /* 字体大小 */
  font-weight: bold; /* 字体加粗 */
  color: black; /* 黑色字体 */
  background: none; /* 移除按钮的背景 */
  border: none; /* 移除按钮的边框 */
  outline: none; /* 去掉焦点时的边框 */
  padding: 0; /* 无额外内边距 */
  cursor: pointer; /* 鼠标悬浮显示手型 */
  text-decoration: none; /* 去掉默认的文本装饰，比如下划线 */
  transition: color 0.3s ease; /* 颜色渐变过渡效果 */
}

.btn-title:hover {
  color: gray; /* 悬停时字体颜色变灰 */
}

.btn-title:focus {
  outline: none; /* 点击时不显示边框 */
}

.horizontal-line {
  width: 100%;
  height: 1px;
  background-color: gray;
  margin-top: 10px; /* 保证横线和按钮之间有足够的间隔 */
}

// 白色矩形区域样式
.white-rectangle {
  background-color: white;
  border-radius: 20px;
  padding: 20px;
  margin-bottom: 20px;

  // 行程天数按钮样式
.day-buttons {
    display: flex;
    overflow-x: auto; /* 使容器可以左右滑动，和Overview保持一致 */
    white-space: nowrap; /* 防止子元素换行，和Overview保持一致 */
    margin-bottom: 5px;
	-webkit-overflow-scrolling: touch; /* 启用iOS惯性滚动效果 */

  .day-button {
        flex: 0 0 auto; /* 防止按钮缩放，保持固定宽度，和Overview保持一致 */
        width: 70px; /* 设置固定的宽度，可以根据需要调整，和Overview保持一致 */
        height: 45px;
        margin-right: 8px; /* 添加按钮间的间距，和Overview保持一致 */
        border: 1px solid #808080; /* 未点击时边框深灰色，和Overview保持一致 */
        border-radius: 20px;
        background-color: white;
        color: #808080; /* 未点击时字体深灰色，和Overview保持一致 */
        cursor: pointer;
        font-weight: normal; /* 未点击时字体正常粗细，和Overview保持一致 */
        transition: all 0.3s ease; /* 添加过渡效果，使样式变化更平滑，和Overview保持一致 */

        &.active {
            border: 2px solid black; /* 点击后边框加粗且为黑色，和Overview保持一致 */
            color: black; /* 点击后字体变为黑色，和Overview保持一致 */
            font-weight: bold; /* 点击后字体加粗，和Overview保持一致 */
        }
    }
}

.day-header {
      margin-top: 25px;
      font-size: 25px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;

    .day-label {
          font-size: 18px;
          font-weight: bold;
      }

    .add-note {
          font-size: 14px;
          color: blue;
          cursor: pointer;

          &:hover {
            text-decoration: underline;
          }
      }
  }

.place-item {
      background-color: white;
      box-shadow: 0 0 5px lightgray;
      padding: 15px;
      margin-bottom: 20px;
      border-radius: 10px;
      display: flex;
      align-items: center;

    .place-image {
          width: 80px;
          height: 80px;
          margin-right: 15px;
          border-radius: 10px;
      }

    .place-info {
          flex: 1;

        .place-type {
              font-size: 14px;
              color: gray;
              margin-bottom: 5px;
          }

        .place-name {
              font-size: 16px;
              font-weight: bold;
              margin-bottom: 5px;
          }
      }

    .delete-place-btn {
        cursor: pointer;
        box-shadow: none; /* 去除阴影 */
        display: inline-block; // 使用 inline-block 方便和其他元素在同一行排列，也可以根据实际布局需求调整为 flex 等其他方式
        padding: 0; // 去除内边距，让图标更贴合
        margin: 0; // 去除外边距，避免影响布局
        border: none; // 去掉边框，仅展示图标
        background-color: transparent; // 设置为透明背景，使按钮融入背景中，只显示图标
    
       .delete-icon {
            width: 15px;
            height: 15px;
            display: block;
            border: none;
        }
    }
  }

.add-place-row {
      display: flex;
      align-items: center;
      padding: 10px;
      border-radius: 10px;
      background-color: white;
      box-shadow: 0 0 5px lightgray;
      cursor: pointer;

    .add-place-image {
          width: 20px;
          height: 20px;
          margin-right: 10px;
      }

    .add-place-text {
          font-size: 16px;
          color: gray;
      }
  }

.add-place-input-row {
      display: flex;
      align-items: center;
      margin-top: 10px;
  }

.add-place-input {
      flex: 1;
      border: 1px solid #ccc;
      border-radius: 5px;
      padding: 5px;
  }

.add-place-confirm-btn {
      margin-left: 10px;
      padding: 0px 10px;
      border: none;
      border-radius: 5px;
      background-color: #007aff;
      color: white;
	  font-size: 13px;
      cursor: pointer;
  }
}
</style>