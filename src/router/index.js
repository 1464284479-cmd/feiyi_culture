import { createRouter, createWebHistory } from 'vue-router'

// 1. 引入所有页面组件
import HomeView from '../views/HomeView.vue'
import ContactView from '../views/ContactView.vue'
import ArtisansView from '../views/ArtisansView.vue'
import WindowGalleryView from '../views/WindowGalleryView.vue'
import PatternsView from '../views/PatternsView.vue'
import MaterialsView from '../views/MaterialsView.vue'
import DoubleHeritageView from '../views/DoubleHeritageView.vue'

// 🔥 新增：引入商城相关的两个新页面
import ShopHomeView from '../views/ShopHomeView.vue' // 商城入口页 (图一)
import ShopMainView from '../views/ShopMainView.vue' // 商城主页 (图二的占位符)
    // 引入组件
import MaterialsDetailView from '../views/MaterialsDetailView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView 
    },
    {
      path: '/contact',
      name: 'contact',
      component: ContactView
    },
    {
      path: '/artisans',
      name: 'artisans',
      component: ArtisansView
    },
    {
      path: '/window-gallery',
      name: 'window-gallery',
      component: WindowGalleryView
    },
    {
      path: '/patterns',
      name: 'patterns',
      component: PatternsView
    },
    {
      // ✅ 修正：此路径现在明确指向素材库
      path: '/materials',
      name: 'materials',
      component: MaterialsView
    },
    {
      // ✅ 修正：/shop 路径现在指向新的商城入口页 (图一)
      path: '/shop',
      name: 'shop',
      component: ShopHomeView 
    },
    {
      // 🔥 新增：为商城主页 (图二) 创建一个新路径
      path: '/shop-main',
      name: 'shop-main',
      component: ShopMainView // 以后您开发图二页面时，替换这里即可
    },
    {
      path: '/double-heritage',
      name: 'double-heritage',
      component: DoubleHeritageView
    },

// 在 routes 数组中添加：
{
  // 动态路由，:id 会匹配 fengwen, flower 等
  path: '/materials/:id',
  name: 'materials-detail',
  component: MaterialsDetailView
}
  ]
})

export default router