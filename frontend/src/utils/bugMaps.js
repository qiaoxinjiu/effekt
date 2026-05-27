/** Bug 枚举与展示（与接口一致：bug_type 1–11） */

export const BUG_TYPE_MAP = {
  1: '功能缺陷',
  2: 'UI问题',
  3: '性能问题',
  4: '安全漏洞',
  5: '兼容性问题',
  6: '前端bug',
  7: '后端bug',
  8: '配置问题',
  9: '产品设计缺陷',
  10: '产品优化',
  11: '其他'
}

export const SEVERITY_MAP = {
  1: '致命',
  2: '严重',
  3: '中等',
  4: '轻微'
}

export const PRIORITY_MAP = {
  1: '高',
  2: '中',
  3: '低'
}

/** 复现概率 / 复现率（与接口 reproduceRate 一致） */
export const REPRODUCE_RATE_MAP = {
  1: '必现',
  2: '偶现',
  3: '仅一次',
  4: '难重现'
}

export function formatReproduceRate(v) {
  const n = Number(v)
  if (Number.isNaN(n)) return v === undefined || v === null || v === '' ? '-' : String(v)
  return REPRODUCE_RATE_MAP[n] != null ? REPRODUCE_RATE_MAP[n] : String(v)
}

export const STATUS_MAP = {
  0: '新建',
  1: '待处理',
  2: '进行中',
  3: '已解决',
  4: '已关闭',
  5: '已拒绝'
}

/** 已解决状态值（与接口一致） */
export const BUG_STATUS_RESOLVED = 3

/** 已关闭 */
export const BUG_STATUS_CLOSED = 4

/** 待处理（重新打开目标状态） */
export const BUG_STATUS_PENDING = 1

/** 已拒绝 */
export const BUG_STATUS_REJECTED = 5

/**
 * 主流程下一状态：新建→待处理→进行中→已解决→已关闭；已拒绝→待处理。
 * 已关闭、未知状态无下一档。
 */
export function getBugStatusNextTransition(status) {
  const s = Number(status)
  if (Number.isNaN(s)) return null
  const nextMap = {
    0: 1,
    1: 2,
    2: 3,
    3: 4,
    5: 1
  }
  const next = nextMap[s]
  if (next === undefined) return null
  const label = STATUS_MAP[next]
  if (label == null) return null
  return { nextStatus: next, nextLabel: label }
}

export function formatBugType(v) {
  return BUG_TYPE_MAP[v] != null ? BUG_TYPE_MAP[v] : v
}

export function formatSeverity(v) {
  return SEVERITY_MAP[v] != null ? SEVERITY_MAP[v] : v
}

export function formatPriority(v) {
  return PRIORITY_MAP[v] != null ? PRIORITY_MAP[v] : v
}

export function formatStatus(v) {
  return STATUS_MAP[v] != null ? STATUS_MAP[v] : v
}

/** ElementUI el-tag type */
export function statusTagType(status) {
  const map = {
    0: 'info',
    1: 'warning',
    2: 'primary',
    3: 'success',
    4: 'info',
    5: 'danger'
  }
  return map[Number(status)] || 'info'
}

/** 详情页等：状态角标独立配色（class 名） */
export function statusBadgeClass(status) {
  const map = {
    0: 'bug-status-new',
    1: 'bug-status-pending',
    2: 'bug-status-progress',
    3: 'bug-status-resolved',
    4: 'bug-status-closed',
    5: 'bug-status-rejected'
  }
  return map[Number(status)] != null ? map[Number(status)] : 'bug-status-unknown'
}

export function severityTagType(severity) {
  const map = { 1: 'danger', 2: 'warning', 3: '', 4: 'info' }
  return map[Number(severity)] || 'info'
}

export function priorityTagType(priority) {
  const map = { 1: 'danger', 2: 'warning', 3: 'success' }
  return map[Number(priority)] || 'info'
}

export function bugTypeTagType(bugType) {
  const n = Number(bugType)
  if (!n || n < 1) return ''
  const cycle = ['', 'success', 'warning', 'danger', 'info']
  return cycle[(n - 1) % cycle.length]
}
