import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import Landing from '../views/Landing.vue'
import HomeView from '../views/HomeView.vue'
import ReportsView from '../views/ReportsView.vue'
import SpecificReportView from '../views/SpecificReportView.vue'
import AboutView from '../views/AboutView.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'landing',
    component: Landing,
    meta: { hideNavbar: true }
  },
  {
    path: '/home',
    name: 'home',
    component: HomeView
  },
  {
    path: '/reports',
    name: 'reports',
    component: ReportsView
  },
  {
    path: '/reports/:id',
    name: 'specificReport',
    component: SpecificReportView,
    props: true
  },
  {
    path: '/about',
    name: 'About',
    component: AboutView
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router