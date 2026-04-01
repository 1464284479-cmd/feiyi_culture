<script setup>
import { RouterView } from 'vue-router'
// 引入头部和底部组件
import SiteHeader from './components/SiteHeader.vue'
import SiteFooter from './components/SiteFooter.vue'
</script>

<template>
  <div class="app-wrapper">
    <!-- 1. 显示头部 -->
    <SiteHeader />

    <!-- 2. 显示当前页面的内容 (比如联系我们页) -->
    <main class="page-body">
      <RouterView />
    </main>

    <!-- 3. 显示底部 -->
    <SiteFooter />
  </div>
</template>

<style>
/* 全局基础样式 */
body {
  margin: 0;
  padding: 0;
  background-color: #f5f5f5;
  font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
}

/* 布局容器：保证页面至少有屏幕那么高，且 Footer 永远在最底下 */
.app-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.page-body {
  flex: 1; /* 自动撑开中间区域 */
  display: flex;
  flex-direction: column;
}
</style>