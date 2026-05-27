import request from '@/utils/request'

export function getBuilderList(projectId, params) {
  return request({
    url: '/data/builder/list',
    method: 'get',
    params: Object.assign({ project_id: projectId, pageNo: 1, pageSize: 10 }, params || {})
  })
}

export function getBuilderDetail(projectId, builderId) {
  return request({
    url: '/data/builder/detail',
    method: 'get',
    params: {
      project_id: projectId,
      id: builderId
    }
  })
}

export function createBuilder(projectId, data) {
  return request({
    url: '/data/builder/create',
    method: 'post',
    data: Object.assign({ project_id: projectId }, data)
  })
}

export function updateBuilder(projectId, builderId, data) {
  return request({
    url: '/data/builder/update',
    method: 'post',
    data: Object.assign({ project_id: projectId, id: builderId }, data)
  })
}

export function deleteBuilder(projectId, builderId) {
  return request({
    url: '/data/builder/delete',
    method: 'post',
    data: {
      project_id: projectId,
      id: builderId
    }
  })
}

export function executeBuilder(projectId, builderId, data) {
  return request({
    url: '/data/builder/execute',
    method: 'post',
    data: Object.assign({ project_id: projectId, builder_id: builderId }, data)
  })
}

export function getDataTaskStatus(projectId, taskId) {
  return request({
    url: '/data/task/status',
    method: 'get',
    params: {
      project_id: projectId,
      task_id: taskId
    }
  })
}
