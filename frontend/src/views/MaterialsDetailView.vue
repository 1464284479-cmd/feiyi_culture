<template>
  <div class="material-detail-page">
    
    <!-- 1. 顶部返回栏 -->
    <div class="detail-header">
      <button class="back-btn" @click="$router.go(-1)">← 返回纹样馆</button>
      <h2>{{ categoryName }}系列纹样</h2>
    </div>

    <!-- 2. 纹样网格展示 (分页) -->
    <div class="detail-container" id="gallery-top">
      <div 
        v-for="(img, index) in paginatedImages" 
        :key="index" 
        class="pattern-card"
        @click="openCustomizeModal(img)"
      >
        <div class="img-box">
          <img :src="img.src" :alt="img.name" @error="handleImgError">
        </div>
        <div class="pattern-info">
          <p class="p-name">{{ img.name }}</p>
          <button class="btn-customize">立即定制</button>
        </div>
      </div>
    </div>

    <!-- 3. 底部智能分页 -->
    <div class="pagination-smart" v-if="totalPages > 1">
      <button class="page-btn prev" :disabled="currentPage === 1" @click="changePage(currentPage - 1)">&lt;</button>
      <div class="page-numbers">
        <span v-for="(page, index) in paginationList" :key="index" class="page-num" :class="{ 'active': page === currentPage, 'dots': page === '...' }" @click="page !== '...' ? changePage(page) : null">{{ page }}</span>
      </div>
      <button class="page-btn next" :disabled="currentPage === totalPages" @click="changePage(currentPage + 1)">&gt;</button>
    </div>

    <!-- 4. 专属定制弹窗 (全面升级) -->
    <Transition name="fade">
      <div v-if="showModal" class="modal-mask" @click.self="showModal = false">
        <div class="customize-modal">
          <button class="close-btn" @click="showModal = false">×</button>
          
          <div class="modal-left">
            <div class="preview-box">
              <img :src="selectedPattern.src" class="preview-img">
            </div>
            <p class="selected-text">已选纹样：<span>{{ selectedPattern.name }}</span></p>
            <div class="pattern-id">编号：{{ selectedPattern.id || 'Custom-' + Date.now().toString().slice(-4) }}</div>
          </div>

          <div class="modal-right">
            <h3>专属定制需求</h3>
            <p class="tip">大师手工复刻，请选择您的定制偏好，我们将为您打造独一无二的非遗器物。</p>
            
            <div class="scroll-form">
              <!-- 1. 选择器具类型 (分类展示) -->
              <div class="form-group">
                <label>1. 选择器型：<span class="required">*</span></label>
                <div class="category-group" v-for="(items, category) in artifactTypes" :key="category">
                  <span class="cat-label">{{ category }}：</span>
                  <div class="tags">
                    <span 
                      v-for="model in items" 
                      :key="model" 
                      :class="{ active: form.model === model }"
                      @click="form.model = model"
                    >
                      {{ model }}
                    </span>
                  </div>
                </div>
              </div>

              <!-- 2. 选择定制位置 (新增) -->
              <div class="form-group">
                <label>2. 纹样位置：<span class="required">*</span></label>
                <div class="tags simple-tags">
                  <span 
                    v-for="pos in positions" 
                    :key="pos"
                    :class="{ active: form.position === pos }"
                    @click="form.position = pos"
                  >
                    {{ pos }}
                  </span>
                </div>
              </div>

              <!-- 3. 备注 -->
              <div class="form-group">
                <label>3. 特殊备注：</label>
                <textarea v-model="form.note" placeholder="例如：希望加金边、刻字“赠吾友”、底部落款等..."></textarea>
              </div>

              <!-- 4. 联系方式 -->
              <div class="form-group">
                <label>4. 联系方式：<span class="required">*</span></label>
                <div class="row">
                   <input type="text" v-model="form.userName" placeholder="您的称呼" class="short-input">
                   <input type="text" v-model="form.contact" placeholder="手机号或微信号 (必填)" class="long-input">
                </div>
              </div>
            </div>

            <button class="submit-btn" @click="submitCustomOrder" :disabled="isSubmitting">
              {{ isSubmitting ? '提交中...' : '提交定制申请' }}
            </button>
          </div>
        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const categoryId = route.params.id; 
const categoryName = ref('');
const allImages = ref([]); 
const isSubmitting = ref(false);

// --- 分页逻辑 ---
const currentPage = ref(1);
const pageSize = 12;

const paginatedImages = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  const end = start + pageSize;
  return allImages.value.slice(start, end);
});

const totalPages = computed(() => Math.ceil(allImages.value.length / pageSize));

const paginationList = computed(() => {
  const current = currentPage.value;
  const total = totalPages.value;
  const delta = 2;
  const range = [];
  const rangeWithDots = [];
  let l;
  range.push(1);
  for (let i = current - delta; i <= current + delta; i++) { if (i < total && i > 1) range.push(i); }
  if (total > 1) range.push(total);
  for (let i of range) {
    if (l) { if (i - l === 2) rangeWithDots.push(l + 1); else if (i - l !== 1) rangeWithDots.push('...'); }
    rangeWithDots.push(i); l = i;
  }
  return rangeWithDots;
});

