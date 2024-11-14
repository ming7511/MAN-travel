<template>
  <!-- 行程概览部分 -->
  <view class="travel-plan-overview-page">
    <!-- 行程名 -->
    <view class="trip-name">{{ tripTitle }}</view>
    <!-- 旅行时间 -->
    <view class="travel-time">{{ travelDateRange }}  {{ tripDuration }}</view>
    <!-- 行程标题及横线 -->
    <view class="trip-section">
      <view class="trip-title">行程</view>
      <view class="horizontal-line"></view>
    </view>
    <!-- 白色矩形区域 -->
    <view class="white-rectangle">
      <!-- 行程天数按钮 -->
      <view class="day-buttons">
        <button
          v-for="(day, index) in days"
          :key="index"
          :class="['day-button', { active: currentDay === day }]"
          @click="handleDayClick(day)"
        >
          {{ day }}
        </button>
      </view>
    </view>
  </view>

  <!-- 具体行程内容部分 -->
  <view v-if="currentDay !== '总览'" class="travel-plan-detail-page">
    <scroll-view class="daily-trips-scroll" :scroll-y="true">
      <view class="day-trip-section">
        <!-- DAY 行程标题 -->
        <view class="day-header">
          <view class="day-label">{{ currentDay }}</view>
          <view class="add-note" @click="addNote(currentDay)">添加备注</view>
        </view>
        <!-- 行程地点信息 -->
        <view v-for="(place, pIndex) in places" :key="pIndex" class="place-item">
          <image class="place-image" :src="getPlaceImage(place)" :alt="place" mode="aspectFill" />
          <view class="place-info">
            <view class="place-type">{{ getPlaceType(place) }}</view>
            <view class="place-name">{{ place }}</view>
            <view class="place-distance">{{ getDistance(place) }} | {{ getDriveTime(place) }}</view>
            <view class="expand-button" @click="expandPlace(place)">展开详情</view>
          </view>
        </view>
        <!-- 添加地点行 -->
        <view class="add-place-row">
          <image class="add-place-image" src="/static/add_icon.png" />
          <view class="add-place-text">添加地点</view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>


