<template>
  <div class="materials-page">
    
    <!-- 1. 顶部转盘 Banner 区域 -->
    <div class="banner-area">
      <!-- 静态背景图 -->
      <div class="banner-bg">
        <img src="/images/materials/banner_bg.jpg" alt="背景" />
      </div>

      <!-- 动态转盘容器 -->
      <div class="turntable-wrapper">
        <!-- 中心的圆图 (中国地图) -->
        <div class="center-piece">
          <img src="/images/materials/center_map.png" alt="Center" />
        </div>

        <!-- 旋转的轮盘 -->
        <div class="rotating-wheel">
          <!-- 循环生成8个扇形区域的图片 -->
          <div 
            class="wheel-item" 
            v-for="(item, index) in categories" 
            :key="index"
            :style="{ transform: `rotate(${index * 45}deg) translateY(-280px)` }"
            @click="scrollToCategory(item.id)"
          >
             <!-- 点击事件绑定在上面：scrollToCategory -->
             <img :src="item.previews[0]" alt="icon" />
          </div>
        </div>
      </div>
    </div>

    <!-- 2. 素材列表区域 -->
    <div class="container list-container">
      
      <!-- 侧边红线装饰 -->
      <div class="left-line"></div>

      <!-- 循环渲染 8 个分类 -->
      <!-- 关键修改：添加 :id="cat.id" 用于锚点定位 -->
      <div 
        class="category-row" 
        v-for="(cat, index) in categories" 
        :key="index" 
        :id="cat.id"
      >
        
        <!-- 左侧：圆形图标与标题 -->
        <div class="cat-header">
          <div class="cat-circle">
            <img :src="cat.previews[0]" alt="icon" />
          </div>
          <h3 class="cat-title">{{ cat.name }}</h3>
        </div>

        <!-- 中间：预览图片展示 (取前4-5张) -->
        <div class="cat-preview-grid">
          <div class="preview-img" v-for="(img, idx) in cat.previews.slice(0, 5)" :key="idx">
            <img :src="img" alt="preview" />
          </div>
        </div>

        <!-- 右侧：查看更多按钮 -->
        <div class="cat-action">
          <button class="btn-view-more" @click="goToDetail(cat.id)">
            点击查看更多
          </button>
        </div>

        <!-- 底部分隔线 (虚线) -->
        <div class="row-divider"></div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

// 模拟数据库数据
const categories = reactive([
  {
    id: 'fengwen',
    name: '锦簇团纹”',
    previews: [
      '/images/materials/fengwen/1.png',
      '/images/materials/fengwen/2.png',
      '/images/materials/fengwen/3.png',
      '/images/materials/fengwen/4.png',
      '/images/materials/fengwen/5.png'
    ]
  },
  {
    id: 'flower',
    name: '雅卉清纹',
    previews: [
      '/images/materials/flower/1.png',
      '/images/materials/flower/2.png',
      '/images/materials/flower/3.png',
      '/images/materials/flower/4.png',
      '/images/materials/flower/5.png'
    ]
  },
  {
    id: 'fish',
    name: '鱼嬉吉纹',
    previews: [
      '/images/materials/fish/1.png',
      '/images/materials/fish/2.png',
      '/images/materials/fish/3.png',
      '/images/materials/fish/4.png',
      '/images/materials/fish/5.png'
    ]
  },
  {
    id: 'xi',
    name: '喜吉福纹',
    previews: [
      '/images/materials/xi/1.png',
      '/images/materials/xi/2.png',
      '/images/materials/xi/3.png',
      '/images/materials/xi/4.png',
      '/images/materials/xi/5.png'
    ]
  },
  {
    id: 'huadian',
    name: '戏韵纹绘',
    previews: [
      '/images/materials/huadian/1.png',
      '/images/materials/huadian/2.png',
      '/images/materials/huadian/3.png',
      '/images/materials/huadian/4.png',
      '/images/materials/huadian/5.png'
    ]
  },
  {
    id: 'blessing',
    name: '俗韵人物纹',
    previews: [
      '/images/materials/blessing/1.png',
      '/images/materials/blessing/2.png',
      '/images/materials/blessing/3.png',
      '/images/materials/blessing/4.png',
      '/images/materials/blessing/5.png'
    ]
  },
  {
    id: 'lantern',
    name: '吉灯祥纹',
    previews: [
      '/images/materials/lantern/1.png',
      '/images/materials/lantern/2.png',
      '/images/materials/lantern/3.png',
      '/images/materials/lantern/4.png',
      '/images/materials/lantern/5.png'
    ]
  },
  {
    id: 'zodiac',
    name: '瑞兽萌纹',
    previews: [
      '/images/materials/zodiac/1.png',
      '/images/materials/zodiac/2.png',
      '/images/materials/zodiac/3.png',
      '/images/materials/zodiac/4.png',
      '/images/materials/zodiac/5.png'
    ]
  }
]);

