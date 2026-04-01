<template>
  <div class="home-page" @mousemove="handleGlobalMouseMove" @click="createRipple">
    
    <!-- ================== 1. 探照灯首屏 ================== -->
    <div class="hero-section">
      <div class="layer-dark">
        <div class="texture-overlay"></div>
        <div class="embers-container">
          <div v-for="n in 20" :key="n" class="ember" :style="getRandomEmberStyle()"></div>
        </div>
        <h1 class="hero-title hidden-title">
          <div>千年窑火</div>
          <div>釉色天成</div>
        </h1>
      </div>

      <div class="layer-light" :style="maskStyle">
        <div class="light-content">
          <img :src="goldPatternImg" class="pattern-bg" alt="剪纸纹样" />
          <h1 class="hero-title reveal-title">
            <div>鄂州剪韵</div>
            <div>点亮吉州</div>
          </h1>
        </div>
      </div>

      <div class="floating-leaf-container">
        <img 
          :src="leafImg" 
          class="leaf-img"
          :class="{ 'leaf-burned': isLeafHovered }"
          @mouseenter="isLeafHovered = true"
          @mouseleave="isLeafHovered = false"
        />
        <div class="leaf-hint" v-if="!isLeafHovered">试着触碰落叶</div>
      </div>

      <div class="scroll-hint">
        <div class="mouse-icon"></div>
        <p>移动鼠标探寻 · 点击屏幕泛起茶韵涟漪</p>
      </div>

      <div class="ripples-container">
        <div 
          v-for="ripple in ripples" 
          :key="ripple.id" 
          class="ripple"
          :style="{ top: ripple.y + 'px', left: ripple.x + 'px' }"
        ></div>
      </div>
    </div>

    <!-- ================== 2. 双遗介绍 ================== -->
    <section class="intro-section">
      <div class="parallax-bg" :style="parallaxStyle">
        <img :src="goldPatternImg" class="parallax-layer layer-1" />
        <img :src="goldPatternImg" class="parallax-layer layer-2" />
      </div>

      <div class="intro-container">
        <div class="intro-text">
          <h2>土与火的骨骼 · 纸与刀的灵魂</h2>
          <p>
            吉州窑，以其变幻莫测的“玳瑁釉”与“木叶贴花”闻名于世。<br>
            当鄂州雕花剪纸的细腻纹样，遇上吉州窑高温流动的褐釉，<br>
            瞬间的高温将纸灰化为永恒的纹理，<br>
            成就了“刀剪成花，入窑成画”的东方绝唱。
          </p>
        </div>
        <div class="intro-visual">
          <div class="circle-fusion">
            <div class="half fire"></div>
            <div class="half paper"></div>
            <div class="center-text">共生</div>
          </div>
        </div>
      </div>
    </section>

    <!-- ================== 3. 指尖定格 (DIY Lite) ================== -->
    <section class="diy-lite-section">
      <div class="diy-container">
        <div class="diy-header">
          <h2>指尖定格 · 瞬息成画</h2>
          <p>轻触纹样，体验剪纸在素胚之上的光影重生</p>
        </div>
        
        <div class="diy-workspace">
          <!-- 左侧：碗的预览区 -->
          <div class="bowl-preview-container">
            <img :src="bowlBaseImg" class="bowl-base-img" alt="吉州窑素胚" />
            
            <transition name="fade-scale">
              <img 
                v-if="currentDiyPattern" 
                :src="currentDiyPattern" 
                class="pattern-overlay-img"
              />
            </transition>
            
            <div class="bowl-shine-overlay"></div>
          </div>

          <!-- 右侧：纹样选择区 -->
          <div class="pattern-selector">
            <div 
              v-for="(pat, index) in diyPatterns" 
              :key="index"
              class="pattern-option"
              :class="{ active: currentDiyPattern === pat.src }"
              @click="selectDiyPattern(pat.src)"
            >
              <img :src="pat.src" />
              <span>{{ pat.name }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ================== 4. 数字工坊入口 ================== -->
    <section class="unity-entry-section">
      <div class="unity-content">
        <div class="unity-text">
          <h2 class="unity-title">数字工坊 · 亲历造物</h2>
          <p class="unity-desc">
            穿越时空，化身宋代陶工。<br>
            在 Unity 3D 引擎构建的虚拟世界中，亲手体验拉坯、施釉、贴花、烧制的完整工艺。<br>
            让千年的技艺，在您的指尖重生。
          </p>
          <button class="unity-btn" @click="openUnityModal">
            <span class="icon">🎮</span> 启动虚拟窑炉
          </button>
        </div>
        <div class="unity-visual holographic-container" @click="openUnityModal">
          <img :src="unityPreviewImg" alt="Unity Preview" class="holo-img" />
          <div class="scan-line"></div>
          <div class="glitch-overlay"></div>
        </div>
      </div>
    </section>

    <!-- ================== 5. 非遗回响 (Sound Section) ================== -->
    <section class="sound-section">
      <h2 class="section-title">非遗回响 · 听见历史</h2>
      <p style="color: #666; margin-bottom: 30px; font-size: 14px;">( 点击图标聆听制作原声 )</p>
      
      <div class="sound-grid">
        <div class="sound-item" @click="playSound('cut')">
          <div class="sound-circle">
            <span class="sound-icon">✂️</span>
            <div class="wave-ring" v-if="activeSound === 'cut'"></div>
            <div class="wave-ring delay-1" v-if="activeSound === 'cut'"></div>
          </div>
          <h3>纸间惊雷</h3>
          <p>剪刀游走于红纸的沙沙声</p>
        </div>

        <div class="sound-item" @click="playSound('fire')">
          <div class="sound-circle">
            <span class="sound-icon">🔥</span>
            <div class="wave-ring" v-if="activeSound === 'fire'"></div>
            <div class="wave-ring delay-1" v-if="activeSound === 'fire'"></div>
          </div>
          <h3>窑火轰鸣</h3>
          <p>松木在千度高温下的爆裂声</p>
        </div>

        <div class="sound-item" @click="playSound('tea')">
          <div class="sound-circle">
            <span class="sound-icon">🍵</span>
            <div class="wave-ring" v-if="activeSound === 'tea'"></div>
            <div class="wave-ring delay-1" v-if="activeSound === 'tea'"></div>
          </div>
          <h3>茶汤入盏</h3>
          <p>宋代点茶击拂的汤花声</p>
        </div>
      </div>
    </section>

    <!-- ================== 6. 探索入口 ================== -->
    <section class="explore-section">
      <h2 class="section-title">开启非遗数字化之旅</h2>
      <div class="cards-grid">
        <router-link to="/double-heritage" class="explore-card">
          <div class="card-inner">
            <div class="card-front"><span class="card-icon">📊</span><h3>双遗数览</h3></div>
            <div class="card-back"><p>大数据视角下的<br>非遗传承现状</p><span class="go-btn">查看数据 →</span></div>
          </div>
        </router-link>
        <router-link to="/window-gallery" class="explore-card">
          <div class="card-inner">
            <div class="card-front"><span class="card-icon">🏺</span><h3>窗韵图鉴</h3></div>
            <div class="card-back"><p>沉浸式画卷<br>赏析千年瓷器</p><span class="go-btn">赏析文物 →</span></div>
          </div>
        </router-link>
        <router-link to="/patterns" class="explore-card">
          <div class="card-inner">
            <div class="card-front"><span class="card-icon">✂️</span><h3>剪纸纹样</h3></div>
            <div class="card-back"><p>数字化纹样库<br>与创新应用</p><span class="go-btn">浏览素材 →</span></div>
          </div>
        </router-link>
      </div>
    </section>

    <!-- Unity Modal -->
    <div v-if="showUnity" class="unity-modal-overlay">
      <div class="unity-window">
        <button class="close-unity-btn" @click="closeUnityModal">×</button>
        <div class="unity-header"><h3>吉州窑虚拟制瓷体验 (Unity WebGL)</h3></div>
        
        <div class="unity-iframe-container">
          <!-- 
            src="/unity/index.html" : 指向 public/unity 文件夹
            @load="onUnityLoaded"   : 监听加载完成事件
          -->
          <iframe 
            src="/unity/index.html" 
            frameborder="0" 
            class="unity-iframe"
            :class="{ 'visible': isUnityLoaded }"
            @load="onUnityLoaded"
          ></iframe>

          <!-- 加载时的遮罩层 -->
          <div class="unity-placeholder" v-if="!isUnityLoaded">
            <div class="loader"></div>
            <p>正在连接虚拟引擎...</p>
            <p style="font-size: 12px; color: #888; margin-top: 10px;">资源加载可能需要 10-30 秒</p>
          </div>
        </div>
      </div>
    </div>

    <!-- ================== 7. AI 守艺人 (悬浮助手) ================== -->
    <div class="ai-floater" @click="toggleChat" :class="{ 'hide': isChatOpen }">
      <div class="ai-avatar">
        <span>🧙‍♂️</span>
      </div>
      <div class="ai-tip">有不懂的？问问守艺人</div>
    </div>

    <!-- 聊天面板 -->
    <transition name="slide-up">
      <div v-if="isChatOpen" class="chat-panel">
        <div class="chat-header">
          <div class="header-info">
            <span class="avatar-small">🧙‍♂️</span>
            <span class="name">AI 守艺人</span>
            <span class="status">在线中...</span>
          </div>
          <button class="close-chat" @click="toggleChat">×</button>
        </div>

        <div class="chat-body" ref="chatBodyRef">
          <div v-for="(msg, index) in chatMessages" :key="index" class="message-row" :class="msg.role">
            <div class="avatar" v-if="msg.role === 'bot'">🧙‍♂️</div>
            <div class="bubble">
              <span v-html="msg.content"></span>
            </div>
          </div>
          <div v-if="isTyping" class="message-row bot">
            <div class="avatar">🧙‍♂️</div>
            <div class="bubble typing">
              <span>.</span><span>.</span><span>.</span>
            </div>
          </div>
        </div>

        <div class="chat-footer">
          <div class="quick-tags">
            <span @click="askQuestion('吉州窑在哪里？')">📍 地址在哪</span>
            <span @click="askQuestion('什么是木叶天目？')">🍃 木叶天目</span>
            <span @click="askQuestion('剪纸怎么保存？')">🛡️ 剪纸保养</span>
          </div>
          <div class="input-box">
            <input 
              v-model="inputMessage" 
              @keyup.enter="sendMessage" 
              type="text" 
              placeholder="请输入您关于非遗的问题..." 
            />
            <button @click="sendMessage">发送</button>
          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, computed, reactive, nextTick } from 'vue';

