<template>
  <div class="feedback-page">
    <!-- 顶部返回按钮和标题 -->

    <!-- 描述输入框 -->
    <div class="description-box">
      <textarea
        v-model="feedbackText"
        placeholder="描述问题的详细情况，有助于我们快速帮您解决（必填）"
        rows="5"
        class="feedback-textarea"
      ></textarea>
    </div>

    <!-- 添加图片按钮 -->
    <div class="image-upload">
      <div class="upload-box" @click="chooseImage">
        <div class="add-icon">+</div>
        <div class="upload-text">添加图</div>
      </div>
    </div>

    <!-- 提交按钮 -->
    <div class="submit-button" @click="submitFeedback">
      提交
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// 用于保存反馈文本的内容
const feedbackText = ref('');

// 跳转到上一个页面
const goBack = () => {
  uni.navigateBack({
    delta: 1
  });
};

// 选择图片
const chooseImage = () => {
  uni.chooseImage({
    count: 1,
    success: (res) => {
      uni.showToast({
        title: '图片已选择',
        icon: 'success'
      });
      console.log('选择的图片路径:', res.tempFilePaths);
    },
    fail: (err) => {
      console.error('图片选择失败:', err);
    }
  });
};

// 提交反馈
const submitFeedback = () => {
  if (!feedbackText.value.trim()) {
    uni.showToast({
      title: '请填写反馈内容',
      icon: 'none'
    });
    return;
  }

  uni.showToast({
    title: '反馈已提交',
    icon: 'success'
  });
  console.log('反馈内容:', feedbackText.value);
};
</script>

<style scoped>
.feedback-page {
  padding: 20px;
  background-color: #f8f8f8;
  min-height: 100vh;
}

.header {
  display: flex;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #e0e0e0;
}

.back-button {
  font-size: 16px;
  cursor: pointer;
  color: #333;
}

.title {
  font-size: 18px;
  font-weight: bold;
  margin-left: 20px;
}

.description-box {
  margin-top: 20px;
  background-color: #ffffff;
  padding: 10px;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.feedback-textarea {
  width: 100%;
  height: 120px; /* 明确设置高度，确保可以正常输入 */
  border: none;
  outline: none;
  resize: none;
  font-size: 16px;
  color: #333;
  line-height: 1.5;
}

.feedback-textarea::placeholder {
  color: #aaa;
}

.image-upload {
  margin-top: 20px;
  display: flex;
  align-items: center;
}

.upload-box {
  width: 100px;
  height: 100px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  cursor: pointer;
}

.add-icon {
  font-size: 30px;
  color: #999;
}

.upload-text {
  font-size: 14px;
  color: #666;
  margin-top: 5px;
}

.submit-button {
  margin-top: 30px;
  background-color: #007aff;
  color: white;
  text-align: center;
  padding: 15px;
  border-radius: 25px;
  font-size: 18px;
  cursor: pointer;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
</style>
