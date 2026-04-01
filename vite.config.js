import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    port: 5173,
    // 🔥 新增代理配置
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000', // 👈 统一指向你的后端端口
        changeOrigin: true,
        // rewrite: (path) => path.replace(/^\/api/, '') 
        // 注意：如果你的 Flask Blueprint 已经带了 /api 前缀，这里就不需要 rewrite
      }
    }
  }
})