// 引入图片
import goldPatternImg from '@/assets/images/home/gold_pattern_bg.png';
import unityPreviewImg from '@/assets/images/home/unity_preview.png';
import leafImg from '@/assets/images/home/leaf.png'; 
import bowlBaseImg from '@/assets/images/home/bowl_base.png';
import patPhoenix from '@/assets/images/home/pattern_phoenix.png';
import patFlower from '@/assets/images/home/pattern_flower.png';
import patFish from '@/assets/images/home/pattern_fish.png';

// --- 全局鼠标 ---
const mouseX = ref(0);
const mouseY = ref(0);
const handleGlobalMouseMove = (e) => {
  mouseX.value = e.clientX;
  mouseY.value = e.clientY;
};
const parallaxStyle = computed(() => ({
  '--parallax-x': `${(window.innerWidth / 2 - mouseX.value) / 20}px`,
  '--parallax-y': `${(window.innerHeight / 2 - mouseY.value) / 20}px`
}));
const maskStyle = computed(() => ({
  'mask-image': `radial-gradient(circle 250px at ${mouseX.value}px ${mouseY.value}px, black 100%, transparent 100%)`,
  '-webkit-mask-image': `radial-gradient(circle 250px at ${mouseX.value}px ${mouseY.value}px, black 100%, transparent 100%)`
}));

