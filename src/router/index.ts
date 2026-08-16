import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import Dashboard from '../views/HomeView.vue'
import Landing from '../views/Landing.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: Landing,
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: Dashboard,
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router