import axios from 'axios'
import request from '@/utils/request'

export function importMockDocument(data) {
  return request({
    url: '/mock/document/import',
    method: 'post',
    data
  })
}

export function uploadImportMockDocument(data) {
  return request({
    url: '/mock/document/upload-import',
    method: 'post',
    data,
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

export function urlImportMockDocument(data) {
  return request({
    url: '/mock/document/url-import',
    method: 'post',
    data
  })
}

export function getMockDocumentList(params) {
  return request({
    url: '/mock/document/list',
    method: 'get',
    params
  })
}

export function getMockInterfaceList(params) {
  return request({
    url: '/mock/interface/list',
    method: 'get',
    params
  })
}

export function getMockInterfaceDetail(params) {
  return request({
    url: '/mock/interface/detail',
    method: 'get',
    params
  })
}

export function updateMockInterface(data) {
  return request({
    url: '/mock/interface/update',
    method: 'post',
    data
  })
}

export function enableMockInterface(interfaceId) {
  return request({
    url: '/mock/interface/enable',
    method: 'post',
    data: { interfaceId }
  })
}

export function disableMockInterface(interfaceId) {
  return request({
    url: '/mock/interface/disable',
    method: 'post',
    data: { interfaceId }
  })
}

export function getMockSceneList(params) {
  return request({
    url: '/mock/scene/list',
    method: 'get',
    params
  })
}

export function updateMockScene(data) {
  return request({
    url: '/mock/scene/update',
    method: 'post',
    data
  })
}

export function enableMockScene(sceneId) {
  return request({
    url: '/mock/scene/enable',
    method: 'post',
    data: { sceneId }
  })
}

export function disableMockScene(sceneId) {
  return request({
    url: '/mock/scene/disable',
    method: 'post',
    data: { sceneId }
  })
}

export function getMockLogList(params) {
  return request({
    url: '/mock/log/list',
    method: 'get',
    params
  })
}

export function getMockParseIssueList(params) {
  return request({
    url: '/mock/parse-issue/list',
    method: 'get',
    params
  })
}

export function runMockRuntime({ method, path, projectId, mockScene, query, body, headers }) {
  const params = Object.assign({}, query || {}, { projectId })
  if (mockScene) {
    params.mockScene = mockScene
  }
  const accessToken = localStorage.getItem('accessToken')
  const nextHeaders = Object.assign({}, headers || {})
  if (accessToken) {
    nextHeaders.accessToken = accessToken
  }
  return axios({
    baseURL: '/it/api',
    url: '/mock/runtime' + normalizePath(path),
    method: (method || 'GET').toLowerCase(),
    params,
    data: body || {},
    headers: nextHeaders,
    validateStatus: function () { return true }
  })
}

function normalizePath(path) {
  const value = String(path || '').trim()
  if (!value) return '/'
  return value.charAt(0) === '/' ? value : '/' + value
}