<script>
import { ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router'; // 引入 useRoute 和 useRouter

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
      default: '[]' // 新增：dailyTrips 用于存储每天的行程详情
    }
  },

  setup(props) {
    const currentDay = ref(props.day); // 当前选择的天数
    const places = ref(props.places ? decodeURIComponent(props.places).split(' - ') : []); // 存储地点的数组
    const tripId = ref(props.id); // 行程ID
    const tripTitle = ref(decodeURIComponent(props.title)); // 行程名称
    const travelDateRange = ref(decodeURIComponent(props.dateRange)); // 旅行日期范围
    const tripDuration = ref(decodeURIComponent(props.duration)); // 行程时长，直接从 props 获取
    const dailyTrips = ref([]); // 用于存储每天的行程数据
    const days = ref([]); // 动态存储行程天数

    const router = useRouter(); // 使用 router 进行页面跳转
    const route = useRoute(); // 使用 useRoute 获取 URL 参数

    // 更新当前显示的地点数据的方法
    const updatePlacesForDay = (day) => {
      if (day !== '总览') {
        const selectedTrip = dailyTrips.value.find((trip) => trip.day === day);
        if (selectedTrip) {
          places.value = selectedTrip.places.split(' - '); // 更新显示的地点
        }
      } else {
        places.value = []; // 如果是总览，清空 places
      }
    };

    // 在页面加载时，设置行程天数按钮
    onMounted(() => {
      // 使用传递下来的 duration 来动态设置天数按钮
      const durationMatch = /(\d+)天/.exec(tripDuration.value);
      const numberOfDays = durationMatch ? parseInt(durationMatch[1]) : 3;
      days.value = ['总览', ...Array.from({ length: numberOfDays }, (_, i) => `DAY${i + 1}`)];

      // 从路由获取参数，确保页面加载时正确获取 places 和 dailyTrips
      if (route.query.places) {
        places.value = decodeURIComponent(route.query.places).split(' - ');
      }

      if (route.query.dailyTrips) {
        dailyTrips.value = JSON.parse(decodeURIComponent(route.query.dailyTrips));
      }
    });

    // 监听路由参数变化，更新数据
    watch(
      () => route.query,
      (newQuery) => {
        if (newQuery.places) {
          places.value = decodeURIComponent(newQuery.places).split(' - ');
        }

        if (newQuery.dailyTrips) {
          dailyTrips.value = JSON.parse(decodeURIComponent(newQuery.dailyTrips));
        }

        if (newQuery.day) {
          currentDay.value = newQuery.day;
          updatePlacesForDay(newQuery.day);
        }
      },
      { immediate: true }
    );

    // 获取地点图片的方法
    const getPlaceImage = (place) => {
      return "/static/logo.png"; // 返回一个固定的图片地址，实际中可以根据地点返回不同图片
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

    // 获取距离的方法
    const getDistance = (place) => {
      return "7.8km";
    };

    // 获取驾车时间的方法
    const getDriveTime = (place) => {
      return "27min";
    };

    // 展开地点详情的方法
    const expandPlace = (place) => {
      console.log(`展开${place}详情`);
    };

    // 添加备注的方法
    const addNote = (day) => {
      console.log(`添加${day}备注`);
    };

    // 处理点击天数按钮的方法
    const handleDayClick = (day) => {
      currentDay.value = day;

      if (day === '总览') {
        // 如果点击了“总览”按钮，则返回到 Overview 页面
        backToOverview();
      } else {
        // 更新当前显示的地点数据
        updatePlacesForDay(day);
      }
    };

    // 返回总览的方法
    const backToOverview = () => {
      router.push({
        path: '/pages/Overview/Overview', // 假设 Overview 页面路径是 '/pages/Overview/Overview'
        query: {
          id: tripId.value, // 返回行程的 ID 以便 Overview 页面正确显示
          title: encodeURIComponent(tripTitle.value),
          dateRange: encodeURIComponent(travelDateRange.value),
          duration: encodeURIComponent(tripDuration.value),
          places: encodeURIComponent(places.value.join(' - ')), // 确保 places 被正确传递
          dailyTrips: encodeURIComponent(JSON.stringify(dailyTrips.value)) // 确保 dailyTrips 被正确传递
        }
      });
    };

    return {
      currentDay,
      places,
      tripId,
      tripTitle,
      travelDateRange,
      tripDuration,
      days,
      getPlaceImage,
      getPlaceType,
      getDistance,
      getDriveTime,
      expandPlace,
      addNote,
      handleDayClick,
      backToOverview
    };
  }
};
</script>





<style lang="scss">
.travel-plan-overview-page {
  background-color: lightblue;
  padding: 20px;

  .trip-name {
    font-size: 24px;
    font-weight: bold;
    text-align: left;
    margin-bottom: 10px;
  }

  .travel-time {
    font-size: 16px;
    color: dimgray;
    text-align: left;
    margin-bottom: 10px;
  }

  .trip-section {
    text-align: left;
    margin-bottom: 10px;

    .trip-title {
      font-size: 20px;
      font-weight: bold;
      margin-bottom: 5px;
    }

    .horizontal-line {
      width: 100%;
      height: 1px;
      background-color: gray;
    }
  }

  .white-rectangle {
    background-color: white;
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 20px;

    .day-buttons {
      display: flex;
      justify-content: space-around;
      margin-bottom: 10px;

      .day-button {
        padding: 1px 8px;
        border: 1px solid #808080;
        border-radius: 20px;
        background-color: white;
        color: #808080;
        cursor: pointer;
        font-weight: normal;
        transition: all 0.3s ease;

        &.active {
          border: 2px solid black;
          color: black;
          font-weight: bold;
        }
      }
    }
  }
}

.travel-plan-detail-page {
  background-color: lightblue;
  padding: 0px 20px 20px 20px;

  .daily-trips-scroll {
    height: calc(100vh - 200px);
    overflow-y: auto;

    .day-trip-section {
      margin-bottom: 5px;

      .day-header {
        font-size: 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;

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

          .place-distance {
            font-size: 14px;
            color: lightgray;
            margin-bottom: 10px;
          }

          .expand-button {
            font-size: 14px;
            color: blue;
            cursor: pointer;

            &:hover {
              text-decoration: underline;
            }
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
    }
  }
}
</style>