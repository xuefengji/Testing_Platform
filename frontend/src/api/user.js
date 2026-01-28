import request from '../utils/request'

/**
 * 用户相关 API
 */

// 获取当前用户信息
export const getCurrentUser = () => {
  return request({
    url: '/v1/user/me',
    method: 'get'
  })
}

// 更新用户信息
export const updateUser = (data) => {
  return request({
    url: '/v1/user/me',
    method: 'put',
    data
  })
}

// 修改密码
export const changePassword = (data) => {
  return request({
    url: '/v1/user/change-password',
    method: 'post',
    data
  })
}
