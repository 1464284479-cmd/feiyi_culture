<template>
  <div class="gallery-page">
    
    <!-- 1. 顶部 Banner (新增点击播放按钮) -->
    <div class="banner-section reveal-on-scroll">
      <img src="../assets/images/gallery_banner.png" alt="千年吉州窑" class="banner-img" />
      
      <!-- 🔥🔥🔥 新增：点击了解更多按钮 🔥🔥🔥 -->
      <div class="banner-overlay">
        <div class="play-btn" @click="openVideo">
          <span class="icon">▶</span>
          <span class="text">点击了解更多</span>
          <span class="hand-icon">👆</span>
        </div>
      </div>
    </div>

    <!-- 2. 吉州窑简史 -->
    <section class="section-block history-section reveal-on-scroll">
      <div class="section-title-wrapper">
        <img src="../assets/images/section_title_bg.png" class="title-bg" />
        <h2 class="section-title">吉州窑简史</h2>
      </div>

      <div class="history-content-box inner-card"> 
        <div class="history-img">
          <img src="../assets/images/history_book.png" alt="历史书籍" />
        </div>
        <div class="history-text">
          <p>
            吉州窑是中国宋代著名民间瓷窑，位于江西吉安永和镇，烧造于晚唐至元末（历时近 700 年），为江南地区综合性瓷窑代表。以黑釉瓷闻名，独创木叶天目（天然树叶入釉形成叶脉纹理）、剪纸贴花（民俗纹样贴饰）等工艺，茶盏等器型适配宋代斗茶风尚，胎质疏松保温，釉色丰富多变。作为 “海上陶瓷之路” 重要节点，产品远销海外。
          </p>
          <p>
            1980 年窑址列为全国重点文保单位，2006 年烧制技艺入选国家级非遗。当代通过龙窑复烧与文创开发，让木叶天目等传统工艺焕发新生，成为中国陶瓷文化重要遗产。
          </p>
        </div>
      </div>
    </section>

    <!-- 3. 吉州窑碗展 -->
    <section class="section-block exhibition-section reveal-on-scroll">
      <div class="section-title-wrapper">
        <img src="../assets/images/section_title_bg.png" class="title-bg" />
        <h2 class="section-title">吉州窑碗展</h2>
      </div>

      <div class="scrolls-container">
        <div class="scroll-frame staggered-child">
          <img src="../assets/images/scroll.png" alt="画卷背景" class="scroll-image">
          <div class="scroll-content">
            <img src="../assets/images/bowl_strip_1.png" alt="吉州窑作品" class="bowl-strip-img">
          </div>
        </div>
        <div class="scroll-frame staggered-child" style="transition-delay: 0.2s;">
          <img src="../assets/images/scroll.png" alt="画卷背景" class="scroll-image">
          <div class="scroll-content">
            <img src="../assets/images/bowl_strip_2.png" alt="吉州窑作品" class="bowl-strip-img">
          </div>
        </div>
      </div>
    </section>

    <!-- 4. 每日文物 -->
    <section class="daily-artifact-section reveal-on-scroll">
      <div class="section-title-wrapper">
        <img src="../assets/images/section_title_bg.png" class="title-bg" />
        <h2 class="section-title">每日文物</h2>
      </div>

      <div class="artifact-display-area">
        <div class="arrow arrow-left" @click="prevArtifact">&lt;</div>
        
        <div class="artifact-content-wrapper">
          <div v-if="artifacts.length === 0" class="loading-text">
            正在从历史长河中打捞文物数据...
          </div>

          <Transition name="artifact-fade" mode="out-in">
            <div v-if="artifacts.length > 0" class="artifact-content" :key="currentArtifact.id">
              <div class="artifact-img-wrapper">
                <img :src="getImageUrl(currentArtifact.image_name)" :alt="currentArtifact.title" />
              </div>
              
              <div class="artifact-info">
                <h3>每日文物 | {{ currentArtifact.title }}</h3>
                <ul class="artifact-meta">
                  <li><strong>类别：</strong>{{ currentArtifact.category }}</li>
                  <li><strong>年代：</strong>{{ currentArtifact.era }}</li>
                  <li><strong>规格：</strong>{{ currentArtifact.specs }}</li>
                  <li><strong>现藏：</strong>{{ currentArtifact.location }}</li>
                </ul>
                <p class="artifact-desc">
                  {{ currentArtifact.description }}
                </p>
                <div class="artifact-pagination">
                  第 {{ currentIndex + 1 }} / {{ artifacts.length }} 件珍宝
                </div>
              </div>
              
              <div class="mini-screen">
                 <img src="../assets/images/bowl_1.png" alt="预览" />
              </div>
            </div>
          </Transition>
        </div>

        <div class="arrow arrow-right" @click="nextArtifact">&gt;</div>
      </div>
    </section>

    <!-- 5. 知识科普 -->
    <section class="section-block knowledge-section reveal-on-scroll">
      <div class="section-title-wrapper">
        <img src="../assets/images/section_title_bg.png" class="title-bg" />
        <h2 class="section-title">知识科普</h2>
      </div>

      <div class="knowledge-viewport">
        <Transition name="knowledge-fade" mode="out-in">
          <div v-if="currentSlide === 0" class="slide-page page-1" key="p1">
             <div class="poster-item"><img src="../assets/images/knowledge_1.jpg" alt="木叶纹" /></div>
             <div class="poster-item center-item"><img src="../assets/images/knowledge_2.jpg" alt="木叶纹细节" /></div>
             <div class="poster-item"><img src="../assets/images/knowledge_3.jpg" alt="纹样" /></div>
          </div>
          <div v-else-if="currentSlide === 1" class="slide-page page-2" key="p2">
             <div class="big-layout-wrapper"><img src="../assets/images/knowledge_page_2.png" alt="吉州窑纹样科普" /></div>
          </div>
          <div v-else-if="currentSlide === 2" class="slide-page page-3" key="p3">
             <div class="scroll-wrapper-box">
                <div class="horizontal-scroll-list" ref="scrollContainer" @wheel.prevent="handleWheelScroll" @mousedown="startDrag" @mousemove="onDrag" @mouseup="stopDrag" @mouseleave="stopDrag">
                  <div class="scroll-item" v-for="n in 10" :key="n">
                    <img :src="`/images/patterns/pattern_${n}.png`" onerror="this.src='https://via.placeholder.com/200x300?text=Pattern'" draggable="false" />
                  </div>
                </div>
             </div>
          </div>
        </Transition>
      </div>
      
      <div class="gallery-controls">
        <span class="control-arrow" @click="prevSlide">&larr;</span>
        <div class="dots-container">
          <span v-for="i in 3" :key="i" class="dot" :class="{ active: currentSlide === i-1 }" @click="setSlide(i-1)"></span>
        </div>
        <span class="control-arrow" @click="nextSlide">&rarr;</span>
      </div>
    </section>

    <!-- 🔥🔥🔥 新增：视频弹窗 🔥🔥🔥 -->
    <Transition name="modal">
      <div v-if="showVideoModal" class="video-modal-mask" @click.self="closeVideo">
        <div class="video-modal-content">
          <button class="close-btn" @click="closeVideo">×</button>
          <video controls autoplay class="main-video">
            <source :src="videoPath" type="video/mp4">
            您的浏览器不支持视频播放。
          </video>
        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

