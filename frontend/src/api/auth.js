import request from '../utils/request'

/**
 * 认证相关 API
 */

// 登录
export const login = (data) => {
  return request({
    url: '/v1/auth/login',
    method: 'post',
    data
  })
}

// 登出（如果需要）
export const logout = () => {
  return request({
    url: '/v1/auth/logout',
    method: 'post'
  })
}

// 刷新 token
export const refreshToken = (refreshToken) => {
  return request({
    url: '/v1/auth/refresh',
    method: 'post',
    data: { refresh_token: refreshToken }
  })
}
