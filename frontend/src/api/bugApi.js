import request from '@/utils/request'

export function getBugList(params) {
  return request({
    url: '/bug/list',
    method: 'get',
    params: Object.assign({ pageNo: 1, pageSize: 20 }, params || {})
  })
}

export function getBugDetail(bugId) {
  return request({
    url: '/bug/detail',
    method: 'get',
    params: {
      bugId,
      id: bugId
    }
  })
}

export function createBug(data) {
  return request({
    url: '/bug/create',
    method: 'post',
    data: data || {}
  })
}

export function updateBug(data) {
  return request({
    url: '/bug/update',
    method: 'post',
    data: data || {}
  })
}

export function deleteBug(data) {
  return request({
    url: '/bug/delete',
    method: 'post',
    data: data || {}
  })
}

export function addBugComment(data) {
  return request({
    url: '/bug/comment/add',
    method: 'post',
    data: data || {}
  })
}

/** Bug 操作历史：POST /bug/history/add */
export function addBugHistory(data) {
  return request({
    url: '/bug/history/add',
    method: 'post',
    data: data || {}
  })
}

export function getBugStats(params) {
  return request({
    url: '/bug/stats',
    method: 'get',
    params: params || {}
  })
}

/** 复现步骤截图：POST /bug/upload，表单字段 file；成功返回 data.url */
export function uploadBugStepImage(file) {
  const formData = new FormData()
  formData.append('file', file)
  return request({
    url: '/bug/upload',
    method: 'post',
    data: formData
  })
}
