import { createSSRApp } from 'vue'
import App from './App'

// 引入 axios（或 uni.request 配置）
import axios from 'axios'

// #ifdef VUE3
export function createApp() {
  const app = createSSRApp(App)

  // 配置 axios 请求拦截器（为每个请求添加 token）
  axios.defaults.baseURL = 'https://your-api-base-url.com/' // 替换为你的 API 基础地址

  // 请求拦截器：自动将 token 添加到请求头中
  axios.interceptors.request.use(
    (config) => {
      const token = uni.getStorageSync('access_token')  // 从本地存储获取 token
      if (token) {
        config.headers['Authorization'] = `Bearer ${token}`  // 添加 Authorization header
      }
      return config
    },
    (error) => {
      return Promise.reject(error)
    }
  )

  // 响应拦截器：处理 token 失效等情况
  axios.interceptors.response.use(
    (response) => {
      return response
    },
    (error) => {
      if (error.response && error.response.status === 401) {
        // 如果收到 401 错误（未授权），可以清除 token 并跳转到登录页面
        uni.removeStorageSync('access_token')
        uni.removeStorageSync('refresh_token')
        uni.redirectTo({
          url: '/pages/login/login'  // 跳转到登录页
        })
      }
      return Promise.reject(error)
    }
  )

  // 返回应用实例
  return {
    app
  }
}
// #endif
