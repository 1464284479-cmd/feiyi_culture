<template>
  <div class="patterns-page">
    
    <!-- 1. Banner (带入场动画 & 点击播放视频) -->
    <div class="banner reveal-on-scroll">
      <img src="@/assets/images/patterns/banner.jpg" alt="鄂州剪纸" class="banner-img" />
      
      <!-- 🔥🔥🔥 新增：点击了解更多按钮 🔥🔥🔥 -->
      <div class="banner-overlay">
        <div class="play-btn" @click="openVideo">
          <span class="icon">▶</span>
          <span class="text">点击了解更多</span>
          <span class="hand-icon">👆</span>
        </div>
      </div>
    </div>

    <div class="container">
      
      <!-- ================= Section 1: 千年剪纸史 ================= -->
      <section class="section-block history-section reveal-on-scroll">
        <div class="section-title">
          <img src="@/assets/images/patterns/title_history.png" alt="千年剪纸史" />
        </div>
        <div class="history-grid">
          <div 
            class="history-item" 
            v-for="(item, index) in historyList" 
            :key="index"
            @mouseenter="setActiveHistory(index)"
            @mouseleave="setActiveHistory(-1)"
            :class="{ active: activeHistoryIndex === index }"
          >
            <div class="history-img-wrapper">
              <img :src="item.img" :alt="item.title" class="history-photo" />
            </div>
            <div class="history-info">
              <h3>{{ item.title }}</h3>
              <h4>{{ item.subtitle }}</h4>
              <p>{{ item.desc }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- ================= Section 2: 巧手剪春秋 ================= -->
      <section class="section-block skill-section reveal-on-scroll">
        <div class="section-title">
          <img src="@/assets/images/patterns/title_skill.png" alt="巧手剪春秋" />
        </div>
        <div class="carousel-container">
          <div class="nav-arrow left-arrow" @click="scrollCarousel(-1)">
            <svg viewBox="0 0 24 24"><polyline points="15 18 9 12 15 6"></polyline></svg>
          </div>
          <div class="carousel-viewport">
            <div class="carousel-track" :style="{ transform: `translateX(-${currentOffset}px)` }">
              <div class="carousel-card" v-for="(item, index) in skillList" :key="index" @click="openModal(item)">
                <div class="card-img"><img :src="item.image" :alt="item.title" /></div>
                <div class="card-title"><h3>{{ item.title }}</h3><div class="title-line"></div></div>
                <div class="card-desc"><p>{{ item.shortDesc }}</p></div>
              </div>
            </div>
          </div>
          <div class="nav-arrow right-arrow" @click="scrollCarousel(1)">
            <svg viewBox="0 0 24 24"><polyline points="9 18 15 12 9 6"></polyline></svg>
          </div>
        </div>
      </section>

      <!-- ================= Section 3: 高德地图 · 纹样溯源 ================= -->
      <div class="section-title" style="margin-top: 80px;">
          <img src="@/assets/images/patterns/3.png" alt="纹样溯源" />
        </div>
      <section class="section-block map-api-section reveal-on-scroll" id="map-section-observer">
        <!-- 地图容器 -->
        <div id="map-container" class="map-container-amap"></div>
      </section>

      <!-- ================= Section 4: 纹样藏乾坤 ================= -->
      <section class="section-block pattern-display reveal-on-scroll">
        <div class="section-title">
          <img src="@/assets/images/patterns/title_pattern.png" alt="纹样藏乾坤" />
        </div>
        <div class="pattern-content">
          <div class="pattern-row">
            <img src="@/assets/images/patterns/pattern_row_1.png" alt="第一排纹样" />
            <router-link to="/materials" class="btn-material" @click="playRipple">
              <img src="@/assets/images/patterns/btn_material.png" alt="进入素材库" />
            </router-link>
          </div>
          <div class="pattern-row mt-30">
            <img src="@/assets/images/patterns/pattern_row_2.png" alt="第二排纹样" />
          </div>
        </div>
      </section>

      <!-- ================= Section 5: 薪火永相传 ================= -->
      <section class="section-block inherit-section reveal-on-scroll">
        <div class="section-title">
          <img src="@/assets/images/patterns/title_inherit.png" alt="薪火永相传" />
        </div>
        <div class="inherit-list">
          <div class="inherit-item" v-for="(item, index) in inheritList" :key="index">
            <img src="@/assets/images/patterns/inherit_frame.png" class="frame-bg" alt="背景框" />
            <div class="inherit-content">
              <div class="icon-box"><img :src="item.icon" alt="图标" /></div>
              <div class="photo-circle"><img :src="item.photo" alt="照片" /></div>
              <div class="text-box"><p>{{ item.text }}</p></div>
            </div>
          </div>
        </div>
      </section>

    </div>

    <!-- 详情弹窗组件 (巧手剪春秋用) -->
    <PatternDetailModal 
      :visible="showModal"
      :title="modalData.title"
      :content="modalData.content"
      :image="modalData.image"
      @close="showModal = false"
    />

    <!-- 🔥🔥🔥 新增：视频弹窗 (Banner点击用) 🔥🔥🔥 -->
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
import { reactive, ref, onMounted } from 'vue';
import PatternDetailModal from '@/components/PatternDetailModal.vue';

// --- 🔥🔥🔥 新增：视频播放逻辑 🔥🔥🔥 ---
const showVideoModal = ref(false);
// 视频存放路径：public/videos/ezhou_intro.mp4 (请确保文件存在)
const videoPath = '/videos/ezhou_intro.mp4'; 

const openVideo = () => {
  showVideoModal.value = true;
};
const closeVideo = () => {
  showVideoModal.value = false;
};

// --- 高德地图逻辑 ---
let map = null; 
const mapPlaces = [
  { id: 'xinjiang', name: '新疆', lnglat: [87.6177, 43.7928], title: '西域 · 随葬剪纸', desc: '新疆吐鲁番阿斯塔那古墓群出土了最早的剪纸实物，如“对马”“对猴”，证明剪纸艺术在丝绸之路上的早期传播。' },
  { id: 'dunhuang', name: '敦煌', lnglat: [94.6617, 40.1466], title: '北朝 · “对马”“对猴”', desc: '敦煌莫高窟出土的北朝剪纸，是中国最早的剪纸实物，多为对称动物纹样，开启了千年传统。' },
  { id: 'yangzhou', name: '扬州', lnglat: [119.42, 32.39], title: '隋唐 · “镂花”', desc: '隋炀帝令宫女采集民间花样，“镂金箔为花”，扬州成为剪纸艺术的重要发展地，技法更为精细。' },
  { id: 'nanjing', name: '南京', lnglat: [118.7969, 32.0603], title: '六朝 · “人胜”', desc: '六朝时期南京地区流行“人日剪彩为人”，即“人胜”，用以祈福，是剪纸民俗化的重要标志。' },
  { id: 'ezhou', name: '鄂州', lnglat: [114.8928, 30.4046], title: '楚地 · “雕花”', desc: '鄂州剪纸继承楚文化浪漫主义，构图饱满，线条流畅，以“雕花”闻名，技艺自成一派。' }
];
const initMap = () => {
  if (map || !window.AMap) return;
  
  map = new AMap.Map('map-container', {
    zoom: 4.5,
    center: [104, 34], 
    viewMode: '2D',
    mapStyle: 'amap://styles/whitesmoke', 
  });

  const infoWindow = new AMap.InfoWindow({ isCustom: true, autoMove: true, offset: new AMap.Pixel(0, -40) });
  
  mapPlaces.forEach(place => {
    const marker = new AMap.Marker({
      position: place.lnglat,
      content: `<div class="custom-marker"><div class="pulse"></div><span>${place.name}</span></div>`,
      offset: new AMap.Pixel(-35, -35),
      extData: place
    });
    marker.on('mouseover', (e) => {
      const data = e.target.getExtData();
      infoWindow.setContent(`<div class="info-window-light"><h4>${data.title}</h4><p>${data.desc}</p></div>`);
      infoWindow.open(map, e.target.getPosition());
    });
    marker.on('mouseout', () => infoWindow.close());
    map.add(marker);
  });
  
  const linePaths = [
    [mapPlaces[0].lnglat, mapPlaces[1].lnglat], // 新疆 -> 敦煌
    [mapPlaces[1].lnglat, mapPlaces[4].lnglat], // 敦煌 -> 鄂州
    [mapPlaces[2].lnglat, mapPlaces[4].lnglat], // 扬州 -> 鄂州
    [mapPlaces[3].lnglat, mapPlaces[4].lnglat]  // 南京 -> 鄂州
  ];
  linePaths.forEach(path => {
    const polyline = new AMap.Polyline({
      path: path,
      strokeColor: "#8B1A1A", 
      strokeOpacity: 0.8,
      strokeWeight: 2,
      strokeStyle: "solid",
      showDir: true, 
    });
    map.add(polyline);
  });
};

// --- 入场动画 ---
onMounted(() => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => { 
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        if (entry.target.id === 'map-section-observer') {
          initMap();
        }
      } 
    });
  }, { threshold: 0.1 });
  
  document.querySelectorAll('.reveal-on-scroll').forEach(el => observer.observe(el));
});

