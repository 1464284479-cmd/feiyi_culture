<template>
  <div class="shop-container">
    
    <!-- 1. 顶部 Header -->
    <header class="main-header">
      <div class="top-bar">
        <div class="top-bar-inner">
          <div class="brand-text">剪釉双坊</div>
          <div class="user-actions">
            <div class="cart-btn" @click="toggleCart">
              <span class="icon">🛒</span> 购物车
              <span class="badge" v-if="cartCount > 0">{{ cartCount }}</span>
            </div>
            <div class="divider">|</div>
            <div class="auth-links" v-if="!currentUser">
              <span class="highlight" @click="openAuthModal('login')">登录</span>
              <span @click="openAuthModal('register')">注册</span>
            </div>
            <div class="auth-links user-profile" v-else @click="showProfileModal = true">
              <img :src="getAvatarUrl(currentUser.avatar)" class="user-avatar-small">
              <span class="username">{{ currentUser.username }}</span>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- 核心布局：左右结构 -->
    <div class="main-layout">
      
      <!-- 2. 左侧：悬浮侧边栏 -->
      <aside class="sticky-sidebar">
        <!-- 搜索框 -->
        <div class="sidebar-block search-block">
          <input type="text" v-model="searchQuery" placeholder="搜非遗好物..." @keyup.enter="handleSearch">
          <button @click="handleSearch">🔍</button>
        </div>

        <!-- 核心分类 -->
        <div class="sidebar-block">
          <h3 class="block-title">珍品分类</h3>
          <ul class="filter-list">
            <li 
              v-for="cat in categories" 
              :key="cat.key" 
              :class="{ active: currentCategory === cat.key }" 
              @click="filterCategory(cat.key)"
            >
              <span class="dot"></span> {{ cat.name }}
            </li>
          </ul>
        </div>

        <!-- 场景推荐 -->
        <div class="sidebar-block">
          <h3 class="block-title">场景雅集</h3>
          <ul class="filter-list">
            <li :class="{ active: sceneFilter === 'all' }" @click="filterScene('all')">全部场景</li>
            <li :class="{ active: sceneFilter === 'tea' }" @click="filterScene('tea')">🍵 茶室雅集</li>
            <li :class="{ active: sceneFilter === 'gift' }" @click="filterScene('gift')">🎁 礼赠首选</li>
            <li :class="{ active: sceneFilter === 'home' }" @click="filterScene('home')">🏠 家居装饰</li>
          </ul>
        </div>

        <!-- 个人服务 -->
        <div class="sidebar-block">
          <h3 class="block-title">个人服务</h3>
          <div class="mini-card" @click="openOrderListModal">📦 我的订单</div>
        </div>
      </aside>

      <!-- 3. 右侧：主要内容区 -->
      <main class="content-area">
        
        <!-- 3.1 Hero 轮播图 -->
        <section class="carousel-section">
          <div class="carousel-container" @mouseenter="pauseCarousel" @mouseleave="startCarousel">
            <div class="carousel-track" :style="{ transform: `translateX(-${currentSlide * 100}%)` }">
              <div v-for="(item, index) in hotProducts" :key="index" class="carousel-slide">
                <img :src="getImageUrl(item.mainImage)" class="slide-bg">
                <div class="slide-content">
                  <span class="slide-tag">热门推荐</span>
                  <h2>{{ item.name }}</h2>
                  <p>{{ item.description }}</p>
                  <button @click="openProductModal(item)">立即查看</button>
                </div>
              </div>
            </div>
            <button class="arrow left" @click="prevSlide">‹</button>
            <button class="arrow right" @click="nextSlide">›</button>
          </div>
        </section>

        <!-- 3.2 优惠券专区 -->
        <section class="coupon-section" id="coupons">
          <h3 class="inner-title">限时礼遇</h3>
          <div class="coupon-grid">
            <div 
              v-for="coupon in coupons" 
              :key="coupon.id" 
              class="coupon-card" 
              :class="{ claimed: isCouponClaimed(coupon.id) }" 
              @click="claimCoupon(coupon)"
            >
              <div class="cp-left">
                <div class="cp-price"><span>¥</span>{{ coupon.amount }}</div>
                <div class="cp-cond">满{{ coupon.threshold }}可用</div>
              </div>
              <div class="cp-right">
                <div class="cp-name">{{ coupon.name }}</div>
                <div class="cp-btn">{{ isCouponClaimed(coupon.id) ? '已领' : '领取' }}</div>
              </div>
              <div class="circle top"></div>
              <div class="circle bottom"></div>
            </div>
          </div>
        </section>

        <!-- 3.3 趣味体验 · 云端开窑 -->
        <section class="kiln-game-section">
          <h3 class="inner-title" style="color: #E65100; border-color: #E65100;">趣味体验 · 云端开窑</h3>
          <div class="kiln-wrapper">
            <!-- 状态1: 准备/烧制中 -->
            <div v-if="kilnState !== 'done'" class="kiln-furnace" :class="{ 'is-firing': kilnState === 'firing' }">
              <div class="furnace-door">
                <div class="fire-glow" v-if="kilnState === 'firing'"></div>
                <div class="furnace-text" v-if="kilnState === 'idle'">吉州古窑</div>
                <div class="furnace-text firing-text" v-else>烈火淬炼中...</div>
              </div>
              <div class="furnace-controls">
                <p>“入窑一色，出窑万彩”。点击点火，寻觅您的天选珍品。</p>
                <button class="fire-btn" @click="startFiring" :disabled="kilnState === 'firing'">
                  {{ kilnState === 'firing' ? '正在烧制...' : '🔥 点火开窑' }}
                </button>
              </div>
            </div>

            <!-- 状态2: 开窑结果 -->
            <div v-else class="kiln-result">
              <div class="result-card">
                <div class="result-header">
                  <span class="luck-tag">签文：{{ firedResult.luck }}</span>
                </div>
                <img :src="getImageUrl(firedResult.product.mainImage)" class="result-img">
                <h4>{{ firedResult.product.name }}</h4>
                <p class="result-desc">{{ firedResult.product.description }}</p>
                <div class="result-price">市场价：¥ {{ getMinPrice(firedResult.product) }}</div>
                <div class="result-actions">
                  <button class="view-btn" @click="openProductModal(firedResult.product)">查看详情</button>
                  <button class="retry-btn" @click="resetKiln">再烧一窑</button>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- 3.4 大师工坊工艺演示 -->
        <section class="workshop-section">
          <h3 class="inner-title" style="color:#E6CFA2;border-color:#E6CFA2">大师工坊 · 窑纸共生</h3>
          <div class="process-flow">
            <div class="process-step"><div class="icon-circle">✂️</div><h4>剪纸创作</h4><p>非遗传承人手工刻制</p></div>
            <div class="arrow-anim">→</div>
            <div class="process-step"><div class="icon-circle">🏺</div><h4>贴花入窑</h4><p>将纹样贴于素坯之上</p></div>
            <div class="arrow-anim">→</div>
            <div class="process-step"><div class="icon-circle">🔥</div><h4>高温烧制</h4><p>1300℃ 窑变天成</p></div>
            <div class="arrow-anim">→</div>
            <div class="process-step"><div class="icon-circle">🎁</div><h4>成品出窑</h4><p>独一无二的艺术品</p></div>
          </div>
        </section>

        <!-- 3.5 扩展分区：非遗知识问答 -->
        <section class="quiz-section">
          <div class="inner-header">
            <h3 class="inner-title" style="margin-bottom:0;border:none;">每日一答 · 涨知识</h3>
            <span class="refresh-quiz" @click="fetchQuiz" style="cursor:pointer; color:#8B4513; font-size:12px;">🔄 换一题</span>
          </div>
          
          <div class="quiz-card" v-if="currentQuiz">
            <div class="quiz-q">
              <span class="q-badge">问</span>
              <p>{{ currentQuiz.question }}</p>
            </div>
            
            <div class="quiz-options">
              <button 
                v-for="opt in currentQuiz.options" 
                :key="opt.key"
                :class="{ 
                  'correct': quizResult === 'correct' && currentQuiz.correct === opt.key,
                  'wrong': quizResult === 'wrong' && selectedOption === opt.key,
                  'disabled': quizResult !== null 
                }"
                @click="answerQuiz(opt.key)"
                :disabled="quizResult !== null"
              >
                {{ opt.key }}. {{ opt.text }}
              </button>
            </div>

            <!-- 答题反馈 -->
            <div class="quiz-feedback" v-if="quizResult">
              <p :class="quizResult === 'correct' ? 'green' : 'red'">
                {{ quizResult === 'correct' ? '🎉 回答正确！' : '😂 回答错误，正确答案是 ' + currentQuiz.correct }}
              </p>
              <p class="explanation">{{ currentQuiz.explanation }}</p>
            </div>
          </div>
          <div v-else class="loading-state">题目加载中...</div>
        </section>

        <!-- 3.6 商品列表 -->
        <div class="product-section" id="product-list">
          <div class="section-header">
            <h2>{{ getCurrentTitle() }}</h2>
            <span class="count">共 {{ totalItems }} 件珍品</span>
          </div>

          <div v-if="loading" class="loading-state"><div class="spinner"></div> 正在搬运珍品...</div>
          <div v-else-if="products.length === 0" class="empty-state">暂无相关商品。</div>
          
          <div v-else class="product-grid">
            <div v-for="product in products" :key="product.id" class="product-card">
              <div class="card-img" @click="openProductModal(product)">
                <img :src="getImageUrl(product.mainImage)" @error="handleImgError">
                <div class="overlay">查看详情</div>
              </div>
              <div class="card-info">
                <div class="tag" :class="product.category">{{ product.category === 'kiln' ? '吉州窑' : '鄂州剪纸' }}</div>
                <h3>{{ product.name }}</h3>
                <div class="bottom-row">
                  <span class="price">¥ {{ getMinPrice(product) }}</span>
                  <button class="add-btn" @click="openProductModal(product)">+</button>
                </div>
              </div>
            </div>
          </div>

          <div class="pagination" v-if="totalPages > 1">
            <button :disabled="currentPage === 1" @click="changePage(currentPage - 1)">上一页</button>
            <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
            <button :disabled="currentPage === totalPages" @click="changePage(currentPage + 1)">下一页</button>
          </div>
        </div>

        <!-- 3.7 资讯区 -->
        <section class="news-section" id="news">
          <h3 class="inner-title">非遗头条</h3>
          <div class="news-list">
            <div v-for="item in newsList" :key="item.id" class="news-item" @click="openNewsModal(item.id)">
              <span class="news-tag">{{ item.tag }}</span>
              <span class="news-title">{{ item.title }}</span>
              <span class="news-date">{{ item.date }}</span>
            </div>
          </div>
        </section>

      </main>
    </div>

    <!-- 4. 弹窗组件 -->

    <!-- 填写订单/收货地址弹窗 -->
    <Transition name="fade">
      <div v-if="showCheckoutModal" class="modal-mask">
        <div class="checkout-box">
          <div class="checkout-header">
            <h3>确认订单信息</h3>
            <span @click="showCheckoutModal = false" class="close-icon">×</span>
          </div>
          <div class="checkout-body">
            <div class="form-section">
              <h4>收货人信息</h4>
              <div class="form-row">
                <input type="text" v-model="addressForm.name" placeholder="姓名 (必填)">
                <input type="text" v-model="addressForm.phone" placeholder="手机号 (必填)">
              </div>
              <div class="form-row">
                <input type="text" v-model="addressForm.address" placeholder="详细地址: 省/市/区/街道/门牌号 (必填)" class="full-width">
              </div>
            </div>
            <div class="order-summary">
              <h4>商品清单</h4>
              <div class="summary-item" v-for="item in cartItems" :key="item.id">
                <span>{{ item.productName }} ({{ item.variantName }}) x {{ item.quantity }}</span>
                <span>¥ {{ (item.price * item.quantity).toFixed(2) }}</span>
              </div>
              <div class="summary-total">
                <p>商品总额: ¥ {{ cartTotalRaw.toFixed(2) }}</p>
                <p class="red">优惠减免: -¥ {{ bestCoupon }}</p>
                <p class="final">实付金额: ¥ {{ finalTotal.toFixed(2) }}</p>
              </div>
            </div>
          </div>
          <div class="checkout-footer">
            <button class="cancel-btn" @click="showCheckoutModal = false">取消</button>
            <button class="pay-btn" @click="createOrder">提交订单并支付</button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- 收银台/支付弹窗 -->
    <Transition name="fade">
      <div v-if="showPaymentModal" class="modal-mask">
        <div class="payment-box">
          <h3>收银台</h3>
          <p class="pay-amount">¥ {{ currentOrder.totalPrice }}</p>
          <div class="qr-container">
            <div class="qr-code">
              <div class="qr-inner"></div>
              <p>支付宝/微信 扫码支付</p>
            </div>
          </div>
          <p class="pay-tip">正在等待支付结果...</p>
          <button class="mock-pay-btn" @click="confirmPayment">模拟支付成功 (测试用)</button>
        </div>
      </div>
    </Transition>

    <!-- 我的订单列表弹窗 -->
    <Transition name="fade">
      <div v-if="showOrderListModal" class="modal-mask" @click.self="showOrderListModal = false">
        <div class="order-list-box">
          <div class="ol-header">
            <h3>我的订单</h3>
            <span @click="showOrderListModal = false" class="close-icon">×</span>
          </div>
          <div class="ol-body">
            <div v-if="myOrders.length === 0" class="empty-state">暂无订单</div>
            <div v-else class="order-card" v-for="order in myOrders" :key="order.id">
              <div class="oc-top">
                <span class="oc-time">{{ order.createTime }}</span>
                <span class="oc-status" :class="order.status">{{ getStatusText(order.status) }}</span>
              </div>
              <div class="oc-products">
                <div v-for="item in order.items" :key="item.id" class="oc-item">
                  {{ item.productName }} - {{ item.variantName }} x {{ item.quantity }}
                </div>
              </div>
              <div class="oc-bottom">
                <span class="oc-total">实付: ¥ {{ order.totalPrice }}</span>
                <button v-if="order.status === 'Pending'" class="action-btn primary" @click="continuePay(order)">去支付</button>
                <button v-if="order.status === 'Paid'" class="action-btn disabled">等待发货</button>
                <button v-if="order.status === 'Shipped'" @click="confirmReceive(order.id)" class="action-btn primary">确认收货</button>
                <button v-if="order.status === 'Completed'" class="action-btn text-btn">已完成</button>
                <button v-if="order.status === 'Paid'" @click="mockShip(order.id)" class="cheat-btn">(测试发货)</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- 登录/注册 -->
    <Transition name="fade">
      <div v-if="showAuthModal" class="modal-mask" @click.self="showAuthModal = false">
        <div class="auth-card">
          <div class="auth-sidebar">
            <h3>剪釉双坊</h3>
            <p>传承非遗 · 匠心独运</p>
          </div>
          <div class="auth-main">
            <h2 class="auth-title">{{ authMode === 'login' ? '欢迎回来' : '创建账号' }}</h2>
            <div class="input-group">
              <input type="text" v-model="authForm.username" required>
              <label>用户名</label>
            </div>
            <div class="input-group">
              <input type="password" v-model="authForm.password" required>
              <label>密码</label>
            </div>
            <button class="auth-btn" @click="handleAuth">
              {{ authMode === 'login' ? '登 录' : '注 册' }}
            </button>
            <div class="auth-footer">
              <span @click="switchAuthMode">
                {{ authMode === 'login' ? '没有账号？去注册' : '已有账号？去登录' }}
              </span>
            </div>
            <p class="error-msg" v-if="authError">{{ authError }}</p>
          </div>
        </div>
      </div>
    </Transition>

    <!-- 个人中心 (本地上传头像) -->
    <Transition name="fade">
      <div v-if="showProfileModal" class="modal-mask" @click.self="showProfileModal = false">
        <div class="profile-card">
          <div class="profile-header">
            <div class="avatar-wrapper">
              <img :src="getAvatarUrl(currentUser.avatar)">
              <input type="file" ref="fileInput" @change="handleFileChange" accept="image/*" style="display: none;">
              <div class="avatar-edit" @click="triggerFileUpload">📷</div>
            </div>
            <h3>{{ currentUser.username }}</h3>
            <p class="user-role">非遗传承守护者</p>
          </div>
          <div class="profile-footer">
            <button class="logout-btn" @click="handleLogout">退出登录</button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- 商品详情 -->
    <Transition name="fade">
      <div v-if="showProductModal" class="modal-mask" @click.self="showProductModal = false">
        <div class="product-modal-box">
          <button class="close-btn" @click="showProductModal = false">×</button>
          <div class="pm-left"><img :src="getImageUrl(selectedProduct.mainImage)" @error="handleImgError"></div>
          <div class="pm-right">
            <h2>{{ selectedProduct.name }}</h2>
            <p class="desc">{{ selectedProduct.description }}</p>
            <div class="variant-area">
              <h4>款式:</h4>
              <div class="tags">
                <span v-for="v in selectedProduct.variants" :key="v.id" :class="{ active: selectedVariant?.id === v.id, disabled: v.stock <= 0 }" @click="v.stock > 0 && (selectedVariant = v)">
                  {{ v.name }} (¥{{ v.price }})
                </span>
              </div>
            </div>
            <div class="qty-area">
              <h4>数量:</h4>
              <div class="qty-control">
                <button @click="buyQuantity > 1 && buyQuantity--">-</button>
                <input type="text" v-model="buyQuantity" readonly>
                <button @click="buyQuantity++">+</button>
              </div>
            </div>
            <div class="pm-footer">
               <div class="total" v-if="selectedVariant">¥ {{ (selectedVariant.price * buyQuantity).toFixed(2) }}</div>
               <div class="total" v-else>请选择款式</div>
               <button class="confirm-btn" @click="addToCart">加入购物车</button>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- 新闻详情 -->
    <Transition name="fade">
      <div v-if="showNewsModal" class="modal-mask" @click.self="showNewsModal = false">
        <div class="news-modal">
          <button class="close-btn" @click="showNewsModal = false">×</button>
          <h2 class="news-modal-title">{{ currentNews.title }}</h2>
          <p class="news-meta">{{ currentNews.date }}</p>
          <div class="news-content">{{ currentNews.content }}</div>
        </div>
      </div>
    </Transition>

    <!-- 购物车抽屉 -->
    <div class="cart-drawer" :class="{ open: isCartOpen }">
      <div class="drawer-header"><h3>购物车</h3><span @click="isCartOpen = false" class="close-icon">×</span></div>
      <div class="drawer-body">
        <div v-if="!currentUser" class="empty-tip">请先登录</div>
        <div v-else-if="cartItems.length === 0" class="empty-tip">空空如也</div>
        <div v-else class="cart-list">
          <div v-for="item in cartItems" :key="item.id" class="cart-item">
            <img :src="getImageUrl(item.image)" class="thumb">
            <div class="info"><h4>{{ item.productName }}</h4><p>{{ item.variantName }} x {{ item.quantity }}</p><span class="price">¥ {{ item.price }}</span></div>
          </div>
        </div>
      </div>
      <div class="drawer-footer" v-if="cartItems.length > 0">
        <div class="discount-info" v-if="bestCoupon > 0">
          <span class="tag">优惠券</span> 已自动减免: <span class="red">-¥ {{ bestCoupon }}</span>
        </div>
        <div class="total-bar">合计: <span class="red">¥ {{ finalTotal.toFixed(2) }}</span></div>
        <button class="checkout-btn" @click="openCheckoutModal">去结算</button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue';