// --- 粒子 ---
const getRandomEmberStyle = () => ({ width: Math.random()*4+2+'px', height: Math.random()*4+2+'px', left: Math.random()*100+'%', animationDuration: Math.random()*3+2+'s', animationDelay: Math.random()*5+'s' });

// --- 木叶 ---
const isLeafHovered = ref(false);

// --- 涟漪 ---
const ripples = ref([]);
const createRipple = (e) => {
  if (window.scrollY > window.innerHeight) return;
  const id = Date.now();
  ripples.value.push({ id, x: e.clientX, y: e.clientY });
  setTimeout(() => ripples.value = ripples.value.filter(r => r.id !== id), 1000);
};

// --- DIY Lite ---
const currentDiyPattern = ref(patPhoenix); 
const diyPatterns = [
  { name: '有凤来仪', src: patPhoenix },
  { name: '花开富贵', src: patFlower },
  { name: '连年有余', src: patFish },
  { name: '吉州木叶', src: leafImg }
];
const selectDiyPattern = (src) => { currentDiyPattern.value = src; };

// --- Sound Section ---
const activeSound = ref(null);
const currentAudio = ref(null);

const playSound = (type) => {
  activeSound.value = type;
  setTimeout(() => { activeSound.value = null; }, 2000);

  try {
    if (currentAudio.value) {
      currentAudio.value.pause();
      currentAudio.value.currentTime = 0; 
    }
    const audio = new Audio(`/sounds/${type}.mp3`);
    audio.volume = 0.6;
    currentAudio.value = audio;
    audio.play().catch(e => console.warn(`无法播放 /sounds/${type}.mp3`, e));
  } catch (error) {
    console.error("Audio Error:", error);
  }
};

