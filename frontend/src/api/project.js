import request from '../utils/request'

/**
 * 项目相关 API
 */

// 获取项目列表
export const getProjects = () => {
  return request({
    url: '/v1/projects',
    method: 'get'
  })
}

// 获取项目详情
export const getProject = (projectId) => {
  return request({
    url: `/v1/projects/${projectId}`,
    method: 'get'
  })
}

// 创建项目
export const createProject = (data) => {
  return request({
    url: '/v1/projects',
    method: 'post',
    data
  })
}

// 更新项目
export const updateProject = (projectId, data) => {
  return request({
    url: `/v1/projects/${projectId}`,
    method: 'put',
    data
  })
}

// 删除项目
export const deleteProject = (projectId) => {
  return request({
    url: `/v1/projects/${projectId}`,
    method: 'delete'
  })
}