// --- 入场动画 ---
onMounted(() => {
  const observerOptions = { root: null, rootMargin: '0px', threshold: 0.1 };
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => { if (entry.isIntersecting) entry.target.classList.add('is-visible'); });
  }, observerOptions);
  document.querySelectorAll('.reveal-on-scroll').forEach(el => observer.observe(el));
  fetchArtifacts();
});

// --- 🔥🔥🔥 新增：视频播放逻辑 🔥🔥🔥 ---
const showVideoModal = ref(false);
// 视频存放路径：public/videos/jizhou_intro.mp4
const videoPath = '/videos/jizhou_intro.mp4'; 

const openVideo = () => {
  showVideoModal.value = true;
};
const closeVideo = () => {
  showVideoModal.value = false;
};

// --- 每日文物 ---
const artifacts = ref([]);
const currentIndex = ref(0);
const fetchArtifacts = async () => {
  try {
    // 💡 无论本地还是服务器，统一请求 /api/artifacts
    // 本地靠 Vite 代理转发，服务器靠 Nginx 转发
    const response = await fetch('/api/artifacts');
    
    if (!response.ok) throw new Error('Network error');
    artifacts.value = await response.json();
  } catch (error) {
    console.error("获取文物数据失败:", error);
  }
};
const currentArtifact = computed(() => artifacts.value[currentIndex.value] || {});
const prevArtifact = () => { currentIndex.value = (currentIndex.value - 1 + artifacts.value.length) % artifacts.value.length; };
const nextArtifact = () => { currentIndex.value = (currentIndex.value + 1) % artifacts.value.length; };
const getImageUrl = (name) => {
  if (!name) return '';
  return new URL(`../assets/images/${name}`, import.meta.url).href;
};