// --- Unity ---
// --- Unity ---
const showUnity = ref(false);
const isUnityLoaded = ref(false); // 新增：控制加载状态

const openUnityModal = () => { 
  showUnity.value = true; 
  isUnityLoaded.value = false; // 每次打开先显示加载中
  document.body.style.overflow = 'hidden'; 
};

const closeUnityModal = () => { 
  showUnity.value = false; 
  document.body.style.overflow = ''; 
  // 关闭时重置 iframe src 可以停止 Unity 的声音和运行，下次打开重新加载
  // 如果希望后台运行，可以不重置，但在 Vue 中通常建议关闭即销毁
};

// iframe 加载完成的回调
const onUnityLoaded = () => {
  // 稍微延迟一点，确保 Unity 进度条已经接管画面
  setTimeout(() => {
    isUnityLoaded.value = true;
  }, 1000);
};

// --- AI 助手 ---
const isChatOpen = ref(false);
const isTyping = ref(false);
const inputMessage = ref('');
const chatBodyRef = ref(null);
const chatMessages = ref([
  { role: 'bot', content: '您好！我是您的专属<b>非遗守艺人</b>。<br>关于吉州窑的烧制技艺，或是鄂州剪纸的历史，您都可以问我。' }
]);

const toggleChat = () => { isChatOpen.value = !isChatOpen.value; };
const scrollToBottom = () => { 
  nextTick(() => { 
    if (chatBodyRef.value) chatBodyRef.value.scrollTop = chatBodyRef.value.scrollHeight; 
  }); 
};

const sendMessage = async () => {
  if (!inputMessage.value.trim()) return;

  const userText = inputMessage.value;
  chatMessages.value.push({ role: 'user', content: userText });
  inputMessage.value = '';
  scrollToBottom();

  isTyping.value = true;

  try {
    // 🔥 修改点：直接使用相对路径 /api
    // 这样本地开发走 vite 代理，服务器部署走 nginx 转发，永远不会报错
    const response = await fetch('/api/ai/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: userText }) // 确保后端用 data.get('message') 接收
    });

    if (!response.ok) throw new Error('网络请求失败');

    const result = await response.json();
    isTyping.value = false;
    
    // 把 AI 的回复放进对话框
    chatMessages.value.push({ role: 'bot', content: result.answer });
    scrollToBottom();

  } catch (error) {
    console.error('AI Error:', error);
    isTyping.value = false;
    chatMessages.value.push({ role: 'bot', content: '（守艺人暂时无法连接，请检查后端服务）' });
    scrollToBottom();
  }
};

const askQuestion = (q) => { inputMessage.value = q; sendMessage(); };
</script>

