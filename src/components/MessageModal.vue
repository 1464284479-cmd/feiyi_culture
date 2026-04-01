<!-- src/components/MessageModal.vue -->
<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-card">
      <!-- 顶部浮起来的图片 -->
      <div class="modal-img-wrapper">
        <img src="@/assets/images/popup_character.png" alt="Success" />
      </div>
      
      <h2 class="modal-title">叮咚！您的留言敲响了“非遗回音钟”</h2>
      
      <p class="modal-text">
        您的心意像吉州窑的金叶纹，悄悄落在我们的“瓷盏”里啦✨<br>
        匠人会带着非遗的温度，<br>
        认真回应您的故事～
      </p>

      <div class="modal-buttons">
        <!-- 点击按钮时，向父组件发送信号 -->
        <button class="btn-cancel" @click="$emit('close')">知道了</button>
        <button class="btn-confirm" @click="$emit('confirm')">逛逛非遗小馆</button>
      </div>
    </div>
  </div>
</template>

<script setup>
// 定义这个组件会向外发送哪些事件
// 'close': 用户点了关闭/知道了
// 'confirm': 用户点了逛逛非遗小馆
defineEmits(['close', 'confirm']);
</script>

<style scoped>
/* 
  这里只放弹窗相关的样式 
  (代码直接从之前写好的那里剪切过来)
*/
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 9999;
  display: flex;
  justify-content: center;
  align-items: center;
  backdrop-filter: blur(3px);
}

.modal-card {
  background: linear-gradient(180deg, #FDF7EC 0%, #E6CCAA 100%);
  width: 480px;
  max-width: 90%;
  border-radius: 30px;
  padding: 40px 30px 30px 30px;
  text-align: center;
  position: relative;
  box-shadow: 
    10px 10px 0 rgba(255, 255, 255, 0.5),
    0 10px 30px rgba(0, 0, 0, 0.2);
  animation: popIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.modal-img-wrapper {
  margin-top: -100px;
  margin-bottom: 20px;
}
.modal-img-wrapper img {
  width: 230px;
  height: auto;
  filter: drop-shadow(0 10px 10px rgba(0,0,0,0.15));
}

.modal-title {
  font-size: 20px;
  color: #000;
  font-weight: bold;
  margin-bottom: 20px;
}

.modal-text {
  font-size: 14px;
  color: #6d5c4d;
  line-height: 1.8;
  margin-bottom: 30px;
  padding: 0 20px;
}

.modal-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.btn-cancel {
  background: rgba(255, 255, 255, 0.4);
  border: 1px solid #fff;
  padding: 10px 30px;
  border-radius: 50px;
  font-size: 16px;
  color: #fff;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.2s;
}
.btn-cancel:hover {
  background: rgba(255, 255, 255, 0.6);
}

.btn-confirm {
  background: linear-gradient(90deg, #F0D396 0%, #E2B264 100%);
  border: none;
  padding: 10px 30px;
  border-radius: 50px;
  font-size: 16px;
  color: #fff;
  cursor: pointer;
  font-weight: bold;
  box-shadow: 0 4px 10px rgba(226, 178, 100, 0.4);
  transition: all 0.2s;
}
.btn-confirm:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(226, 178, 100, 0.5);
}

@keyframes popIn {
  0% { transform: scale(0.5) translateY(50px); opacity: 0; }
  100% { transform: scale(1) translateY(0); opacity: 1; }
}

@media (max-width: 768px) {
  .modal-card { width: 85%; padding-top: 50px; }
  .modal-img-wrapper { margin-top: -80px; }
  .modal-img-wrapper img { width: 140px; }
  .modal-buttons { flex-direction: column; gap: 10px; }
}
</style>