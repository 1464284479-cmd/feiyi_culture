

import { createApp } from 'vue'
import App from './App.vue'
import router from './router' // 确保这里导入了router

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App)

// 【关键】确保这行在 app.mount 之前！
app.use(router) 
app.use(ElementPlus)

app.mount('#app')