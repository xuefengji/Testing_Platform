/**
 * API 模块统一导出
 * 按模块组织 API，便于维护和管理
 */

// 认证相关
export * from './auth'

// API 端点管理
export * from './apiEndpoints'

// API 文件夹管理
export * from './apiFolders'

// 用户相关
export * from './user'

// 项目相关
export * from './project'

// 为了向后兼容，保留旧的导出（已废弃，建议使用新的模块化 API）
import * as authApi from './auth'
import * as apiEndpointsApi from './apiEndpoints'

export const login = authApi.login
export const getApiList = apiEndpointsApi.getApiEndpoints
export const createApi = apiEndpointsApi.createApiEndpoint
export const updateApi = apiEndpointsApi.updateApiEndpoint
export const deleteApi = apiEndpointsApi.deleteApiEndpoint