// --- 知识科普 ---
const currentSlide = ref(0);
const totalSlides = 3;
const nextSlide = () => { currentSlide.value = (currentSlide.value + 1) % totalSlides; };
const prevSlide = () => { currentSlide.value = (currentSlide.value - 1 + totalSlides) % totalSlides; };
const setSlide = (index) => { currentSlide.value = index; };

// --- 拖拽滚动 ---
const scrollContainer = ref(null);
let isDragging = false, startX = 0, scrollLeft = 0;
const handleWheelScroll = (e) => { if (scrollContainer.value) scrollContainer.value.scrollLeft += e.deltaY * 1.5; };
const startDrag = (e) => { isDragging = true; if (!scrollContainer.value) return; startX = e.pageX - scrollContainer.value.offsetLeft; scrollLeft = scrollContainer.value.scrollLeft; scrollContainer.value.style.cursor = 'grabbing'; };
const onDrag = (e) => { if (!isDragging || !scrollContainer.value) return; e.preventDefault(); const x = e.pageX - scrollContainer.value.offsetLeft; const walk = (x - startX) * 2; scrollContainer.value.scrollLeft = scrollLeft - walk; };
const stopDrag = () => { isDragging = false; if (scrollContainer.value) scrollContainer.value.style.cursor = 'grab'; };
</script>

<style scoped>
/* 入场动画 */
.reveal-on-scroll { opacity: 0; transform: translateY(50px); transition: opacity 1s cubic-bezier(0.25, 0.46, 0.45, 0.94), transform 1s cubic-bezier(0.25, 0.46, 0.45, 0.94); }
.reveal-on-scroll.is-visible { opacity: 1; transform: translateY(0); }
.reveal-on-scroll .staggered-child { opacity: 0; transform: translateY(30px); transition: opacity 0.8s ease-out, transform 0.8s ease-out; }
.reveal-on-scroll.is-visible .staggered-child { opacity: 1; transform: translateY(0); }

.gallery-page { font-family: "Songti SC", "SimSun", serif; background-color: #FDF5E6; padding-bottom: 50px; overflow-x: hidden; }

/* 🔥🔥🔥 修改：Banner 区域 & 按钮样式 🔥🔥🔥 */
.banner-section { width: 100%; height: 800px; overflow: hidden; position: relative; }
.banner-img { width: 100%; height: 100%; object-fit: cover; }
.banner-overlay {
  position: absolute;
  bottom: 100px; /* 调整按钮垂直位置 */
  right: 100px;  /* 调整按钮水平位置 */
  z-index: 10;
}
.play-btn {
  background-color: rgba(69, 21, 2, 0.85); /* 深棕色背景 */
  color: #E6CFA2; /* 金色文字 */
  padding: 15px 35px;
  border-radius: 50px;
  border: 2px solid #E6CFA2;
  font-size: 20px;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.5);
  transition: all 0.3s ease;
  animation: pulse 2s infinite; /* 呼吸动画 */
}
.play-btn:hover {
  background-color: #E6CFA2;
  color: #451502;
  transform: scale(1.05);
}
.play-btn .icon { font-size: 18px; }
.play-btn .hand-icon { font-size: 22px; animation: point 1s infinite alternate; }

@keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(230, 207, 162, 0.4); } 70% { box-shadow: 0 0 0 15px rgba(230, 207, 162, 0); } 100% { box-shadow: 0 0 0 0 rgba(230, 207, 162, 0); } }
@keyframes point { from { transform: translateX(0); } to { transform: translateX(5px); } }

