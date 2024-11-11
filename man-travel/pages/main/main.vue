<template>
	<view>
		<!-- 显示文字 -->
		<text>{{ message }}</text>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				// 初始化文字内容
				message: "这是main页面"
			}
		},
		methods: {
			// 可以在此定义页面方法
		}
	}
</script>

<style>
	/* 样式部分，可以自定义文字样式 */
	text {
		font-size: 24px;
		color: #333;
		text-align: center;
	}
</style>
