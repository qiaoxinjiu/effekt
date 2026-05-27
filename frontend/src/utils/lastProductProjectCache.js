/**
 * 全局「最近选择的产品 + 项目」缓存（localStorage），供 Bug 列表、用例、计划、报告等共用。
 * 兼容旧 key：effekt_bug_list_last_product_project
 */
export const LAST_PRODUCT_PROJECT_CACHE_KEY = 'effekt_last_product_project'

const LEGACY_BUG_LIST_CACHE_KEY = 'effekt_bug_list_last_product_project'

export function readLastProductProjectCache() {
  try {
    let raw = localStorage.getItem(LAST_PRODUCT_PROJECT_CACHE_KEY)
    if (!raw) raw = localStorage.getItem(LEGACY_BUG_LIST_CACHE_KEY)
    if (!raw) return null
    const o = JSON.parse(raw)
    if (!o || typeof o !== 'object') return null
    return { productId: o.productId, projectId: o.projectId }
  } catch (e) {
    return null
  }
}

export function saveLastProductProjectCache(productId, projectId) {
  if (productId === '' || productId === undefined || productId === null) return
  if (projectId === '' || projectId === undefined || projectId === null) return
  try {
    const payload = JSON.stringify({ productId, projectId })
    localStorage.setItem(LAST_PRODUCT_PROJECT_CACHE_KEY, payload)
    if (localStorage.getItem(LEGACY_BUG_LIST_CACHE_KEY)) {
      localStorage.removeItem(LEGACY_BUG_LIST_CACHE_KEY)
    }
  } catch (e) {
    // quota / 隐私模式等忽略
  }
}

export function pickIdFromOptions(options, rawId) {
  const row = (options || []).find(p => String(p.id) === String(rawId))
  return row ? row.id : rawId
}