// --- 图片引入 ---
import hist1 from '@/assets/images/patterns/history_1.png';
import hist2 from '@/assets/images/patterns/history_2.png';
import hist3 from '@/assets/images/patterns/history_3.png';
import hist4 from '@/assets/images/patterns/history_4.png';
import skillTools from '@/assets/images/patterns/skill_tools.jpg';
import skillTech from '@/assets/images/patterns/skill_tech.jpg';
import skillProc from '@/assets/images/patterns/skill_process.jpg';
import skillStyle from '@/assets/images/patterns/skill_style.jpg';
import skillNew from '@/assets/images/patterns/skill_new.jpg';
import icon1 from '@/assets/images/patterns/icon_1.png';
import photo1 from '@/assets/images/patterns/inherit_1.jpg';
import icon2 from '@/assets/images/patterns/icon_2.png';
import photo2 from '@/assets/images/patterns/inherit_2.jpg';
import icon3 from '@/assets/images/patterns/icon_3.png';
import photo3 from '@/assets/images/patterns/inherit_3.jpg';
import icon4 from '@/assets/images/patterns/icon_4.png';
import photo4 from '@/assets/images/patterns/inherit_4.jpg';

// --- 历史区域交互 ---
const activeHistoryIndex = ref(-1);
const setActiveHistory = (index) => { activeHistoryIndex.value = index; };

