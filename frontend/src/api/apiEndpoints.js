import request from '../utils/request'

/**
 * API 端点管理相关 API
 */

// 获取 API 端点列表
export const getApiEndpoints = (params) => {
  return request({
    url: '/v1/api-endpoints',
    method: 'get',
    params
  })
}

// 获取 API 端点详情
export const getApiEndpoint = (endpointId) => {
  return request({
    url: `/v1/api-endpoints/${endpointId}`,
    method: 'get'
  })
}

// 创建 API 端点
export const createApiEndpoint = (data) => {
  return request({
    url: '/v1/api-endpoints',
    method: 'post',
    data
  })
}

// 更新 API 端点
export const updateApiEndpoint = (endpointId, data) => {
  return request({
    url: `/v1/api-endpoints/${endpointId}`,
    method: 'put',
    data
  })
}

// 删除 API 端点
export const deleteApiEndpoint = (endpointId) => {
  return request({
    url: `/v1/api-endpoints/${endpointId}`,
    method: 'delete'
  })
}

// 获取 API 端点版本列表
export const getApiEndpointVersions = (endpointId) => {
  return request({
    url: `/v1/api-endpoints/${endpointId}/versions`,
    method: 'get'
  })
}

// 获取 API 端点指定版本
export const getApiEndpointVersion = (endpointId, versionId) => {
  return request({
    url: `/v1/api-endpoints/${endpointId}/versions/${versionId}`,
    method: 'get'
  })
}

// 创建 API 端点版本
export const createApiEndpointVersion = (endpointId, data) => {
  return request({
    url: `/v1/api-endpoints/${endpointId}/versions`,
    method: 'post',
    data
  })
}

// 设置最新版本
export const setLatestVersion = (endpointId, versionId) => {
  return request({
    url: `/v1/api-endpoints/${endpointId}/versions/${versionId}/set-latest`,
    method: 'post'
  })
}
