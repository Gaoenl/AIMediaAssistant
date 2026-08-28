import { defineStore } from 'pinia'
import { login as loginApi } from '../api/auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('aima_token') || '',
    username: localStorage.getItem('aima_user') || ''
  }),
  actions: {
    async login(username, password) {
      const data = await loginApi(username, password)
      this.token = data.token
      this.username = data.username
      localStorage.setItem('aima_token', data.token)
      localStorage.setItem('aima_user', data.username)
    },
    logout() {
      this.token = ''
      this.username = ''
      localStorage.removeItem('aima_token')
      localStorage.removeItem('aima_user')
    }
  }
})
