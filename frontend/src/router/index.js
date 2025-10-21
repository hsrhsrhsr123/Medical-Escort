import { createRouter, createWebHistory } from 'vue-router'
import Layout from '@/components/Layout.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: Layout,
      redirect: '/home',
      children: [
        {
          path: 'home',
          name: 'Home',
          component: () => import('@/views/Home.vue'),
          meta: { title: '首页', icon: 'House' }
        },
        {
          path: 'users',
          name: 'Users',
          component: () => import('@/views/Users.vue'),
          meta: { title: '用户管理', icon: 'User' }
        },
        {
          path: 'appointments',
          name: 'Appointments',
          component: () => import('@/views/Appointments.vue'),
          meta: { title: '预约挂号', icon: 'Calendar' }
        },
        {
          path: 'guidance',
          name: 'Guidance',
          component: () => import('@/views/Guidance.vue'),
          meta: { title: '就医指导', icon: 'Guide' }
        },
        {
          path: 'medications',
          name: 'Medications',
          component: () => import('@/views/Medications.vue'),
          meta: { title: '用药指导', icon: 'Medicine' }
        }
      ]
    }
  ]
})

export default router


