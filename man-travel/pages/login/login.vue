<template>
  <view class="container">
    <!-- Logo 图片 -->
    <view class="logo-section">
      <image src="/static/logo.png" alt="Logo" class="logo-image" />
      <image src="/static/logo3.png" alt="man游 Logo" class="text-logo-image" />
    </view>

    <!-- 输入框区域 -->
    <view class="input-section">
      <!-- 手机号码输入框 -->
      <view class="input-wrapper">
        <input type="text" placeholder="请输入手机号" class="input" v-model="phoneNumber" />
      </view>

      <!-- 验证码输入框和按钮 -->
      <view class="verification-input-wrapper">
        <input type="text" placeholder="请输入验证码" class="input" v-model="verificationCode" />
        <button class="verification-button" @click="getVerificationCode">获取验证码</button>
      </view>
    </view>

    <!-- 登录按钮 -->
    <view class="login-button-wrapper">
      <button class="login-button" @click="login">登录</button>
    </view>
  </view>
</template>
<script>
export default {
  name: "LoginPage",
  data() {
    return {
      phoneNumber: '',
      verificationCode: ''
    };
  },
  methods: {
    getVerificationCode() {
      console.log("获取验证码");
    },
    login() {
      // 可以在这里进行输入验证，例如判断手机号和验证码是否符合要求
      if (this.phoneNumber && this.verificationCode) {
        // 执行页面跳转到主页
        uni.redirectTo({
          url: '/pages/index/index'
        });
      } else {
        uni.showToast({
          title: '请输入手机号和验证码',
          icon: 'none'
        });
      }
    }
  }
};
</script>
<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100vh;
  background-color: #fff;
}

.logo-section {
  margin-top: 80px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.logo-image {
  width: 120px;
  height: 120px;
}

.text-logo-image {
  margin-top: 10px;
  width: 120px;
  height: 40px;
}

.input-section {
  width: 80%;
  margin-top: 40px;
}

.input-wrapper,
.verification-input-wrapper {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  background-color: #f2f2f2;
  border-radius: 40px;
  padding: 10px;
  height: 40px;
}

.input {
  flex-grow: 1;
  border: none;
  outline: none;
  background: none;
  font-size: 16px;
  height: 100%;
}

.verification-button {
  margin-left: 0px;
  color: #3b82f6;
  font-size: 14px;
  border: none;
  background: none;
  padding: 0;
  width: 100px;
  background-color: transparent;
}

.login-button-wrapper {
  margin-top: 40px;
  width: 80%;
}

.login-button {
  width: 100%;
  padding: 5px;
  background-color: #69C0FF;
  color: #ffffff;
  font-size: 18px;
  border: none;
  border-radius: 40px;
  text-align: center;
}
</style>
