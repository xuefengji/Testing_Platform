import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '../router'

const service = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    // 后端统一返回格式：{ code, success, data, message }
    const res = response.data
    
    // 检查是否是统一响应格式
    if (res && typeof res === 'object' && 'code' in res) {
      // 业务错误（code !== 200）
      if (res.code !== 200) {
        // 401 未授权，自动跳转登录页
        if (res.code === 401) {
          localStorage.removeItem('token')
          if (router.currentRoute.value.path !== '/login') {
            router.push('/login')
          }
        }
        // 抛出错误，让业务代码处理错误消息
        const error = new Error(res.message || '请求失败')
        error.code = res.code
        error.data = res.data
        return Promise.reject(error)
      }
      // 成功时返回 data 字段
      return res.data !== undefined ? res.data : res
    }
    
    // 兼容直接返回数据的情况（向后兼容）
    return res
  },
  error => {
    console.error('Response error:', error)
    
    // 处理 HTTP 错误（网络错误、服务器错误等）
    if (error.response) {
      const res = error.response.data
      // 如果后端返回了统一格式的错误响应
      if (res && typeof res === 'object' && 'code' in res) {
        const err = new Error(res.message || '请求失败')
        err.code = res.code
        err.data = res.data
        // 401 未授权，自动跳转登录页
        if (res.code === 401) {
          localStorage.removeItem('token')
          if (router.currentRoute.value.path !== '/login') {
            router.push('/login')
          }
        }
        return Promise.reject(err)
      }
      
      // 处理 HTTP 状态码错误
      if (error.response.status === 401) {
        localStorage.removeItem('token')
        if (router.currentRoute.value.path !== '/login') {
          router.push('/login')
        }
      }
    }
    
    return Promise.reject(error)
  }
)

export default service