// --- 数据：历史 ---
const historyList = [
  { img: hist1, title: '唐代起源', subtitle: '祭祀与民俗的共生', desc: '唐代鄂州剪纸以“花样”用于祭祀装饰及刺绣模板，《舆地纪胜》载“剪纸为幡，迎祥纳福”，与民俗紧密关联。' },
  { img: hist2, title: '宋元发展', subtitle: '技艺与材质的突破', desc: '宋元鄂州陶瓷业兴盛，剪纸纹样融入瓷器装饰促镂空技法精进，元代棉花普及使剪纸成婚嫁年节装饰，形成粗细剪并行风格。' },
  { img: hist3, title: '明清鼎盛', subtitle: '文人参与风格定型', desc: '明清鄂州剪纸向观赏艺术转型，文人参与设计融入书画意趣，创“单色剪”“套色剪”等技法，清代剪纸谱收录经典纹样，技艺臻熟。' },
  { img: hist4, title: '现代传承', subtitle: '非遗保护与当代创新', desc: '20世纪50年代剪纸结合时代主题，2008年“鄂州雕花剪纸”列国家级非遗，现保留传统技艺并融入现代元素，活态传承千年技艺。' },
];

// --- 数据：巧手剪春秋 ---
const skillList = [
  {
    title: '工具材料',
    image: skillTools,
    shortDesc: '“一剪一刀一蜡盘，薄纸承韵传千年” —— 鄂州剪纸以尖嘴剪走细，圆头剪塑形，枣木蜡盘减震，生宣吸色不洇，成就“剪如笔走，刻若刀耕”的精妙。',
    content: [
      '鄂州剪纸的工具与材料是其工艺的“基石”，每一件都承载着非遗的细节：',
      '1. 核心工具：分“尖嘴剪”（针尖式剪头，用于游丝纹、月牙纹等精细线条）和“圆头剪”（圆弧形剪头，用于轮廓裁剪、大面积造型）；刻刀常用“六把刻刀”组合（含不同宽度的刀头），适配锯齿纹、镂空等刻制工艺；蜡盘以枣木为底，填充特制蜡油（硬度适中），既保护刀锋，又能固定纸张避免移位。',
      '2. 纸张：首选“万年红单面红”宣纸——纸张薄而韧，吸色不洇，红色饱和度高，是鄂州剪纸“喜庆底色”的经典载体。',
      '3. 辅助工具：包含自动铅笔（起稿）、镇纸（固定纸张）、订书机（批量订纸）等，让剪刻过程更稳定高效。'
    ]
  },
  {
    title: '剪刻技法',
    image: skillTech,
    shortDesc: '“阴刻见线，阳刻留面，阴阳交错生乾坤” —— 细剪游丝纹仅 0.1 毫米，打毛锯齿纹仿生灵动，月牙纹流转如波，展现“以剪代笔，以纸为帛”的东方美学。',
    content: [
      '鄂州剪纸的技法核心是“千刻不落，万剪不断”，三大基础技法奠定其艺术特色：',
      '1. 游丝纹：以尖嘴剪剪出0.1毫米级的细密线条，流畅不断，常用于表现花瓣脉络、动物毛发等细节，如凤凰尾羽的“丝缕感”；',
      '2. 锯齿纹：以刻刀短促发力，形成细密的“锯齿状纹理”，仿生效果极强（如梅花的花瓣边缘、雄狮的鬃毛）；',
      '3. 月牙纹：以剪刀弧形运剪，剪出圆润的“月牙形镂空”，用于表现光影、弧度（如荷花的花瓣层次、祥云的曲线）。',
      '这三种技法常“阴阳结合”（阴刻镂空、阳刻留形），让作品兼具细腻与张力。'
    ]
  },
  {
    title: '工艺流程',
    image: skillProc,
    shortDesc: '“起稿定乾坤，剪刻见匠心” —— 从 pencil 勾稿的“意在笔先”，到蜡盘固定的“稳如磐石”，再到“千剪不断、万刻不乱”的剪刻节奏，每一步都是与时光的对话。',
    content: [
      '一副完整的鄂州剪纸作品，需经历6个严谨步骤：',
      '1. 构思起稿：“意在笔先”——先确定主题（如“莲年有鱼”），用铅笔在纸上勾勒纹样；',
      '2. 熏样或复印：传统用“烟熏法”复制稿样（将纸稿贴于木板，燃香熏出轮廓），现代多用复印；',
      '3. 订纸固定：将多张纸（可批量剪刻）用订书机固定在蜡盘上；',
      '4. 剪刻制作：按“先内后外、先细后粗”的顺序剪刻（先做游丝纹、锯齿纹等细节，再剪轮廓）；',
      '5. 揭离：剪刻完成后，轻轻揭开叠纸，分离出单幅作品；',
      '6. 粘贴装裱：将作品贴于衬纸或装裱成卷轴，完成最终呈现。',
      '其中“剪刻”是核心：需心手合一，刀刀精准，避免“断纹”破坏作品完整性。'
    ]
  },
  {
    title: '艺术特色',
    image: skillStyle,
    shortDesc: '“图必有意，意必吉祥”。鄂州剪纸构图饱满，善用谐音寓意，如“莲（连）年有鱼（余）”，线条挺拔而不失柔美，具有浓郁的楚文化浪漫色彩。',
    content: [
      '鄂州剪纸的艺术风格，是楚文化与民间审美结合的产物：',
      '1. 构图特点：打破时空限制的“满构图”——如“双凤朝阳”中，将凤凰、太阳、缠枝牡丹等元素压缩在同一画面，追求“画面饱满、寓意完整”；',
      '2. 造型特点：“夸张而不失真”——如荷花剪纸会放大花瓣的层次，狮子剪纸会强化鬃毛的动感，既保留物象特征，又充满艺术张力；',
      '3. 文化寓意：善用“谐音符号”——如“莲（连）年有鱼（余）”“梅（眉）鹊（雀）报春”，每一幅作品都是“吉祥寓意的视觉载体”，承载着楚地的民俗文化。'
    ]
  },
  {
    title: '现代创新',
    image: skillNew,
    shortDesc: '非遗不老，正青春。现代传承人将剪纸元素融入服装、灯具、文创产品中，并利用数字技术建立纹样库，让古老的剪纸技艺走进现代生活。',
    content: [
      '鄂州剪纸正以“传统内核+现代载体”的方式焕发新生：',
      '1. 文创融合：将剪纸纹样融入生活用品——如“剪纸丝巾”（把“双凤纹”印于真丝）、“AR数字书签”（扫码可观看剪刻工艺视频）、“武汉长江大桥剪纸装饰画”（地域文化IP）；',
      '2. 公共艺术：以“巨型剪纸装置”亮相城市空间——如灯光剪纸（将传统纹样做成大型灯饰），既保留剪纸的镂空美感，又适配现代城市的夜景氛围；',
      '3. 数字传承：建立“鄂州剪纸纹样库”——将游丝纹、月牙纹等传统纹样数字化，供设计师、创作者复用，让非遗元素走进现代设计产业链。'
    ]
  }
];

