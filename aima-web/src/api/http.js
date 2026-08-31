import axios from 'axios'

const http = axios.create({ baseURL: '/api/v1', timeout: 30000 })

http.interceptors.request.use((config) => {
  const token = localStorage.getItem('aima_token')
  // 兼容历史脏数据:旧版本登录失败时会存入字符串 "undefined",这里一并拦截
  if (token && token !== 'undefined') config.headers.Authorization = `Bearer ${token}`
  return config
})

http.interceptors.response.use(
  // 后端统一返回 {code, message, data},成功时直接剥出 data
  (res) => res.data.data,
  (err) => {
    const message = err.response?.data?.message || err.message || '请求失败'
    return Promise.reject(new Error(message))
  }
)

export default http