import axios from 'axios';
import defaultImg from '@/assets/images/product_sakura.png';
import defaultAvatar from '@/assets/images/shop_logo.png'; 

const API_BASE_URL = 'http://127.0.0.1:5000/api';

// --- 状态数据 ---
const currentUser = ref(null);
const products = ref([]);
const hotProducts = ref([]); 
const coupons = ref([]);     
const myCoupons = ref([]);
const newsList = ref([]);
const claimedCoupons = ref(new Set()); 
const myOrders = ref([]); // 订单列表

const cartItems = ref([]);
const loading = ref(false);
const searchQuery = ref('');
const currentCategory = ref('all');
const sceneFilter = ref('all'); 
const currentPage = ref(1);
const totalPages = ref(1);
const totalItems = ref(0);

// --- UI 弹窗控制 ---
const isCartOpen = ref(false);
const showAuthModal = ref(false);
const showProfileModal = ref(false);
const showProductModal = ref(false);
const showNewsModal = ref(false);
const showCheckoutModal = ref(false); // 结算弹窗
const showPaymentModal = ref(false);  // 支付弹窗
const showOrderListModal = ref(false); // 订单列表弹窗

// --- 业务数据 ---
const currentNews = ref({});
const fileInput = ref(null); 
const authMode = ref('login');
const authError = ref('');
const authForm = reactive({ username: '', password: '' });
const addressForm = reactive({ name: '', phone: '', address: '' }); // 收货地址表单
const currentOrder = ref({}); // 当前正在支付的订单

