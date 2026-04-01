<template>
  <footer class="site-footer">
    <div class="container footer-content">
      <div class="footer-left">
        <img src="@/assets/images/logo.png" alt="Logo" class="footer-logo"/>
        <div class="footer-address">
          <h4>双华剪釉</h4>
          <p>中国湖北省武汉市江夏区<br>金融港北路<br>中国</p>
        </div>
      </div>
      <div class="footer-right">
        <nav class="footer-nav">
          <router-link to="/">首页</router-link>
          <router-link to="/double-heritage">双遗数览</router-link>
          <router-link to="/window-gallery">窑韵图鉴</router-link>
          <router-link to="/patterns">剪纸纹样</router-link>
          <router-link to="/shop">非遗商城</router-link>
          <router-link to="/artisans">匠人故事</router-link>
          <router-link to="/contact">联系我们</router-link>
        </nav>
        <div class="footer-links">
          <a href="#">使用条款</a> • <a href="#">隐私政策</a>
        </div>
        <p class="copyright">版权所有 @ 楚赣镂窑 2026</p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.container {
  width: 1200px;
  max-width: 95%;
  margin: 0 auto;
}

.site-footer {
  background-color: #5D0E0E;
  color: #fff;
  padding: 40px 0;
  margin-top: auto; /* 关键：配合 flex 布局让 footer 沉底 */
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}

.footer-left {
  display: flex;
  flex-direction: row;  
  align-items: center; 
  gap: 30px;            
}
.footer-logo {
  width: 120px;
   height: auto;
  opacity: 1;  
  } 
.footer-address h4 {
  font-size: 16px;
  margin-bottom: 5px;
  margin-top: 0;
}
.footer-address p {
  font-size: 12px;
  line-height: 1.5;
  color: #ddd;
  margin: 0;
}

.footer-right {
  text-align: right;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.footer-nav a {
  color: #fff;
  margin-left: 30px;    /* 增加间距，防止字变大后挤在一起 */
  text-decoration: none;
  font-size: 20px;      /* ✅ 字体放大 (你可以改成 18px 或 24px) */
  font-weight: bold;    /* ✅ 加粗，让文字更显眼 */
  letter-spacing: 1px;  /* 稍微增加字与字之间的距离 */
  transition: color 0.3s; /* 增加一点鼠标悬停的平滑效果 */
}

/* 建议同时增加鼠标悬停变色效果，体验更好 */
.footer-nav a:hover {
  color: #E0C38C; /* 悬停变成金色 */
}

.footer-links a {
  color: #ccc;
  text-decoration: underline;
  font-size: 12px;
}

.copyright {
  font-size: 12px;
  color: #aaa;
  margin: 0;
}

@media (max-width: 768px) {
  .footer-content {
    flex-direction: column;
    text-align: center;
    align-items: center;
  }
  .footer-right {
    text-align: center;
    align-items: center;
    margin-top: 20px;
  }
}
</style>