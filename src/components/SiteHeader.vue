<template>
  <header class="site-header">
    <div class="container header-content">
      <div class="logo">
        <router-link to="/">
          <img src="@/assets/images/logo.png" alt="Logo" />
        </router-link>
      </div>
      <nav class="nav-links">
        <router-link to="/">首页</router-link>
        <router-link to="/double-heritage">双遗数览</router-link>
        <router-link to="/window-gallery">窑韵图鉴</router-link>
        <router-link to="/patterns">剪纸纹样</router-link>
        <router-link to="/shop">非遗商城</router-link>
        <router-link to="/artisans">匠人故事</router-link>
        <router-link to="/contact">联系我们</router-link>
      </nav>
    </div>
  </header>
</template>

<style scoped>
.container {
  width: 1200px;
  max-width: 95%;
  margin: 0 auto;
}

.site-header {
  background-color: #5D0E0E; /* 深红色背景 */
  padding: 15px 0;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo img {
  height: 50px;
  display: block;
}

.nav-links a {
  color: #fff;
  text-decoration: none;
  margin-left: 25px;
  font-size: 16px;
  font-weight: 500;
  padding-bottom: 5px;
  transition: all 0.3s;
}

.nav-links a:hover,
.nav-links a.router-link-active {
  color: #E0C38C; /* 悬停或激活变成金色 */
  font-weight: bold;
  border-bottom: 2px solid #D4AF37;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    text-align: center;
  }
  .nav-links {
    margin-top: 15px;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>