<style scoped>
.home-page { font-family: "Songti SC", "SimSun", serif; background-color: #1a100c; color: #fff; overflow-x: hidden; cursor: default; }
.hero-section { position: relative; width: 100%; height: 100vh; overflow: hidden; background-color: #1a100c; }
.embers-container { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 5; }
.ember { position: absolute; bottom: -10px; background: rgba(255, 215, 0, 0.6); border-radius: 50%; box-shadow: 0 0 10px rgba(255, 69, 0, 0.8); animation: floatUp linear infinite; opacity: 0; }
@keyframes floatUp { 0% { transform: translateY(0) scale(1); opacity: 0; } 10% { opacity: 1; } 100% { transform: translateY(-100vh) scale(0.5); opacity: 0; } }
.floating-leaf-container { position: absolute; top: 20%; right: 15%; z-index: 20; animation: leafFloat 6s ease-in-out infinite alternate; }
.leaf-img { width: 120px; opacity: 0.8; transition: all 0.5s ease; filter: brightness(0.8) sepia(1) hue-rotate(50deg); cursor: crosshair; }
.leaf-burned { filter: brightness(1.5) sepia(1) saturate(5) hue-rotate(0deg) drop-shadow(0 0 20px gold); transform: scale(1.2) rotate(10deg); }
.leaf-hint { position: absolute; bottom: -30px; width: 200px; left: -40px; font-size: 12px; color: rgba(255,255,255,0.5); pointer-events: none; animation: fadeInOut 2s infinite; }
@keyframes leafFloat { 0% { transform: translateY(0) rotate(0deg); } 100% { transform: translateY(20px) rotate(5deg); } }
@keyframes fadeInOut { 0%,100% { opacity: 0.3; } 50% { opacity: 1; } }
.ripples-container { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 30; overflow: hidden; }
.ripple { position: absolute; width: 10px; height: 10px; border-radius: 50%; border: 2px solid rgba(212, 175, 55, 0.8); transform: translate(-50%, -50%); animation: rippleAnim 1s ease-out forwards; }
@keyframes rippleAnim { 0% { width: 0; height: 0; opacity: 1; border-width: 5px; } 100% { width: 500px; height: 500px; opacity: 0; border-width: 0px; } }
.hero-title { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; font-size: 80px; font-weight: bold; letter-spacing: 10px; line-height: 1.2; white-space: nowrap; font-family: "Xingkai SC", cursive; pointer-events: none; }
.layer-dark { position: absolute; width: 100%; height: 100%; background: radial-gradient(circle at center, #5D4037 0%, #3E2723 40%, #1a100c 100%); display: flex; justify-content: center; align-items: center; }
.texture-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='4' height='4' viewBox='0 0 4 4'%3E%3Cpath fill='%23000000' fill-opacity='0.2' d='M1 3h1v1H1V3zm2-2h1v1H3V1z'%3E%3C/path%3E%3C/svg%3E"); opacity: 0.5; }
.hidden-title { color: rgba(255, 235, 205, 0.1); text-shadow: 0 0 10px rgba(255, 235, 205, 0.05); }
.layer-light { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-color: #000; pointer-events: none; z-index: 10; }
.light-content { position: relative; width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; background: radial-gradient(circle, #8B4513 0%, #3E2723 100%); }
.pattern-bg { position: absolute; width: 100%; height: 100%; object-fit: cover; opacity: 0.7; mix-blend-mode: overlay; }
.reveal-title { background: linear-gradient(to bottom, #FFECB3, #FFD54F); -webkit-background-clip: text; color: transparent; text-shadow: 0 0 30px rgba(255, 213, 79, 0.6); }
.scroll-hint { position: absolute; bottom: 50px; left: 50%; transform: translateX(-50%); text-align: center; color: rgba(255, 255, 255, 0.4); font-size: 14px; animation: float 3s ease-in-out infinite; z-index: 20; }
.mouse-icon { width: 20px; height: 30px; border: 2px solid rgba(255, 255, 255, 0.4); border-radius: 10px; margin: 0 auto 10px auto; position: relative; }
.mouse-icon::before { content: ''; position: absolute; top: 5px; left: 50%; transform: translateX(-50%); width: 4px; height: 4px; background: #fff; border-radius: 50%; animation: scrollWheel 2s infinite; }
@keyframes scrollWheel { 0% { top: 5px; opacity: 1; } 100% { top: 15px; opacity: 0; } }
@keyframes float { 0%, 100% { transform: translate(-50%, 0); } 50% { transform: translate(-50%, -10px); } }
.intro-section { padding: 100px 0; background: #231612; display: flex; justify-content: center; position: relative; overflow: hidden; }
.intro-section::before { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-image: url('https://www.transparenttextures.com/patterns/wood-pattern.png'); opacity: 0.1; z-index: 1; }
.parallax-bg { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 0; pointer-events: none; }
.parallax-layer { position: absolute; width: 600px; opacity: 0.05; filter: invert(1); transition: transform 0.1s linear; }
.layer-1 { top: -100px; left: -100px; transform: translate(var(--parallax-x), var(--parallax-y)); }
.layer-2 { bottom: -100px; right: -100px; transform: translate(calc(var(--parallax-x) * -1.5), calc(var(--parallax-y) * -1.5)); }
.intro-container { width: 1200px; max-width: 95%; display: flex; align-items: center; justify-content: space-between; z-index: 2; }
.intro-text { width: 50%; }
.intro-text h2 { font-size: 36px; color: #E6CFA2; margin-bottom: 30px; border-left: 4px solid #D4AF37; padding-left: 20px; }
.intro-text p { font-size: 16px; line-height: 2; color: #BCAAA4; text-align: justify; }
.intro-visual { width: 40%; display: flex; justify-content: center; }
.circle-fusion { width: 300px; height: 300px; border-radius: 50%; position: relative; overflow: hidden; box-shadow: 0 0 50px rgba(139, 69, 19, 0.3); animation: rotateCircle 20s linear infinite; }
.half { position: absolute; width: 100%; height: 100%; top: 0; left: 0; }
.fire { background: linear-gradient(135deg, #5D4037 0%, #3E2723 50%); clip-path: polygon(0 0, 100% 0, 100% 100%); }
.paper { background: linear-gradient(-45deg, #FFD54F 0%, transparent 60%); clip-path: polygon(0 0, 0 100%, 100% 100%); }
.center-text { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 80px; height: 80px; background: #231612; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 1px solid #D4AF37; color: #D4AF37; font-size: 20px; z-index: 2; }
@keyframes rotateCircle { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
.diy-lite-section { padding: 80px 0; background-color: #1f1512; text-align: center; }
.diy-header h2 { font-size: 32px; color: #E6CFA2; margin-bottom: 10px; font-family: "Xingkai SC", cursive; }
.diy-header p { color: #888; margin-bottom: 40px; }
.diy-container { width: 1200px; max-width: 95%; margin: 0 auto; }
.diy-workspace { display: flex; justify-content: center; gap: 80px; align-items: center; }
.bowl-preview-container { position: relative; width: 400px; height: 300px; }
.bowl-base-img { width: 300px; height: 300px; object-fit: contain; filter: brightness(0.8); z-index: 1; position: relative; margin: 0 auto; }
.pattern-overlay-img {
  position: absolute;
  top: 60%; 
  left: 50%;
  width: 35%; 
  transform: translate(-50%, -40%); 
  opacity: 0.9;
  z-index: 2;
  mix-blend-mode: color-dodge;
  filter: drop-shadow(0 0 5px rgba(212, 175, 55, 0.5));
}
.bowl-shine-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(ellipse at 40% 30%, rgba(255,255,255,0.1) 0%, transparent 60%); pointer-events: none; z-index: 3; }
.pattern-selector { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
.pattern-option { width: 100px; height: 100px; border: 1px solid #5D4037; border-radius: 10px; display: flex; flex-direction: column; align-items: center; justify-content: center; cursor: pointer; transition: all 0.3s; background: #2D2420; }
.pattern-option img { width: 60%; height: 60%; object-fit: contain; }
.pattern-option span { font-size: 12px; color: #aaa; margin-top: 5px; }
.pattern-option:hover, .pattern-option.active { border-color: #D4AF37; background: #3E2723; transform: scale(1.05); }
.fade-scale-enter-active, .fade-scale-leave-active { transition: all 0.5s ease; }
.fade-scale-enter-from, .fade-scale-leave-to { opacity: 0; transform: scale(0.8); }
.unity-entry-section { padding: 80px 0; background: linear-gradient(to bottom, #231612, #1a100c); border-top: 1px solid #3E2723; border-bottom: 1px solid #3E2723; }
.unity-content { width: 1200px; max-width: 95%; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; }
.unity-text { width: 50%; }
.unity-title { font-size: 36px; color: #D4AF37; margin-bottom: 20px; font-family: "Xingkai SC", cursive; }
.unity-desc { font-size: 16px; color: #ccc; line-height: 1.8; margin-bottom: 40px; }
.unity-btn { padding: 15px 40px; background: linear-gradient(90deg, #D4AF37 0%, #8B4513 100%); color: #fff; font-size: 18px; font-weight: bold; border: none; border-radius: 50px; cursor: pointer; transition: transform 0.3s, box-shadow 0.3s; display: flex; align-items: center; gap: 10px; box-shadow: 0 5px 15px rgba(212, 175, 55, 0.3); }
.unity-btn:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(212, 175, 55, 0.5); }
.unity-visual {
  width: 35%; /* 父容器缩至35% */
}
.unity-visual img {
  width: 70%; /* 图片缩至70% */
  border-radius: 8px; /* 圆角同步缩小 */
  box-shadow: 0 6px 20px rgba(0,0,0,0.4); /* 阴影更柔和、更小 */
  border: 1px solid #5D4037; /* 边框从2px减为1px */
}

.holo-img { width: 100%; border-radius: 8px; box-shadow: 0 0 20px rgba(212, 175, 55, 0.2); border: 1px solid #5D4037; transition: all 0.3s; }
.holographic-container:hover .holo-img { box-shadow: 0 0 40px rgba(212, 175, 55, 0.6); border-color: #D4AF37; }
.scan-line { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(to bottom, transparent 50%, rgba(212, 175, 55, 0.1) 51%, transparent 55%); background-size: 100% 4px; pointer-events: none; opacity: 0; transition: opacity 0.3s; }
.holographic-container:hover .scan-line { opacity: 1; animation: scanMove 2s linear infinite; }
@keyframes scanMove { 0% { background-position: 0 0; } 100% { background-position: 0 100%; } }
.sound-section { padding: 80px 0; background-color: #1a100c; text-align: center; }
.section-title { font-size: 32px; color: #E6CFA2; margin-bottom: 60px; font-weight: normal; letter-spacing: 2px; }
.sound-grid { width: 1000px; margin: 0 auto; display: flex; justify-content: space-around; }
.sound-item { display: flex; flex-direction: column; align-items: center; cursor: pointer; }
.sound-circle { width: 100px; height: 100px; border-radius: 50%; border: 1px solid #5D4037; display: flex; justify-content: center; align-items: center; position: relative; transition: all 0.3s; background: #231612; }
.sound-icon { font-size: 40px; filter: drop-shadow(0 0 5px gold); }
.sound-item:hover .sound-circle { border-color: #D4AF37; background: #3E2723; transform: scale(1.1); box-shadow: 0 0 20px rgba(212, 175, 55, 0.4); }
.sound-item h3 { margin-top: 20px; color: #E6CFA2; font-size: 18px; }
.sound-item p { color: #888; font-size: 12px; margin-top: 5px; }
.wave-ring { position: absolute; width: 100%; height: 100%; border: 2px solid #D4AF37; border-radius: 50%; opacity: 0; animation: soundWave 1.5s infinite ease-out; }
.delay-1 { animation-delay: 0.5s; }
@keyframes soundWave { 0% { transform: scale(1); opacity: 0.8; } 100% { transform: scale(2); opacity: 0; } }
.explore-section { padding: 80px 0 120px 0; background-color: #1a100c; text-align: center; }
.cards-grid { width: 1200px; max-width: 95%; margin: 0 auto; display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px; }
.explore-card { background-color: transparent; height: 350px; perspective: 1000px; text-decoration: none; }
.card-inner { position: relative; width: 100%; height: 100%; text-align: center; transition: transform 0.8s; transform-style: preserve-3d; cursor: pointer; border: 1px solid #5D4037; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
.explore-card:hover .card-inner { transform: rotateY(180deg); border-color: #FFD54F; }
.card-front, .card-back { position: absolute; width: 100%; height: 100%; backface-visibility: hidden; display: flex; flex-direction: column; justify-content: center; align-items: center; }
.card-front { background-color: #2D2420; color: #E6CFA2; }
.card-icon { font-size: 60px; margin-bottom: 20px; transform: translateZ(30px); }
.card-front h3 { font-size: 24px; letter-spacing: 2px; transform: translateZ(20px); }
.card-back { background-color: #D4AF37; color: #3E2723; transform: rotateY(180deg); }
.card-back p { font-size: 18px; line-height: 1.5; font-weight: bold; margin-bottom: 20px; transform: translateZ(20px); }
.go-btn { font-size: 14px; border: 1px solid #3E2723; padding: 8px 20px; border-radius: 30px; transition: all 0.3s; transform: translateZ(30px); }
.go-btn:hover { background: #3E2723; color: #D4AF37; }
.unity-modal-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background-color: rgba(0, 0, 0, 0.9); z-index: 9999; display: flex; justify-content: center; align-items: center; backdrop-filter: blur(5px); animation: fadeIn 0.3s; }
.unity-window { width: 90%; height: 90%; max-width: 1600px; background-color: #000; border: 2px solid #5D4037; border-radius: 10px; position: relative; display: flex; flex-direction: column; box-shadow: 0 0 50px rgba(0,0,0,0.8); }
.close-unity-btn { position: absolute; top: -20px; right: -20px; width: 40px; height: 40px; background: #D4AF37; color: #000; border: none; border-radius: 50%; font-size: 24px; cursor: pointer; z-index: 10; font-weight: bold; }
.close-unity-btn:hover { background: #fff; }
.unity-header { height: 40px; background-color: #1a100c; display: flex; align-items: center; padding-left: 20px; border-bottom: 1px solid #333; }
.unity-header h3 { color: #aaa; font-size: 14px; font-weight: normal; margin: 0; }
.unity-iframe-container { flex: 1; position: relative; width: 100%; height: 100%; }
.unity-iframe { 
  width: 100%; 
  height: 100%; 
  display: block; 
  z-index: 2; 
  position: relative; 
  background: transparent; 
  opacity: 0; /* 默认隐藏 */
  transition: opacity 0.5s ease;
}

.unity-iframe.visible {
  opacity: 1; /* 加载完成后显示 */
}

.unity-placeholder { 
  position: absolute; 
  top: 0; 
  left: 0; 
  width: 100%; 
  height: 100%; 
  display: flex; 
  flex-direction: column; 
  justify-content: center; 
  align-items: center; 
  z-index: 1; 
  color: #D4AF37; 
  background: #000; /* 纯黑背景防止透出 */
}
.unity-placeholder { position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 1; color: #D4AF37; }
.loader { border: 4px solid #333; border-top: 4px solid #D4AF37; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin-bottom: 20px; }
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

/* AI Floater */
.ai-floater { position: fixed; bottom: 30px; right: 30px; z-index: 100; cursor: pointer; display: flex; align-items: center; transition: all 0.3s; }
.ai-floater.hide { transform: scale(0); opacity: 0; }
.ai-avatar { width: 80px; height: 80px; background: linear-gradient(135deg, #D4AF37, #8B4513); border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 30px; box-shadow: 0 0 20px rgba(212, 175, 55, 0.4); animation: floatAvatar 3s ease-in-out infinite; border: 2px solid #fff; }
@keyframes floatAvatar { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
.ai-tip { background: rgba(0,0,0,0.8); color: #fff; padding: 8px 15px; border-radius: 20px; margin-right: 15px; font-size: 14px; opacity: 0; transform: translateX(20px); transition: all 0.3s; pointer-events: none; }
.ai-floater:hover .ai-tip { opacity: 1; transform: translateX(0); }
.chat-panel { position: fixed; bottom: 100px; right: 30px; width: 350px; height: 500px; background: rgba(26, 16, 12, 0.95); border: 1px solid #5D4037; border-radius: 15px; z-index: 101; display: flex; flex-direction: column; box-shadow: 0 10px 40px rgba(0,0,0,0.6); backdrop-filter: blur(10px); overflow: hidden; }
.chat-header { padding: 15px; background: #2D2420; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #3E2723; }
.header-info { display: flex; align-items: center; gap: 10px; }
.avatar-small { font-size: 20px; background: #D4AF37; width: 30px; height: 30px; border-radius: 50%; display: flex; justify-content: center; align-items: center; }
.name { color: #E6CFA2; font-weight: bold; }
.status { font-size: 12px; color: #4CAF50; }
.close-chat { background: none; border: none; color: #888; font-size: 24px; cursor: pointer; }
.close-chat:hover { color: #fff; }
.chat-body { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 15px; }
.chat-body::-webkit-scrollbar { width: 5px; }
.chat-body::-webkit-scrollbar-thumb { background: #5D4037; border-radius: 5px; }
.message-row { display: flex; gap: 10px; align-items: flex-start; }
.message-row.user { flex-direction: row-reverse; }
.message-row .avatar { width: 35px; height: 35px; background: #3E2723; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 18px; border: 1px solid #D4AF37; }
.message-row .bubble { max-width: 70%; padding: 10px 15px; border-radius: 10px; font-size: 14px; line-height: 1.5; position: relative; }
.message-row.bot .bubble { background: #3E2723; color: #E6CFA2; border-top-left-radius: 0; }
.message-row.user .bubble { background: #D4AF37; color: #1a100c; border-top-right-radius: 0; font-weight: bold; }
.typing span { display: inline-block; animation: bounce 1s infinite; margin: 0 2px; font-size: 20px; }
.typing span:nth-child(2) { animation-delay: 0.2s; }
.typing span:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-5px); } }
.chat-footer { padding: 15px; background: #231612; border-top: 1px solid #3E2723; }
.quick-tags { display: flex; gap: 8px; margin-bottom: 10px; overflow-x: auto; padding-bottom: 5px; }
.quick-tags span { white-space: nowrap; background: rgba(212, 175, 55, 0.1); color: #D4AF37; padding: 4px 10px; border-radius: 15px; font-size: 12px; border: 1px solid rgba(212, 175, 55, 0.3); cursor: pointer; transition: all 0.2s; }
.quick-tags span:hover { background: #D4AF37; color: #000; }
.input-box { display: flex; gap: 10px; }
.input-box input { flex: 1; background: #1a100c; border: 1px solid #5D4037; color: #fff; padding: 8px 12px; border-radius: 20px; outline: none; }
.input-box input:focus { border-color: #D4AF37; }
.input-box button { background: #D4AF37; color: #000; border: none; padding: 0 15px; border-radius: 20px; cursor: pointer; font-weight: bold; }
.input-box button:hover { background: #FFD54F; }
.slide-up-enter-active, .slide-up-leave-active { transition: all 0.3s ease; }
.slide-up-enter-from, .slide-up-leave-to { transform: translateY(20px); opacity: 0; }

@media (max-width: 768px) {
  .hero-title { font-size: 40px; }
  .intro-container, .unity-content, .diy-workspace { flex-direction: column; }
  .intro-text, .intro-visual, .unity-text, .unity-visual { width: 100%; margin-bottom: 40px; }
  .cards-grid, .sound-grid { grid-template-columns: 1fr; flex-direction: column; gap: 30px; }
  .unity-window { width: 100%; height: 100%; border: none; }
  .close-unity-btn { top: 10px; right: 10px; }
  .parallax-layer { display: none; }
  .bowl-preview { width: 200px; height: 200px; margin-bottom: 30px; }
  .chat-panel { width: 90%; right: 5%; bottom: 80px; }
}
</style>