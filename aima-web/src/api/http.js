import axios from 'axios'

const http = axios.create({ baseURL: '/api/v1', timeout: 30000 })

http.interceptors.request.use((config) => {
  const token = localStorage.getItem('aima_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

http.interceptors.response.use(
  (res) => res.data,
  (err) => {
    const message = err.response?.data?.message || err.message || '请求失败'
    return Promise.reject(new Error(message))
  }
)

export default http