const currentSlide = ref(0);
const carouselTimer = ref(null);

// 开窑游戏状态
const kilnState = ref('idle'); // idle, firing, done
const firedResult = ref({ product: {}, luck: '' });

// 问答游戏状态
const currentQuiz = ref(null);
const quizResult = ref(null); // null, 'correct', 'wrong'
const selectedOption = ref(null);

const selectedProduct = ref({});
const selectedVariant = ref(null);
const buyQuantity = ref(1);

// 配置
const categories = [ { name: '全部珍品', key: 'all' }, { name: '吉州窑瓷', key: 'kiln' }, { name: '鄂州剪纸', key: 'paper-cut' } ];

// 计算属性
const cartCount = computed(() => cartItems.value.reduce((s, i) => s + i.quantity, 0));
const cartTotalRaw = computed(() => cartItems.value.reduce((s, i) => s + i.price * i.quantity, 0));
const bestCoupon = computed(() => {
  if (myCoupons.value.length === 0) return 0;
  let maxDisc = 0;
  myCoupons.value.forEach(c => {
    if (cartTotalRaw.value >= c.threshold) {
      if (c.amount > maxDisc) maxDisc = c.amount;
    }
  });
  return maxDisc;
});
const finalTotal = computed(() => Math.max(0, cartTotalRaw.value - bestCoupon.value));

