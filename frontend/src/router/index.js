import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Layout from '../components/Layout.vue'
import Home from '../views/Home.vue'
import ApiTest from '../views/ApiTest.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/',
    component: Layout,
    redirect: '/home',
    meta: { requiresAuth: true },
    children: [
      {
        path: '/home',
        name: 'Home',
        component: Home
      },
      {
        path: '/api-test',
        name: 'ApiTest',
        component: ApiTest
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
