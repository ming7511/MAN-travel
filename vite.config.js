// vite.config.js
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

// 使用 defineConfig 来定义配置
export default defineConfig({
  plugins: [vue()],
  build: {
    outDir: 'dist' // 指定构建输出目录为 'dist'
  }
});