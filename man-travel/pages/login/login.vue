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
        <button class="verification-button" @click="getVerificationCode" :disabled="isCodeButtonDisabled">{{ buttonText }}</button>
      </view>
    </view>

    <!-- 登录按钮 -->
    <view class="login-button-wrapper">
      <button class="login-button" @click="login">登录</button>
    </view>
  </view>
</template>

<script>
import axios from 'axios';

export default {
  name: "LoginPage",
  data() {
    return {
      phoneNumber: '',         // 用户输入的手机号
      verificationCode: '',    // 用户输入的验证码
      buttonText: '获取验证码',  // 按钮文本
      isCodeButtonDisabled: false, // 控制按钮禁用
      countdown: 60             // 倒计时
    };
  },
  methods: {
    // 获取验证码
    async getVerificationCode() {
      if (!this.phoneNumber) {
        uni.showToast({
          title: '手机号不能为空',
          icon: 'none'
        });
        return;
      }

      // 发起请求获取验证码
      try {
        const response = await axios.post('https://734dw56037em.vicp.fun/api/accounts/register/', {
          phone: this.phoneNumber
        });
        uni.showToast({
          title: response.data.message,
          icon: 'none'
        });

        // 启动倒计时
        this.startCountdown();
      } catch (error) {
        if (error.response && error.response.data) {
          uni.showToast({
            title: error.response.data.error || '验证码发送失败',
            icon: 'none'
          });
        } else {
          uni.showToast({
            title: '请求失败，请稍后重试',
            icon: 'none'
          });
        }
      }
    },

    // 启动倒计时
    startCountdown() {
      this.isCodeButtonDisabled = true;
      let countdownInterval = setInterval(() => {
        if (this.countdown <= 0) {
          clearInterval(countdownInterval);
          this.isCodeButtonDisabled = false;
          this.countdown = 60;
          this.buttonText = '获取验证码';
        } else {
          this.countdown--;
          this.buttonText = `${this.countdown}s 后重新获取`;
        }
      }, 1000);
    },

    // 用户登录
    async login() {
      if (!this.phoneNumber || !this.verificationCode) {
        uni.showToast({
          title: '请输入手机号和验证码',
          icon: 'none'
        });
        return;
      }

      try {
        const response = await axios.post('https://734dw56037em.vicp.fun/api/accounts/login/', {
          phone: this.phoneNumber,
          code: this.verificationCode
        });
        // 登录成功后保存 Token 并跳转到主页
        const { access, refresh } = response.data;
        uni.setStorageSync('access_token', access);
        uni.setStorageSync('refresh_token', refresh);
		
		// 打印 token 到控制台
		    console.log('Access Token:', access);
		    console.log('Refresh Token:', refresh);

        uni.redirectTo({
          url: '/pages/index/index'
        });
      } catch (error) {
        if (error.response && error.response.data) {
          uni.showToast({
            title: error.response.data.error || '登录失败',
            icon: 'none'
          });
        } else {
          uni.showToast({
            title: '登录请求失败，请稍后重试',
            icon: 'none'
          });
        }
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
