// src/services/messageService.js
import axios from 'axios';

// 配置axios实例，指定后端的基地址
const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:5000/api', // 你的后端API地址
  headers: {
    'Content-Type': 'application/json'
  }
});

export default {
  // 导出一个方法，用于提交留言
  submitMessage(messageData) {
    return apiClient.post('/messages/submit', messageData);
  }
};