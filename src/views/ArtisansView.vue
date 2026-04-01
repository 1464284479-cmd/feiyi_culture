<template>
  <div class="artisan-page">
    
    <!-- 1. 顶部 Banner 轮播区域 (保持不变) -->
    <div class="banner-section" @mouseenter="stopAutoPlay" @mouseleave="startAutoPlay">
      <div 
        v-for="(banner, index) in bannerList" 
        :key="index"
        class="banner-slide"
        :class="{ active: currentSlide === index }"
      >
        <img :src="banner.src" :alt="banner.alt" class="banner-img" />
        <div class="banner-text">
          <h1 class="main-title">{{ banner.title }}</h1>
          <p class="sub-title">{{ banner.subTitle }}</p>
        </div>
      </div>
      <div class="arrow arrow-left" @click="prevSlide">&lt;</div>
      <div class="arrow arrow-right" @click="nextSlide">&gt;</div>
      <div class="dots">
        <span 
          v-for="(banner, index) in bannerList" 
          :key="index" 
          class="dot" 
          :class="{ active: currentSlide === index }"
          @click="setSlide(index)"
        ></span>
      </div>
    </div>

    <!-- 动态波浪 SVG 分隔 (保持不变) -->
    <div class="wave-separator">
      <svg class="waves" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
      viewBox="0 24 150 28" preserveAspectRatio="none" shape-rendering="auto">
        <defs>
          <path id="gentle-wave" d="M-160 44c30 0 58-18 88-18s 58 18 88 18 58-18 88-18 58 18 88 18 v44h-352z" />
        </defs>
        <g class="parallax">
          <use xlink:href="#gentle-wave" x="48" y="0" fill="rgba(246,241,230,0.7)" />
          <use xlink:href="#gentle-wave" x="48" y="3" fill="rgba(246,241,230,0.5)" />
          <use xlink:href="#gentle-wave" x="48" y="5" fill="rgba(246,241,230,0.3)" />
          <use xlink:href="#gentle-wave" x="48" y="7" fill="#F6F1E6" />
        </g>
      </svg>
    </div>

    <!-- 2. 主体内容区域 (羊皮纸背景) -->
    <div class="paper-content">
      
      <!-- 守艺人介绍区域 -->
      <section class="section-block" ref="kilnSection">
        <div class="section-header">
          <span class="decoration-line left"></span><h2 class="section-title">窑火守艺人</h2><span class="decoration-line right"></span>
        </div>
         <div class="cards-container">
          <div v-for="(item, index) in kilnArtisans" :key="index" class="artisan-card kiln-style" @mousemove="handleCardMouseMove" @mouseleave="resetCardTransform">
            <div class="card-inner">
              <div class="avatar-wrapper"><img :src="item.image" :alt="item.name" /></div>
              <h3 class="artisan-name">{{ item.name }}</h3>
              <p class="artisan-desc">{{ item.desc }}</p>
              
              <!-- 🔥🔥🔥 修改这里：调用通用函数 handleReadMore，传入整个 item 对象 🔥🔥🔥 -->
              <div class="read-more" @click="handleReadMore(item)">点击了解更多 ▶</div>
            </div>
          </div>
        </div>
      </section>

      <section class="section-block" ref="paperSection">
        <div class="section-header red-theme">
          <span class="decoration-line left"></span><h2 class="section-title">鄂州剪纸守艺人</h2><span class="decoration-line right"></span>
        </div>
         <div class="cards-container">
          <div v-for="(item, index) in paperArtisans" :key="index" class="artisan-card paper-style" @mousemove="handleCardMouseMove" @mouseleave="resetCardTransform">
             <div class="card-inner">
              <div class="avatar-wrapper"><img :src="item.image" :alt="item.name" /></div>
              <h3 class="artisan-name">{{ item.name }}</h3>
              <p class="artisan-desc">{{ item.desc }}</p>
              
              <!-- 🔥🔥🔥 修改这里：调用通用函数 handleReadMore，传入整个 item 对象 🔥🔥🔥 -->
              <div class="read-more" @click="handleReadMore(item)">点击了解更多 ▶</div>
            </div>
          </div>
        </div>
      </section>

      <!-- 作品鉴赏区域 -->
      <section class="section-block" ref="gallerySection">
        <div class="section-header">
          <span class="decoration-line left"></span><h2 class="section-title">匠心独运 · 作品鉴赏</h2><span class="decoration-line right"></span>
        </div>
        <div class="gallery-filters">
          <button @click="setFilter('all')" :class="{ active: activeFilter === 'all' }">全部作品</button>
          <button @click="setFilter('kiln')" :class="{ active: activeFilter === 'kiln' }">窑火瓷艺</button>
          <button @click="setFilter('paper-cut')" :class="{ active: activeFilter === 'paper-cut' }">鄂州剪纸</button>
        </div>
        <div class="gallery-grid">
          <div v-for="item in filteredGallery" :key="item.src" class="gallery-item">
            <img :src="item.src" :alt="item.title" />
            <div class="gallery-overlay">
              <h3>{{ item.title }}</h3>
              <p>{{ item.creator }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 技艺探秘：陶艺工坊 -->
      <section class="section-block" ref="potteryTimelineSection">
        <div class="section-header">
          <span class="decoration-line left"></span><h2 class="section-title">技艺探秘 · 陶艺工坊</h2><span class="decoration-line right"></span>
        </div>
        <div class="timeline-container timeline-container-6-steps">
          <div v-for="(step, index) in potteryCraftSteps" :key="index" class="timeline-item">
            <div class="timeline-content">
              <div class="timeline-icon"><img :src="step.icon" :alt="step.title"/></div>
              <h3>{{ step.title }}</h3>
              <p>{{ step.desc }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 技艺探秘：剪纸工坊 -->
      <section class="section-block" ref="paperCutTimelineSection">
        <div class="section-header red-theme">
          <span class="decoration-line left"></span><h2 class="section-title">技艺探秘 · 剪纸工坊</h2><span class="decoration-line right"></span>
        </div>
        <div class="timeline-container timeline-container-6-steps red-theme">
          <div v-for="(step, index) in paperCutCraftSteps" :key="index" class="timeline-item">
            <div class="timeline-content paper-cut-theme">
              <div class="timeline-icon"><img :src="step.icon" :alt="step.title"/></div>
              <h3>{{ step.title }}</h3>
              <p>{{ step.desc }}</p>
            </div>
          </div>
        </div>
      </section>
      
      <!-- 寻根溯源 · 技艺地图 -->
      <section class="section-block" ref="mapSection">
         <div class="section-header">
          <span class="decoration-line left"></span><h2 class="section-title">寻根溯源 · 技艺地图</h2><span class="decoration-line right"></span>
        </div>
        <div class="map-showcase">
          <div class="map-area">
            <img :src="mapBg" alt="技艺地图" class="map-bg-img">
            <div 
              class="map-pin kiln-pin" 
              @click="setActiveLocation('kiln')" 
              :class="{ active: activeLocationId === 'kiln' }">
              <img :src="locationPin" alt="吉州窑产地">
              <span>吉州窑</span>
            </div>
            <div 
              class="map-pin paper-cut-pin" 
              @click="setActiveLocation('paper-cut')" 
              :class="{ active: activeLocationId === 'paper-cut' }">
               <img :src="locationPin" alt="鄂州剪纸产地">
              <span>鄂州剪纸</span>
            </div>
          </div>
          <div class="map-info-area">
            <Transition name="info-fade" mode="out-in">
              <div v-if="activeLocation" :key="activeLocation.id" class="info-card">
                <h3>{{ activeLocation.name }}</h3>
                <p class="info-origin"><strong>发源地：</strong>{{ activeLocation.origin }}</p>
                <p>{{ activeLocation.description }}</p>
              </div>
            </Transition>
          </div>
        </div>
      </section>

    </div>

    <!-- 🔥🔥🔥 新增：视频弹窗组件 🔥🔥🔥 -->
    <Transition name="modal">
      <div v-if="showVideoModal" class="video-modal-mask" @click.self="closeVideo">
        <div class="video-modal-content">
          <button class="close-btn" @click="closeVideo">×</button>
          <!-- key 属性确保切换视频时重新渲染 -->
          <video :key="currentVideoPath" controls autoplay class="main-video">
            <source :src="currentVideoPath" type="video/mp4">
            您的浏览器不支持视频播放。
          </video>
        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup>
import { reactive, ref, onMounted, onUnmounted, computed } from 'vue';

// --- 图片资源 ---
import bannerImg1 from '@/assets/images/artisan_banner.png'; 
import bannerImg2 from '@/assets/images/artisan_banner_2.png';
import img1 from '@/assets/images/artisan_1.png';
import img2 from '@/assets/images/artisan_2.png';
import img3 from '@/assets/images/artisan_3.png';
import img4 from '@/assets/images/artisan_4.png';
import img5 from '@/assets/images/artisan_5.png';
import img6 from '@/assets/images/artisan_6.png';
import gallery1 from '@/assets/images/gallery_kiln_1.png';
import gallery2 from '@/assets/images/gallery_kiln_2.png';
import gallery3 from '@/assets/images/gallery_paper_1.png';
import gallery4 from '@/assets/images/gallery_paper_2.png';
import gallery5 from '@/assets/images/gallery_kiln_3.png';
import gallery6 from '@/assets/images/gallery_paper_3.png';
import potteryIcon1 from '@/assets/images/pottery_icon_1.png';
import potteryIcon2 from '@/assets/images/pottery_icon_2.png';
import potteryIcon3 from '@/assets/images/pottery_icon_3.png';
import potteryIcon4 from '@/assets/images/pottery_icon_4.png';
import potteryIcon5 from '@/assets/images/pottery_icon_5.png';
import potteryIcon6 from '@/assets/images/pottery_icon_6.png';
import paperCutIcon1 from '@/assets/images/paper_cut_icon_1.png';
import paperCutIcon2 from '@/assets/images/paper_cut_icon_2.png';
import paperCutIcon3 from '@/assets/images/paper_cut_icon_3.png';
import paperCutIcon4 from '@/assets/images/paper_cut_icon_4.png';
import paperCutIcon5 from '@/assets/images/paper_cut_icon_5.png';
import paperCutIcon6 from '@/assets/images/paper_cut_icon_6.png';
import mapBg from '@/assets/images/map_bg.png';
import locationPin from '@/assets/images/location_pin.png';

// --- 轮播图与匠人卡片逻辑 (保持不变) ---
const currentSlide = ref(0);
const timer = ref(null);
const bannerList = [ { src: bannerImg1, alt: '匠人匠心', title: '匠人 · 匠心', subTitle: '鄂州剪韵守艺人' }, { src: bannerImg2, alt: '非遗传承', title: '非遗 · 传承', subTitle: '千年窑火生生不息' } ];
const nextSlide = () => { currentSlide.value = (currentSlide.value + 1) % bannerList.length; };
const prevSlide = () => { currentSlide.value = (currentSlide.value - 1 + bannerList.length) % bannerList.length; };
const setSlide = (index) => { currentSlide.value = index; };
const startAutoPlay = () => { if (timer.value) clearInterval(timer.value); timer.value = setInterval(nextSlide, 5000); };
const stopAutoPlay = () => { if (timer.value) clearInterval(timer.value); };
onUnmounted(() => { stopAutoPlay(); });

// --- 🔥🔥🔥 匠人数据 (新增 video 字段) 🔥🔥🔥 ---
// 请确保 /public/videos/ 目录下有对应的 mp4 文件
const kilnArtisans = reactive([ 
  { name: '段敏瑞', image: img1, desc: '段敏瑞是国家级非物质文化遗产“吉州窑陶瓷烧制技艺”吉安市代表性传承人，他同时担任吉州窑本觉坊创始人，拥有国家一级陶瓷装饰工资质，还获评省级陶瓷艺术大师。他深耕吉州窑陶瓷领域多年，在陶瓷装饰与传统烧制技艺上造诣深厚，尤其擅长将木叶纹、剪纸贴花等吉州窑经典技法与现代创作理念结合，作品既存古韵又含新意。此外，他通过本觉坊开展技艺教学与交流，多次在陶瓷赛事中展现实力，为吉州窑技艺的传承与创新注入活力。', video: '/videos/artisan_duan.mp4' }, 
  { name: '罗仲华', image: img2, desc: ' 罗仲华是吉州窑陶瓷烧制技艺吉安市非遗传承人，现任吉安嘉瑞实业公司总经理、吉州窑陶瓷协会会长，深耕吉州窑陶瓷设计研发领域超30年。他不仅研发推出近2000种陶瓷新品，还获国家专利授权76项，其《吉州窑四大名盏》等代表作品多次斩获国内重要陶瓷赛事金奖。此外，他曾赴日本、波兰等多国推广吉州窑文化，还整合65家相关企业及作坊成立产业知识联盟，助力吉州窑行业升级与庐陵文化传播。', video: '/videos/artisan_luo.mp4' }, 
  { name: '王启慧', image: img3, desc: '王启慧，女，汉族，中国籍，1988年生于江西吉安，是国家非物质文化遗产“吉州窑陶瓷烧制技艺”从业者，现为中国陶瓷艺术家、陶瓷高级工艺美术师。她深耕吉州窑陶瓷领域多年，擅长融合传统工艺与现代审美，在木叶纹、釉下彩绘等技法上钻研深厚，作品兼具古韵与新意。其创作以茶器、陈设瓷为主，多次参展，部分作品因精准复刻并创新表达传统釉色获关注，助力技艺传承与当代发展。', video: '/videos/artisan_wang.mp4' } 
]);
const paperArtisans = reactive([
  {
    name: '曹小琴',
    image: img4,
    desc: '曹小琴是湖北省工艺美术大师，同时担任鄂州雕花剪纸省级传承人，在剪纸创作与文化传播领域成果显著。她不仅精通鄂州剪纸的传统技法，还注重理论研究与技艺推广，主编的《鄂州雕花剪纸艺术》一书，系统梳理了鄂州剪纸的历史脉络、技艺特点与经典作品，为技艺传承提供了重要文献支撑。此外，她常代表鄂州剪纸参与国际文化交流活动，曾赴多个国家展示剪纸技艺，让鄂州雕花剪纸走出国门，成为中外文化交流的重要载体，也进一步提升了这门非遗技艺的国际影响力。',
    video: '/videos/artisan_cao.mp4' // 曹小琴保留视频
  },
  {
    name: '夏祖康',
    image: img5,
    desc: '夏祖康，世界名录 •国家级非物质文化遗产《鄂州雕花剪纸》项目省级代表性传承人、中华民族文化促进会剪纸艺术委员会会员，中央美术学院非遗研修生，南京大学剪纸研究会创研员、鄂州市非遗专家库专家。剪纸作品《鄂州传统花样》，被中央美术学院收藏，并用于非物质文化遗产教学之用。剪纸作品多次荣获中国非物质文化遗产博览会传统工艺剪纸比赛大奖，传承事迹多次被中央及省市媒体报道。',
    link: 'https://www.baidu.com/link?url=mWdJZx9xCsdO4yWtQV7TSvCU_VoPdwvEo2xi-SS25wBBisCPFpkgcueJKtlf7GYMBXxQdODHgtVLwW07q1RCKiCfFKwdlRma3oSuJ8--JJqt8mk5vNLHXnut3ZVF1FRE&wd=&eqid=a4c4bde00020210200000006695b619f'
  },
  {
    name: '张家忠',
    image: img6,
    desc: '张家忠是第三批国家级非物质文化遗产项目“鄂州雕花剪纸”代表性传承人，深耕剪纸领域数十年，是鄂州剪纸传统技艺的核心继承者之一。他的作品题材广泛，涵盖民俗生活、花鸟虫鱼、神话故事等，既保留鄂州剪纸“构图饱满、线条流畅、花样精巧”的传统特质，又融入对当代生活的观察。其创作的多幅传统花样作品，因兼具艺术价值与文化传承意义，被中国艺术研究院、鄂州市博物馆等专业机构收藏，还常通过技艺教学、非遗展演等活动，向大众普及鄂州剪纸文化。',
    link: 'https://www.baidu.com/link?url=wZfs1h_O6PTWjdER6x4uvdNj0cPog_porCwOeJ0dZv1PsL_9CBEeVEI-W5tsW11QcEQLBqKFiEKJk16p12QxEhlM2bYxRvp5gSaXEFJ5KE2-bwnCfVzNo_hyEaKk71SK&wd=&eqid=bbc48d360046842100000006695b63e0'
  }
]);

// --- 3D 卡片悬浮效果 ---
const handleCardMouseMove = (e) => { const card = e.currentTarget; const { left, top, width, height } = card.getBoundingClientRect(); const x = e.clientX - left; const y = e.clientY - top; const rotateX = -1 * ((y - height / 2) / (height / 2)) * 8; const rotateY = ((x - width / 2) / (width / 2)) * 8; card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`; const innerCard = card.querySelector('.card-inner'); innerCard.style.backgroundImage = `radial-gradient(circle at ${x}px ${y}px, rgba(255,255,255,0.2), transparent 40%)`; };
const resetCardTransform = (e) => { const card = e.currentTarget; card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)'; const innerCard = card.querySelector('.card-inner'); innerCard.style.backgroundImage = 'none'; };

// --- 🔥🔥🔥 视频弹窗逻辑 🔥🔥🔥 ---
const showVideoModal = ref(false);
const currentVideoPath = ref('');

const openVideo = (videoPath) => {
  if (videoPath) {
    currentVideoPath.value = videoPath;
    showVideoModal.value = true;
  } else {
    alert("暂无该匠人的视频资料");
  }
};
const handleReadMore = (item) => {
  if (item.link) {
    // 如果有链接，打开新窗口跳转
    window.open(item.link, '_blank');
  } else if (item.video) {
    // 如果有视频，打开视频弹窗
    openVideo(item.video);
  } else {
    alert("暂无更多资料");
  }
};
const closeVideo = () => {
  showVideoModal.value = false;
  currentVideoPath.value = ''; // 清空路径停止播放
};

// --- 作品画廊 ---
const galleryItems = reactive([ { src: gallery1, title: '玳瑁釉', creator: '曾平', category: 'kiln' }, { src: gallery3, title: '枕顶花', creator: '张家忠', category: 'paper-cut' }, { src: gallery2, title: '木叶纹黑釉瓷', creator: '知叶堂', category: 'kiln' }, { src: gallery5, title: '元青花', creator: '廖光荣', category: 'kiln' }, { src: gallery4, title: '龙跃楚天・飞桥通途', creator: '夏祖康', category: 'paper-cut' }, { src: gallery6, title: '龙舞盛世', creator: '张家忠', category: 'paper-cut' }, ]);
const activeFilter = ref('all');
const setFilter = (filter) => { activeFilter.value = filter; };
const filteredGallery = computed(() => { if (activeFilter.value === 'all') return galleryItems; return galleryItems.filter(item => item.category === activeFilter.value); });

// --- 工艺流程 ---
const potteryCraftSteps = reactive([ { icon: potteryIcon1, title: '原料 · 真空练泥', desc: '精选优质瓷土，通过真空处理，排除泥料中的气泡，使其质地更均匀、细腻。' }, { icon: potteryIcon2, title: '设计 · 配色揉泥', desc: '根据设计构想，将不同颜色的泥料按比例混合，反复揉捏，创造出独特的色彩基调。' }, { icon: potteryIcon3, title: '设计 · 绞揉花团', desc: '将多种色泥绞合揉制，形成如木纹、云雾般变幻莫测的自然纹理，是为绞胎。' }, { icon: potteryIcon4, title: '造型 · 拉坯', desc: '将泥团置于陶车中心，运用指尖的力量与智慧，随旋转拉伸，赋予器物最初的生命。' }, { icon: potteryIcon5, title: '造型 · 修坯', desc: '待坯体半干，精修其口、身、底足，使线条更流畅，器型更规整，肌理更完善。' }, { icon: potteryIcon6, title: '成品 · 入窑烧制', desc: '经干燥、上釉后，送入窑中。在千度高温的淬炼下，土与火交融，最终化为温润美瓷。' }, ]);
const paperCutCraftSteps = reactive([ { icon: paperCutIcon1, title: '构思画稿', desc: '创作的起点，匠人将腹稿或灵感绘制于纸上，确定剪纸的主题、构图与纹样。' }, { icon: paperCutIcon2, title: '选纸订稿', desc: '选用柔韧的宣纸，将画稿与数层宣纸叠放，并用针线沿边缘仔细固定，确保雕刻时不错位。' }, { icon: paperCutIcon3, title: '湿润粘贴', desc: '将订好的纸叠适当湿润，使其紧密粘贴在一起，便于刻刀游走，线条流畅。' }, { icon: paperCutIcon4, title: '精雕细刻', desc: '手持刻刀，心神合一。或阳刻，或阴刻，于方寸之间雕琢出细腻繁复的万千世界。' }, { icon: paperCutIcon5, title: '揭离分拣', desc: '将刻好的作品逐层小心揭开，如同揭晓秘密。每一张都是饱含心血的独立艺术品。' }, { icon: paperCutIcon6, title: '装裱成品', desc: '为脆弱的剪纸衬上底色，精心装裱。不仅为了保护，更是艺术呈现的最后一步。' }, ]);

// --- 技艺地图 ---
const locations = { kiln: { id: 'kiln', name: '吉州窑', origin: '江西吉安', description: '吉州窑创烧于晚唐，兴于五代、北宋，极盛于南宋。它以其丰富多样的装饰技法，如木叶纹、剪纸贴花、窑变釉等，在中国陶瓷史上独树一帜，是民间艺术与智慧的结晶。' }, 'paper-cut': { id: 'paper-cut', name: '鄂州雕花剪纸', origin: '湖北鄂州', description: '鄂州雕花剪纸以其独特的“阴刻为主、阳刻为辅”的雕刻技法而闻名。其作品构图饱满、线条精巧、寓意吉祥，题材多源于民间生活与传说，充满了浓郁的乡土气息和艺术感染力。' } };
const activeLocationId = ref('kiln'); 
const activeLocation = computed(() => locations[activeLocationId.value]);
const setActiveLocation = (id) => { activeLocationId.value = id; };

// --- 滚动进入动画 ---
const kilnSection = ref(null);
const paperSection = ref(null);
const gallerySection = ref(null);
const potteryTimelineSection = ref(null);
const paperCutTimelineSection = ref(null);
const mapSection = ref(null);
onMounted(() => {
  startAutoPlay();
  const observer = new IntersectionObserver( (entries) => {
      entries.forEach((entry) => { if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); } });
    }, { root: null, threshold: 0.1, }
  );
  const sections = [kilnSection, paperSection, gallerySection, potteryTimelineSection, paperCutTimelineSection, mapSection];
  sections.forEach(sec => { if(sec.value) observer.observe(sec.value); });
  onUnmounted(() => { if (observer) observer.disconnect(); });
});
</script>

<style scoped>
/* 样式保持不变，新增视频弹窗样式 */
.artisan-page { font-family: "Songti SC", "SimSun", serif; background-color: #FDF5E6; overflow-x: hidden; }
.banner-section { position: relative; width: 100%; height: 700px; overflow: hidden; background-color: #333; }
.banner-slide { position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0; transition: opacity 1s ease-in-out; z-index: 1; }
.banner-slide.active { opacity: 1; z-index: 2; }
.banner-img { width: 100%; height: 100%; object-fit: cover; }
.banner-text { position: absolute; top: 50%; right: 10%; transform: translateY(-50%); color: #fff; text-shadow: 2px 2px 8px rgba(0,0,0,0.7); z-index: 3; }
.main-title { font-size: 60px; margin: 0; font-family: "Xingkai SC", "Brush Script MT", cursive; }
.sub-title { font-size: 24px; margin-top: 10px; letter-spacing: 5px; }
.arrow { position: absolute; top: 50%; transform: translateY(-50%); font-size: 60px; color: rgba(255,255,255,0.4); cursor: pointer; user-select: none; font-family: monospace; z-index: 10; padding: 0 20px; transition: color 0.3s; }
.arrow:hover { color: rgba(255,255,255,0.9); }
.arrow-left { left: 10px; }
.arrow-right { right: 10px; }
.dots { position: absolute; bottom: 30px; left: 50%; transform: translateX(-50%); z-index: 10; display: flex; gap: 10px; }
.dot { width: 12px; height: 12px; border-radius: 50%; background-color: rgba(255,255,255,0.5); cursor: pointer; transition: all 0.3s; }
.dot.active { background-color: #E6CFA2; transform: scale(1.2); }
.wave-separator { position: relative; width: 100%; height: 100px; margin-top: -100px; z-index: 9; }
.waves { position:absolute; width: 100%; height:100px; bottom:0; left:0; }
.parallax > use { animation: move-forever 25s cubic-bezier(.55,.5,.45,.5) infinite; }
.parallax > use:nth-child(1) { animation-delay: -2s; animation-duration: 7s; }
.parallax > use:nth-child(2) { animation-delay: -3s; animation-duration: 10s; }
.parallax > use:nth-child(3) { animation-delay: -4s; animation-duration: 13s; }
.parallax > use:nth-child(4) { animation-delay: -5s; animation-duration: 20s; }
@keyframes move-forever { 0% { transform: translate3d(-90px,0,0); } 100% { transform: translate3d(85px,0,0); } }
.paper-content { background-color: #F6F1E6; background-image: radial-gradient(#E8DCCA 1px, transparent 1px); background-size: 20px 20px; position: relative; padding: 80px 0; box-shadow: 0 -10px 30px rgba(0,0,0,0.1); z-index: 8; }
.section-block { width: 1200px; max-width: 95%; margin: 0 auto 100px auto; opacity: 0; transform: translateY(40px); transition: opacity 0.8s ease-out, transform 0.8s ease-out; }
.section-block.is-visible { opacity: 1; transform: translateY(0); }
.section-header { display: flex; justify-content: center; align-items: center; margin-bottom: 50px; }
.section-title { font-size: 32px; margin: 0 20px; font-weight: bold; color: #333; }
.decoration-line { height: 2px; width: 100px; }
.decoration-line.left { background: linear-gradient(to right, transparent, #8B4513); }
.decoration-line.right { background: linear-gradient(to left, transparent, #8B4513); }
.red-theme .decoration-line { background: #A61D1D; }
.cards-container { display: flex; justify-content: space-between; gap: 20px; flex-wrap: wrap; }
.artisan-card { flex: 1; min-width: 300px; background-color: #fff; padding: 10px; box-shadow: 5px 5px 15px rgba(0,0,0,0.05); transition: transform 0.2s cubic-bezier(0.25, 0.46, 0.45, 0.94); transform-style: preserve-3d; }
.card-inner { border: 1px solid #ccc; padding: 30px 20px; height: 100%; display: flex; flex-direction: column; align-items: center; text-align: center; background-color: #FFFAFA; transform: translateZ(20px); transition: background-image 0.2s ease; }
.avatar-wrapper { width: 140px; height: 140px; border-radius: 50%; overflow: hidden; margin-bottom: 20px; border: 4px solid #fff; box-shadow: 0 0 10px rgba(0,0,0,0.2); }
.avatar-wrapper img { width: 100%; height: 100%; object-fit: cover; }
.artisan-name { font-size: 22px; color: #333; margin-bottom: 15px; position: relative; display: inline-block; padding: 0 10px; }
.artisan-name::before, .artisan-name::after { content: ''; display: block; width: 30px; height: 2px; background-color: #ccc; position: absolute; top: 50%; }
.artisan-name::before { left: -40px; }
.artisan-name::after { right: -40px; }
.artisan-desc { font-size: 14px; color: #666; line-height: 1.8; margin-bottom: 20px; text-align: justify; }

/* 🔥🔥🔥 修改：查看更多按钮样式 🔥🔥🔥 */
.read-more { margin-top: auto; padding-top: 10px; font-size: 14px; color: #A61D1D; text-decoration: none; cursor: pointer; border: 1px solid #A61D1D; padding: 5px 15px; border-radius: 20px; transition: all 0.3s; }
.read-more:hover { background-color: #A61D1D; color: #FFF; }

.kiln-style { border: 2px solid #D2B48C; }
.kiln-style .card-inner { border: 1px solid #8B4513; background-color: #FDFCF5; }
.kiln-style .artisan-name { color: #8B4513; }
.paper-style { border: 2px solid #E89A9A; }
.paper-style .card-inner { border: 2px solid #A61D1D; border-radius: 8px; background-color: #FFF; }
.paper-style .artisan-name { color: #A61D1D; }
.paper-style .artisan-name::before, .paper-style .artisan-name::after { background-color: #A61D1D; }
.gallery-filters { text-align: center; margin-bottom: 40px; }
.gallery-filters button { margin: 0 10px; padding: 10px 25px; font-size: 16px; font-family: inherit; border: 1px solid #D2B48C; background-color: transparent; color: #8B4513; cursor: pointer; transition: all 0.3s ease; border-radius: 20px; }
.gallery-filters button.active, .gallery-filters button:hover { background-color: #8B4513; color: #fff; box-shadow: 0 4px 10px rgba(139, 69, 19, 0.3); }
.gallery-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
.gallery-item { position: relative; overflow: hidden; border-radius: 8px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); cursor: pointer; }
.gallery-item img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s ease; }
.gallery-item:hover img { transform: scale(1.1); }
.gallery-overlay { position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(0,0,0,0.8), transparent); color: #fff; padding: 40px 20px 20px; transform: translateY(100%); opacity: 0; transition: all 0.4s ease; }
.gallery-item:hover .gallery-overlay { transform: translateY(0); opacity: 1; }
.gallery-overlay h3 { margin: 0 0 5px 0; font-size: 20px; }
.gallery-overlay p { margin: 0; font-size: 14px; opacity: 0.8; }
.timeline-container { display: flex; justify-content: space-between; position: relative; padding: 20px 0; }
.timeline-container::before { content: ''; position: absolute; top: 70px; left: 5%; width: 90%; height: 2px; background-image: linear-gradient(to right, #D2B48C, #8B4513, #D2B48C); }
.timeline-container.red-theme::before { background-image: linear-gradient(to right, #E89A9A, #A61D1D, #E89A9A); }
.timeline-container-6-steps .timeline-item { width: 15%; }
.timeline-item { text-align: center; position: relative; }
.timeline-content { background: #FFFAFA; padding: 20px 15px; border-radius: 8px; border: 1px solid #D2B48C; box-shadow: 0 4px 12px rgba(0,0,0,0.08); height: 100%; }
.timeline-icon { width: 100px; height: 100px; border-radius: 50%; background-color: #fff; border: 3px solid #D2B48C; display: flex; justify-content: center; align-items: center; margin: -70px auto 20px auto; z-index: 2; position: relative; }
.timeline-icon img { max-width: 60%; max-height: 60%; object-fit: contain; }
.timeline-content h3 { color: #8B4513; margin: 0 0 10px; font-size: 18px; }
.timeline-content p { font-size: 14px; color: #666; line-height: 1.6; margin: 0; text-align: justify; }
.timeline-content.paper-cut-theme { border-color: #E89A9A; }
.timeline-content.paper-cut-theme .timeline-icon { border-color: #A61D1D; }
.timeline-content.paper-cut-theme h3 { color: #A61D1D; }
.map-showcase { display: flex; gap: 30px; align-items: center; background: #FFFAFA; padding: 30px; border: 1px solid #D2B48C; border-radius: 10px; }
.map-area { flex: 2; position: relative; }
.map-bg-img { width: 100%; border-radius: 8px; }
.map-pin { position: absolute; cursor: pointer; display: flex; flex-direction: column; align-items: center; transition: transform 0.3s ease; }
.map-pin:hover { transform: scale(1.15); }
.map-pin img { width: 40px; height: 40px; filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3)); }
.map-pin span { background: rgba(255,255,255,0.8); padding: 2px 8px; border-radius: 10px; font-size: 14px; font-weight: bold; margin-top: 5px; white-space: nowrap; }
.map-pin.active { transform: scale(1.2); }
.map-pin.active img { filter: drop-shadow(0 0 10px #8B4513); }
.kiln-pin { top: 60%; left: 65%; } 
.paper-cut-pin { top: 48%; left: 63%; }
.map-info-area { flex: 1; }
.info-card { background: #FDFCF5; border: 1px solid #D2B48C; padding: 25px; border-radius: 8px; }
.info-card h3 { color: #8B4513; margin: 0 0 15px; font-size: 24px; }
.info-card .info-origin { color: #333; margin-bottom: 15px; font-size: 16px; }
.info-card p { font-size: 14px; color: #666; line-height: 1.8; text-align: justify; margin: 0; }
.info-fade-enter-active, .info-fade-leave-active { transition: opacity 0.4s ease; }
.info-fade-enter-from, .info-fade-leave-to { opacity: 0; }

/* 🔥🔥🔥 视频弹窗样式 🔥🔥🔥 */
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

@media (max-width: 1200px) {
  .timeline-container { flex-wrap: wrap; justify-content: center; gap: 30px; }
  .timeline-container::before { display: none; }
  .timeline-item { width: 30%; min-width: 250px; }
  .map-showcase { flex-direction: column; }
}
@media (max-width: 768px) {
  .banner-text { right: 50%; transform: translateX(50%); text-align: center; width: 90%; }
  .cards-container { flex-direction: column; }
  .timeline-item { width: 45%; }
  .map-pin span { font-size: 12px; }
}
@media (max-width: 500px) {
  .timeline-item { width: 90%; }
}
</style>