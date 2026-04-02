<template>
  <div class="shop-home-page">
    <div class="content-wrapper">
      <!-- 背景书法字 -->
      <img :src="textYaoCi" alt="窑瓷书法" class="bg-text text-yaoci">
      <img :src="textJianZhi" alt="剪纸书法" class="bg-text text-jainzhi">
      
      <!-- 3D 轮播图容器 -->
      <div class="carousel-container">
        <div class="carousel-track">
          <div
            v-for="(slide, index) in slides"
            :key="slide.id"
            class="slide-item"
            :style="getSlideStyle(index)"
            @click="goToSlide(index)"
          >
            <img :src="slide.src" :alt="slide.alt">
          </div>
        </div>
      </div>

      <!-- 文字和按钮 -->
      <div class="cta-section">
        <p>欢迎来到剪釉双坊创意商城</p>
        <button @click="navigateToShop">点击进入商城</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';

// --- 图片资源引入 ---
// ⚠️ 请确保您已将这些图片按命名放入 src/assets/images/ 文件夹
import carouselImg1 from '@/assets/images/shop/shop_carousel_1.png';
import carouselImg2 from '@/assets/images/shop/shop_carousel_2.png';
import carouselImg3 from '@/assets/images/shop/shop_carousel_3.png';
import carouselImg4 from '@/assets/images/shop/shop_carousel_4.png';
import carouselImg5 from '@/assets/images/shop/shop_carousel_5.png';
import textYaoCi from '@/assets/images/shop/text_yaoci.png'; // "窑瓷" 书法字
import textJianZhi from '@/assets/images/shop/text_jainzhi.png'; // "剪纸" 书法字

// --- 路由 ---
const router = useRouter();
const navigateToShop = () => {
  router.push('/shop-main'); // 跳转到商城主页
};

// --- 轮播图逻辑 ---
const slides = ref([
  { id: 1, src: carouselImg1, alt: '作品一' },
  { id: 2, src: carouselImg2, alt: '作品二' },
  { id: 3, src: carouselImg3, alt: '作品三' },
  { id: 4, src: carouselImg4, alt: '作品四' },
  { id: 5, src: carouselImg5, alt: '作品五' },
]);

const currentIndex = ref(0);
const timer = ref(null);

// 计算每个卡片的动态样式
const getSlideStyle = (index) => {
  const total = slides.value.length;
  let offset = index - currentIndex.value;

  // 处理循环，让-4变成+1，+4变成-1
  if (offset > total / 2) offset -= total;
  if (offset < -total / 2) offset += total;
  
  const isCenter = offset === 0;
  const isAdjacent = Math.abs(offset) === 1;

  const transform = `
    translateX(${offset * 200}px) 
    scale(${isCenter ? 1.2 : (isAdjacent ? 1 : 0.8)}) 
    rotateY(${offset * -15}deg)
  `;
  
  const zIndex = total - Math.abs(offset);
  const filter = isCenter ? 'brightness(1)' : 'brightness(0.7)';

  return {
    transform,
    zIndex,
    filter,
    cursor: isCenter ? 'default' : 'pointer'
  };
};

// 切换到指定幻灯片
const goToSlide = (index) => {
  currentIndex.value = index;
};

// 自动播放
const startAutoPlay = () => {
  stopAutoPlay();
  timer.value = setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % slides.value.length;
  }, 2000); // 2秒切换一次
};

const stopAutoPlay = () => {
  if (timer.value) {
    clearInterval(timer.value);
  }
};

onMounted(() => {
  startAutoPlay();
});

onUnmounted(() => {
  stopAutoPlay();
});
</script>

<style scoped>
.shop-home-page {
  width: 100%;
  height: calc(100vh - 160px); /* 假设头部和尾部总高160px, 可自行调整 */
  min-height: 800px;
  background-image: url('@/assets/images/shop/shop_background.png');
  background-size: cover;
  background-position: center;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  position: relative;
}

.content-wrapper {
  position: relative;
  width: 100%;
  max-width: 1400px;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

/* 背景书法字通用样式（保留原有） */
.bg-text {
  position: absolute;
  pointer-events: none;
  opacity: 0.9;
}

/* 窑瓷书法字：调整大小+左侧位置 */
.text-yaoci {
  width: 300px; 
  top: 50%; 
  left: 2%; 
  transform: translateY(-50%); 
}

/* 剪纸书法字：调整大小+右侧位置 */
.text-jainzhi {
  width: 380px; 
  top: 40%; 
  right: 1%; 
  transform: translateY(-50%); 
}

/* 轮播图核心样式 */
.carousel-container {
  height: 500px;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  perspective: 1500px; /* 开启3D透视 */
  margin-top: 50px;
}

.carousel-track {
  position: relative;
  width: 300px; /* 仅作为定位参考 */
  height: 400px;
  transform-style: preserve-3d;
}

.slide-item {
  position: absolute;
  top: 0;
  left: 0;
  width: 300px;
  height: 400px;
  transition: transform 0.6s ease-out, filter 0.6s ease-out;
  border-radius: 0; /* 若图片自带圆角，可设为0 */
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2); /* 弱化阴影，避免遮挡图片边框 */
  background-color: transparent; /* 图片加载前底色改为透明（可选） */
  overflow: hidden;
}

.slide-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  /* 图片自带蓝色装饰边框，所以这里不需要再加边框 */
}

/* 文字和按钮区域 */
.cta-section {
  text-align: center;
  color: #fff;
  margin-top: 40px;
  z-index: 100;
}

.cta-section p {
  font-size: 20px;
  text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.7);
}

.cta-section button {
  margin-top: 15px;
  padding: 12px 40px;
  font-size: 18px;
  color: #4a2b1a;
  background-color: rgba(222, 184, 135, 0.8); /* 类似图中的米色 */
  border: 2px solid #fff;
  border-radius: 30px;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(5px);
}

.cta-section button:hover {
  background-color: rgba(255, 255, 255, 0.9);
  color: #333;
  transform: scale(1.05);
}

/* 响应式调整 */
@media (max-width: 1200px) {
  .text-yaoci, .text-jainzhi { width: 300px; }
  .getSlideStyle { /* 简化变换以适应更小的屏幕 */
    transform: translateX(calc(var(--offset) * 150px)) scale(calc(1 - (var(--abs-offset) * 0.2)));
  }
}

@media (max-width: 768px) {
  .bg-text { display: none; } /* 小屏幕隐藏背景字 */
  .slide-item { width: 200px; height: 280px; }
  .carousel-container { height: 350px; }
  .getSlideStyle {
     transform: translateX(calc(var(--offset) * 100px)) scale(calc(1 - (var(--abs-offset) * 0.2)));
  }
}
</style>