// 初始化
onMounted(() => {
  const savedUser = localStorage.getItem('feiyi_user');
  if (savedUser) { 
    currentUser.value = JSON.parse(savedUser); 
    fetchCart(); 
  }
  fetchProducts(); 
  fetchHotProducts(); 
  fetchCoupons(); 
  fetchNews(); 
  fetchQuiz(); // 初始化题目
});
onUnmounted(() => pauseCarousel());

// --- 核心业务逻辑 ---

// 1. 云端开窑逻辑 (新功能)
const startFiring = () => {
  if (kilnState.value === 'firing') return;
  kilnState.value = 'firing';
  
  // 模拟烧制过程 3秒
  setTimeout(() => {
    const pool = products.value.length > 0 ? products.value : hotProducts.value;
    const safePool = pool.length > 0 ? pool : [{ name: '神秘珍品', description: '非遗传承之作', mainImage: defaultImg, category: 'kiln' }];
    const randomProduct = safePool[Math.floor(Math.random() * safePool.length)];
    const lucks = ['紫气东来', '窑变天成', '福星高照', '喜上眉梢', '吉祥如意', '欧气爆棚', '鸿运当头'];
    
    firedResult.value = {
      product: randomProduct,
      luck: lucks[Math.floor(Math.random() * lucks.length)]
    };
    
    kilnState.value = 'done';
  }, 3000);
};
const resetKiln = () => { kilnState.value = 'idle'; };

// 2. 问答逻辑 (修复后的正确版本)
const fetchQuiz = async () => {
  quizResult.value = null; 
  selectedOption.value = null;
  try {
    const res = await axios.get(`${API_BASE_URL}/shop/quiz/random`);
    currentQuiz.value = res.data;
  } catch (e) {
    console.error("获取题目失败", e);
  }
};
const answerQuiz = (key) => {
  if (quizResult.value !== null) return;
  selectedOption.value = key;
  quizResult.value = (key === currentQuiz.value.correct) ? 'correct' : 'wrong';
};

// 3. 优惠券逻辑
const isCouponClaimed = (id) => claimedCoupons.value.has(id);
const claimCoupon = (c) => {
  if (!currentUser.value) { openAuthModal('login'); return; }
  if (isCouponClaimed(c.id)) return;
  myCoupons.value.push(c);
  claimedCoupons.value.add(c.id);
  alert('领取成功！结算时自动抵扣');
};

// 4. 下单结算流程
const openCheckoutModal = () => {
  if (!currentUser.value) { openAuthModal('login'); return; }
  isCartOpen.value = false;
  showCheckoutModal.value = true;
};
const createOrder = async () => {
  if(!addressForm.name || !addressForm.phone || !addressForm.address) {
    alert('请填写完整的收货信息');
    return;
  }
  try {
    const res = await axios.post(`${API_BASE_URL}/shop/orders/create`, { 
      userId: currentUser.value.id, 
      discount: bestCoupon.value,
      addressInfo: addressForm 
    });
    
    currentOrder.value = { 
      id: res.data.orderId, 
      totalPrice: res.data.totalPrice 
    };
    showCheckoutModal.value = false;
    showPaymentModal.value = true;
    fetchCart(); 
    myCoupons.value = []; 
  } catch (e) { 
    alert(e.response?.data?.error || '下单失败'); 
  }
};
const confirmPayment = async () => {
  try {
    const res = await axios.post(`${API_BASE_URL}/shop/pay`, { orderId: currentOrder.value.id });
    alert(`支付成功！交易号：${res.data.tradeNo}`);
    showPaymentModal.value = false;
    openOrderListModal(); 
  } catch (e) {
    alert(e.response?.data?.error || '支付失败');
  }
};
const continuePay = (order) => {
  currentOrder.value = { id: order.id, totalPrice: order.totalPrice };
  showOrderListModal.value = false;
  showPaymentModal.value = true;
};

// 5. 订单管理
const openOrderListModal = () => {
  if (!currentUser.value) { openAuthModal('login'); return; }
  fetchMyOrders();
  showOrderListModal.value = true;
};
const fetchMyOrders = async () => {
  try {
    const res = await axios.get(`${API_BASE_URL}/shop/orders`, { params: { userId: currentUser.value.id } });
    myOrders.value = res.data;
  } catch (e) { console.error(e); }
};
const confirmReceive = async (orderId) => {
  if(!confirm('确认已收到货品吗？')) return;
  try {
    await axios.post(`${API_BASE_URL}/shop/orders/receive`, { orderId });
    fetchMyOrders();
  } catch(e) { alert('操作失败'); }
};
const mockShip = async (orderId) => {
  try {
    await axios.post(`${API_BASE_URL}/shop/orders/ship`, { orderId });
    alert('已模拟发货');
    fetchMyOrders();
  } catch(e) {}
};
const getStatusText = (status) => {
  const map = { 'Pending': '待支付', 'Paid': '待发货', 'Shipped': '待收货', 'Completed': '已完成' };
  return map[status] || status;
};

// 6. 商品与搜索
const fetchProducts = async (page = 1) => {
  loading.value = true; currentPage.value = page;
  try {
    const params = { 
      page, per_page: 12, 
      category: currentCategory.value !== 'all' ? currentCategory.value : undefined, 
      scene: sceneFilter.value !== 'all' ? sceneFilter.value : undefined, 
      q: searchQuery.value || undefined 
    };
    const res = await axios.get(`${API_BASE_URL}/shop/products`, { params });
    products.value = res.data.products; totalPages.value = res.data.pages; totalItems.value = res.data.total;
  } catch (e) {} finally { loading.value = false; }
};
const filterScene = (s) => { sceneFilter.value = s; fetchProducts(1); };
const filterCategory = (c) => { currentCategory.value = c; fetchProducts(1); };
const handleSearch = () => fetchProducts(1);
const changePage = (p) => { fetchProducts(p); document.getElementById('product-list').scrollIntoView({behavior:'smooth'}); };
const getCurrentTitle = () => {
  if (searchQuery.value) return `搜索 "${searchQuery.value}" 的结果`;
  if (sceneFilter.value !== 'all') { const map = { tea: '茶室雅集', gift: '礼赠首选', home: '家居装饰' }; return map[sceneFilter.value]; }
  if (currentCategory.value !== 'all') return currentCategory.value === 'kiln' ? '吉州窑瓷' : '鄂州剪纸';
  return '全部珍品';
};