// --- 轮播与弹窗 ---
const currentOffset = ref(0);
const scrollCarousel = (direction) => { const oneStep = 320 + 30; const maxOffset = (skillList.length - 3) * oneStep; let newOffset = currentOffset.value + (direction * oneStep); if (newOffset < 0) newOffset = 0; if (newOffset > maxOffset) newOffset = maxOffset; currentOffset.value = newOffset; };
const showModal = ref(false);
const modalData = reactive({ title: '', content: [], image: '' });
const openModal = (item) => { modalData.title = item.title; modalData.content = item.content; modalData.image = item.image; showModal.value = true; };
const playRipple = (e) => { const btn = e.currentTarget; const circle = document.createElement("span"); const diameter = Math.max(btn.clientWidth, btn.clientHeight); const radius = diameter / 2; circle.style.width = circle.style.height = `${diameter}px`; circle.style.left = `${e.clientX - btn.offsetLeft - radius}px`; circle.style.top = `${e.clientY - btn.offsetTop - radius}px`; circle.classList.add("ripple"); const ripple = btn.getElementsByClassName("ripple")[0]; if (ripple) ripple.remove(); btn.appendChild(circle); };

// --- 数据：传承 ---
const inheritList = [
  { icon: icon1, photo: photo1, text: '国家级非遗（鄂州雕花剪纸）传承人骆清霞，领衔五代技艺传承谱系 —— 自清末祖父骆翰卿奠定剪纸风格，经父辈改良刀法，再由骆清霞融合楚地纹样与现代审美，形成 “粗犷中见细腻、民俗中藏雅致” 的独特风格。她以家族式培养体系授徒 300 余人，其中 12 人成为省级非遗传承人，既守住了 “无稿创作、一刀成型” 的传统技法，也为鄂州剪纸注入了年轻传承力量。' },
  { icon: icon2, photo: photo2, text: '鄂州 200 所中小学将雕花剪纸纳入必修课体系 —— 从小学低年级的 “基础剪法启蒙”，到中学的 “纹样设计与非遗文化解读”，构建了分阶式课程框架。课程配套校本教材《楚韵剪艺》，年培训超 1.2 万人次，不仅让青少年掌握 “阳刻、阴刻” 等核心技法，更通过 “剪纸讲楚俗” 的形式，让非遗成为连接传统文化与校园生活的纽带。' },
  { icon: icon3, photo: photo3, text: '以鄂州剪纸纹样为核心元素，开发出 12 大类 200 余款衍生品：既有 “剪纸纹样国潮服饰”“AR 数字书签” 等年轻化产品（扫码可观看剪纸工艺视频），也有 “武汉长江大桥剪纸装饰画” 等地域文化 IP 作品。这些文创既保留了 “缠枝莲、双凤纹” 等传统符号，又以现代设计语言重构，让非遗从 “展柜” 走进日常消费场景。' },
  { icon: icon4, photo: photo4, text: '连续八年亮相米兰设计周、巴黎非遗展等国际舞台，曾作为 “中国非遗代表” 在联合国教科文组织活动中展示；与大英博物馆联合推出限定剪纸文创 —— 以 “梅鹊纹、木叶纹”（吉州窑 + 鄂州剪纸跨界元素）为主题，推出艺术版画、文具套装等产品，让楚地非遗纹样成为跨文化交流的视觉语言，累计吸引超 50 万海外受众关注。' },
];
</script>

