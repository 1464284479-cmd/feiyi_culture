<!-- src/components/PatternDetailModal.vue -->
<template>
  <Transition name="modal">
    <div v-if="visible" class="modal-mask" @click="$emit('close')">
      <div class="modal-container" @click.stop>
        <div class="modal-header">
          <h3>{{ title }}</h3>
          <button class="close-btn" @click="$emit('close')">×</button>
        </div>
        
        <div class="modal-body">
          <div class="modal-img">
            <img :src="image" :alt="title" />
          </div>
          <div class="modal-text">
            <p v-for="(paragraph, index) in content" :key="index">{{ paragraph }}</p>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
defineProps({
  visible: Boolean,
  title: String,
  content: Array, // 接收段落数组
  image: String
});

defineEmits(['close']);
</script>

<style scoped>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  transition: opacity 0.3s ease;
}

.modal-container {
  width: 800px;
  max-width: 90%;
  max-height: 85vh;
  background-color: #FDF5E6; /* 米黄背景 */
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  padding: 30px;
  overflow-y: auto;
  border: 4px solid #8B4513; /* 棕色边框 */
  position: relative;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  border-bottom: 2px solid #D4AF37;
  padding-bottom: 10px;
}

.modal-header h3 {
  margin: 0;
  color: #8B4513;
  font-size: 24px;
  font-weight: bold;
}

.close-btn {
  background: none;
  border: none;
  font-size: 30px;
  color: #8B4513;
  cursor: pointer;
}

.modal-body {
  display: flex;
  gap: 30px;
}

.modal-img {
  width: 40%;
}
.modal-img img {
  width: 100%;
  border-radius: 5px;
  border: 2px solid #D4AF37;
}

.modal-text {
  flex: 1;
  font-size: 16px;
  line-height: 1.8;
  color: #333;
  text-align: justify;
}
.modal-text p { margin-bottom: 15px; }

/* 动画 */
.modal-enter-from { opacity: 0; }
.modal-leave-to { opacity: 0; }
.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  transform: scale(0.9);
}
</style>