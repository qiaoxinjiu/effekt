import axios from 'axios'

/** 与 request 实例一致，避免走带拦截器的 axios 造成循环 */
const REFRESH_URL = '/it/api/auth/refresh'

let inflightRefresh = null

/**
 * 静默续期：POST /auth/refresh（仅当业务接口返回 code 451 时由 request 响应拦截器调用）
 * body 优先 refreshToken，否则传 accessToken；成功 code=20000 且 data.token
 * @returns {Promise<boolean>}
 */
export function tryRefreshAccessToken() {
  if (inflightRefresh) {
    return inflightRefresh
  }
  const refreshToken = localStorage.getItem('refreshToken')
  const accessToken = localStorage.getItem('accessToken')
  if (!refreshToken && !accessToken) {
    return Promise.resolve(false)
  }
  inflightRefresh = axios({
    method: 'post',
    url: REFRESH_URL,
    timeout: 30000,
    headers: {
      'Content-Type': 'application/json',
      ...(accessToken ? { accessToken } : {})
    },
    data: refreshToken ? { refreshToken } : accessToken ? { accessToken } : {}
  })
    .then(res => {
      const body = res && res.data
      if (!body || body.code !== 20000) {
        return false
      }
      const d = body.data || {}
      const token = d.token || body.token
      if (token) {
        localStorage.setItem('accessToken', token)
      }
      const rt = d.refresh_token || d.refreshToken
      if (rt) {
        localStorage.setItem('refreshToken', rt)
      }
      return !!token
    })
    .catch(() => false)
    .finally(() => {
      inflightRefresh = null
    })
  return inflightRefresh
}

export function clearTokenStorage() {
  localStorage.removeItem('accessToken')
  localStorage.removeItem('refreshToken')
}
