import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import TaskList from '../views/TaskList.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/login', component: Login },
    { path: '/', redirect: '/tasks' },
    { path: '/tasks', component: TaskList, meta: { requiresAuth: true } }
  ]
})

router.beforeEach((to) => {
  const token = localStorage.getItem('aima_token')
  if (to.meta.requiresAuth && !token) return '/login'
  if (to.path === '/login' && token) return '/tasks'
})

export default router