// 7. 用户与头像
const triggerFileUpload = () => { fileInput.value.click(); };
const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (e) => {
    const base64Img = e.target.result;
    currentUser.value.avatar = base64Img;
    localStorage.setItem('feiyi_user', JSON.stringify(currentUser.value));
    updateAvatarInBackend(base64Img);
  };
  reader.readAsDataURL(file);
};
const updateAvatarInBackend = async (imgStr) => { try { await axios.post(`${API_BASE_URL}/auth/avatar`, { userId: currentUser.value.id, avatarUrl: imgStr }); } catch (e) {} };
const getAvatarUrl = (path) => { if (!path || path === 'default_avatar.png') return defaultAvatar; if (path.startsWith('data:image')) return path; return getImageUrl(path); };
const handleAuth = async () => { authError.value = ''; const url = authMode.value === 'login' ? '/auth/login' : '/auth/register'; try { const res = await axios.post(`${API_BASE_URL}${url}`, authForm); const u = res.data.user; currentUser.value = u; localStorage.setItem('feiyi_user', JSON.stringify(u)); showAuthModal.value = false; fetchCart(); if(authMode.value==='register') alert('注册成功'); } catch (e) { authError.value = e.response?.data?.error; } };
const switchAuthMode = () => { authMode.value = authMode.value === 'login' ? 'register' : 'login'; authError.value = ''; };
const handleLogout = () => { currentUser.value = null; localStorage.removeItem('feiyi_user'); cartItems.value = []; showProfileModal.value = false; };

// 8. 其他辅助逻辑
const fetchHotProducts = async () => { 
  try { 
    const res = await axios.get(`${API_BASE_URL}/shop/hot_products`); 
    hotProducts.value = res.data; 
    startCarousel(); 
  } catch (e) {
    console.error("获取热门商品失败:", e);
  } 
};
const fetchCoupons = async () => { try { const res = await axios.get(`${API_BASE_URL}/shop/coupons`); coupons.value = res.data; } catch (e) {} };
const fetchNews = async () => { try { const res = await axios.get(`${API_BASE_URL}/shop/news`); newsList.value = res.data; } catch (e) {} };
const fetchCart = async () => { if(!currentUser.value) return; try{ const res = await axios.get(`${API_BASE_URL}/shop/cart`, {params:{userId:currentUser.value.id}}); cartItems.value = res.data; }catch(e){} };

const openNewsModal = async (id) => { try { const res = await axios.get(`${API_BASE_URL}/shop/news/${id}`); currentNews.value = res.data; showNewsModal.value = true; } catch (e) {} };
const addToCart = async () => { if (!currentUser.value) { showProductModal.value = false; openAuthModal('login'); return; } if (!selectedVariant.value) { alert('请选择款式'); return; } try { await axios.post(`${API_BASE_URL}/shop/cart/add`, {userId:currentUser.value.id, variantId:selectedVariant.value.id, quantity:buyQuantity.value}); alert('已加入购物车'); showProductModal.value = false; fetchCart(); isCartOpen.value = true; } catch (e) { alert(e.response?.data?.error); } };
const toggleCart = () => { if(!currentUser.value) openAuthModal('login'); else isCartOpen.value = !isCartOpen.value; };
const openProductModal = (p) => { selectedProduct.value = p; selectedVariant.value = null; buyQuantity.value = 1; showProductModal.value = true; };
const openAuthModal = (m) => { authMode.value = m; showAuthModal.value = true; authError.value = ''; };
const getImageUrl = (path) => path || defaultImg;
const handleImgError = (e) => e.target.src = defaultImg;
const getMinPrice = (p) => p.variants?.length ? Math.min(...p.variants.map(v=>v.price)) : 0;
const startCarousel = () => { if (carouselTimer.value) clearInterval(carouselTimer.value); carouselTimer.value = setInterval(() => nextSlide(), 2000); };
const pauseCarousel = () => clearInterval(carouselTimer.value);
const nextSlide = () => currentSlide.value = (currentSlide.value + 1) % hotProducts.value.length;
const prevSlide = () => currentSlide.value = (currentSlide.value - 1 + hotProducts.value.length) % hotProducts.value.length;
</script>

