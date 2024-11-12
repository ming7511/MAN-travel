<template>
  <div class="edit-profile-page">
    <!-- 顶部返回按钮和标题 -->


    <!-- 头像编辑 -->
    <div class="profile-item avatar-item" @click="editAvatar">
      <span class="label">头像</span>
      <image src="/static/avatar.png" alt="头像" class="avatar-image" />
      <span class="arrow">></span>
    </div>

    <!-- 信息编辑列表 -->
    <div class="profile-item" @click="editNickname">
      <span class="label">昵称</span>
      <span class="value">一个真正的man</span>
      <span class="arrow">></span>
    </div>
    <div class="profile-item" @click="editRealName">
      <span class="label">真实姓名</span>
      <span class="value">小蓝龙</span>
      <span class="arrow">></span>
    </div>
    <div class="profile-item" @click="editGender">
      <span class="label">性别</span>
      <span class="value">男</span>
      <span class="arrow">></span>
    </div>
    <div class="profile-item">
      <span class="label">手机</span>
      <span class="value">189****9999</span>
    </div>
    <div class="profile-item">
      <span class="label">邮箱</span>
      <span class="value">189****9999@qq.com</span>
    </div>

    <!-- 提交按钮 -->
    <div class="submit-button" @click="submitChanges">
      保存
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// 跳转到上一个页面
const goBack = () => {
  uni.navigateBack({
    delta: 1
  });
};

// 编辑头像
const editAvatar = () => {
  uni.chooseImage({
    count: 1,
    success: (res) => {
      uni.showToast({
        title: '头像已选择',
        icon: 'success'
      });
      console.log('选择的头像路径:', res.tempFilePaths);
    },
    fail: (err) => {
      console.error('头像选择失败:', err);
    }
  });
};

// 编辑昵称
const editNickname = () => {
  uni.showModal({
    title: '编辑昵称',
    editable: true,
    placeholderText: '请输入新的昵称',
    success: (res) => {
      if (res.confirm && res.content) {
        uni.showToast({
          title: `昵称已修改为 ${res.content}`,
          icon: 'success'
        });
      }
    }
  });
};

// 编辑真实姓名
const editRealName = () => {
  uni.showModal({
    title: '编辑真实姓名',
    editable: true,
    placeholderText: '请输入真实姓名',
    success: (res) => {
      if (res.confirm && res.content) {
        uni.showToast({
          title: `真实姓名已修改为 ${res.content}`,
          icon: 'success'
        });
      }
    }
  });
};

// 编辑性别
const editGender = () => {
  uni.showActionSheet({
    itemList: ['男', '女'],
    success: (res) => {
      const gender = res.tapIndex === 0 ? '男' : '女';
      uni.showToast({
        title: `性别已修改为 ${gender}`,
        icon: 'success'
      });
    }
  });
};

// 提交修改
const submitChanges = () => {
  uni.showToast({
    title: '信息已保存',
    icon: 'success'
  });
  // 在这里可以执行保存到服务器的逻辑
};
</script>

<style scoped>
.edit-profile-page {
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

.profile-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px 0;
  border-bottom: 1px solid #f0f0f0;
  background-color: #ffffff;
}

.avatar-item {
  padding: 15px 0;
}

.label {
  font-size: 16px;
  color: #333;
}

.value {
  font-size: 16px;
  color: #999;
  text-align: right; /* 设置右对齐 */
  flex-grow: 1; /* 占用剩余空间 */
  margin-right: 10px;
}

.avatar-image {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}

.arrow {
  font-size: 16px;
  color: #999;
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
