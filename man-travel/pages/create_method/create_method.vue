<template>
	<view class="container">
		<!-- 按钮组容器 -->
		<view class="button-group">
			<!-- 第一个按钮：AI智能推荐 -->
			<view class="button" @click="handleClick('AI推荐')">
				<view class="text-content">
					<text class="title">AI智能推荐旅游行程</text>
					<text class="description">根据您的旅游偏好，AI量身定制旅游行程~</text>
				</view>
				<image src="/static/icons/magic-wand.png" class="icon" mode="aspectFit"></image>
			</view>

			<!-- 第二个按钮：自定义行程 -->
			<view class="button" @click="handleClick('自定义行程')">
				<view class="text-content">
					<text class="title">自行创建新的行程</text>
					<text class="description">完美 J 人就是要自己打造专属旅游计划！</text>
				</view>
				<image src="/static/icons/plus.png" class="icon" mode="aspectFit"></image>
			</view>

			<!-- 第三个按钮：智能导入 -->
			<view class="button" @click="handleClick('智能导入')">
				<view class="text-content">
					<text class="title">智能导入行程/地点</text>
					<text class="description">粘贴小红书等笔记链接，即可导入地点或行程</text>
				</view>
				<image src="/static/icons/link.png" class="icon" mode="aspectFit"></image>
			</view>
		</view>

		<!-- 关闭按钮 -->
		<view class="close-button" @click="close">
			<text>✖</text>
		</view>
	</view>
</template>



<script>
export default {
  data() {
    return {};
  },
  methods: {
    handleClick(action) {
      // 检查点击的按钮是否是 '智能导入'
      if (action === '智能导入') {
        // 跳转到 'create_linkimport' 页面
        uni.navigateTo({
          url: '/pages/create_method/create_linkimport/create_linkimport' // 新页面路径
        });
      } else if (action === '自定义行程') {
        // 跳转到 'self_create' 页面
        uni.navigateTo({
          url: '/pages/create_method/self_create/self_create' // 新页面路径
        });
      } else if (action === 'AI推荐') {
        // 跳转到 'self_create' 页面
        uni.navigateTo({
          url: '/pages/create_method/ai_create/ai_create' // 新页面路径
        });
      } else {
        // 显示点击了哪个按钮的提示
        uni.showToast({
          title: `您点击了${action}`,
          icon: 'none'
        });
      }
    },
    close() {
      uni.navigateTo({
        url: '/pages/index/index'  // 这里填写你想返回的页面路径
      });
    }

  }
};
</script>


<style scoped>
/* 背景容器 */
.container {
	width: 430px;
	height: 852px;
	background-color: #000;
	display: flex;
	flex-direction: column;
	justify-content: flex-end; /* 让按钮组靠下对齐 */
	align-items: center;
	padding-bottom: 40rpx;
}

/* 按钮组容器，垂直排列 */
.button-group {
	width: 260px;
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 20rpx; /* 按钮之间的间距 */
	animation: buttonSlideUp 0.5s ease-out; /* 按钮组动画 */
}

/* 按钮组动画 */
@keyframes buttonSlideUp {
	from {
		transform: translateY(50%); /* 从下方进入 */
		opacity: 0;
	}
	to {
		transform: translateY(0); /* 到达最终位置 */
		opacity: 1;
	}
}

/* 按钮样式 */
.button {
	width: 260px;
	height: 90px;
	background-color: #ffffff;
	border-radius: 20px;
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	align-items: center;
	padding: 20rpx;
	box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

/* 按钮内文字 */
.text-content {
	display: flex;
	flex-direction: column;
}

.title {
	font-size: 32rpx;
	font-weight: bold;
	color: #000;
}

.description {
	font-size: 26rpx;
	color: #888888;
	margin-top: 15rpx; /* 调整标题和描述的间距 */
	margin-right: 20rpx; /* 增加描述的右边距 */
	line-height: 1.5; /* 增加行高让文本更易读 */
}


/* 图标样式 */
.icon {
	width: 50px;
	height: 50px;
	margin-top: 30rpx; /* 向下偏移调整 */
}

/* 关闭按钮，底部居中 */
.close-button {
	bottom: 40rpx; /* 底部居中 */
	width: 50px;
	height: 50px;
	border-radius: 70%;
	background-color: #ffffff;
	display: flex;
	align-items: center;
	justify-content: center;
	font-size: 36px;
	color: #000;
	margin-top: 40rpx; /* 与按钮组的间距 */
	line-height: 5rpx;
}
</style>