<style scoped>
/* ================== 🔥 1. 入场动画基础样式 🔥 ================== */
.reveal-on-scroll { opacity: 0; transform: translateY(40px); transition: opacity 0.8s ease-out, transform 0.8s ease-out; }
.reveal-on-scroll.is-visible { opacity: 1; transform: translateY(0); }

/* ================== 🔥 2. Banner 区域样式 (含播放按钮) 🔥 ================== */
.banner { width: 100%; position: relative; }
.banner img { width: 100%; display: block; }
.banner-overlay {
  position: absolute;
  bottom: 80px;  /* 距离底部 */
  right: 120px;   /* 距离右侧 */
  z-index: 10;
}
.play-btn {
  background-color: rgba(69, 21, 2, 0.85); /* 深红棕色背景 */
  color: #E6CFA2; /* 金色文字 */
  padding: 12px 30px;
  border-radius: 50px;
  border: 2px solid #E6CFA2;
  font-size: 18px;
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
.play-btn .icon { font-size: 16px; }
.play-btn .hand-icon { font-size: 20px; animation: point 1s infinite alternate; }

@keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(230, 207, 162, 0.4); } 70% { box-shadow: 0 0 0 15px rgba(230, 207, 162, 0); } 100% { box-shadow: 0 0 0 0 rgba(230, 207, 162, 0); } }
@keyframes point { from { transform: translateX(0); } to { transform: translateX(5px); } }

