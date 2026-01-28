import request from '../utils/request'

/**
 * API 文件夹管理相关 API
 */

// 获取文件夹树
export const getApiFoldersTree = () => {
  return request({
    url: '/v1/api-folders/tree',
    method: 'get'
  })
}

// 创建文件夹
export const createApiFolder = (data) => {
  return request({
    url: '/v1/api-folders',
    method: 'post',
    data
  })
}

// 更新文件夹
export const updateApiFolder = (folderId, data) => {
  return request({
    url: `/v1/api-folders/${folderId}`,
    method: 'put',
    data
  })
}

// 删除文件夹
export const deleteApiFolder = (folderId) => {
  return request({
    url: `/v1/api-folders/${folderId}`,
    method: 'delete'
  })
}