const changePage = (page) => {
  if (page < 1 || page > totalPages.value) return;
  currentPage.value = page;
  const topElement = document.getElementById('gallery-top');
  if (topElement) topElement.scrollIntoView({ behavior: 'smooth' });
};

// --- 定制数据 ---
// 🔥 扩展后的器型库
const artifactTypes = {
  '茶器': ['主人杯', '盖碗', '品茗杯', '茶壶', '公道杯', '建盏'],
  '文房': ['笔筒', '镇纸', '印泥盒', '笔洗'],
  '陈设': ['梅瓶', '玉壶春瓶', '瓷板画', '挂盘', '香炉'],
  '日用': ['餐盘', '马克杯', '花插', '小夜灯']
};
// 🔥 新增位置选择
const positions = ['器物正面中心', '器物背面', '杯底/碗心 (内侧)', '器物底部 (外侧)', '口沿环绕'];

const showModal = ref(false);
const selectedPattern = ref({});
const form = reactive({ 
  model: '', 
  position: '', 
  note: '', 
  contact: '',
  userName: ''
});

// 配置映射
const categoryMap = {
  'fengwen': { name: '锦簇团纹', count: 350, prefix: '铭匠设计' }, 
  'flower': { name: '雅卉清纹', count: 350, prefix: '铭匠设计' },
  'fish': { name: '鱼嬉吉纹', count: 350, prefix: '铭匠设计' },
  'xi': { name: '喜吉福纹', count: 350, prefix: '铭匠设计' },
  'huadian': { name: '戏韵纹绘', count: 350, prefix: '铭匠设计' },
  'blessing': { name: '俗韵人物纹', count: 350, prefix: '铭匠设计' },
  'lantern': { name: '吉灯祥纹', count: 350, prefix: '铭匠设计' },
  'zodiac': { name: '瑞兽萌纹', count: 350, prefix: '铭匠设计' } 
};

onMounted(() => {
  const info = categoryMap[categoryId];
  if (info) {
    categoryName.value = info.name;
    for (let i = 1; i <= info.count; i++) {
      let fileName = info.prefix ? `${info.prefix} (${i}).png` : `${i}.png`;
      allImages.value.push({
        src: `/images/materials/${categoryId}/${fileName}`,
        name: `${info.name} - 样式 ${i}`
      });
    }
  }
});

const handleImgError = (e) => {
  const card = e.target.closest('.pattern-card');
  if (card) card.style.display = 'none';
};

const openCustomizeModal = (img) => {
  selectedPattern.value = img;
  // 重置表单
  form.model = ''; 
  form.position = '';
  form.note = ''; 
  form.contact = '';
  form.userName = '';
  showModal.value = true;
};