/* 🔥🔥🔥 新增：视频弹窗样式 🔥🔥🔥 */
.video-modal-mask {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0,0,0,0.85);
  z-index: 9999;
  display: flex; justify-content: center; align-items: center;
  backdrop-filter: blur(5px);
}
.video-modal-content {
  position: relative;
  width: 80%;
  max-width: 1000px;
  background: #000;
  border-radius: 10px;
  box-shadow: 0 20px 50px rgba(0,0,0,0.5);
  border: 2px solid #E6CFA2;
}
.main-video { width: 100%; height: auto; display: block; border-radius: 8px; outline: none; }
.close-btn {
  position: absolute;
  top: -40px; right: -40px;
  font-size: 40px; color: #FFF;
  background: none; border: none;
  cursor: pointer;
  transition: transform 0.3s;
}
.close-btn:hover { transform: rotate(90deg); color: #E6CFA2; }

/* Vue 弹窗动画 */
.modal-enter-active, .modal-leave-active { transition: opacity 0.3s; }
.modal-enter-from, .modal-leave-to { opacity: 0; }

/* 其他样式保持不变 */
.section-title-wrapper { position: relative; width: 300px; margin: 60px auto 40px auto; text-align: center; display: flex; justify-content: center; align-items: center; }
.title-bg { width: 100%; height: auto; }
.section-title { position: absolute; color: #8B5A2B; font-size: 34px; font-weight: bold; letter-spacing: 2px; margin: 0; top: 50%; transform: translateY(-55%); }
.history-section { width: 1000px; margin: 0 auto; }
.history-content-box { background-color: #2C2C2C; border-radius: 20px; padding: 40px; display: flex; align-items: center; color: #D4AF37; box-shadow: 0 10px 20px rgba(0,0,0,0.2); position: relative; transition: transform 0.3s; }
.history-content-box:hover { transform: translateY(-5px); }
.history-img { width: 30%; margin-right: 30px; }
.history-img img { width: 100%; transform: scale(1.1) rotate(-5deg); box-shadow: 5px 5px 15px rgba(0,0,0,0.5); }
.history-text { flex: 1; font-size: 16px; line-height: 1.8; text-align: justify; }
.exhibition-section { width: 1100px; margin: 0 auto; }
.scrolls-container { display: flex; justify-content: space-around; margin-top: 20px; }
.scroll-frame { width: 700px; height: 1150px; position: relative; }
.scroll-image { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }
.scroll-content { position: absolute; z-index: 2; top: 12%; left: 16%; width: 68%; height: 76%; overflow: hidden; display: flex; justify-content: center; align-items: center; }
.bowl-strip-img { width: 80%; height: 100%; object-fit: cover; display: block; transition: transform 0.4s; }
.bowl-strip-img:hover { transform: scale(1.03); }
.daily-artifact-section { background-image: url('../assets/images/artifact_bg.png'); background-color: #D2B48C; background-size: cover; padding: 40px 0 80px 0; margin-top: 60px; }
.artifact-display-area { width: 1100px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; }
.arrow { font-size: 60px; color: #6B4226; cursor: pointer; opacity: 0.6; transition: all 0.3s; user-select: none; }
.arrow:hover { opacity: 1; transform: scale(1.1); }
.artifact-content-wrapper { flex: 1; width: 90%; min-height: 500px; position: relative; }
.loading-text { text-align: center; font-size: 20px; color: #6B4226; padding: 100px 0; font-weight: bold; }
.artifact-content { display: flex; align-items: flex-start; width: 100%; position: relative; }
.artifact-img-wrapper { width: 300px; margin-right: 40px; }
.artifact-img-wrapper img { width: 100%; filter: drop-shadow(10px 10px 15px rgba(0,0,0,0.4)); border-radius: 5px; }
.mini-screen { position: absolute; top: 0; right: 0; width: 150px; border-radius: 5px; overflow: hidden; }
.mini-screen img { width: 100%; display: block; opacity: 0.8; }
.artifact-info { flex: 1; color: #4B3822; }
.artifact-info h3 { font-size: 28px; font-weight: bold; color: #3D2B1F; border-bottom: 2px solid #A0522D; padding-bottom: 12px; margin-bottom: 25px; display: inline-block; }
.artifact-meta { list-style: none; padding: 0; margin-bottom: 30px; font-size: 18px; font-weight: 1000; line-height: 2; color: #6B4226; }
.artifact-meta strong { font-weight: bold; color: #3D2B1F; margin-right: 8px; }
.artifact-desc { font-size: 18px; line-height: 2.0; text-align: justify; font-weight: bold; }
.artifact-pagination { margin-top: 20px; font-size: 16px; font-weight: bold; color: #7c3502ff; text-align: right; opacity: 0.7; }
.knowledge-section { width: 1200px; margin: 0 auto; padding-bottom: 60px; }
.knowledge-viewport { min-height: 550px; position: relative; overflow: hidden; display: flex; justify-content: center; align-items: center; margin-top: 30px; }
.slide-page { width: 100%; display: flex; justify-content: center; align-items: center; gap: 20px; }
.page-1 .poster-item { width: 280px; height: 400px; overflow: hidden; border: 5px solid #8B4513; box-shadow: 0 5px 15px rgba(0,0,0,0.2); transition: all 0.3s; }
.page-1 .poster-item:hover { transform: translateY(-10px); box-shadow: 0 15px 25px rgba(0,0,0,0.3); }
.page-1 .poster-item img { width: 100%; height: 100%; object-fit: cover; }
.page-1 .center-item { width: 320px; height: 450px; z-index: 2; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }
.page-2 .big-layout-wrapper { width: 100%; max-width: 1100px; padding: 10px; background: transparent; }
.page-2 img { width: 100%; height: auto; display: block; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
.page-3 .scroll-wrapper-box { width: 1100px; height: 450px; background-color: #3e3a33; border: 8px solid #2c2824; padding: 20px; border-radius: 10px; box-sizing: border-box; display: flex; align-items: center; }
.horizontal-scroll-list { display: flex; gap: 30px; overflow-x: auto; overflow-y: hidden; width: 100%; height: 100%; padding: 10px; cursor: grab; scrollbar-width: none; -ms-overflow-style: none; }
.horizontal-scroll-list::-webkit-scrollbar { display: none; }
.scroll-item { flex: 0 0 auto; width: 220px; height: 340px; background-color: #000; border: 2px solid #D4AF37; border-radius: 10px; overflow: hidden; transition: transform 0.3s; user-select: none; }
.scroll-item:hover { transform: scale(1.05); z-index: 10; }
.scroll-item img { width: 100%; height: 100%; object-fit: contain; pointer-events: none; }
.gallery-controls { margin-top: 40px; display: flex; justify-content: center; align-items: center; gap: 20px; }
.control-arrow { font-size: 40px; color: #8B4513; cursor: pointer; user-select: none; font-weight: bold; transition: color 0.3s; }
.control-arrow:hover { color: #D4AF37; }
.dots-container { display: flex; gap: 15px; }
.dot { width: 14px; height: 14px; border-radius: 50%; background-color: #ccc; cursor: pointer; transition: all 0.3s; }
.dot.active { background-color: #8B4513; transform: scale(1.3); }

/* --- 🔥🔥🔥 3. Vue 切换动画 🔥🔥🔥 --- */
.artifact-fade-enter-active, .artifact-fade-leave-active { transition: opacity 0.5s ease; }
.artifact-fade-enter-from, .artifact-fade-leave-to { opacity: 0; }
.knowledge-fade-enter-active, .knowledge-fade-leave-active { transition: all 0.5s ease; }
.knowledge-fade-enter-from, .knowledge-fade-leave-to { opacity: 0; transform: scale(0.98); }

@media (max-width: 768px) {
  .history-content-box, .scrolls-container, .artifact-content, .knowledge-gallery, .page-1, .page-2, .page-3 { flex-direction: column; }
  .history-img { width: 60%; margin: 0 auto 20px auto; }
  .scroll-frame { width: 450px; height: 800px; background-size: contain; padding: 80px 50px; }
  .artifact-img-wrapper { width: 60%; margin: 0 auto 20px auto; }
  .mini-screen { position: static; width: 100px; margin: 10px auto; }
  .page-3 .scroll-wrapper-box { width: 100%; height: auto; }
  .horizontal-scroll-list { flex-direction: row; }
  .banner-overlay { bottom: 20px; right: 20px; }
  .play-btn { font-size: 16px; padding: 10px 25px; }
}
</style>