/* ================== 🔥 3. 视频弹窗样式 🔥 ================== */
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

/* ================== 4. 高德地图样式 ================== */
.map-api-section { padding: 40px 0; background: #fdf5e6; }
.map-container-amap { width: 100%; height: 600px; border-radius: 15px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin-top: 15px; margin-bottom: 15px; }
:deep(.custom-marker) { position: relative; background-color: #8B1A1A; color: #fff; border-radius: 20px; padding: 5px 15px; font-size: 14px; box-shadow: 0 2px 5px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.5); white-space: nowrap; }
:deep(.pulse) { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 20px; height: 20px; background: #8B1A1A; border-radius: 50%; animation: pulseMarker 2s infinite; z-index: -1; }
@keyframes pulseMarker { 0% { transform: translate(-50%,-50%) scale(1); opacity: 0.7; } 100% { transform: translate(-50%,-50%) scale(3); opacity: 0; } }
:deep(.info-window-light) { background: #fff; border-radius: 8px; padding: 15px; width: 250px; box-shadow: 0 5px 15px rgba(0,0,0,0.2); border: 1px solid #ddd; }
:deep(.info-window-light h4) { color: #8B1A1A; font-size: 16px; margin: 0 0 10px 0; border-bottom: 1px solid #eee; padding-bottom: 5px; }
:deep(.info-window-light p) { font-size: 13px; line-height: 1.6; color: #333; margin: 0; }

/* ================== 5. 原有样式 (保持不变) ================== */
.patterns-page { font-family: "Songti SC", "SimSun", serif; background-color: #fff; padding-bottom: 80px; }
.container { width: 1200px; max-width: 95%; margin: 0 auto; }
.section-block { margin-top: 80px; }
.section-title { text-align: center; margin-bottom: 50px; }
.section-title img { height: 120px; }
.history-grid { display: flex; justify-content: space-between; gap: 20px; }
.history-item { flex: 1; text-align: center; cursor: pointer; position: relative; }
.history-img-wrapper { width: 100%; max-width: 250px; transition: transform 0.4s; position: relative; z-index: 2; margin: 0 auto; }
.history-photo { width: 100%; filter: grayscale(1); transition: all 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94); }
.history-info { margin-top: 15px; text-align: left; padding: 0 10px; transition: all 0.5s; }
.history-info h3 { color: #8B1A1A; font-size: 20px; font-weight: bold; }
.history-info h4 { font-size: 18px; font-weight: bold; color: #333; }
.history-info p { font-size: 16px; color: #666; line-height: 1.6; text-align: justify; }
.history-item.active .history-photo { filter: grayscale(0); transform: scale(1.1); box-shadow: 0 15px 30px rgba(0,0,0,0.2); }
.history-item.active .history-info { transform: translateY(10px) scale(0.8); opacity: 0; }
.carousel-container { display: flex; align-items: center; justify-content: space-between; padding: 0 20px; }
.nav-arrow { cursor: pointer; transform: scale(1.5); opacity: 0.5; transition: all 0.2s; }
.nav-arrow:hover { transform: scale(1.8); opacity: 1; }
.nav-arrow svg { width: 40px; height: 40px; stroke: #C0C0C0; stroke-width: 2; fill: none; }
.carousel-viewport { width: 1020px; overflow: hidden; padding: 20px 0; }
.carousel-track { display: flex; gap: 30px; transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1); }
.carousel-card { flex: 0 0 320px; background: #fff; cursor: pointer; transition: transform 0.4s; perspective: 1000px; }
.carousel-card:hover { transform: translateY(-10px) rotateX(5deg) scale(1.03); box-shadow: 0 20px 40px rgba(0,0,0,0.2); }
.card-img img { width: 100%; height: 240px; object-fit: cover; border-radius: 15px; }
.card-title { margin: 15px 0 10px 0; padding-left: 10px; }
.card-title h3 { font-size: 22px; color: #8B5A2B; font-weight: bold; }
.title-line { width: 100px; height: 3px; background-color: #D4AF37; }
.card-desc { background-color: #f5f5f5; padding: 15px; border-radius: 10px; height: 140px; overflow: hidden; }
.card-desc p { font-size: 16px; color: #333; line-height: 1.8; text-align: justify; }
.pattern-content { position: relative; padding: 0 20px; }
.pattern-row { position: relative; width: 100%; text-align: center; }
.pattern-row img { width: 100%; height: auto; }
.mt-30 { margin-top: 30px; }
.btn-material { position: absolute; right: -100px; top: 105%; transform: translateY(-50%); width: 220px; transition: transform 0.3s; animation: pulse 2s infinite; overflow: hidden; }
.btn-material:hover { animation-play-state: paused; transform: translateY(-50%) scale(1.05); }
.btn-material img { width: 100%; }
:deep(.ripple) { position: absolute; border-radius: 50%; transform: scale(0); animation: ripple-effect 0.6s linear; background-color: rgba(255, 255, 255, 0.7); }
@keyframes ripple-effect { to { transform: scale(4); opacity: 0; } }
.inherit-item { position: relative; width: 100%; min-height: 220px; display: flex; justify-content: center; align-items: center; padding: 20px 0; transition: all 0.8s ease-out; }
.inherit-item > * { transition: all 0.6s ease-out; opacity: 0; transform: translateY(20px); }
.is-visible .inherit-item > * { opacity: 1; transform: translateY(0); }
.is-visible .inherit-item .frame-bg { transition-delay: 0s; }
.is-visible .inherit-item .icon-box { transition-delay: 0.2s; }
.is-visible .inherit-item .photo-circle { transition-delay: 0.4s; }
.is-visible .inherit-item .text-box { transition-delay: 0.6s; }
.frame-bg { position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: fill; z-index: 0; }
.inherit-content { position: relative; z-index: 1; width: 100%; display: flex; align-items: center; padding: 0 60px; }
.icon-box { width: 120px; margin-right: 30px; }
.icon-box img { width: 100%; }
.photo-circle { width: 170px; height: 170px; border-radius: 50%; overflow: hidden; border: 3px solid #fff; box-shadow: 0 5px 15px rgba(0,0,0,0.3); }
.photo-circle img { width: 100%; height: 100%; object-fit: cover; }
.text-box { flex: 1; max-width: 650px; }
.text-box p { font-size: 16px; color: #333; line-height: 1.8; text-decoration: underline; text-decoration-color: #8B4A13; text-underline-offset: 5px; text-align: justify; }

@media (max-width: 768px) {
  .history-grid, .inherit-list { flex-direction: column; }
  .carousel-viewport { width: 100%; }
  .nav-arrow { display: none; }
  .btn-material { position: static; margin: 20px auto; display: block; transform: none; }
  .inherit-content { flex-direction: column; text-align: center; }
  .icon-box, .photo-circle { margin: 0 0 15px 0; }
  .banner-overlay { bottom: 20px; right: 20px; }
  .play-btn { padding: 10px 20px; font-size: 14px; }
}
</style>