// 🔥 真实提交到后端
const submitCustomOrder = async () => {
  if (!form.model) { alert("请选择器型"); return; }
  if (!form.position) { alert("请选择定制位置"); return; }
  if (!form.contact) { alert("请填写联系方式"); return; }
  
  isSubmitting.value = true;

  try {
    // 调用我们在 routes.py 中新写的 /api/custom/create 接口
    const res = await axios.post('http://127.0.0.1:5000/api/custom/create', {
      userName: form.userName,
      contact: form.contact,
      pattern: selectedPattern.value.name,
      patternImg: selectedPattern.value.src,
      artifact: form.model,
      position: form.position,
      note: form.note
    });

    if (res.status === 201) {
      alert(`提交成功！需求编号：${res.data.id}。\n客服将尽快通过 ${form.contact} 联系您确认方案。`);
      showModal.value = false;
    }
  } catch (e) {
    console.error(e);
    alert(e.response?.data?.error || "提交失败，请检查网络或后端连接");
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style scoped>
/* 基础样式 */
.material-detail-page { min-height: 100vh; background-color: #F9F5F0; font-family: "Songti SC", serif; padding-bottom: 50px; }
.detail-header { background: #FFF; padding: 20px 50px; display: flex; align-items: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05); position: sticky; top: 0; z-index: 10; }
.back-btn { border: 1px solid #8B4513; background: none; color: #8B4513; padding: 5px 15px; border-radius: 20px; cursor: pointer; margin-right: 30px; transition: all 0.3s; }
.back-btn:hover { background: #8B4513; color: #FFF; }
.detail-header h2 { color: #5D4037; font-size: 24px; margin: 0; }
.detail-container { width: 1200px; margin: 40px auto; display: grid; grid-template-columns: repeat(4, 1fr); gap: 30px; min-height: 600px; }
.pattern-card { background: #FFF; border-radius: 8px; overflow: hidden; box-shadow: 0 5px 15px rgba(0,0,0,0.05); cursor: pointer; transition: transform 0.3s; border: 1px solid #EEE; }
.pattern-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); border-color: #D4AF37; }
.img-box { height: 200px; padding: 20px; display: flex; justify-content: center; align-items: center; background: #FAFAFA; }
.img-box img { max-width: 100%; max-height: 100%; object-fit: contain; transition: transform 0.3s; }
.pattern-card:hover img { transform: scale(1.1); }
.pattern-info { padding: 15px; text-align: center; border-top: 1px dashed #EEE; }
.p-name { font-size: 16px; color: #333; margin-bottom: 10px; }
.btn-customize { background: #8B4513; color: #FFF; border: none; padding: 6px 20px; border-radius: 4px; cursor: pointer; font-size: 14px; transition: 0.2s; }
.btn-customize:hover { background: #5D4037; }

/* 分页 */
.pagination-smart { display: flex; justify-content: center; align-items: center; gap: 15px; margin-top: 40px; }
.page-numbers { display: flex; gap: 8px; }
.page-num { width: 36px; height: 36px; display: flex; justify-content: center; align-items: center; border-radius: 6px; border: 1px solid #DDD; color: #333; cursor: pointer; transition: all 0.2s; font-size: 15px; background-color: #FFF; font-weight: bold; }
.page-num:hover:not(.dots) { border-color: #8B4513; color: #8B4513; }
.page-num.active { border: 2px solid #8B4513; color: #8B4513; background-color: #FFF; }
.page-num.dots { border: none; cursor: default; color: #999; background: transparent; font-weight: normal; }
.page-btn { width: 36px; height: 36px; border: 1px solid #DDD; background: #FFF; border-radius: 6px; cursor: pointer; color: #999; display: flex; justify-content: center; align-items: center; transition: all 0.2s; font-size: 16px; }
.page-btn:hover:not(:disabled) { border-color: #8B4513; color: #8B4513; }
.page-btn:disabled { opacity: 0.5; cursor: not-allowed; background: #FAFAFA; }

/* 弹窗样式 */
.modal-mask { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); z-index: 1000; display: flex; justify-content: center; align-items: center; backdrop-filter: blur(2px); }
.customize-modal { background: #FFF; width: 900px; height: 650px; border-radius: 12px; display: flex; overflow: hidden; box-shadow: 0 20px 50px rgba(0,0,0,0.3); }
.close-btn { position: absolute; top: 20px; right: 20px; font-size: 32px; background: none; border: none; cursor: pointer; color: #999; z-index: 10; }

.modal-left { width: 350px; background: #F5F1EB; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 40px; border-right: 1px solid #E0E0E0; }
.preview-box { width: 100%; height: 300px; background: #FFF; border: 8px solid #FFF; box-shadow: 0 10px 20px rgba(0,0,0,0.1); display: flex; align-items: center; justify-content: center; margin-bottom: 30px; }
.preview-img { max-width: 90%; max-height: 90%; object-fit: contain; }
.selected-text { font-size: 18px; color: #5D4037; font-weight: bold; margin-bottom: 10px; }
.pattern-id { font-size: 12px; color: #999; font-family: monospace; }

.modal-right { flex: 1; padding: 40px; overflow-y: auto; }
.modal-right h3 { margin: 0 0 10px 0; color: #8B4513; font-size: 24px; font-weight: bold; font-family: "Xingkai SC"; }
.tip { font-size: 13px; color: #888; margin-bottom: 25px; border-bottom: 1px solid #EEE; padding-bottom: 15px; }

.form-group { margin-bottom: 25px; }
.form-group label { display: block; font-weight: bold; margin-bottom: 12px; font-size: 15px; color: #333; }
.required { color: #D32F2F; margin-left: 5px; }

.category-group { margin-bottom: 15px; display: flex; align-items: flex-start; }
.cat-label { font-size: 13px; color: #888; width: 50px; margin-top: 6px; }
.tags { display: flex; flex-wrap: wrap; gap: 8px; flex: 1; }
.tags span { padding: 6px 15px; border: 1px solid #DDD; border-radius: 4px; cursor: pointer; font-size: 13px; transition: all 0.2s; background: #FFF; }
.tags span:hover { border-color: #8B4513; color: #8B4513; }
.tags span.active { background: #8B4513; color: #FFF; border-color: #8B4513; }

.simple-tags span { margin-bottom: 5px; }

.row { display: flex; gap: 15px; }
textarea, input { width: 100%; padding: 12px; border: 1px solid #DDD; border-radius: 6px; outline: none; font-family: inherit; font-size: 14px; transition: border 0.3s; }
textarea:focus, input:focus { border-color: #8B4513; background: #FFFCF9; }
.short-input { width: 30%; }
.long-input { width: 70%; }

.submit-btn { width: 100%; padding: 15px; background: linear-gradient(to right, #C19D68, #8B4513); color: #FFF; border: none; border-radius: 6px; font-size: 18px; cursor: pointer; margin-top: 10px; font-weight: bold; letter-spacing: 2px; transition: opacity 0.3s; }
.submit-btn:disabled { opacity: 0.6; cursor: not-allowed; }
.submit-btn:hover:not(:disabled) { opacity: 0.9; box-shadow: 0 5px 15px rgba(139, 69, 19, 0.3); }

/* 弹窗过渡动画 */
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>