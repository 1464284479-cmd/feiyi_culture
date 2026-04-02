<template>
  <div class="contact-page-content">
    <!-- 1. 页面标题栏 -->
    <section class="page-title-bar">
      <h1>联系我们</h1>
      <p>我们期待听到您的意见和建议</p>
    </section>

    <!-- 2. 主体内容区域 -->
    <div class="main-content-wrapper">
      <div class="container content-box">
        
        <div class="bell-wrapper">
          <img src="@/assets/images/bell.png" class="bell-decoration" alt="bell" />
        </div>

        <div class="content-flex">
          <div class="left-info">
            <div class="brand-logo">
              <img src="@/assets/images/logo_main.png" alt="楚韵镂窗" class="info-logo"/>
            </div>
            <div class="info-block">
               <h3>联系我们</h3>
               <div class="divider"></div>
               <p><strong>地址：</strong> 湖北省武汉市江夏区</p>
               <p><strong>电话：</strong> 027-88888888</p>
               <p><strong>邮箱：</strong> contact@feiyi.com</p>
               <p><strong>开放时间：</strong> 周一至周五 9:00 - 18:00</p>
            </div>
            <div class="social-block">
               <h3>关注我们</h3>
               <div class="divider"></div>
               <!-- 🔥🔥🔥 关键修改：添加了 href 跳转链接，并加上 target="_blank" 在新标签页打开 🔥🔥🔥 -->
               <a href="https://xhslink.com/m/NXp44aaVlS" target="_blank" class="social-icon">
                 <img src="@/assets/images/xiaohongshu.png" alt="小红书" />
               </a>
            </div>
          </div>

          <div class="right-form">
            <div class="form-header">
              <h3>留言咨询</h3>
              <div class="divider"></div>
            </div>
            
            <form @submit.prevent="submitForm">
              <div class="form-group">
                <label>姓名</label>
                <input type="text" v-model="form.name" />
              </div>
              <div class="form-group">
                <label>邮箱</label>
                <input type="email" v-model="form.email" />
              </div>
              <div class="form-group">
                <label>电话</label>
                <input type="tel" v-model="form.phone" />
              </div>
              <div class="form-group">
                <label>主题</label>
                <input type="text" v-model="form.subject" />
              </div>
              <div class="form-group">
                <label>留言内容</label>
                <textarea v-model="form.message" rows="5"></textarea>
              </div>
              <button type="submit" class="submit-btn">提交留言</button>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- 弹窗组件 -->
    <MessageModal 
      v-if="showModal" 
      @close="closeModal" 
      @confirm="goToShop" 
    />

  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
// 引入弹窗组件
import MessageModal from '@/components/MessageModal.vue';

const router = useRouter();
const showModal = ref(false); 

const form = reactive({
  name: '',
  email: '',
  phone: '',
  subject: '',
  message: ''
});

const submitForm = async () => {
  if (!form.name || !form.message) {
    alert("请至少填写姓名和留言内容");
    return;
  }

  try {
    const response = await fetch('http://127.0.0.1:5000/api/messages/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    });

    // 🔥 关键优化：先判断响应是否成功
    if (!response.ok) {
      // 尝试解析错误信息（如果后端返回 JSON）
      let errorMsg = "服务器错误";
      try {
        const errData = await response.json();
        errorMsg = errData.message;
      } catch (e) {
        // 如果解析失败，直接使用状态码描述
        errorMsg = `${response.status} ${response.statusText}`;
      }
      throw new Error(errorMsg);
    }

    const result = await response.json();
    showModal.value = true;
    Object.keys(form).forEach(key => form[key] = '');
  } catch (error) {
    console.error('Error:', error);
    alert(`❌ ${error.message}`);
  }
};

// 处理组件传回来的事件
const closeModal = () => {
  showModal.value = false;
};

const goToShop = () => {
  showModal.value = false;
  router.push('/shop'); // 跳转商城
};
</script>

<style scoped>
.container { width: 1200px; max-width: 95%; margin: 0 auto; }
.page-title-bar { background-color: #f5f5f5; text-align: center; padding: 40px 0; border-bottom: 1px solid #e0e0e0; }
.page-title-bar h1 { color: #8B1A1A; font-size: 32px; margin: 0 0 10px 0; }
.page-title-bar p { color: #666; font-size: 14px; }
.main-content-wrapper { background: linear-gradient(to bottom, #f5f5f5, #fff); padding-bottom: 60px; position: relative; flex: 1; }
.content-box { background-color: #fff; border-radius: 20px 20px 0 0; box-shadow: 0 -5px 20px rgba(0,0,0,0.05); margin-top: -20px; padding: 50px; position: relative; min-height: 600px; }

/* 铃铛样式 */
.bell-wrapper { position: absolute; top: 0; right: 50px; z-index: 10; transform-origin: top center; animation: swing 3s ease-in-out infinite alternate; }
.bell-decoration { width: 180px; display: block; }
@keyframes swing { 0% { transform: rotate(10deg); } 100% { transform: rotate(-10deg); } }

/* 布局与表单样式 */
.content-flex { display: flex; justify-content: space-between; }
.left-info { width: 35%; padding-right: 40px; }
.brand-logo { text-align: center; margin-bottom: 40px; }
.info-logo { width: 120px; margin-bottom: 10px; }
.brand-name { color: #C19D68; font-size: 24px; letter-spacing: 2px; }
.info-block, .social-block { margin-bottom: 40px; }
.info-block h3, .social-block h3, .form-header h3 { color: #8B1A1A; font-size: 20px; margin-bottom: 5px; font-weight: bold; }
.divider { width: 40px; height: 4px; background-color: #C19D68; margin-bottom: 20px; }
.info-block p { line-height: 2.5; font-size: 15px; color: #333; }
.social-icon img { width: 40px; height: 40px; cursor: pointer; transition: transform 0.2s; }
.social-icon img:hover { transform: scale(1.1); }
.right-form { width: 50%; padding-top: 20px; }
.form-group { margin-bottom: 20px; }
.form-group label { display: block; font-weight: bold; margin-bottom: 8px; color: #333; }
.form-group input, .form-group textarea { width: 100%; padding: 10px 15px; border: 1px solid #ccc; border-radius: 20px; font-size: 14px; outline: none; background-color: #fff; font-family: inherit; }
.form-group input:focus, .form-group textarea:focus { border-color: #8B1A1A; box-shadow: 0 0 5px rgba(139, 26, 26, 0.1); }
.submit-btn { width: 100%; padding: 12px; background: linear-gradient(to right, #E0C38C, #D4AF37); border: none; border-radius: 5px; color: #fff; font-size: 16px; cursor: pointer; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: opacity 0.3s; }
.submit-btn:hover { opacity: 0.9; }

@media (max-width: 768px) {
  .content-flex { flex-direction: column; }
  .left-info, .right-form { width: 100%; }
  .bell-wrapper { display: none; }
}
</style>