<style scoped>
/* ================== 基础样式 ================== */
.shop-container { min-height: 100vh; background: #F9F5F0; font-family: "Songti SC", serif; color: #4A3B32; }
.main-header { background: #FFF; box-shadow: 0 2px 10px rgba(0,0,0,0.05); position: sticky; top: 0; z-index: 100; }
.top-bar { padding: 15px 0; }
.top-bar-inner { width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; }
.brand-text { font-family: "Xingkai SC", cursive; font-size: 28px; color: #8B4513; }
.user-actions { display: flex; align-items: center; gap: 15px; font-size: 14px; }
.cart-btn { cursor: pointer; display: flex; align-items: center; gap: 5px; position: relative; }
.badge { background: #D32F2F; color: white; font-size: 10px; padding: 2px 5px; border-radius: 10px; position: absolute; top: -8px; right: -8px; }
.auth-links span { cursor: pointer; margin-left: 10px; }
.highlight { color: #D32F2F; font-weight: bold; }
.user-profile { display: flex; align-items: center; gap: 8px; cursor: pointer; padding: 5px 10px; border-radius: 20px; transition: background 0.3s; }
.user-profile:hover { background: #F0E6DC; }
.user-avatar-small { width: 30px; height: 30px; border-radius: 50%; object-fit: cover; border: 1px solid #DDD; }

/* 核心左右布局 */
.main-layout { width: 1200px; margin: 30px auto; display: flex; gap: 30px; }

/* 左侧固定侧边栏 */
.sticky-sidebar { width: 240px; flex-shrink: 0; position: sticky; top: 80px; height: fit-content; }
.sidebar-block { background: #FFF; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.03); }
.block-title { font-size: 16px; margin-bottom: 15px; border-left: 4px solid #8B4513; padding-left: 10px; font-weight: bold; }
.search-block { display: flex; gap: 5px; }
.search-block input { width: 100%; border: 1px solid #DDD; padding: 8px; border-radius: 4px; outline: none; }
.search-block button { background: #8B4513; color: white; border: none; padding: 0 10px; border-radius: 4px; cursor: pointer; }
.filter-list { list-style: none; padding: 0; margin: 0; }
.filter-list li { padding: 10px 15px; cursor: pointer; border-radius: 6px; color: #666; transition: 0.2s; display: flex; align-items: center; }
.filter-list li:hover, .filter-list li.active { background: #F4E4D0; color: #8B4513; font-weight: bold; }
.dot { width: 6px; height: 6px; background: #CCC; border-radius: 50%; margin-right: 10px; }
.filter-list li.active .dot { background: #8B4513; }
.mini-card { background: #FDFCF5; border: 1px dashed #DCC6B0; padding: 15px; text-align: center; cursor: pointer; border-radius: 6px; font-weight: bold; color: #8B4513; transition: 0.3s; }
.mini-card:hover { transform: translateY(-2px); box-shadow: 0 4px 10px rgba(0,0,0,0.05); }

/* 右侧内容区 */
.content-area { flex: 1; }

/* 轮播图 */
.carousel-section { width: 100%; height: 380px; overflow: hidden; border-radius: 12px; position: relative; box-shadow: 0 5px 20px rgba(0,0,0,0.1); margin-bottom: 30px; }
.carousel-container { width: 100%; height: 100%; position: relative; }
.carousel-track { display: flex; width: 100%; height: 100%; transition: transform 0.5s ease-in-out; }
.carousel-slide { width: 100%; height: 100%; flex-shrink: 0; position: relative; }
.slide-bg { width: 100%; height: 100%; object-fit: cover; filter: brightness(0.85); }
.slide-content { position: absolute; top: 50%; left: 60px; transform: translateY(-50%); color: #FFF; text-shadow: 0 2px 5px rgba(0,0,0,0.6); max-width: 400px; }
.slide-tag { background: #D32F2F; padding: 5px 10px; font-size: 12px; border-radius: 4px; margin-bottom: 15px; display: inline-block; }
.slide-content h2 { font-size: 36px; margin: 0 0 20px 0; font-family: "Xingkai SC"; }
.slide-content button { padding: 10px 25px; background: #E6CFA2; border: none; font-size: 16px; font-weight: bold; cursor: pointer; color: #5D4037; border-radius: 25px; transition: 0.3s; }
.arrow { position: absolute; top: 50%; transform: translateY(-50%); background: rgba(0,0,0,0.3); color: white; border: none; padding: 15px 10px; cursor: pointer; font-size: 24px; z-index: 10; transition: 0.3s; }
.arrow:hover { background: rgba(0,0,0,0.6); }
.arrow.left { left: 0; } .arrow.right { right: 0; }

/* 优惠券 (调整样式以适应右侧布局) */
.coupon-section { background: #FFF; padding: 25px; border-radius: 8px; margin-bottom: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.03); }
.inner-title { font-size: 20px; margin-bottom: 20px; color: #5D4037; font-weight: bold; border-left: 4px solid #D32F2F; padding-left: 10px; }
.coupon-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; }
.coupon-card { height: 90px; display: flex; background: linear-gradient(135deg, #FF6B6B, #EE5253); color: white; border-radius: 8px; position: relative; cursor: pointer; transition: 0.3s; }
.coupon-card:hover { transform: translateY(-3px); }
.cp-left { width: 40%; display: flex; flex-direction: column; justify-content: center; align-items: center; border-right: 2px dashed rgba(255,255,255,0.5); }
.cp-price { font-size: 28px; font-weight: bold; }
.cp-right { flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; }
.cp-btn { background: #FFF; color: #EE5253; padding: 4px 12px; border-radius: 15px; font-size: 12px; font-weight: bold; }
.coupon-card.claimed { background: #AAA; } .coupon-card.claimed .cp-btn { color: #AAA; }
.circle { width: 20px; height: 20px; background: #FFF; border-radius: 50%; position: absolute; left: 37%; }
.circle.top { top: -10px; } .circle.bottom { bottom: -10px; }

/* 开窑游戏区 */
.kiln-game-section { background: #FFF; padding: 25px; border-radius: 8px; margin-bottom: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.03); }
.kiln-wrapper {
 background: url('@/assets/images/kiln_game_bg.png') no-repeat center; background-size: cover; 
  border-radius: 10px;
  min-height: 400px;
  display: flex; justify-content: center; align-items: center;
  position: relative;
  overflow: hidden;
  box-shadow: inset 0 0 50px rgba(0,0,0,0.5);
}

.kiln-furnace { text-align: center; position: relative; transition: 0.3s; z-index: 2; }
.furnace-door { width: 200px; height: 240px; background: #3E2723; border: 8px solid #8D6E63; border-radius: 100px 100px 0 0; margin: 0 auto 20px; display: flex; align-items: center; justify-content: center; position: relative; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
.furnace-text { font-family: "Xingkai SC"; font-size: 36px; color: #D7CCC8; z-index: 2; text-shadow: 0 0 10px #000; }
.fire-glow { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(circle, rgba(255,87,34,0.9) 0%, rgba(255,87,34,0) 70%); animation: fire 0.8s infinite alternate; z-index: 1; }
@keyframes fire { 0% { opacity: 0.6; transform: scale(0.95); } 100% { opacity: 1; transform: scale(1.05); } }
.is-firing .furnace-door { animation: shake 0.1s infinite; border-color: #FF5722; }
@keyframes shake { 0% { transform: translateX(-1px); } 50% { transform: translateX(1px); } 100% { transform: translateX(-1px); } }
.furnace-controls p { color: #FFF; margin-bottom: 20px; text-shadow: 0 2px 4px #000; font-size: 16px; }
.fire-btn { padding: 15px 50px; background: linear-gradient(to right, #FF5722, #D84315); color: #FFF; border: 2px solid #FFAB91; border-radius: 30px; font-size: 20px; cursor: pointer; font-weight: bold; transition: 0.3s; box-shadow: 0 0 20px rgba(255,87,34,0.6); }
.fire-btn:hover:not(:disabled) { transform: scale(1.05); box-shadow: 0 0 30px rgba(255,87,34,0.8); }
.fire-btn:disabled { background: #555; border-color: #777; cursor: not-allowed; box-shadow: none; }

.kiln-result { text-align: center; animation: popIn 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275); z-index: 5; }
@keyframes popIn { 0% { transform: scale(0.5); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
.result-card { background: rgba(255,255,255,0.95); color: #333; padding: 25px; border-radius: 12px; width: 320px; margin: 0 auto; box-shadow: 0 20px 50px rgba(0,0,0,0.5); border: 2px solid #E6CFA2; }
.result-header { border-bottom: 1px dashed #DDD; padding-bottom: 10px; margin-bottom: 15px; }
.luck-tag { background: #D32F2F; color: #FFF; padding: 5px 15px; border-radius: 20px; font-size: 16px; font-weight: bold; }
.result-img { width: 100%; height: 220px; object-fit: cover; border-radius: 8px; margin-bottom: 15px; border: 1px solid #EEE; }
.result-card h4 { font-size: 18px; margin-bottom: 5px; color: #333; }
.result-desc { font-size: 13px; color: #666; margin-bottom: 10px; height: 36px; overflow: hidden; }
.result-price { font-size: 20px; color: #D32F2F; font-weight: bold; margin-bottom: 20px; }
.result-actions { display: flex; gap: 15px; justify-content: center; }
.view-btn { padding: 10px 25px; background: #8B4513; color: #FFF; border: none; border-radius: 6px; cursor: pointer; transition: 0.2s; }
.view-btn:hover { background: #6D380F; }
.retry-btn { padding: 10px 25px; background: #EEE; color: #666; border: none; border-radius: 6px; cursor: pointer; transition: 0.2s; }
.retry-btn:hover { background: #DDD; }

/* 大师工坊 */
.workshop-section { background: #2C2C2C; padding: 40px; color: #FFF; margin-bottom: 30px; border-radius: 8px; }
.process-flow { display: flex; justify-content: space-between; align-items: center; }
.process-step { text-align: center; }
.icon-circle { width: 60px; height: 60px; border-radius: 50%; border: 2px solid #E6CFA2; display: flex; align-items: center; justify-content: center; font-size: 24px; margin: 0 auto 10px; background: rgba(255,255,255,0.1); transition: 0.5s; }
.process-step:hover .icon-circle { background: #E6CFA2; transform: scale(1.1); }
.arrow-anim { font-size: 20px; color: #555; animation: blink 1.5s infinite; }
@keyframes blink { 0%, 100% { opacity: 0.2; } 50% { opacity: 1; } }

/* 问答区 */
.quiz-section { background: #FFF; padding: 25px; border-radius: 8px; margin-bottom: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.03); }
.quiz-card { background: #F9F5F0; padding: 20px; border-radius: 8px; border: 1px solid #E0D0B8; }
.inner-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border-left: 4px solid #D32F2F; padding-left: 10px; }
.quiz-q { display: flex; align-items: start; gap: 10px; margin-bottom: 20px; }
.q-badge { background: #8B4513; color: #FFF; padding: 2px 8px; border-radius: 4px; font-size: 14px; font-weight: bold; }
.quiz-q p { font-size: 16px; font-weight: bold; margin: 0; color: #4A3B32; }
.quiz-options { display: flex; flex-direction: column; gap: 10px; }
.quiz-options button { padding: 12px; background: #FFF; border: 1px solid #DCC6B0; border-radius: 6px; cursor: pointer; color: #666; transition: 0.2s; text-align: left; padding-left: 20px; }
.quiz-options button:hover:not(.disabled) { border-color: #8B4513; color: #8B4513; background: #FFFBF5; }
.quiz-options button.correct { background: #E8F5E9; border-color: #4CAF50; color: #2E7D32; font-weight: bold; }
.quiz-options button.wrong { background: #FFEBEE; border-color: #F44336; color: #C62828; }
.quiz-options button.disabled { cursor: default; opacity: 0.8; }
.quiz-feedback { margin-top: 15px; padding-top: 15px; border-top: 1px dashed #DCC6B0; animation: fadeIn 0.5s; }
.quiz-feedback .green { color: #2E7D32; font-weight: bold; margin-bottom: 5px; }
.quiz-feedback .red { color: #C62828; font-weight: bold; margin-bottom: 5px; }
.quiz-feedback .explanation { font-size: 13px; color: #666; line-height: 1.5; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(-5px); } to { opacity: 1; transform: translateY(0); } }

/* 商品列表 */
.product-section { background: #FFF; padding: 25px; border-radius: 8px; margin-bottom: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.03); }
.section-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 20px; border-bottom: 1px solid #EEE; padding-bottom: 10px; }
.section-header h2 { font-size: 22px; color: #4A3B32; margin: 0; }
.count { color: #999; font-size: 14px; }
.product-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 30px; }
.product-card { background: #FFF; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.05); transition: 0.3s; border: 1px solid #EEE; }
.product-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
.card-img { height: 180px; position: relative; cursor: pointer; overflow: hidden; }
.card-img img { width: 100%; height: 100%; object-fit: cover; transition: 0.5s; }
.product-card:hover img { transform: scale(1.05); }
.overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.3); color: #FFF; display: flex; align-items: center; justify-content: center; opacity: 0; transition: 0.3s; }
.card-img:hover .overlay { opacity: 1; }
.card-info { padding: 12px; }
.tag { font-size: 10px; display: inline-block; padding: 2px 6px; border-radius: 4px; margin-bottom: 5px; }
.tag.kiln { background: #F4E4D0; color: #8B4513; }
.tag.paper-cut { background: #FFEBEE; color: #D32F2F; }
.card-info h3 { margin: 0 0 8px 0; font-size: 15px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.bottom-row { display: flex; justify-content: space-between; align-items: center; }
.price { color: #D32F2F; font-size: 16px; font-weight: bold; }
.add-btn { width: 28px; height: 28px; border-radius: 50%; border: 1px solid #DDD; background: #FFF; cursor: pointer; color: #8B4513; }
.add-btn:hover { background: #8B4513; color: #FFF; border-color: #8B4513; }
.pagination { display: flex; justify-content: center; gap: 15px; align-items: center; }
.pagination button { padding: 5px 15px; border: 1px solid #DDD; background: #FFF; cursor: pointer; border-radius: 4px; font-size: 13px; }
.pagination button:disabled { opacity: 0.5; cursor: not-allowed; }

/* 资讯区 */
.news-section { background: #FFF; padding: 25px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.03); }
.news-list { display: grid; grid-template-columns: 1fr; gap: 10px; }
.news-item { display: flex; align-items: center; padding: 10px; border-bottom: 1px dashed #EEE; cursor: pointer; transition: 0.2s; }
.news-item:hover { color: #8B4513; }
.news-tag { background: #F0F0F0; font-size: 12px; padding: 2px 6px; border-radius: 4px; margin-right: 10px; color: #666; }
.news-title { flex: 1; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; font-size: 14px; }
.news-date { font-size: 12px; color: #999; }

/* 漂亮的 Auth 卡片 */
.modal-mask { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); z-index: 3000; display: flex; justify-content: center; align-items: center; backdrop-filter: blur(4px); }
.auth-card { display: flex; background: #FFF; width: 600px; height: 400px; border-radius: 15px; overflow: hidden; box-shadow: 0 20px 50px rgba(0,0,0,0.2); }
.auth-sidebar { width: 200px; background: linear-gradient(135deg, #8B4513, #5D4037); color: white; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 20px; }
.auth-sidebar h3 { font-size: 24px; margin-bottom: 10px; font-family: "Xingkai SC"; }
.auth-main { flex: 1; padding: 40px; display: flex; flex-direction: column; justify-content: center; }
.auth-title { font-size: 22px; color: #333; margin-bottom: 25px; }
.input-group { position: relative; margin-bottom: 25px; }
.input-group input { width: 100%; padding: 10px 0; border: none; border-bottom: 1px solid #DDD; outline: none; font-size: 16px; background: transparent; }
.input-group label { position: absolute; top: 10px; left: 0; font-size: 14px; color: #999; transition: 0.3s; pointer-events: none; }
.input-group input:focus + label, .input-group input:valid + label { top: -12px; font-size: 12px; color: #8B4513; }
.input-group input:focus { border-bottom-color: #8B4513; }
.auth-btn { width: 100%; padding: 12px; background: #8B4513; color: white; border: none; border-radius: 25px; font-size: 16px; cursor: pointer; transition: 0.3s; box-shadow: 0 5px 15px rgba(139,69,19,0.3); }
.auth-btn:hover { background: #601208; transform: translateY(-2px); }
.auth-footer { text-align: center; margin-top: 20px; font-size: 14px; color: #666; cursor: pointer; text-decoration: underline; }
.error-msg { color: #D32F2F; font-size: 12px; margin-top: 10px; text-align: center; }

/* 漂亮的 Profile 卡片 */
.profile-card { background: #FFF; width: 350px; border-radius: 15px; overflow: hidden; text-align: center; padding-bottom: 20px; }
.profile-header { background: #F4E4D0; padding: 30px 20px; }
.avatar-wrapper { width: 100px; height: 100px; margin: 0 auto 15px; position: relative; }
.avatar-wrapper img { width: 100%; height: 100%; object-fit: cover; border-radius: 50%; border: 4px solid #FFF; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
.avatar-edit { position: absolute; bottom: 0; right: 0; background: #333; color: #FFF; width: 30px; height: 30px; border-radius: 50%; font-size: 14px; display: flex; align-items: center; justify-content: center; cursor: pointer; border: 2px solid #FFF; }
.user-role { font-size: 12px; background: #8B4513; color: #FFF; padding: 2px 8px; border-radius: 10px; display: inline-block; }
.profile-body { padding: 20px; color: #666; font-size: 14px; }
.logout-btn { padding: 8px 30px; border: 1px solid #DDD; background: transparent; border-radius: 20px; cursor: pointer; color: #666; transition: 0.3s; }
.logout-btn:hover { border-color: #D32F2F; color: #D32F2F; }

/* 其他弹窗通用 */
.news-modal { background: #FDFCF8; width: 700px; padding: 50px; border-radius: 4px; position: relative; max-height: 85vh; overflow-y: auto; box-shadow: 0 10px 40px rgba(0,0,0,0.3); border: 1px solid #E0D0B8; }
.news-modal-title { margin-bottom: 15px; font-size: 28px; color: #5D4037; font-family: "Xingkai SC"; text-align: center; font-weight: normal; }
.news-meta { color: #998A78; font-size: 14px; margin-bottom: 30px; border-bottom: 1px dashed #DCC6B0; padding-bottom: 15px; text-align: center; letter-spacing: 1px; }
.news-content { line-height: 2; color: #4A3B32; font-size: 16px; text-align: justify; text-indent: 2em; white-space: pre-wrap; padding: 0 10px; }
.close-btn { position: absolute; top: 15px; right: 20px; border: none; background: none; font-size: 32px; cursor: pointer; color: #998A78; transition: transform 0.3s; }
.close-btn:hover { transform: rotate(90deg); color: #5D4037; }
.product-modal-box { background: #FFF; width: 700px; padding: 30px; border-radius: 8px; position: relative; display: flex; gap: 30px; }
.pm-left { width: 300px; height: 300px; }
.pm-left img { width: 100%; height: 100%; object-fit: cover; border-radius: 4px; }
.pm-right { flex: 1; text-align: left; }
.variant-area { margin-top: 20px; }
.tags span { display: inline-block; padding: 5px 10px; border: 1px solid #DDD; margin: 0 10px 10px 0; cursor: pointer; border-radius: 4px; }
.tags span.active { border-color: #8B4513; color: #8B4513; background: #FAF3EF; }
.qty-control { display: flex; width: 100px; margin-top: 10px; }
.qty-control button { width: 30px; background: #EEE; border: none; cursor: pointer; }
.qty-control input { flex: 1; text-align: center; border: 1px solid #EEE; outline: none; }
.pm-footer { margin-top: 30px; border-top: 1px solid #EEE; padding-top: 20px; display: flex; justify-content: space-between; align-items: center; }
.total { color: #D32F2F; font-size: 20px; font-weight: bold; }
.confirm-btn { background: #8B4513; color: #FFF; border: none; padding: 10px 30px; border-radius: 4px; cursor: pointer; }
.cart-drawer { position: fixed; top: 0; right: -350px; width: 320px; height: 100vh; background: #FFF; z-index: 2000; box-shadow: -5px 0 15px rgba(0,0,0,0.1); transition: right 0.3s; display: flex; flex-direction: column; }
.cart-drawer.open { right: 0; }
.drawer-header { padding: 15px; background: #F5F5F5; display: flex; justify-content: space-between; }
.drawer-body { flex: 1; padding: 15px; overflow-y: auto; }
.cart-item { display: flex; gap: 10px; margin-bottom: 15px; border-bottom: 1px dashed #EEE; padding-bottom: 10px; }
.cart-item .thumb { width: 50px; height: 50px; object-fit: cover; }
.drawer-footer { padding: 15px; border-top: 1px solid #EEE; background: #FDFCF5; }
.discount-info { font-size: 12px; color: #666; margin-bottom: 10px; display: flex; justify-content: space-between; }
.total-bar { margin-bottom: 10px; font-weight: bold; text-align: right; }
.red { color: #D32F2F; }
.checkout-btn { width: 100%; padding: 10px; background: #D32F2F; color: #FFF; border: none; cursor: pointer; border-radius: 5px; }
.loading-state, .empty-state { text-align: center; padding: 50px; color: #999; }

/* 结算弹窗 & 支付弹窗 & 订单列表弹窗 */
.checkout-box, .payment-box, .order-list-box { background: #FFF; width: 600px; padding: 30px; border-radius: 8px; position: relative; max-height: 80vh; overflow-y: auto; }
.checkout-header, .ol-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #EEE; padding-bottom: 15px; margin-bottom: 20px; font-size: 18px; font-weight: bold; }
.close-icon { cursor: pointer; font-size: 20px; color: #999; }
.form-section h4, .order-summary h4 { margin-bottom: 15px; font-size: 15px; border-left: 3px solid #8B4513; padding-left: 10px; }
.form-row { display: flex; gap: 15px; margin-bottom: 15px; }
.form-row input { flex: 1; padding: 10px; border: 1px solid #DDD; border-radius: 4px; outline: none; }
.full-width { width: 100%; }
.summary-item { display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 14px; color: #666; }
.summary-total { border-top: 1px dashed #EEE; padding-top: 15px; text-align: right; }
.summary-total .final { font-size: 18px; color: #D32F2F; font-weight: bold; margin-top: 5px; }
.checkout-footer { display: flex; justify-content: flex-end; gap: 15px; margin-top: 20px; }
.cancel-btn { padding: 8px 20px; background: #EEE; border: none; border-radius: 4px; cursor: pointer; }
.pay-btn { padding: 8px 25px; background: #D32F2F; color: #FFF; border: none; border-radius: 4px; cursor: pointer; }

/* 支付弹窗 */
.payment-box { text-align: center; width: 400px; }
.pay-amount { font-size: 36px; font-weight: bold; color: #333; margin: 20px 0; }
.qr-container { background: #F5F5F5; padding: 20px; display: inline-block; border-radius: 8px; margin-bottom: 20px; }
.qr-code { width: 150px; height: 150px; background: #FFF; margin: 0 auto; display: flex; flex-direction: column; align-items: center; justify-content: center; }
.qr-inner { width: 120px; height: 120px; background: #333; margin-bottom: 5px; }
.pay-tip { color: #999; font-size: 12px; margin-bottom: 20px; }
.mock-pay-btn { padding: 10px 30px; background: #4CAF50; color: #FFF; border: none; border-radius: 20px; cursor: pointer; font-size: 14px; }

/* 订单列表 */
.order-list-box { width: 700px; }
.order-card { border: 1px solid #EEE; border-radius: 8px; margin-bottom: 20px; overflow: hidden; }
.oc-top { background: #F9F9F9; padding: 10px 15px; display: flex; justify-content: space-between; font-size: 12px; color: #666; }
.oc-status { font-weight: bold; }
.oc-status.Pending { color: #E6A23C; } .oc-status.Paid { color: #409EFF; } .oc-status.Shipped { color: #67C23A; }
.oc-products { padding: 15px; border-bottom: 1px solid #EEE; }
.oc-item { font-size: 14px; margin-bottom: 5px; }
.oc-bottom { padding: 10px 15px; display: flex; justify-content: space-between; align-items: center; }
.oc-total { font-weight: bold; }
.action-btn { padding: 5px 15px; border: 1px solid #DDD; background: #FFF; border-radius: 4px; cursor: pointer; font-size: 12px; }
.action-btn.primary { background: #8B4513; color: #FFF; border-color: #8B4513; }
.action-btn.disabled { opacity: 0.6; cursor: default; }
.cheat-btn { font-size: 10px; color: #999; text-decoration: underline; background: none; border: none; cursor: pointer; margin-left: 10px; }
</style>