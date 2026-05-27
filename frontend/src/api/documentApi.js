import request from '@/utils/request'

/** 文档列表 */
export function getDocumentList(params) {
  return request({
    url: '/document/list',
    method: 'get',
    params
  })
}

/** 文档详情 */
export function getDocumentDetail(params) {
  return request({
    url: '/document/detail',
    method: 'get',
    params
  })
}

/** 上传 PDF（multipart，单文件一次请求） */
export function uploadDocumentPdf({ file, productId, projectId, createdBy }) {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('productId', productId)
  formData.append('projectId', projectId)
  if (createdBy != null && createdBy !== '') {
    formData.append('createdBy', createdBy)
  }
  return request({
    url: '/document/upload',
    method: 'post',
    data: formData
  })
}

/** 创建文档 */
export function createDocument(data) {
  return request({
    url: '/document/create',
    method: 'post',
    data
  })
}

/** 更新文档 */
export function updateDocument(data) {
  return request({
    url: '/document/update',
    method: 'post',
    data
  })
}

/** 删除文档 */
export function deleteDocument(data) {
  return request({
    url: '/document/delete',
    method: 'post',
    data
  })
}

/** 刷新飞书文档 */
export function refreshDocument(data) {
  return request({
    url: '/document/refresh',
    method: 'post',
    data
  })
}

/** 生成测试用例（预览） */
export function generateDocumentCases(data) {
  return request({
    url: '/document/generate-cases',
    method: 'post',
    data
  })
}

/** 模块匹配 */
export function matchDocumentModules(data) {
  return request({
    url: '/document/match-modules',
    method: 'post',
    data
  })
}

/** 导入测试用例 */
export function importDocumentCases(data) {
  return request({
    url: '/document/import-cases',
    method: 'post',
    data
  })
}

/** 批量创建模块 */
export function batchCreateDocumentModules(data) {
  return request({
    url: '/document/batch-create-modules',
    method: 'post',
    data
  })
}