// 核心功能：点击转盘图标，平滑滚动到对应位置
const scrollToCategory = (id) => {
  const element = document.getElementById(id);
  if (element) {
    element.scrollIntoView({ 
      behavior: 'smooth', // 平滑滚动
      block: 'center'     // 滚动到屏幕中间
    });
  }
};

// 跳转到详情页
const goToDetail = (categoryId) => {
  router.push({ path: `/materials/${categoryId}` });
};
</script>

<style scoped>
.materials-page {
  background-color: #fff;
  font-family: "Songti SC", "SimSun", serif;
  overflow-x: hidden;
}

/* ================== Banner 转盘区域 ================== */
.banner-area {
  position: relative;
  width: 100%;
  height: 800px;
  background-color: #fdf5e6;
  overflow: hidden;
}

/* 静态背景 */
.banner-bg {
  width: 100%;
  height: 100%;
}
.banner-bg img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 转盘容器 */
.turntable-wrapper {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 700px; /* 转盘整体大小 */
  height: 700px;
}

/* 中心的圆（不转动） */
.center-piece {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 220px;
  height: 220px;
  border-radius: 50%;
  background: #fff;
  z-index: 10;
  box-shadow: 0 0 20px rgba(0,0,0,0.2);
  display: flex;
  justify-content: center;
  align-items: center;
}
.center-piece img {
  width: 90%;
  height: 90%;
  object-fit: contain;
}

/* 旋转层 */
.rotating-wheel {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  /* 开启旋转动画 */
  animation: rotate-wheel 20s linear infinite;
}

/* 悬停时暂停转动 */
.turntable-wrapper:hover .rotating-wheel {
  animation-play-state: paused;
}

/* 转盘上的图片元素 */
.wheel-item {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 150px; /* 图片大小 */
  height: 150px;
  /* 初始居中，通过 transform 移动到圆周上 */
  /* margin 修正偏移 */
  margin-top: -60px; 
  margin-left: -60px;
  
  transition: transform 0.3s;
  cursor: pointer;
}

.wheel-item img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  filter: drop-shadow(0 5px 5px rgba(0,0,0,0.2));
}

/* 悬停放大效果 */
.wheel-item:hover {
  /* 保持原有位置的同时放大 */
  filter: drop-shadow(0 0 10px rgba(255, 0, 0, 0.5));
  z-index: 20;
}
.wheel-item:hover img {
  transform: scale(1.3); /* 只放大图片 */
}

@keyframes rotate-wheel {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* ================== 列表区域 ================== */
.list-container {
  width: 1200px;
  max-width: 95%;
  margin: 0 auto;
  position: relative;
  padding: 50px 0;
}

/* 左侧贯穿红线 */
.left-line {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 80px; /* 调整这个值对齐圆圈中心 */
  width: 2px;
  background-color: #E89A9A;
  z-index: 0;
}

.category-row {
  display: flex;
  align-items: center;
  position: relative;
  padding: 10px 0;
  z-index: 1; /* 在红线之上 */
  /* 增加 scroll-margin，确保跳转时不会被顶部固定导航栏遮挡（如果有的话） */
  scroll-margin-top: 100px; 
}

/* 分隔线 */
.row-divider {
  position: absolute;
  bottom: 0;
  left: 150px;
  right: 0;
  height: 3px;
  background-image: linear-gradient(to right, #800202ff 50%, transparent 50%);
  background-size: 6px 3px; /* 3px粗，6px间距 */
  opacity: 0.5;
  border: none;
}
/* 左侧 Header */
.cat-header {
  width: 150px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  margin-right: 40px;
}
.cat-circle {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background: #fff;
  border: 4px solid #E89A9A; /* 粉红边框 */
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
  margin-bottom: 10px;
}
.cat-circle img {
  width: 80%;
  height: 80%;
  object-fit: contain;
}
.cat-title {
  font-size: 30px;
  font-weight: 900;
  color: #8B4513; /* 深棕（楚文化传统色） */
  text-shadow: 1px 1px 2px rgba(0,0,0,0.2); /* 轻微阴影增加质感 */
}

/* 中间预览图 */
.cat-preview-grid {
  flex: 1;
  display: flex;
  gap: 30px;
  justify-content: flex-start;
}
.preview-img {
  width: 150px;
  height: 150px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.preview-img img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  transition: transform 0.3s;
}
.preview-img:hover img {
  transform: scale(1.1);
}

/* 右侧按钮 */
.cat-action {
  width: 150px;
  display: flex;
  justify-content: flex-end;
}
.btn-view-more {
  background-color: #C19D68; /* 金棕色 */
  color: #fff;
  border: none;
  padding: 8px 20px;
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.3s;
}
.btn-view-more:hover {
  background-color: #8B5A2B;
}

/* 最后一行的分割线和红线处理 */
.category-row:last-child .row-divider {
  display: none;
}
</style>